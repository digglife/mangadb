#!/usr/bin/env python3

import sys
import requests
from bs4 import BeautifulSoup

URL_HOME = 'https://www.ebookjapan.jp'


def search(keyword):
    r = requests.get(URL_HOME + '/ebj/search_book/', params={'q': keyword})
    bs = BeautifulSoup(r.text, 'lxml')
    item = bs.find('div', class_='item')
    if item:
        return URL_HOME + item.a['href']
    return


def download_cover_image(book_url, filename):
    r = requests.get(book_url)
    bs = BeautifulSoup(r.text, 'lxml')
    a = bs.select_one('div > figure > a')
    with open(filename, 'wb') as f:
        f.write(requests.get("https:" + a['href']).content)


def main():
    keyword = sys.argv[1]
    book = search(keyword)
    if not book:
        print("没有找到和{}相关的书籍".format(book))
        sys.exit(1)
    book_name = "{}.jpg".format(keyword)
    download_cover_image(book, book_name)


main()
