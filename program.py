import requests
from bs4 import BeautifulSoup

def scrapping():
    url = "https://eatandmeet.sk/"
    html_response = requests.get(url)

    print(html_response)

    #test
    with open("test_scrap","w", encoding="utf-8") as f:
        f.write(html_response.text)