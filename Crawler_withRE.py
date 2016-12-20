
# coding: utf-8

# In[128]:


import requests
import sys
from bs4 import BeautifulSoup as bs

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
studentid = "H34021042"
pwd = ""


login_data = {'studentid': studentid, 'pwd': pwd}
login_request_url = "http://tfcfd.acad.ncku.edu.tw/ncku/tfcfd/service/login.php"
rs = requests.session()
rs.post(login_request_url, login_data)


# In[129]:

data_url = 'http://tfcfd.acad.ncku.edu.tw/ncku/tfcfd/service/courser1.php?tco_no=A92G700'
requests_data = rs.get(data_url, headers=headers)
requests_data.encoding = "utf-8"


# In[130]:

Request_Line = requests_data.text.split('\n')
import re
_class_message = re.search('科目代號[:][a-zA-z0-9]*',requests_data.text).group(0)
print(_class_message)
##add ? after * can help re to be non-gready search.
_teacher_message = re.findall('(\D{2,3}\(\D*?,\D*?\))',requests_data.text)
print(_teacher_message)


# In[176]:

soup = bs(requests_data.text, "lxml")
_Answer_List = []
for td in soup.findAll('td'):
    if td.string!=None :
        print(td.string)



# In[ ]:



