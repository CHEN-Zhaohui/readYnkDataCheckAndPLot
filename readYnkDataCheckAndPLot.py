# -*- coding: utf-8 -*-
'''
Created on Wed Feb 26 20:06:55 2020
@author: Chen Zhaohui
'''
# Python 3.7
'''
基于LGADJ平差所需文件，转换python贝叶斯平差程序的引导文件，包含一些可能需要的备注，
此外还可实现对观测数据文件的检查和绘图等。
--------------------------------
数据文件的检查，可实现以下检查：
1.检查数据的气压值低于常理的情况；
2.检查观测时间超过24小时、分钟超过60、观测时间跨天无断开以及观测时间排序错误问题；
3.检查观测日期排序（相同天没有放在一起）问题；
4.检查相同点号之间没有用55555、44444 或 66666 隔开问题；
5.检查55555、44444 或 66666之间仅有一行数据问题；
6.检查绝对点是否在当期数据中实际联测；
7.检查点值信息文件是否包含高程列；
8.每个测点气压和温度值的相对变化结果图；
9.所有测点气压和温度值的变化曲线，可辅助气压值的检查；
10.生成贝叶斯平差所需的绝对值引导文件。
'''
import os
from itertools import islice
import adjustmentDataCheck
import make_data

#一般只需要修改以下五行就可以实现，分别是定义目录、测网名和观测时间，以及给出格值表和ynk引导文件的名称。
#定义程序运行目录（可使用绝对目录和相对目录），所有输入、输出文件均存储该目录下，目录中存在数字需要\\字符分开
#例如：'E:\!Tibetan_Eastern_gravity\\1309\!adj可运行'
directory = 'E:\野外监测\西藏平差计算测试'
NetName = 'xizang'                              #定义测网名称
Year_Month = '201909'                           #定义测量时间
tab = 'TABLE.DAT'                               #格值表文件
ynk = 'YCXZ1909.YNK'                                #adj运行的ynk引导文件件
#
#输出文件,这里以测网加测量时间和输出文件类型命名,根据前面参数自动生成
pyfile = NetName + Year_Month + '.py'           #定义python脚本文件名称,建议以测网和时间名称
dzfile = NetName + Year_Month + 'dz.txt'        #点值文件：chuandian201409dz.txt
dcfile = NetName + Year_Month + 'dc.txt'        #段差文件：chuandian201409dc.txt
ddfile = NetName + Year_Month + 'dd.txt'        #测段文件：chuandian201409dd.txt
AG = NetName + Year_Month + 'AG.txt'            #贝叶斯平差所需的绝对值引导文件：chuandian201409AG.txt
#
try:
    ynk_file = open(os.path.join(directory, ynk), mode='r')
except FileNotFoundError:
    print("%s 文件不存在" % os.path.join(directory, ynk))
outfile = open(os.path.join(directory, pyfile), mode='w')
AG_file = open(os.path.join(directory, AG), mode='w')
#
outfile.write("# -*- coding: utf-8 -*-\n")
outfile.write("import json\n")
outfile.write("import numpy as np\n")
outfile.write("#local packages\n")
outfile.write("import geoist.gravity.graobj as gg\n")
outfile.write("import geoist.gravity.adjmethods as adj\n")
outfile.write("#以上各行无需修改，其中geoist.gravity.graobj和geoist.gravity.adjmethods是BACGS平差的核心\n")
outfile.write("#---------------------------------------------------------------------------------------\n")
outfile.write("#定义仪器\n")
outfile.write("#根据具体的仪器进行修改，CG-5仪器不用读取table文件，LCR仪器需要读取table文件\n")
outfile.write("#若同一台仪器用在了不同的测网（存在2个及以上的平差数据文件），这台仪器要有不同的仪器名\n")
outfile.write("#比如m1是“C098”仪器，m4是同一台仪器但gg.Meter中定义为“C0981”,它如果需要读取格值表即\n")
outfile.write("#table.dat文件，将table中对应的真实仪器号写在后面（LCR仪器必须，CG5仪器不需要）\n")
#拾取平差dzj文件
for line in islice(ynk_file, 3, 4):
    dzj_line = line.strip()
#
#拾取观测仪器和一次项系数及格值表（LCR仪器必须读取）
i = 0
for line in islice(ynk_file, 0, None):
    name = line.split()
    if name[0] != '99999':
        if name[1][0:1] == 'L' or name[1][0:1] == 'C' or name[1][0:1] == 'B':
            i += 1
            outfile.write("m%d = gg.Meter('%s', '%s')\n" % (i, name[1][0:3], name[0]))
            outfile.write("m%d.msf = %f\n" % (i, float(name[2])))
            if name[1][0:1] == 'L':
                tab_file = os.path.join(directory, tab)  # dzj文件包含目录
                outfile.write("m%d.read_table('%s')\n" % (i, tab_file))
        else:
            continue
    else:
        break
