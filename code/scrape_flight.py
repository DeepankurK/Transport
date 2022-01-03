import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
import time 
import re
import pandas as pd
import sys
from csv import DictWriter
from datetime import datetime
option = webdriver.ChromeOptions()
#option.add_argument('headless')
option.add_argument("--disable-gpu")
option.add_argument("no-sandbox")
driver_path="/usr/bin/chromedriver"


df=pd.DataFrame(columns=["Date","Departure","Arrival","POI"])
d={31:3,1:4,2:4,3:4,4:4,5:4,6:4}
for ke,va in d.items():
    for t in range(0,22,6):
        driver = webdriver.Chrome(options=option, executable_path=driver_path)
        driver.get("https://www.flightstats.com/v2/flight-tracker/departures/JFK/?year=2021&month="+str(va)+"&date="+str(ke)+"&hour="+str(t))
        fl=0
        while(fl==0):
            soup_file=driver.page_source
            soup = BeautifulSoup(soup_file, 'html.parser')
            #print(soup)
            data=soup.find_all(class_="table__TableRowWrapper-s1x7nv9w-9 ggDItd")
            #print(data)
            for i in data:
                q=re.sub('<[^>]+>', ' ', str(i) )
                ls=q.strip().split('  ')
                tim=[p for p in ls if ':' in p]
                #print(str(ke)+"."+str(va),tim)
                df=df.append({"Date":str(ke)+"."+str(va),"Departure":tim[0],"Arrival":tim[1],"POI":ls[-1]},ignore_index=True)
            if len(soup.find_all(class_="pagination__PageNavigationContainer-s1515b5x-1 djrWkq"))!=0:
                curr=soup.find_all(class_="pagination__PageNavItem-s1515b5x-2 eUzddn")
                curr=re.sub('<[^>]+>',' ', str(curr[0])).strip()
                foo = driver.find_elements_by_css_selector("div")
                k=0
                for i in foo:
                    if fl==0 and i.text=='«':
                        fl=1
                        continue
                    elif fl==1 and i.text==str(curr):
                        fl=2
                        continue
                    elif fl==2 and str(i.text)==str(int(curr)+1):
                        k=i
                        break
                if k!=0:
                    i.click()
                    print(ke,t,curr)
                    fl=0
            else: 
                fl=3
        driver.close()
        time.sleep(1)
        driver.quit()
df=df.sort_values(['Date','Departure'],axis=1)
df.head(5)
df.drop_duplicates(inplace=True)
df.to_csv("Data_departure.csv",index=False)