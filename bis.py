import requests
from bs4 import BeautifulSoup
import  string
import csv
import time
import logging

s=requests.Session()
logging.basicConfig(filename="scraper_"+time.strftime("%Y%m%d")+".log", filemode="w", format="%(name)s - %(levelname)s - %(message)s")
with open("employee_file_"+time.strftime("%Y%m%d")+".csv", mode='a+') as daily_file:
                    daily_writer = csv.writer(daily_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    daily_writer.writerow(["StockName","Opening","DailyHigh","DailyLow","YearHigh","YearLow","Market"])
for letter in string.ascii_uppercase:
    response=s.get("https://www.borsaitaliana.it/borsa/azioni/listino-a-z.html?initial="+letter+"&lang=en")
    table_content = BeautifulSoup(response.content, 'html.parser')

    letter_table=table_content.find("div",{"data-bb-view":"list-aZ-stream"})

    for element in letter_table.find_all("a",{"href":True,"class":"u-hidden -xs"}):
            if("id=" not in element["href"] and "code=" not in element["href"]):
                try:
                    single_stock_page =  BeautifulSoup(s.get("https://www.borsaitaliana.it/"+element["href"]).content, 'html.parser')
                    stock_name = single_stock_page.find("h1",{"class":"t-text -flola-bold -size-xlg -inherit"}).find("a",{"href":True})
                    stock_data = single_stock_page.find("div",{"class":"l-box -prl | h-bg--gray | l-screen -sm-half -md-half"})
                    single_stock_data_table = stock_data.find("table",{"class":"m-table -clear-mtop"})
                    data_list = single_stock_data_table.find_all('span',class_=lambda x: "t-text -right" in x)
                    with open("employee_file_"+time.strftime("%Y%m%d")+".csv", mode='a+') as daily_file:
                        daily_writer = csv.writer(daily_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        daily_writer.writerow([stock_name.get_text(),str(data_list[0].get_text()),str(data_list[1].get_text()),str(data_list[2].get_text()),str(data_list[3].get_text()).split("-")[0].strip(),str(data_list[4].get_text()).split("-")[0].strip(),str(data_list[5].get_text()).strip()])
                    logging.info("Analyzed: https://www.borsaitaliana.it/"+element["href"])
                except Exception as ex:
                    logging.error(ex)