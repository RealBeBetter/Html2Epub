from typing import List

from curl_cffi import requests
from bs4 import BeautifulSoup


class Chapter:
    def __init__(self, url, text):
        self.url = url
        self.text = text


def crawl_page(url: str):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/126.0.0.0 Safari/537.36',
        }

        response = requests.get(url=url, timeout=30, headers=headers, impersonate="chrome101")
        content = response.content.decode('utf-8')
    except Exception as e:
        raise ValueError(e)

    return content


def get_pure_page(link: str):
    page = crawl_page(link)

    soup = BeautifulSoup(page, 'html.parser')
    for label in soup.find_all('header', class_='label'):
        label.extract()

    for label in soup.find_all('aside'):
        label.extract()

    return str(soup)


class Crawler:
    def __init__(self, homepage_url):
        self.__title = ""
        self.__homepage_url = homepage_url
        self.__chapters: List[Chapter] = []

    def get_title(self) -> str:
        return self.__title

    def fetch_chapter_urls(self):
        content = crawl_page(self.__homepage_url)

        soup = BeautifulSoup(content, 'html.parser')
        self.__title = soup.title.get_text()

        sidebar_links = soup.find_all('ul', class_='summary')
        if not sidebar_links:
            raise ValueError('No chapters found')

        for chapter_link in sidebar_links:
            sub_chapter_links = chapter_link.find_all('a')
            if not sub_chapter_links:
                continue

            for sub_chapter_link in sub_chapter_links:
                cur_href = sub_chapter_link.get('href')
                if not cur_href:
                    continue
                cur_href = cur_href.strip()
                if cur_href.startswith('./'):
                    cur_href = self.__homepage_url
                elif not cur_href.startswith('http') and not cur_href.startswith('https'):
                    cur_href = self.__homepage_url + cur_href

                if cur_href == 'https://www.gitbook.com' or cur_href == 'http://studygolang.com':
                    continue

                text = sub_chapter_link.get_text().strip()
                chapter = Chapter(cur_href, text)
                self.__chapters.append(chapter)

        return self.__chapters
