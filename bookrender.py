import requests
from bs4 import BeautifulSoup


def search_book(keyword):
    r = requests.get('https://www.manhuadb.com/search?q={}'.format(keyword)).text
    html = BeautifulSoup(r)
    html.select('div.comic-main-section > div.alert')