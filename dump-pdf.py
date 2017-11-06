#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# File: htmltopdf.py
# Author: Eliiik <elikseng@gmail.com>

import codecs
import os
import subprocess
import sys
from datetime import datetime
from bs4 import BeautifulSoup
from common import textutil
import pdfkit
reload(sys)
sys.setdefaultencoding("utf-8")

filepath = "./htmlConverted"
outputpath = "./pdf"
coverpath = "./cover/index.html"
tmppath = "./cover/tmp.html"
server = "http://127.0.0.1:8080/tmp.html"

def main():
    for _,_,files in os.walk(filepath):
        for f in files:
            if str(f)[-4:] == "html":
                wechatname = textutil.ensure_unicode(str(f)[:-5])
                print wechatname
                print len(wechatname)
                mordifyCover(coverpath, wechatname)
                convert(f)

def mordifyCover(coverPath, wechatname):
    with codecs.open(coverPath, encoding="utf8") as f:
        soup = BeautifulSoup(f, "lxml")
        wrap = soup.find("div")
        # Mordify cover
        name = wrap.find("div").findNext()
        name.clear()
        name.append(wechatname)

        # Mordify CSS
        flag = 0
        for i in wechatname:
            if textutil.is_alphabet(i):
                flag += 0.5
            elif textutil.is_chinese(i):
                flag += 1
            elif textutil.is_number(i):
                flag += 0.5
            else:
                flag += 0.4
        if(flag>2):
            name.attrs["style"] = "font-size: {0}px; top: {1}%;".format(330/flag, 20+(flag-3)*0.6)

        currentTime = str(datetime.today().date())
        getHTMLTime = name.findNext().findNext()
        getHTMLTime.clear()
        getHTMLTime.append(u"{0}".format(currentTime))

        tmpPath = coverPath[:-10] + "tmp.html"
        with codecs.open(tmpPath, "w", encoding="utf8") as t:
            t.write(soup.prettify())


def convert(htmlFile):
    fp = os.path.join(filepath,htmlFile)
    op = os.path.join(outputpath, (htmlFile[:-4]+"pdf"))

    command = "wkhtmltopdf --margin-top '0.75in' --margin-bottom '0.75in' --margin-left '1.25in' --margin-right '1.25in' --encoding 'UTF-8' --footer-center '[page]' cover {2} toc {0} {1}".format(fp, op, server)

    subprocess.Popen(command, shell=True).wait()

if __name__ == "__main__":
    main()
