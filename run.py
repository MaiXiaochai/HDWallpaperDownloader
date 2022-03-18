# coding: utf8
"""
------------------------------------------
@File       : run.py
@CreatedOn  : 2022/3/18 22:17
------------------------------------------
"""
from os import makedirs
from os.path import exists, join as path_join, dirname

import requests
import urllib3

from lxml import etree
from fake_headers import Headers

urllib3.disable_warnings()


class HDWallpaperDownloader:
    def __init__(self, save_dir_name):
        self.__save_dir = self.__full_save_dir(save_dir_name)
        self.header = Headers(
            browser="chrome",  # Generate only Chrome UA
            os="win",  # Generate ony Windows platform
            headers=True  # generate misc headers
        )
        self.__other_info = {
            ":authority": "w.wallhaven.cc",
            ":scheme": "https",
            "accept-encoding": "gzip, deflate, br"
        }

    @property
    def __random_header(self):
        headers = self.header.generate()
        # headers.update(self.__other_info)
        return headers

    def get_pic_urls(self, url):
        content = requests.get(url, headers=self.__random_header, verify=False).text
        content = etree.HTML(content)

        data = content.xpath('//a[@class="preview"]/@href')
        return data

    def get_hd_pic_url(self, url):
        content = requests.get(url, headers=self.__random_header, verify=False).text
        content = etree.HTML(content)

        data = content.xpath('//img[@id="wallpaper"]/@src')
        return data

    def get_pic_data(self, url):
        content = requests.get(url, headers=self.__random_header, verify=False).content
        print(f"content: {content}")
        return content

    @staticmethod
    def __full_save_dir(dir_name):
        base_dir = dirname(__file__)
        full_path = path_join(base_dir, dir_name)
        return full_path

    @staticmethod
    def check_dir(full_path):
        if not exists(full_path):
            makedirs(full_path)

        return full_path

    @staticmethod
    def get_short_name(url):
        return url.split('/')[-1]

    def save_pic(self, name, content):
        """
            保存二进制图片
        """
        full_path = path_join(self.__save_dir, name)
        with open(full_path, 'wb') as f:
            f.write(content)


def main():
    save_dir_name = "pics"
    base_url = "https://wallhaven.cc/search?q=id%3A65348&categories=110&purity=100&atleast=2560x1440&sorting=view&order=desc&seed=PNRzaT&page=1"

    spider = HDWallpaperDownloader(save_dir_name)
    urls = spider.get_pic_urls(base_url)
    print(urls)

    for i in urls:
        print(f"i: {i}")
        pic_url = spider.get_hd_pic_url(i)
        if not pic_url:
            continue

        pic_url = str(pic_url[0])

        short_name = spider.get_short_name(pic_url)
        print(f"short_name: {short_name}")
        data = spider.get_pic_data(pic_url)

        print(f"short_name: {short_name}")
        spider.save_pic(short_name, data)


if __name__ == '__main__':
    main()
