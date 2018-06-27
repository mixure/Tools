#! /usr/bin/env python3
# coding=utf-8

import time
from urllib.parse import urljoin
from selenium import webdriver
from bs4 import BeautifulSoup
from logzero import logger

domain="https://www.yirendai.com/abc"
title404="很抱歉，您访问的页面不存在"
page_size404=1308
dr=webdriver.Firefox()

def scrap_url(url,orginal_url):
    status_code=200
    try:
        now=time.time()
        dr.get(url)

        #根据title判断/或者404页面文件都比较小
        if title404 in dr.title: status_code=404
        # if len(dr.page_source)<=page_size404: status_code=404
        t='%.2f' %(time.time()-now)
        html=dr.page_source
        soup=BeautifulSoup(html,'html.parser')
    except Exception as e:
        dr.get_screenshot_as_base64('f{orginal_url}_to_{url}')
    finally:
        if status_code==200:
            mod="32m"
        elif status_code==404:
            mod="31m"
        logger.debug(f'\033[1;33;37m{url}, 从{orginal_url}获取该链接\033[0m  \033[0;34m {t}s \033[0m '
            f'\033[0;{mod}{status_code}\033[0m')

    more_seeds=[]
    #有些网站的站内的超链接不是href参数提供的,需要继续在if修改
    # 有些还有外链，都是在这处理....
    if status_code==200:  # 有些网站404页面有本站超链接
        for a in soup.find_all(href=True):
            if a['href'].startswith('/'):
                more_seeds.append((urljoin(domain,a['href']),url))
    return more_seeds

def main(domain):
    seeds=[(domain,"用户输入")]
    old_urls=[]
    while seeds:
        seed,*seeds=seeds
        url,orginal_url=seed

        if url in old_urls:
            logger.debug(f'{url}, 从{orginal_url}获取该链接,不进行重复访问 ')
        else:
            old_urls.append(url)
            seeds.extend(scrap_url(*seed))

main(domain)
dr.quit()
