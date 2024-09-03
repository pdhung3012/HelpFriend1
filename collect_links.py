import traceback

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os,pathlib
from pathlib import Path

lstAlphabets=list(map(chr, range(97, 123)))
default_page_limits=50
page_limits=1
max_entries=False

fop_output='/home/hungphd/Desktop/HelpTu_Links/'
Path(fop_output).mkdir(exist_ok=True)
fpAll=fop_output+'all.txt'
f1 = open(fpAll, 'w')
f1.write('')
f1.close()
f1=open(fop_output+'all_failed.txt','w')
f1.write('')
f1.close()

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
max_entries=3
for i in range(0,len(lstAlphabets)):
    page_limits=default_page_limits
    page=0
    while page <page_limits:
        index_entry=1
        page+=1
        while index_entry<=max_entries:
            is_ok=False
            try:
                print('begin {} {} {}'.format(lstAlphabets[i],page,index_entry))
                strLink = 'https://nhathuoclongchau.com.vn/thuoc/tra-cuu-thuoc-a-z?alphabet={}&page={}'.format(
                    lstAlphabets[i], page)
                # driver.get("https://nhathuoclongchau.com.vn/thuoc/tra-cuu-thuoc-a-z?alphabet=A&page=2")
                driver.get(strLink)
                div = driver.find_element(By.XPATH, "//div[@class='container-lite']")
                if page == 1:

                    lstUls = div.find_elements(By.XPATH,
                                               "//ul[contains(@class, 'flex') and contains(@class, 'items-center')]")
                    ulLast = lstUls[-1]
                    lstLis = ulLast.find_elements(By.XPATH, 'li')
                    lstContent = [item.get_attribute('innerText') for item in lstLis]
                    lstPageNumbers = []
                    for item in lstContent:
                        isSuccess = True
                        try:
                            num = int(item)
                        except Exception as e:
                            isSuccess = False
                        if isSuccess:
                            lstPageNumbers.append(int(item))
                    if len(lstPageNumbers) > 0:
                        page_limits = max(lstPageNumbers)
                    else:
                        page_limits = 1
                    print('page limit {}'.format(page_limits))


                # print(lstContent)
                listLinks = div.find_elements(By.XPATH, "//a")
                lstTextFoFiles = []
                for link in listLinks:
                    strTitle = link.get_attribute('title')
                    if len(strTitle) >= 5:
                        lstTextFoFiles.append('{}\t{}'.format(link.get_attribute('href'), link.get_attribute('title')))
                    #     print('{}\t{}'.format(link.get_attribute('href'), link.get_attribute('title')))
                name_write = '{}_{}.txt'.format(lstAlphabets[i], page)
                if len(lstTextFoFiles)>0:
                    f1 = open(fop_output + name_write, 'w')
                    f1.write('\n'.join(lstTextFoFiles))
                    f1.close()
                    f1 = open(fpAll, 'a')
                    f1.write('\n'.join(lstTextFoFiles) + '\n')
                    f1.close()
                    is_ok=True
            except Exception as ex:
                traceback.print_exc()
            print('end {}_{}.txt {} {} {}'.format(lstAlphabets[i], page, is_ok, index_entry, len(lstTextFoFiles)))
            if not is_ok:
                f1=open(fop_output+'all_failed.txt','a+')
                f1.write('{}_{}.txt'.format(lstAlphabets[i], page)+'\n')
                f1.close()
                index_entry+=1
            else:
                break




# print(div.get_attribute('innerText'))
driver.close()