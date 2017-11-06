#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# File: dump-all-html.py
# Author: Eliiik <elikseng@gmail.com>

import os
import argparse

from subprocess import Popen
from wechat.parser import WeChatDBParser

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", help = 'path of db file', default="decrypted.db")
    parser.add_argument('--outputFolder', help='output html file folder', default='./html/')
    args = parser.parse_args()
    return args

def main():
    args = get_args()
    dbfile = args.db
    outputFolder = args.outputFolder
    chatids = getallname(dbfile).items()

    for i in chatids:
        name = i[0]
        chatid = i[1]
        print "Processing: " + name
        line = "python dump-html.py ".encode('utf8') + chatid + " --output " + "html/" + name + ".html"
        Popen(line, shell=True).wait()
    for _,_,files in os.walk(outputFolder):
        for file in files:
            refineNames(outputFolder, file)


def getallname(data):
    chatdict = {}
    db_file = data
    flag = 1
    parser = WeChatDBParser(db_file)
    chats = parser.msgs_by_chat.keys()
    for k in chats:
        name = parser.contacts[k]
        if name:
            chatdict[name] = k
        else:
            chatdict["chatID_"+str(flag)] = k
            flag+=1

    return chatdict

def refineNames(output, file):
    if file.split(".")[-1] != "html":
        rename = file.split(".")
        rename[-1],rename[-2] = rename[-2],rename[-1]
        print "Rename " + str(file) + " to " + str('.'.join(rename))
        os.rename(os.path.join(output, file), os.path.join(output, '.'.join(rename)))


if __name__ == "__main__":
    main()