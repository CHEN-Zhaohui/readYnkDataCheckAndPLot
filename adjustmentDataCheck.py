# -*- coding: utf-8 -*-
'''
Created on Wed Feb 27 18:06:55 2020
@author: Chen Zhaohui
'''
# Python 3.7
#
import make_data
#
def check_adjustment_data(adjustmentData):
    [labels, date_times, numbers, pressures] = make_data.data_file(adjustmentData, 1, 1)
    i = 0
    while i < (len(date_times)-1):
        if pressures[i] < 500.0 or pressures[i+1] < 500.0:
            print("数据文件%s: 点号%s %s 气压 %f 低于500hpa，请检查" % (adjustmentData, int(numbers[i]), date_times[i],
                                                          pressures[i]))
        if int(date_times[i][6:]) > 2400 or int(date_times[i+1][6:]) > 2400:
            print("数据文件%s: %s 观测时间超过24小时制" % (adjustmentData, date_times[i]))
        if int(date_times[i][8:]) > 60 or int(date_times[i+1][8:]) > 60:
            print("数据文件%s: %s 观测时间的分钟超过60分钟制" % (adjustmentData,  date_times[i]))
        if int(date_times[i][:6]) > int(date_times[i+1][:6]):
            print("请检查数据%s: %s - %s 前后日期" % (adjustmentData, date_times[i], date_times[i+1]))
        if (numbers[i] == numbers[i+1]) and (labels[i] == labels[i+1]):
            print("请检查数据%s: %s 存在相邻同点号%d" % (adjustmentData, date_times[i], int(numbers[i])))
        if (date_times[i][6:] > date_times[i+1][6:]) and (labels[i] == labels[i+1]):
            print("请检查数据%s: 点号%s %s 的观测时间" % (adjustmentData, int(numbers[i]), date_times[i]))
        if labels[i] == 'oneline':
            print("请检查数据%s: 点号%s %s 只有一行数据" % (adjustmentData, int(numbers[i]), date_times[i]))
        i += 1
#
def check_ag_data(allnumbers,agfile):
    aa = []
    for allnumber in allnumbers:
        aa.append(int(allnumber))
    with open(agfile) as ag:
        for line in ag.readlines():
            if int(line.split()[1]) not in aa:
                print("绝对点 %s %s 没有联测！" % (line.split()[1], line.split()[1]))
                continue
#