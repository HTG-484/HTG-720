#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import sys

def all_file_path(dirname):
    '''
    获取路径下的所有文件路径信息
    :param dirname: 项目路径
    :return: 返回项目路径下面的所有文件路径
    '''
    result = []
    dir_file = []
    for maindir, subdir, file_name_list in os.walk(dirname):
        dir_file.append(subdir)
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            result.append(apath)
    return result,dir_file

def get_ma_mb_file(path):
    '''
    获取i文件后缀名
    :param path: 传入的是文件路径列表(剔除最后文件不是ma,mb文件的文件夹)
    :return: fileType
    '''
    truepath = []
    for i in path:
        if os.path.splitext(i)[1] == '.ma' and '.mb':
            '''其他文件格式将会舍去'''
            truepath.append(i)
        '''此处原本是用正则获取文件后缀'''
        # result = re.findall(r'[^\\/:*?"<>|\r\n]+$', i)
        # if result[0].split('.')[1] == 'mb':
        #     truepath.append(i)
    return truepath

def get_version_file_info(truepath):
    '''
    匹配格式为一个字母三个数字的路径
    :param string: 传入的是路径列表（返回如果不为空说明有版本存在返回出去再做判断）
    :return: match_list
    '''
    #string = ['nihao','123','a2c','1b3','v001','V002','v003']
    match_list = []
    element = []
    for i in truepath:
        lis = i.split('\\')
        for j in lis:
            #word = re.match(r'\w\d{3}', j)
            p = re.compile(r'(v\d{3})')
            a = []
            if p.findall(j) == []:
                pass

            elif p.findall(i)[0] not in lis:
                pass
            elif p.findall(i)[0] in lis:
                element.append(p.findall(i))

            # for h in range(len(element)):
            #     if element[h][0] not in j:
            #         element.remove(element[h])
        if len(element) >0:
            match_list.append(i)
            # if re.match(r'\w\d{3}', j) != None:
            #     match_list.append(i)
        element = []    #初始化
    return match_list

'''得到文件夹下面的子文件夹名称'''
def get_dirs(path):
    dir_name = []
    for i in os.listdir(path):
        dir_name.append(i)
    return dir_name
a = get_dirs('G:/projects/TST/assets/Charater/cube/lookdev/publish/base')
b = []
for i in range(len(a)):
    b.append(int(a[i].split('v')[1]))
print b
# all_path = all_file_path('K:/projects/TST/assets/Charater/cube/lookdev/publish/base')
# mb_file_path = get_ma_mb_file(all_path)
# have_v001_file_path = get_version_file_info(mb_file_path)

# print u'项目文件夹内的所有文件:',all_path,len(all_path)
# print u'排除ma和mb之外的文件:',mb_file_path,len(mb_file_path)
# print u'符合要求的文件路径:',have_v001_file_path,len(have_v001_file_path)
