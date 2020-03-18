# -*- coding: utf-8 -*-
'''
Created on Wed Feb 27 18:06:55 2020
@author: Chen Zhaohui
'''

# Python 3.7

from itertools import islice
from matplotlib import pyplot as plt
import warnings
warnings.filterwarnings("ignore")

def data_file(adjustmentData,hh, key):
    label = 0
    times = 0
    fir_rows, sec_rows, labels, date_times, numbers, values, pressures, temperatures, all_number = [], [], [], [], [],\
                                                                                                 [], [], [], []
    with open(adjustmentData) as input_file:
        for line in islice(input_file, hh, None):
            label += 1
            if line.split()[0] == '44444' or line.split()[0] == '55555' or line.split()[0] == '66666' or \
                    line.split()[0] == '99999':
                times += 1
                if (label-1) == 1:
                    labels.extend(['oneline'] * (label - 1))
                else:
                    labels.extend([times]*(label-1))
                label = 0
                if line.split()[0] == '99999':
                    break
                else:
                    continue
            else:
                try:
                    fir_row = line.split()[0]
                    sec_row = line.split()[1]
                    date_time = line.split()[2]
                    number = float(line.split()[3])
                    value = float(line.split()[4])
                except IndexError:
                    print("DZJ文件有误，可能是高程列信息不全")
                else:
                    fir_rows.append(fir_row)
                    sec_rows.append(sec_row)
                    date_times.append(date_time)
                    numbers.append(number)
                    values.append(value)
                    if key == 1 or key == 3:
                        pressure = float(line.split()[5])
                        temperature = float(line.split()[6])
                        pressures.append(pressure)
                        temperatures.append(temperature)

    all_number.extend(set(numbers))

    if key == 0:
        return fir_rows, sec_rows, date_times, numbers, values
    if key == 1:
        return labels, date_times, numbers, pressures
    if key == 2:
        return all_number
    if key == 3:
        return numbers, pressures, temperatures

def listDifference(lst):
    diffs = []
    i = len(lst)
    for j in range(0, i):
        diff = float(lst[j]) - float(lst[0])
        diffs.append(diff)
    return diffs

def mergeDictionary(list1, list2):
    dp = {}
    for i in range(len(list1)):
        if list1[i] in dp:
            dp[int(list1[i])] += [list2[i]]
        else:
            dp[int(list1[i])] = [list2[i]]
    return dp

def extractionData(list1, list2):
    xxs, yys = [], []
    for key, value in mergeDictionary(list1, list2).items():
        xxs.append(key)
        yys.extend(listDifference(value))
    return xxs, yys

def check_adjustment_data(adjustmentData):
    [labels, date_times, numbers, pressures] = data_file(adjustmentData, 1, 1)
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

def check_ag_data(allnumbers,agfile):
    aa = []
    for allnumber in allnumbers:
        aa.append(int(allnumber))
    with open(agfile) as ag:
        for line in ag.readlines():
            if int(line.split()[1]) not in aa:
                print("绝对点 %s %s 没有联测！" % (line.split()[1], line.split()[1]))
                continue

def pressureAndTemperatureMapping(adjustmentData):
    [numbers, pressures, temperatures] = data_file(adjustmentData, 1, 3)
    [_, pyy] = extractionData(numbers, pressures)
    [_, tyy] = extractionData(numbers, temperatures)
    x, xxs, pyys, tyys = 0, [], [], []
    for i in range(len(_)):
        if pyy[i] == 0 or tyy[i] == 0.0:
            x += 1
            xxs.append(x)
            pyys.append(pyy[i])
            tyys.append(tyy[i])

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号
    fig = plt.figure()
    left, bottom, width, height = 0.1, 0.1, 0.89, 0.85
    ax = fig.add_axes([left, bottom, width, height])
    ax.plot(xxs, pyys, c='black', alpha=0.1)
    ax.scatter(xxs, pyys, c='blue', s=10)
    ax.plot(xxs, tyys, c='black', alpha=0.1)
    ax.scatter(xxs, tyys, c='red', s=10)
    title = "Pressure(blue) and Temperature(red) Change"
    ax.set_title(title, fontsize=12)
    ax.set_xlabel(adjustmentData, fontsize=10)
    ax.set_ylabel("degree / hpa", fontsize=10)
    ax.tick_params(axis='both', which='major', labelsize=10)

    left, bottom, width, height = 0.15, 0.7, 0.24, 0.24
    ax1 = fig.add_axes([left, bottom, width, height])
    ax1.plot(pressures, 'b')
    ax1.tick_params(axis='both', which='major', labelsize=6)

    plt.axes([0.74, 0.7, 0.24, 0.24])
    plt.plot(temperatures, 'r')
    plt.tick_params(axis='both', which='major', labelsize=6)
    # plt.show() #该句有warning，可以用下面代码替换
    plt.savefig(adjustmentData+'.png', bbox_inches='tight')
