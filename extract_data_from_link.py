import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os,pathlib
from pathlib import Path
import pandas as pd
fpInput='all_filter.txt'
f1=open(fpInput,'r')
arrInputs=f1.read().strip().split('\n')
f1.close()
fopOutput='/home/hungphd/Desktop/HelpTu_Csvs/'
Path(fopOutput).mkdir(exist_ok=True)
fpCsv=fopOutput+'all.csv'
fpExcel=fopOutput+'all.xlsx'
# strLink='https://nhathuoclongchau.com.vn/thuoc/farzincol-10mg-3786.html'

strTab=arrInputs[0].split('\t')
strLink=strTab[0]
strProductName='\t'.join(strTab[1:])
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
max_entries=3
driver.get(strLink)
# divImg = driver.find_element(By.XPATH, "//div[@class='cursor-pointer']")
lstImgs=driver.find_elements(By.XPATH, "//div[@class='cursor-pointer']/img")
lstAllImgs=[]
for img in lstImgs:
    strSrcImg=img.get_attribute('src')
    lstAllImgs.append(strSrcImg)
    # strAltImg=img.get_attribute('alt')
    # print(strSrcImg)
    # print(strAltImg)
strTextSrcImg='\n\n'.join(lstAllImgs)
lstTables=driver.find_elements(By.XPATH, "//table[@class='content-list']")
tblContent=lstTables[0]
lstColumn1s=tblContent.find_elements(By.XPATH, "//tr/td[1]")
lstColumn2s=tblContent.find_elements(By.XPATH, "//tr/td[2]")
lstStr1=[item.get_attribute('innerText') for item in lstColumn1s]
lstStr2=[item.get_attribute('innerText') for item in lstColumn2s]
dictCols={}
dictCols['No']=1
dictCols['ProductName']=strProductName
dictCols['Image']=strTextSrcImg
dictCols['Link']=strLink
for i in range(0,len(lstStr1)):
    dictCols[lstStr1[i]]=lstStr2[i]
print(dictCols.keys())
import csv
lstColumns=['No','ProductName','Image','Số đăng ký','Nhà sản xuất','Nước sản xuất','Thuốc cần kê toa','Link']
# fcsv=open(fpCsv, 'w', newline='')
# writer = csv.writer(fcsv)
# writer.writerow(lstColumns)
lstRows=[]
for col in lstColumns:
    strVal='Not Found'
    if col in dictCols.keys():
        strVal=dictCols[col]
    lstRows.append(strVal)
# writer.writerow(lstRows)
# import pandas as pd

df=pd.DataFrame(columns=lstColumns)
df.loc[len(df)]=lstRows
df.to_csv(fpCsv,index=False)
new_dataFrame = pd.read_csv(fpCsv)
new_excel = pd.ExcelWriter(fpExcel)
new_dataFrame.to_excel(new_excel, index=False)
new_excel.save()



# print('{}'.format(len(lstTables)))
# print('{}\n{}'.format(lstStr1,lstStr2))
# print('{}\n{}'.format(len(lstStr1),len(lstStr2)))
# for table in lstTables:
#     pass
