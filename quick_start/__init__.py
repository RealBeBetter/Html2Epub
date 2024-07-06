#!usr/bin/python3
# -*- coding: utf-8 -*-
import time

from quick_start.create_chapters import Crawler, get_pure_page

if __name__ == '__main__':
    import html2epub

    crawler = Crawler(homepage_url="https://books.studygolang.com/go-internals/")
    chapter_urls = crawler.fetch_chapter_urls()

    title = crawler.get_title()
    epub = html2epub.Epub(title)

    index = 0
    for chapter_url in chapter_urls:
        page_content = get_pure_page(chapter_url.url)

        chapter = html2epub.create_chapter_from_string(page_content, url=chapter_url.url, title=chapter_url.text)
        epub.add_chapter(chapter)
        index += 1
        print('Chapter %d: %s' % (index, chapter_url.text))

    epub.create_epub('OUTPUT_DIRECTORY')
