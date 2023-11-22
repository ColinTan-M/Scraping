from bs4 import BeautifulSoup
import pandas as pd
import requests
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from datetime import date

def Plan_Roi(num):
    list = {
    0: 'STT',
    1: 'Thời gian',
    2: 'Tên tàu',
    3: 'Mớn nước',
    4: 'LOA',
    5: 'DWT',
    6: 'Tàu lai',
    7: 'T.Luồng',
    8: 'Từ',
    9: 'Đến',
    10: 'Đại lý'}
    return list.get(num)

def Plan_DiChuyen(num):
    list = {
    0: 'STT',
    1: 'Thời gian',
    2: 'Tên tàu',
    3: 'Mớn nước',
    4: 'LOA',
    5: 'DWT',
    6: 'Tàu lai',
    7: 'T.Luồng',
    8: 'Từ',
    9: 'Đến',
    10: 'Đại lý'}
    return list.get(num)

def Plan_Vao(num):
    list = {
    0: 'STT',
    1: 'Thời gian',
    2: 'Tên tàu',
    3: 'Mớn nước',
    4: 'LOA',
    5: 'DWT',
    6: 'Tàu lai',
    7: 'T.Luồng',
    8: 'Từ',
    9: 'Đến',
    10: 'Đại lý'}
    return list.get(num)

def Plan_QuaLuong(num):
    list = {
    0: 'STT',
    1: 'Thời gian',
    2: 'Tên tàu',
    3: 'Mớn nước',
    4: 'LOA',
    5: 'DWT',
    6: 'Tên luồng',
    7: 'Xuất phát',
    8: 'Nơi đến'}
    return list.get(num)

data_Plan_Roi = pd.DataFrame()
data_Plan_DiChuyen = pd.DataFrame()
data_Plan_Vao = pd.DataFrame()
data_Plan_QuaLuong = pd.DataFrame()

#Select date
start_day = date(2022, 10, 21)
end_day = date(2022, 12, 31)

today = date.today()
d1 = start_day - today
d2 = end_day - today

urls = range(d1.days,d2.days,1)
    
def get_data(url):
    global data_Plan_Roi
    global data_Plan_DiChuyen
    global data_Plan_Vao
    global data_Plan_QuaLuong

    adrr = f"****{url}"
    r = requests.get(adrr)
    soup = BeautifulSoup(r.text, 'html.parser')
    date = soup.find("span",{'id':'lblCapShowDate'}).get_text(strip=True)[-10:]
    print(adrr)

    tr = soup.find_all("tr")
    for tr in soup.find_all("tr"):
        if tr.find("td",{'id':'TD_ShowShipPlan_Roi'}):
            td = tr.find("td",{'id':'TD_ShowShipPlan_Roi'})
            # print(td)
            tmp = pd.DataFrame()
            for i, tr_1 in enumerate(td.find_all("tr")):
                if i>0:
                    for j, td_1 in enumerate(tr_1.find_all("td")):
                        tmp.at[i,Plan_Roi(j)] = td_1.get_text(strip=True)
                    tmp.at[i,'Ngày'] = date
            data_Plan_Roi = pd.concat([data_Plan_Roi, tmp])
            # print(tmp)


        if tr.find("td",{'id':'TD_ShowShipPlan_DiChuyen'}):
            td = tr.find("td",{'id':'TD_ShowShipPlan_DiChuyen'})
            # print(td)
            tmp = pd.DataFrame()
            for i, tr_1 in enumerate(td.find_all("tr")):
                if i>0:
                    for j, td_1 in enumerate(tr_1.find_all("td")):
                        tmp.at[i,Plan_DiChuyen(j)] = td_1.get_text(strip=True)
                    tmp.at[i,'Ngày'] = date
            data_Plan_DiChuyen = pd.concat([data_Plan_DiChuyen, tmp])


        if tr.find("td",{'id':'TD_ShowShipPlan_Vao'}):
            td = tr.find("td",{'id':'TD_ShowShipPlan_Vao'})
            # print(td)
            tmp = pd.DataFrame()
            for i, tr_1 in enumerate(td.find_all("tr")):
                if i>0:
                    for j, td_1 in enumerate(tr_1.find_all("td")):
                        tmp.at[i,Plan_Vao(j)] = td_1.get_text(strip=True)
                    tmp.at[i,'Ngày'] = date
            data_Plan_Vao = pd.concat([data_Plan_Vao, tmp])


        if tr.find("td",{'id':'TD_ShowShipPlan_QuaLuong'}):
            td = tr.find("td",{'id':'TD_ShowShipPlan_QuaLuong'})
            # print(td)
            tmp = pd.DataFrame()
            for i, tr_1 in enumerate(td.find_all("tr")):
                if i>0:
                    for j, td_1 in enumerate(tr_1.find_all("td")):
                        tmp.at[i,Plan_QuaLuong(j)] = td_1.get_text(strip=True)
                    tmp.at[i,'Ngày'] = date
            data_Plan_QuaLuong = pd.concat([data_Plan_QuaLuong, tmp])
    sleep(0.5)

with ThreadPoolExecutor() as executor:
    executor.map(get_data,urls)
