from bs4 import BeautifulSoup
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from datetime import date,timedelta,datetime
import pandas as pd
from time import sleep

def Plan_Den(num):
    list = {
    0: 'STT',
    1: 'Tên Tàu',
    2: 'Quốc Tịch',
    3: 'Hô Hiệu',
    4: 'GT',
    5: ' DWT',
    6: 'Chiều dài L.O.A(m)',
    7: 'Mớn nước(m)',
    8: 'Hàng hóa',
    9: 'Bến cảng',
    10: 'Giờ đến',
    11: 'Đại lý'
    }
    return list.get(num)

def Plan_Roi(num):
    list = {
    0: 'STT',
    1: 'Tên Tàu',
    2: 'Quốc Tịch',
    3: 'Hô Hiệu',
    4: 'GT',
    5: 'DWT',
    6: 'Chiều dài L.O.A(m)',
    7: 'Mớn nước(m)',
    8: 'Hàng hóa',
    9: 'Cầu phao',
    10: 'Giờ rời',
    11: 'Đại lý'
    }
    return list.get(num)

def Plan_Di(num):
    list = {
    0: 'STT',
    1: 'Tên Tàu',
    2: 'Quốc Tịch',
    3: 'Hô Hiệu',
    4: 'GT',
    5: 'DWT',
    6: 'Chiều dài L.O.A(m)',
    7: 'Mớn nước(m)',
    8: 'Loại hàng hóa',
    9: 'Vị trí neo đâu từ',
    10: 'Vị trí neo đậu đến',
    11: 'Giờ dời',
    12: 'Đại lý'
    }
    return list.get(num)

def all_class(num_Plan,num_Table):
    list_class = {
    0: Plan_Den(num_Table),
    1: Plan_Roi(num_Table),
    2: Plan_Di(num_Table)
    }
    return list_class.get(num_Plan)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--blink-settings=imagesEnabled=false')
chrome_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options = chrome_options)

addr = "******"
driver.get(addr)

Data_PlanDen = pd.DataFrame()
Data_PlanRoi = pd.DataFrame()
Data_PlanDi = pd.DataFrame()

dates = []
start_day = date(2023,7,25)
end_day = date(2023,10,28)
temp = start_day

while temp <= end_day:
    dates.append(datetime.strftime(temp,'%d-%m-%Y'))
    temp += timedelta(days=1)
print(dates)

for date in dates:
    driver.find_element('xpath','//*[@id="ctl03_rdpNgay_dateInput"]').clear()
    driver.find_element('xpath','//*[@id="ctl03_rdpNgay_dateInput"]').send_keys(date)
    driver.find_element('xpath','//*[@id="ctl03_btmSubmit"]').click()

    soup = BeautifulSoup(driver.page_source, "html.parser")
    for num_Plan, table in enumerate(soup.find_all('table',{'class':'rgMasterTable'})):
        tmp = pd.DataFrame()
        for num_Bill, tr in enumerate(table.find('tbody').find_all('tr')):
            for num_Table, td in enumerate(tr.find_all('td')):
                tmp.at[num_Bill,all_class(num_Plan,num_Table)] = td.get_text(strip=True)
            tmp.at[num_Bill,"Ngày"] = date
        if num_Plan == 0:
            Data_PlanDen = pd.concat([Data_PlanDen, tmp])
        if num_Plan == 1:
            Data_PlanRoi = pd.concat([Data_PlanRoi, tmp])
        if num_Plan == 2:
            Data_PlanDi = pd.concat([Data_PlanDi, tmp])