#
outfile.write("#---------------------------------------------------------------------------------------\n")
outfile.write("#定义点志记文件\n")
outfile.write("n1 = gg.Network('%s',1)\n" % NetName)
dzj_file = os.path.join(directory, dzj_line)
outfile.write("n1.read_pnts('%s')\n" % dzj_file)
outfile.write("#显示器上显示“n1”这个实例的值，即点志记文件中的测点数\n")
outfile.write("print(n1)\n")
#
outfile.write("#---------------------------------------------------------------------------------------\n")
outfile.write("#定义一个平差的测量\n")
outfile.write("gg.Survey('%s', '%s')\n" % (NetName, Year_Month))
outfile.write("#为平差添加使用的仪器\n")
current_num = 1
while current_num <= i:
    outfile.write("s1.add_meter(m%d)\n" % current_num)
    current_num += 1
#
outfile.write("#为平差添加测网信息文件即点志记文件，无需修改\n")
outfile.write("s1.net = n1\n")
outfile.write("#添加平差数据文件\n")
#
[dzj_numbers, dzj_names, dzj_latitudes, dzj_longitudes, dzj_elevations] = make_data.data_file(dzj_file, 0, 0)
#
for line in islice(ynk_file, 1, None):
    ag = line.split()
    if ag[0] == '99999':
        break
    else:
        j = 0
        while j <= len(dzj_numbers):
            try:
                if int(dzj_numbers[j]) == int(ag[0]):
                    AG_file.write(("%s %d A %.3f %.3f %.1f %.4f %.4f\n" % (dzj_names[j], int(dzj_numbers[j]),
                                                                     float(dzj_longitudes[j]), float(dzj_latitudes[j]),
                                                                     dzj_elevations[j], float(ag[-2]), float(ag[-1]))))
                    break
            except IndexError:
                print("点位信息文件绝对点 %s 无高程，故无法输出高程值至绝对点引导文件" % ag[0])
                break
            j += 1
AG_file.close()
allnumbers = []
for line in islice(ynk_file, 0, None):
    adjustment_file = line.split()[0]
    if adjustment_file == '99999':
        break
    else:
        outfile.write("s1.read_survey_file('%s\%s')\n" % (directory, adjustment_file))
        adjustmentDataCheck.check_adjustment_data(os.path.join(directory, adjustment_file))
        make_data.pressureAndTemperatureMapping(os.path.join(directory, adjustment_file))
        all_number = make_data.data_file(os.path.join(directory, adjustment_file), 1, 2)
        allnumbers.extend(all_number)
#
adjustmentDataCheck.check_ag_data(allnumbers, os.path.join(directory, AG))
#
outfile.write("#---------------------------------------------------------------------------------------\n")
outfile.write("#固体潮、气压改正\n")
outfile.write("s1.corr_aux_effect()\n")
outfile.write("#仪器一次项系数计算，与仪器个数对应，1表示做此仪器的系数标定，一般每次只标定1个1\n")
array = [0]*i
outfile.write("s1.meter_sf_index = %s\n" % array)
outfile.write("#在显示器上显示仪器个数，loops个数，重力读数个数\n")
outfile.write("print(s1)\n")
outfile.write("#添加绝对点信息\n")
outfile.write("gravwork = gg.Campaign('%s', 1)\n" % Year_Month)
outfile.write("gravwork.add_ag_from_file('%s\%s')\n" % (directory, AG))
outfile.write("#将绝对点信息添加测量到平差任务\n")
outfile.write("gravwork.add_surveys(s1)\n")
outfile.write("print(gravwork)\n")
#
outfile.write("#---------------------------------------------------------------------------------------\n")
outfile.write("#开始平差\n")
outfile.write("#1:cls ; 2:Baj; 3:Baj1(当需要对1台仪器做格值标定时用3)\n")
outfile.write("gravwork.adj_method = 2\n")
outfile.write("#pre_adj是完成从观测文件重，生成平差矩阵的\n")
outfile.write("gravwork.pre_adj()\n")
outfile.write("#平差任务开始工作\n")
outfile.write("#输出文件内容包括点值及精度、段差残差、仪器精度信息。文本文件，Json格式，使用Datist来完成后续数据显示\n")
outfile.write("#上面的“3”代表使用L-BFGS-B优化方法，还可以使用“1”代表单纯形，“2”代表牛顿法的优化方法，\n")
outfile.write("#“1”的包容性好，有些数据错误也可以计算通过，但结果不对。“3”运行用时最短\n")
outfile.write("gravwork.run_adj('%s\%s', 2)\n" % (directory, dzfile))
outfile.write("#段差输出export_dc方法\n")
outfile.write("#输出文件内容为平差后各测段的段差及误差。文本文件，TXT列格式\n")
outfile.write("gravwork.export_dc('%s\%s')\n" % (directory, dcfile))
outfile.write("#根据野外实测顺序段差、误差和残差输出\n")
outfile.write("gravwork.export_dc_all('%s\%s')\n" % (directory, ddfile))
#
ynk_file.close()
outfile.close()
#