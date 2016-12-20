import csv
import os

os.chdir("C:/Users/SyuShengWei/Desktop/ClassData")
infile = open('example.csv','a',newline = '')
infile.close()

DataList = [[1,2,3,4,5],[11,12,13,14,15],['11','12','13','14',"15"]]
DataHeader = ["NO1","NO2","NO3","NO4","NO5"]
with open ('example.csv','a') as outfile:
    ##lineterminator='\n' can help to deal with the extra new line
    w = csv.DictWriter(outfile,fieldnames = DataHeader,lineterminator='\n')

    w.writeheader()
    for i in range(len(DataList)):
        w.writerow({DataHeader[0]:DataList[i][0],
                    DataHeader[1]:DataList[i][1],
                    DataHeader[2]:DataList[i][2],
                    DataHeader[3]:DataList[i][3],
                    DataHeader[4]:DataList[i][4]})
print(DataList)