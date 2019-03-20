#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import sys

def all_path(dirname):
    '''
    获取路径下的所有文件路径信息
    :param dirname: 项目路径
    :return: 返回项目路径下面的所有文件路径
    '''
    result = []
    for maindir, subdir, file_name_list in os.walk(dirname):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            result.append(apath)
    return result

def get_True_file_path(path):
    '''
    获取i文件后缀名
    :param path: 传入的是文件路径是一个列表(剔除最后文件不是mb文件的文件夹)
    :return: fileType
    '''
    truepath = []
    for i in path:
        if os.path.splitext(i)[1] == '.ma' and '.mb':
            truepath.append(i)
        '''此处原本是用正则获取文件后缀'''
        # result = re.findall(r'[^\\/:*?"<>|\r\n]+$', i)
        # if result[0].split('.')[1] == 'mb':
        #     truepath.append(i)
    return truepath

def match(truepath):
    '''
    匹配格式为一个字母三个数字的路径
    :param string: 传入的是路径切开的列表（返回如果不为空说明有版本存在返回出去再做判断）
    :return: match_list
    '''
    #string = ['nihao','123','a2c','1b3','v001','V002','v003']
    match_list = []
    for i in truepath:
        for j in i.split('\\'):
            if re.match(r'\w\d{3}', j) != None:
                match_list.append(i)
    return match_list



all_path = all_path('K:\GODTV\Shot')
mb_file_path = get_True_file_path(all_path)
have_v001_file_path = match(mb_file_path)

print all_path,len(all_path)
print mb_file_path,len(mb_file_path)
print have_v001_file_path,len(have_v001_file_path)