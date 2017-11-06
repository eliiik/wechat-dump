#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# File: processHTMLtoPrint.py
# Author: Eliiik <elikseng@gmail.com>
import os
import codecs
import string
import argparse
from bs4 import BeautifulSoup

# htmlBeforeDir = "/mnt/hgfs/UbuntuIIFiles/wechat-dump/html"
# htmlAfterDir = "/mnt/hgfs/UbuntuIIFiles/wechat-dump/htmlConverted"

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--originHTML", help = "the original html file folder", default = "./html/")
    parser.add_argument("--convertedHTML", help = "the path of converted html folder for print", default = "./htmlConverted/")
    args = parser.parse_args()
    return args

def main():
    args = get_args()
    htmlBeforeDir = args.originHTML
    htmlAfterDir = args.convertedHTML
    for _,_,d in os.walk(htmlBeforeDir):
        for htmlFile in d:
            htmlAfter = processHTML(os.path.join(htmlBeforeDir, htmlFile))
            with codecs.open(os.path.join(htmlAfterDir, htmlFile),"w", encoding='utf8') as f:
                f.write(htmlAfter)

def processHTML(htmlFile):
    with codecs.open(htmlFile, "r", encoding='utf8') as f:
        soup = BeautifulSoup(f, "lxml")
        # clear style and script
        soup.style.clear()
        soup.style.find_next().find_next().find_next().clear()
        soup.script.clear()
        soup.script.find_next().clear()
        soup.script.find_next().find_next().clear()

        # clear id and class
        chatclass = soup.select("#chat")[0]
        chatclass["id"] = ""
        chatclass["class"].pop()
        chatclass["class"].pop()

        # mordify background
        cssst = str(soup.style.find_next())[24:-8]
        cssst = string.replace(cssst, "background:#4e5359", "background:#ffffff", 1)
        soup.style.find_next().clear
        soup.style.find_next().append(cssst)
        
        # add the <h1> tag so that it will be more convinient for generate TOC
        timediv = soup.find_all("div", class_="time")
        for i in timediv:
            if len(str(i).split("\n")[2].strip()) > 8:
                chatdate = str(i).split("\n")[2].strip()[:-9]
                #tag = soup.new_tag("h1", style="visibility: hidden;")
                tag = soup.new_tag("h1")
                tag.string = chatdate
                i.insert_before(tag)

        return soup.prettify()

if __name__ == "__main__":
    main()