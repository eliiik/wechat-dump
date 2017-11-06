#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: utils.py
# Date: Wed Jun 17 23:59:25 2015 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import hashlib
import base64

def ensure_bin_str(s):
    if type(s) == str:
        return s
    if type(s) == unicode:
        return s.encode('utf-8')

def ensure_unicode(s):
    if type(s) == str:
        return s.decode('utf-8')
    if type(s) == unicode:
        return s


def md5(s):
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()

def get_file_b64(fname):
    data = open(fname, 'rb').read()
    return base64.b64encode(data)

def safe_filename(fname):
    filename = ensure_unicode(fname)
    return "".join(
        [c for c in filename if c.isalpha() or c.isdigit() or c==' ']).rstrip()

def is_chinese(uchar):
        """判断一个 unicode 是否是汉字"""
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
                return True
        else:
                return False
 
def is_number(uchar):
        """判断一个 unicode 是否是数字"""
        if uchar >= u'\u0030' and uchar<=u'\u0039':
                return True
        else:
                return False
 
def is_alphabet(uchar):
        """判断一个 unicode 是否是英文字母"""
        if (uchar>= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
                return True
        else:
                return False
 
def is_other(uchar):
        """判断是否非汉字，数字和英文字符"""
        if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
                return True
        else:
                return False
