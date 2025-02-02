# -*- coding: utf-8 -*-
import sys
import os
import pprint as pp
from bs4 import BeautifulSoup


if __name__ == '__main__':
    with open('初期天皇系譜.svg') as f:
        data = f.read()
    soup = BeautifulSoup(data, 'lxml-xml')
    print(soup.prettify())



