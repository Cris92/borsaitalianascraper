import requests
from bs4 import BeautifulSoup
import  string


s=requests.Session()
for letter in string.ascii_uppercase:
    response=s.get("https://www.borsaitaliana.it/borsa/azioni/listino-a-z.html?initial="+letter+"&lang=en")
    table_content = BeautifulSoup(response.content, 'html.parser')

    letter_table=table_content.find("div",{"data-bb-view":"list-aZ-stream"})

    for element in letter_table.find_all("a",{"href":True,"class":"u-hidden -xs"}):
            if("id=" not in element["href"] and "code=" not in element["href"]):
                print(element["href"])
                s.get("https://www.borsaitaliana.it/"+element["href"])
                print("-------------------")