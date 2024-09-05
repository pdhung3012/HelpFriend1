import time
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
lstColumns=['No','ProductName','Image','Số đăng ký','Nhà sản xuất','Nước sản xuất','Thuốc cần kê toa','Link']

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
df = pd.DataFrame(columns=lstColumns)
# strLink='https://nhathuoclongchau.com.vn/thuoc/farzincol-10mg-3786.html'
indexNo=0
max_entries=10
for i in range(0,len(arrInputs)):
    is_ok=False
    index_run=0
    while index_run<max_entries:
        index_run+=1
        try:
            strTab = arrInputs[i].split('\t')
            strLink = strTab[0]
            strProductName = '\t'.join(strTab[1:])
            driver.get(strLink)
            # divImg = driver.find_element(By.XPATH, "//div[@class='cursor-pointer']")
            lstImgs = driver.find_elements(By.XPATH, "//div[@class='cursor-pointer']/img")
            lstAllImgs = []
            for img in lstImgs:
                strSrcImg = img.get_attribute('src')
                lstAllImgs.append(strSrcImg)
                # strAltImg=img.get_attribute('alt')
                # print(strSrcImg)
                # print(strAltImg)
            strTextSrcImg = '\n\n'.join(lstAllImgs)
            lstTables = driver.find_elements(By.XPATH, "//table[@class='content-list']")
            tblContent = lstTables[0]
            lstColumn1s = tblContent.find_elements(By.XPATH, "//tr/td[1]")
            lstColumn2s = tblContent.find_elements(By.XPATH, "//tr/td[2]")
            lstStr1 = [item.get_attribute('innerText') for item in lstColumn1s]
            lstStr2 = [item.get_attribute('innerText') for item in lstColumn2s]


            is_ok=True
            indexNo+=1
            dictCols = {}
            dictCols['No'] = indexNo
            dictCols['ProductName'] = strProductName
            dictCols['Image'] = strTextSrcImg
            dictCols['Link'] = strLink
            for iCol in range(0, len(lstStr1)):
                dictCols[lstStr1[iCol]] = lstStr2[iCol]
            lstRows = []
            for col in lstColumns:
                strVal = 'Not Found'
                if col in dictCols.keys():
                    strVal = dictCols[col]
                lstRows.append(strVal)
            # writer.writerow(lstRows)
            # import pandas as pd


            df.loc[len(df)] = lstRows
            df.to_csv(fpCsv, index=False)
            df.to_csv(fpExcel, index=False)
        except Exception as e:
            traceback.print_exc()
        print('Line {}\t{}\t{}'.format(i,is_ok,index_run))
        time.sleep(3)
        if is_ok:
            break
        else:
            pass
            # time.sleep(2)
    # if i>=10:
    #     break
# max_entries=3
# print(dictCols.keys())
import csv
# fcsv=open(fpCsv, 'w', newline='')
# writer = csv.writer(fcsv)
# writer.writerow(lstColumns)
# new_dataFrame = pd.read_csv(fpCsv)
# new_excel = pd.ExcelWriter(fpExcel)
# new_dataFrame.to_excel(new_excel, index=False)
# new_excel.save()



# print('{}'.format(len(lstTables)))
# print('{}\n{}'.format(lstStr1,lstStr2))
# print('{}\n{}'.format(len(lstStr1),len(lstStr2)))
# for table in lstTables:
#     pass
