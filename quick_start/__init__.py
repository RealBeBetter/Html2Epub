#!usr/bin/python3
# -*- coding: utf-8 -*-

if __name__ == '__main__':
    import html2epub

    epub = html2epub.Epub('My First Epub')
    chapter = html2epub.create_chapter_from_url("https://jingyecn.top:18080/architecture/architect-history/primitive-distribution.html")
    epub.add_chapter(chapter)
    epub.create_epub('OUTPUT_DIRECTORY')
