#!/usr/bin/env python3
# -*- coding: utf-8
import re
import requests
from urlparse import urljoin
from bs4 import BeautifulSoup


class Book():
    def __init__(self, meta):
        self.meta = meta
        self.init()


    def init(self):
        for k, v in self.meta.items():
            setattr(self, k, v)

class ManhuaDB():

    def __init__(self, home):
        self.home = home

    def search(self, name, exact=False):
        r = requests.get('https://www.manhuadb.com/search?q={}'.format(name)).text
        html = BeautifulSoup(r)
        search_result_block = html.select_one('div.comic-main-section')
        result_title = search_result_block.find('div', class_='text-muted').text
        book_count = self.extract_count_from_text(result_title)

        if book_count == 0:
            return None

        results = search_result_block.select('div.row > div')
        books = []
        for r in results:
            a = r.h2.a
            r_name = a.text
            r_url = urljoin(self.home, a['href'])

            if exact:
                if r_name != name:
                    continue
            book = parse_book(r_url)
            books.append(book)

        return books

    def search_one(self, name):
        return self.search(name, exact=True)

    def parse_book(self, url):
        r = requests.get(url).text

    @staticmethod
    def extract_count_from_text(text):
        m = re.search(r'\d+', text)
        return int(m.group())


