#!/usr/bin/env python3
# -*- coding: utf-8
import re
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


class Book():
    def __init__(self, meta):
        self.meta = meta
        self.init()


    def init(self):
        for k, v in self.meta.items():
            setattr(self, k, v)

class ManhuaDB():

    HOME = 'https://www.manhuadb.com'

    def search(self, name, exact=False):
        search_url = urljoin(self.HOME, 'search?q={}'.format(name))
        r = requests.get(search_url).text
        html = BeautifulSoup(r, 'lxml')
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
            r_url = urljoin(self.HOME, a['href'])

            if exact:
                if r_name != name:
                    continue
            book = self.parse_book(r_url)
            books.append(book)

        return books

    def search_one(self, name):
        return self.search(name, exact=True)

    def parse_book(self, url):
        r = requests.get(url).text
        html = BeautifulSoup(r, 'lxml')

        meta_table = html.find('table', class_='comic-meta-data-table')
        meta = {}
        for tr in meta_table.find_all('tr'):
            key = tr.find('th').text.strip()
            td = tr.find('td')
            a = td.find_all('a')
            if a:
                values = [i.text.strip() for i in a]
                value = values[0] if len(values) == 1 else values
            else:
                value = td.text.strip()
            meta[key] = value

        return Book(meta)

    @staticmethod
    def extract_count_from_text(text):
        m = re.search(r'\d+', text)
        return int(m.group())


