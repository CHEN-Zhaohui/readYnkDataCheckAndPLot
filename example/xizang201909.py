# -*- coding: utf-8 -*-
import json
import numpy as np
#local packages
import geoist.gravity.graobj as gg
import geoist.gravity.adjmethods as adj
#以上各行无需修改，其中geoist.gravity.graobj和geoist.gravity.adjmethods是BACGS平差的核心
#---------------------------------------------------------------------------------------
#定义仪器
#根据具体的仪器进行修改，CG-5仪器不用读取table文件，LCR仪器需要读取table文件
#若同一台仪器用在了不同的测网（存在2个及以上的平差数据文件），这台仪器要有不同的仪器名
#比如m1是“C098”仪器，m4是同一台仪器但gg.Meter中定义为“C0981”,它如果需要读取格值表即
#table.dat文件，将table中对应的真实仪器号写在后面（LCR仪器必须，CG5仪器不需要）
m1 = gg.Meter('CG-', 'C635')
m1.msf = 0.999961
m2 = gg.Meter('CG-', 'C627')
m2.msf = 1.000039
m3 = gg.Meter('CG-', 'C207')
m3.msf = 0.990215
m4 = gg.Meter('CG-', 'C229')
m4.msf = 0.999225
m5 = gg.Meter('CG-', 'C235')
m5.msf = 0.999931
m6 = gg.Meter('CG-', 'C427')
m6.msf = 1.000079
#---------------------------------------------------------------------------------------
#定义点志记文件
n1 = gg.Network('xizang',1)
n1.read_pnts('E:\野外监测\西藏平差计算测试\YCXZ1909.DZJ')
#显示器上显示“n1”这个实例的值，即点志记文件中的测点数
print(n1)
#---------------------------------------------------------------------------------------
#定义一个平差的测量
gg.Survey('xizang', '201909')
#为平差添加使用的仪器
s1.add_meter(m1)
s1.add_meter(m2)
s1.add_meter(m3)
s1.add_meter(m4)
s1.add_meter(m5)
s1.add_meter(m6)
#为平差添加测网信息文件即点志记文件，无需修改
s1.net = n1
#添加平差数据文件
s1.read_survey_file('E:\野外监测\西藏平差计算测试\YCXZ1906.635')
s1.read_survey_file('E:\野外监测\西藏平差计算测试\YCXZ1906.627')
s1.read_survey_file('E:\野外监测\西藏平差计算测试\YCXZ1909.207')
s1.read_survey_file('E:\野外监测\西藏平差计算测试\YCXZ1909.229')
s1.read_survey_file('E:\野外监测\西藏平差计算测试\YCXZ1909.235')
s1.read_survey_file('E:\野外监测\西藏平差计算测试\YCXZ1909.427')
#---------------------------------------------------------------------------------------
#固体潮、气压改正
s1.corr_aux_effect()
#仪器一次项系数计算，与仪器个数对应，1表示做此仪器的系数标定，一般每次只标定1个1
s1.meter_sf_index = [0, 0, 0, 0, 0, 0]
#在显示器上显示仪器个数，loops个数，重力读数个数
print(s1)
#添加绝对点信息
gravwork = gg.Campaign('201909', 1)
gravwork.add_ag_from_file('E:\野外监测\西藏平差计算测试\xizang201909AG.txt')
#将绝对点信息添加测量到平差任务
gravwork.add_surveys(s1)
print(gravwork)
#---------------------------------------------------------------------------------------
#开始平差
#1:cls ; 2:Baj; 3:Baj1(当需要对1台仪器做格值标定时用3)
gravwork.adj_method = 2
#pre_adj是完成从观测文件重，生成平差矩阵的
gravwork.pre_adj()
#平差任务开始工作
#输出文件内容包括点值及精度、段差残差、仪器精度信息。文本文件，Json格式，使用Datist来完成后续数据显示
#上面的“3”代表使用L-BFGS-B优化方法，还可以使用“1”代表单纯形，“2”代表牛顿法的优化方法，
#“1”的包容性好，有些数据错误也可以计算通过，但结果不对。“3”运行用时最短
gravwork.run_adj('E:\野外监测\西藏平差计算测试\xizang201909dz.txt', 2)
#段差输出export_dc方法
#输出文件内容为平差后各测段的段差及误差。文本文件，TXT列格式
gravwork.export_dc('E:\野外监测\西藏平差计算测试\xizang201909dc.txt')
#根据野外实测顺序段差、误差和残差输出
gravwork.export_dc_all('E:\野外监测\西藏平差计算测试\xizang201909dd.txt')
