# coding: utf-8

import os
import json
import requests
from bs4 import BeautifulSoup


SAVE_PATH = '/Users/jiqinqiang/Desktop/每日小记/blog/Alamofire Tutorial/'


class Photo:

    def __init__(self, url, width=100, height=100):
        self.url = url
        self.width = width
        self.height = height


class ImageCrawler:

    def __init__(self, url):
        self._url = url

    def fetchPhotos(self):
        html = self.fetchHtml()
        photos = self.parseHtml(html)
        self.save(photos)

    def fetchHtml(self):
        r = requests.get(self._url)
        return r.text.encode('utf-8')

    def parseHtml(self, html):
        photos = []

        soup = BeautifulSoup(html, "html.parser")
        for img in soup.body.find_all('img'):
            src = img['src']
            if src.endswith('.svg') or 'avatar' in src:
                continue

            if img.has_attr('width') and img.has_attr('height'):
                photo = Photo(src, img['width'], img['height'])
            else:
                photo = Photo(src)
            photos.append(photo)

        return photos

    def save(self, photos):
        with open(SAVE_PATH + 'Alamofire.txt', 'w') as f:
            for photo in photos:
                f.write(json.dumps(photo.__dict__) + '\n')


crawler = ImageCrawler('https://www.raywenderlich.com/147086/alamofire-tutorial-getting-started-2')
crawler.fetchPhotos()
