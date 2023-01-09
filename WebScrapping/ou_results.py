#before running the program check whether the osmania reult website of 
#the given url for any hall ticket number is running or not
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np 
import time

start_time=time.time()
df=pd.DataFrame(data=[])
RollNumbers=np.arange(160720733061,160720733120)
for htno in RollNumbers:
    response = requests.get(f'https://www.osmania.ac.in/res07/20221206.jsp?mbstatus=SEARCH&htno='+str(htno)+'&Submit.x=21&Submit.y=8', verify=False)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    #print(soup.prettify)
    tds=soup.find_all('td')

    #if student htno is not valid
    if(len(tds)<75):
        print(htno,"result not available")
        continue;

    i=70
    while tds[i].get_text()!=' Result':
        i+=1     
    tds=tds[24:i-1]

    p_count=0
    f_count=0

    grades=dict({})
    grades["RollNo"] = str(htno)[8:]
    for i in range (0,len(tds),5):
        if(tds[i+3].get_text()[1:3])=='10':
            grades[(tds[i+1].get_text())[1:]]=int(10)
            p_count+=1
        elif(tds[i+3].get_text()[1]).isnumeric():
            grades[(tds[i+1].get_text())[1:]]=int((tds[i+3].get_text())[1])
            if(int((tds[i+3].get_text())[1]))!=0:
                p_count+=1
            else:
                f_count+=1
        else:
            grades[(tds[i+1].get_text())[1:]]=(tds[i+3].get_text())[1]
            f_count+=1

    grades["passed"]=p_count
    grades["failed"]=f_count

    df = df.append(grades, ignore_index=True)
    print(htno,"result appended to datafrmae")

df.columns=df.columns.str.rstrip()
df=df.rename(columns={'DATA STRUCTURES AND ALGORITHMS':'DSA', 'OPERATING SYSTEMS':'OS','OPERATING SYSTEM LAB':'OS-LAB', 'COMPUTER ORGANIZATION':'CO', 'SIGNALS AND SYSTEMS':'SS','MATHEMATICS-III':'M-III', 'COMPUTER ORGANIZATION LAB':'CO-LAB','DATABASE MANAGEMENT SYS.LAB':'DBMS-LAB', 'EFFECTIVE TECH.COMM.IN ENGLISH':'ETCE','FINANCE AND ACCOUNTING':'FA', 'DATABASE MANAGEMENT SYSTEMS':'DBMS','BASIC ELECTRONICS':'BE', 'BASIC ELECTRONICS LAB':'BE_LAB', 'DIGITAL ELECTRONICS':'DE','DISCRETE MATHEMATICS':'DM', 'MATHEMATICS-I':'M-I', 'MATHEMATICS-II':'M-II','OOP USING JAVA':'JAVA', 'PHYSICS':'PHY', 'PROG.FOR PROBLEM SOLVING':'PPS', 'CHEMISTRY':'CHEM','BASIC ELECTRICAL ENG.':'BEE', 'OPERATIONS RESEARCH':'OR'})
df=df.reindex(columns=['RollNo', 'OS','OS-LAB', 'CO', 'SS', 'M-III', 'CO-LAB', 'DBMS-LAB', 'ETCE', 'FA', 'DBMS', 'DSA', 'BE', 'BE_LAB', 'DE', 'DM', 'JAVA',  'OR', 'PHY', 'BEE', 'PPS', 'CHEM', 'M-I', 'passed', 'failed'])
roll_count=df["RollNo"].count()
df.loc['Total'] = df.apply(lambda x: x.count(), axis=0).astype(int)
df.loc['Total', 'RollNo'] = "Total"
df.loc['Total', 'passed'] = df.loc['Total', 'failed'] = ""
df.to_csv("CSE_B_results.csv", index=False)
end_time=time.time()
print("Time taken for the whole scrapping is ",end_time - start_time)
print("Completed! check the csv file")