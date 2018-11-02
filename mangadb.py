#!/usr/bin/env python3
# -*- coding: utf-8
import re
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


class Book():

    keys = [
        'title',
        'original-title',
        'authors',
        'episodes',
        'status',
        'category',
        'tags',
        'age',
        'description',
    ]

    def __init__(self, meta):
        self.meta = meta
        self.init(meta)

    def init(self, meta):
        for k in self.keys:
            setattr(self, k, meta.get(k, None))

    def __repr__(self):
        return "<Book(title:{})>".format(self.title)

class ManhuaDB():

    def __init__(self):
        self.home = 'https://www.manhuadb.com'
        self.meta_map = {
            '漫画名称': 'title',
            '漫画原名': 'original-title',
            '单行本数': 'episodes',
            '连载状态': 'status',
            '漫画分类': 'category',
            '漫画标签': 'tags',
            '面向读者': 'age'
        }

    def search(self, name, exact=False):
        search_url = urljoin(self.home, 'search?q={}'.format(name))
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
            r_url = urljoin(self.home, a['href'])

            if exact:
                if r_name != name:
                    continue
            book = self.parse_book(r_url)
            books.append(book)

        return books

    def search_one(self, name):
        books = self.search(name, exact=True)
        if books:
            return books[0]
        return None

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
            if key in self.meta_map:
                meta[self.meta_map[key]] = value

        div_detail_content = html.select_one('div.comic_detail_content > div')
        meta['description'] = div_detail_content.decode_contents().strip()

        a_authors = html.select('a.comic-creator')
        authors = [ a.text.strip() for a in a_authors ]
        meta['authors'] = author

        return Book(meta)

    @staticmethod
    def extract_count_from_text(text):
        m = re.search(r'\d+', text)
        return int(m.group())
