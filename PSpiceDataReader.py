#! python3
# -*- coding:utf-8 -*-
# Author: YiGeeker
# Data: 2017.6.9
# Version: 1.0

import csv
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt


class CData:
    '''Import PSpice output value from *.txt or *.csv file'''

    def __init__(self, fileName):
        self.__readAll = True   # Reserved word for next version
        if not (fileName.endswith('.csv') or fileName.endswith('.txt')):
            raise ValueError("Please select CSV or TXT file, and add .csv or .txt to the end")

        self.__success = True
        if self.__readAll:
            fin = open(fileName, 'rt')
            try:
                if fileName.endswith('.csv'):

                    # Get probe names
                    headerRow = fin.readline()
                    headerRow = headerRow[:-1]  # Remove the end '\n'
                    nameList = headerRow.split(', ')
                    del nameList[0]  # Delete 'Time'
                    self.__names = [name.rstrip() for name in nameList]

                    # Get value at specific time
                    valueNum = len(self.__names)
                    self.__valueList = [[] for i in range(valueNum+1)]

                    contents = csv.reader(fin)
                    for rowList in contents:
                        for i, num in enumerate(rowList):
                            self.__valueList[i].append(float(num))
                else:
                    # Get probe names
                    headerRow = fin.readline()
                    headerRow = headerRow[:-1]  # Remove the end '\n'
                    nameList = headerRow.split(' ')
                    self.__names = [name for name in nameList if len(name)]
                    del self.__names[0]  # Delete 'Time'

                    # Get value at specific time
                    valueNum = len(self.__names)
                    self.__valueList = [[] for i in range(valueNum+1)]

                    for valueRow in fin:
                        preRowList = valueRow[:-1].split(' ')  # Remove the end '\n'
                        rowList = [name for name in preRowList if len(name)]
                        for i, num in enumerate(rowList):
                            self.__valueList[i].append(float(num))
            except:
                self.__success = False
                print("Please input valid file")  # Failed in import file
            fin.close()
        else:
            self.__fileName = fileName

    @property
    def probeNames(self):
        if not self.__success:
            return 0

        if self.__readAll:
            return tuple(self.__names)

    @property
    def timeLine(self):
        if not self.__success:
            return 0

        if self.__readAll:
            return self.__valueList[0]

    def NameValues(self, probeName):
        '''Get probe value from probe name, and return 0 for failing'''

        if not self.__success:
            return 0

        if self.__readAll:
            try:
                i = self.__names.index(probeName)+1
                return self.__valueList[i]
            except:
                print("Please input valid probe name")
                return 0

    def IndexValues(self, index):
        '''Get probe value from probe index, and return 0 for failing'''

        if not self.__success:
            return 0

        if self.__readAll:
            try:
                return self.__valueList[index+1]
            except:
                print("Please input valid probe index")
                return 0

    def PlotFig(self):
        '''Plot the data'''

        if not self.__success:
            print("Failed in reading data")
            return

        time = self.__valueList[0]
        plt.figure('PSpiece Data')
        for i in range(1, len(self.__valueList)):
            plt.plot(time, self.__valueList[i], label=self.__names[i-1])
        plt.grid(True)
        plt.xlim(time[0], time[-1])
        plt.xlabel('Time(s)', fontproperties='Times New Roman')
        plt.ylabel('Value(V or A)', fontproperties='Times New Roman')
        plt.legend(loc='best')
        plt.show()
