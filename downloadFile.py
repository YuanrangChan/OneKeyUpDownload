#!/usr/bin/env/ python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import time
import re

from hostConfig import HostConfigParser
from scp import SCP
from otherTools import OtherTools

class DownloadFile:
    def __init__(self):
        self.other_tools = OtherTools()
        encoding = self.other_tools.get_file_encoding('./conf/download.conf')
        with open('./conf/download.conf', 'r', encoding=encoding) as file:
            is_dirpath_for_storage_exists = False # 用于判断是否设置了存储路径
            is_dirpath_for_storage_bak_exists =  False
            target_begin = False

            self.targets_for_download = []
            line = file.readline()
            while line:
                line = line.rstrip('\n')
                line = line.rstrip('\t')
                line = line.strip()

                if line.startswith('#'): # 注释,跳过
                    line = file.readline()
                    continue
                elif line.startswith('dirpath_for_storage') and line.find('dirpath_for_storage_bak') == -1:
                   self.dirpath_for_storage = line.split('=')[1].strip(' ').strip('\t')
                   is_dirpath_for_storage_exists = True
                   if not self.dirpath_for_storage:
                       print('下载文件存储路径不能为空')
                       is_dirpath_for_storage_exists = False
                       exit()
                elif line.startswith('dirpath_for_storage_bak'):
                   self.dirpath_for_storage_bak = line.split('=')[1].strip(' ').strip('\t')
                   is_dirpath_for_storage_bak_exists = True
                   if not self.dirpath_for_storage_bak:
                       print('下载文件存储备份路径不能为空')
                       is_dirpath_for_storage_bak_exists = False
                       exit()
                elif line.find('[TARGET]') != -1:
                    target_begin = True
                elif target_begin and line:
                    self.targets_for_download.append(line)
                else:
                    line = file.readline()
                    continue
                line = file.readline()
            if not is_dirpath_for_storage_exists:
                print('未设置存储路径，退出程序')
                exit()
            elif not is_dirpath_for_storage_bak_exists:
                print('未设置存储备份路径，退出程序')
                exit()
            elif not self.targets_for_download:
                print('未设置待下载文件，退出程序')
                exit()
        print('要下载|已下载的目标文件：%s' % self.targets_for_download)


    def get_dirpath_for_storage(self):
        return self.dirpath_for_storage

    def get_dirpath_for_storage_bak(self):
        return self.get_dirpath_for_storage_bak

    def get_targets_for_download(self):
        return self.targets_for_download

    def download_file(self):
        self.other_tools.mkdirs_once_many(self.dirpath_for_storage)
        self.other_tools.mkdirs_once_many(self.dirpath_for_storage_bak)
        print('下载文件的目标存储路径为：%s' % self.dirpath_for_storage)
        print('已下载文件的备份存储路径为：%s' % self.dirpath_for_storage_bak)

        print('清空备份目录下，上次下载的文件')
        if not self.other_tools.delete_file(self.dirpath_for_storage_bak)[0]:
            print('清空备份目录下的文件失败')
            exit()

        print('正在备份上次下载的文件')
        if not self.other_tools.copy_dir_or_file(self.dirpath_for_storage, self.dirpath_for_storage_bak)[0]:
            print('备份上次下载文件操作失败')
            exit()

        print('清空目标存储路径下，上次下载的文件')
        if not self.other_tools.delete_file(self.dirpath_for_storage)[0]:
            print('清空目标存储路径下，上次下载的文件')
            exit()
        try:
            hostConfig = HostConfigParser().get_host_config() # 获取主机配置信息
        except Exception as e:
            print('获取主机配置信息失败:%s,提前结束运行\n，烦检查配置文件host_cofig.conf是否配置正确\n' % e)
            exit()
        host_list = hostConfig.sections() # 获取配置信息中，主机节点列表

        file_for_download_success = open('./result/result_for_success.txt', 'w', encoding='utf-8') # 用于记录下载成功的文件
        file_for_download_failure = open('./result/result_for_failure.txt', 'w', encoding='utf-8') # 用于记录下载失败的文件

        download_tool = SCP() # 构造下载工具

        print('正在读取file_for_download.txt配置信息')
        encoding = self.other_tools.get_file_encoding('./conf/file_for_download.txt')
        with open('./conf/file_for_download.txt', 'r', encoding=encoding) as file:
            host, port, username, password= '', '', '', ''
            remark = '' # 记录配置存在的问题
            remark_for_host = '主机配置信息不存在' # 记录主机配置存在的问题
            is_hostconfig_exists = False # 用于判断主机信息是否存在

            line = file.readline()
            while line:
                line = line.rstrip('\n')
                line = line.rstrip('\t')
                line = line.strip()

                if line.startswith('#'): # 注释,跳过
                    line = file.readline()
                    continue
                elif re.findall('[[\d]+\.[\d]+\.[\d]+\.[^\D]+]$', line): # 说明是主机ip,形如 [192.168.1.21]
                    host = line.lstrip('[')
                    host = host.rstrip(']')

                    print('当前解析行为主机信息，host：%s，正在获取主机信息：' % host)
                    if host in host_list:
                        port, username, password = hostConfig[host]['port'],hostConfig[host]['username'], hostConfig[host]['password']
                        print('端口：%s' % port)
                        print('username：%s' % username)
                        print('password：%s\n' % password)
                        is_hostconfig_exists = True
                        remark_for_host = ''
                    else:
                        is_hostconfig_exists = False
                        print('主机信息配置不存在\n')
                        remark_for_host = host + '主机信息配置不存在'
                        host, port,username, password= '','', '', ''
                elif line: # 说明是待下载的文件记录
                    remark = remark + remark_for_host
                    target_for_download = line.strip(' ')
                    target_for_download = target_for_download.strip('\t')
                    target_for_download = target_for_download.rstrip('\\')
                    target_for_download = target_for_download.strip('/')
                    target_for_download = '/' + target_for_download
                    target_for_download = target_for_download.replace('\\', '/')

                    line =  target_for_download + '|' + host + '|'+ '|' + username + '|' + password
                    run_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 记录执行时间

                    if is_hostconfig_exists:
                        temp = target_for_download.split('/')
                        temp = temp[len(temp) - 1]
                        if temp in self.targets_for_download:
                            print('正在下载目标文件（%s）到本地目录 %s' % (target_for_download, self.dirpath_for_storage))
                            result = download_tool.download_file(port, password, target_for_download, username, host, self.dirpath_for_storage)
                            if result[0]:
                                print('下载文件成功，正在记录日志到文件\n')
                                file_for_download_success.write('操作类型：下载文件\n')
                                file_for_download_success.write('执行时间：%s\n' % run_time)
                                file_for_download_success.write('执行信息：\n' + line)
                                file_for_download_success.write('\n-----------------------华丽分割线-----------------------\n\n')
                                file_for_download_success.flush()
                            else:
                                print('下载文件失败，正在进行第二次尝试\n')
                                result = download_tool.download_file(port,password, target_for_download, username, host, self.dirpath_for_storage)
                                if result[0]:
                                    print('下载文件成功，正在记录日志到文件\n')
                                    file_for_download_success.write('操作类型：下载文件\n')
                                    file_for_download_success.write('执行时间：%s\n' % run_time)
                                    file_for_download_success.write('执行信息：\n' + line)
                                    file_for_download_success.write('\n-----------------------华丽分割线-----------------------\n\n')
                                    file_for_download_success.flush()
                                else:
                                    print('下载文件失败，正在记录日志到文件\n')
                                    file_for_download_failure.write('操作类型：下载文件\n')
                                    file_for_download_failure.write('执行时间：%s\n' % run_time)
                                    file_for_download_failure.write('执行信息：\n' + line)
                                    file_for_download_failure.write('\n失败原因：' + result[1] + '\n')
                                    file_for_download_failure.write('-----------------------华丽分割线-----------------------\n\n')
                                    file_for_download_failure.flush()

                    else:
                        print('配置信息有误，正在记录日志到文件\n')
                        file_for_download_failure.write('操作类型：下载文件\n')
                        file_for_download_failure.write('执行时间：%s\n' % run_time)
                        file_for_download_failure.write('执行信息：\n' + line)
                        file_for_download_failure.write('\n失败原因：' + remark.lstrip('&') + '\n')
                        file_for_download_failure.write('-----------------------华丽分割线-----------------------\n\n')
                        file_for_download_failure.flush()

                line = file.readline()
                remark = ''

        file_for_download_failure.close()
        file_for_download_success.close()

        print('--------------------------下载完毕--------------------------')