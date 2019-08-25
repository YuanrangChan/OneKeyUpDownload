#!/usr/bin/env/ python
# -*- coding:utf-8 -*-

__author__ = 'laiyu'

import configparser
import os
import time

class FileTraversal:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./conf/rootpath_for_doc.conf', encoding='utf-8')
        self.rootpath_for_doc = config['DOCROOTPATH']['rootpath_for_doc']
        if not os.path.exists(self.rootpath_for_doc):
            print('待上传文件所在根路径：%s不存在，停止运行程序' % self.rootpath_for_doc)
            exit()
        elif not os.path.isdir(self.rootpath_for_doc):
            print('待上传文件所在根路径：%s非目录，停止运行程序' % self.rootpath_for_doc)
            exit()

        self.rootpath_for_doc =  self.rootpath_for_doc.rstrip('\\')
        self.rootpath_for_doc =  self.rootpath_for_doc.rstrip('/')
        self.rootpath_for_doc = self.rootpath_for_doc + '\\'

        self.fileinfo_set_for_old = set() # 存放开启新一轮脚本执行前已上传过的文件记录(|最近修改时间)
        self.fileinfo_set_for_new = set() # 存放获取到的最新（有更新待上传）文件记录(文件路径|最近修改时间)
        self.filepath_set = set()         # 存放目录及其子目录下的文件名(文件路径)

        # if not os.path.exists('./uploadresult/file_for_old.txt'): # 如果文件不存在，则创建文件，用于存放上传过的文件记录
        #     self.file_for_old = open('./uploadresult/file_for_old.txt', 'w', encoding='utf-8')
        if not os.path.exists('./uresult/file_for_old.txt'): # 如果文件不存在，则创建文件，用于存放上传过的文件记录
            self.file_for_old = open('./result/file_for_old.txt', 'w', encoding='utf-8')
            self.__create_fileupload_history_record(self.rootpath_for_doc)
            self.__close_file()
        else:
            print('正在获取已上文件历史记录信息')
            with open('./uploadresult/file_for_old.txt', 'r', encoding='utf-8') as file_for_old:
                line = file_for_old.readline()
                while line:
                    line = line.rstrip('\n')
                    self.fileinfo_set_for_old.add(line)
                    line = file_for_old.readline()

        print('历史记录信息：')
        print(self.fileinfo_set_for_old)
        print('')

    # 创建基线---首次运行，目录下已有的文件视为未更新，不上传
    def __create_fileupload_history_record(self, dir_path):
        if not os.path.exists(dir_path):
            print('路径：%s 不存在，退出程序' % dir_path)
            exit()
        for name in os.listdir(dir_path):
            full_path = os.path.join(dir_path, name)
            modify_time = time.ctime(os.path.getmtime(full_path))

            if os.path.isdir(full_path):
                self.__create_fileupload_history_record(full_path)
            else:
                self.file_for_old.write(full_path + '|' + modify_time  + '\n')
                self.file_for_old.flush()
                self.fileinfo_set_for_old.add(full_path + '|' + modify_time)

    def __close_file(self):
        self.file_for_old.close()

    # def get_rootpath_for_doc(self):
    #     return self.rootpath_for_doc
    def get_rootpath_for_upload(self):
        return self.get_rootpath_for_upload

    def get_fileinfo_set_for_old(self):
        return self.fileinfo_set_for_old

    def get_fileinfo_set_for_new(self):
        return self.fileinfo_set_for_new

    def get_filepath_set(self):
        return self.filepath_set

    def set_filepath_set(self, filepath_set):
        self.filepath_set = filepath_set

    # 获取目录下的所有文件信息
    def collect_fileinfo_for_newest(self, dir_path):
        if not os.path.exists(dir_path):
            print('路径：%s 不存在，退出程序' % dir_path)
            exit()
        for name in os.listdir(dir_path):
            full_path = os.path.join(dir_path, name)
            modify_time = time.ctime(os.path.getmtime(full_path))

            if os.path.isdir(full_path):
                self.collect_fileinfo_for_newest(full_path)
            else:
                self.fileinfo_set_for_new.add(full_path + '|' + modify_time)

    # 获取某个目录下的文件路径
    def collect_filepath_for_dir(self, dirpath):
        if os.path.exists(dirpath):
            for name in os.listdir(dirpath):
                full_path = os.path.join(dirpath, name)
                if os.path.isdir(full_path):
                    self.collect_filepath_for_dir(full_path)
                else:
                    self.filepath_set.add(full_path)
        else:
            print('warnging:路径[%s]不存在' % dirpath)
            self.filepath_set = set()

    # 获取目录下，有更新的文件信息
    def get_filename_set_for_updated(self):
        self.fileinfo_set_for_new = self.fileinfo_set_for_new - self.fileinfo_set_for_old
        filename_set_for_updated = set()
        for item in self.fileinfo_set_for_new:
            filename_set_for_updated.add(item.split('|')[0])
        return filename_set_for_updated


