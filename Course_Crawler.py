
# coding: utf-8
import requests
import sys
from bs4 import BeautifulSoup as bs
import os
import csv
import codecs

os.chdir('C:/Users/SyuShengWei/Desktop/Practice_Crawler')

infile_name = "course_code.csv"
outfile_name = "questionnaire.csv"

DataHeader = ["課程代碼","授課老師","大題","小題題號","小題問題","Ans_1","Ans_2","Ans_3","Ans_4","Ans_5","Ans_6"]
Course_Code = []
with codecs.open(infile_name,'r','utf-8') as infile:
    Course_Code = infile.readlines()

while(Course_Code != []):
    the_course = Course_Code.pop(0).strip('\n')
    print(the_course,end=' : ')
### this field will login the NCKU course degree system
    try:
        headers = {
        'Cookie': 'lang=zh_tw; PHPSESSID=m12b0kr02odrotg3jft8nbmbtbuj80q6i9spoloq87a5s21v9a00; IPCZQX03a36c6c0a=8f0062008c7432705901c001a35157c52f7c1668; _ga=GA1.3.1189020302.1480766770; _gat=1',
        'Host': 'tfcfd.acad.ncku.edu.tw',
        'Origin': 'http://tfcfd.acad.ncku.edu.tw',
        'Referer': 'http://tfcfd.acad.ncku.edu.tw/ncku/tfcfd/service/login_m.php',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
    ##studentid = input("Please input the studentid and pwd for Cheng-Kung Portal , ID:")
    ##pwd = input("Please input the studentid and pwd for Cheng-Kung Portal ,PWD:")
        studentid = "studentid"
        pwd = "pwd"

        login_data = {'studentid': studentid, 'pwd': pwd}
        login_request_url = "http://tfcfd.acad.ncku.edu.tw/ncku/tfcfd/service/login.php"
        rs = requests.session()
        rs.post(login_request_url, login_data)

    ### this field will connect to the result page of each class

        data_url = 'http://tfcfd.acad.ncku.edu.tw/ncku/tfcfd/service/courser1.php?tco_no=' + the_course
        requests_data = rs.get(data_url, headers=headers)
        requests_data.encoding = "utf-8"

    ### this filed will find out the code and the teacher of the course
        import re

        _PK_of_a_record = []

        Request_Line = requests_data.text.split('\n')
        _course_message = re.search('科目代號[:][a-zA-z0-9]*',requests_data.text).group(0).split(":")
        ##print(_class_message)
        _course_code = _course_message[1]

        ##add ? after * can help re to be non-gready search.
        _teacher_message = re.findall('(\D{2,3}\(\D*?,\D*?\))',requests_data.text)
        ##print(_teacher_message)

        _teachers = ''
        _teachers += _teacher_message[0]
        for i in range(1,len(_teacher_message)):
            _teachers += '&'
            _teachers += _teacher_message[i]

        _PK_of_a_record.append(_course_code)
        _PK_of_a_record.append(_teachers)
        #print(_PK_of_a_record)

    ### this field will record every questions and answers

        Question_List = ["1","2","3","4","5","6","7","8","9","10","11","12","13"]
        soup = bs(requests_data.text, "lxml")
        Find_All_Result = soup.findAll('td')
        _Answer_List = []
        title_of_question = ""
        for i in range(len(Find_All_Result)):

            if Find_All_Result[i].string != None:
                the_word = Find_All_Result[i].string.replace('\xa0','').replace('.','')
                #print(i,end = ' : ')
                #print(the_word)
                if "部分" in the_word or "自評" in the_word :
                    title_of_question = the_word
                    continue


                if the_word in Question_List:
                    a_record = []
                    a_record.append(_PK_of_a_record[0])
                    a_record.append(_PK_of_a_record[1])
                    a_record.append(title_of_question)
                    a_record.append(the_word)
                    a_record.append(Find_All_Result[i+1].string)

                    answer_index = 3
                    while True:
                        answer_word = Find_All_Result[i+answer_index].string
                        if answer_word != None :
                            answer_word = answer_word.replace('\xa0','').replace('.','')
                            if "%" in answer_word :
                                a_record.append(Find_All_Result[i+answer_index].string)
                                answer_index += 1
                            else: break
                        else:
                            break
                    ##print(a_record)
                    _Answer_List.append(a_record)
                else:
                    continue
    ### this file will output the result
        with codecs.open(outfile_name,'a+','utf-8') as outfile:
            w = csv.DictWriter(outfile,fieldnames = DataHeader,lineterminator='\n')
            w.writeheader()
            for i in range(len(_Answer_List)):
                if len(_Answer_List[i]) == 11 :
                    w.writerow({DataHeader[0]:_Answer_List[i][0],
                                DataHeader[1]:_Answer_List[i][1],
                                DataHeader[2]:_Answer_List[i][2],
                                DataHeader[3]:_Answer_List[i][3],
                                DataHeader[4]:_Answer_List[i][4],
                                DataHeader[5]:_Answer_List[i][5],
                                DataHeader[6]:_Answer_List[i][6],
                                DataHeader[7]:_Answer_List[i][7],
                                DataHeader[8]:_Answer_List[i][8],
                                DataHeader[9]:_Answer_List[i][9],
                                DataHeader[10]:_Answer_List[i][10]})
                elif len(_Answer_List[i]) == 10 :
                    w.writerow({DataHeader[0]:_Answer_List[i][0],
                                DataHeader[1]:_Answer_List[i][1],
                                DataHeader[2]:_Answer_List[i][2],
                                DataHeader[3]:_Answer_List[i][3],
                                DataHeader[4]:_Answer_List[i][4],
                                DataHeader[5]:_Answer_List[i][5],
                                DataHeader[6]:_Answer_List[i][6],
                                DataHeader[7]:_Answer_List[i][7],
                                DataHeader[8]:_Answer_List[i][8],
                                DataHeader[9]:_Answer_List[i][9]})
        print('Success')
    except:
        Course_Code.append(the_course)
        print('Error')
        print(Find_All_Result)