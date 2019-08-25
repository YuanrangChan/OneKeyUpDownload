#!/usr/bin/env/ python
# -*- coding:utf-8 -*-

__author__ = 'laifuyu'

import os
import  chardet
import subprocess

class OtherTools:
    def __init__(self):
        self.filepath_list = []

    # 获取文件编码
    def get_file_encoding(self, filepath):
        filehandler = open(filepath, 'rb')
        encoding = chardet.detect(filehandler.read())['encoding']
        if encoding == 'GB2312':
            encoding = 'gbk'
        elif encoding == 'utf-8':
            pass
        elif encoding == 'ascii':
            encoding = 'unicode_escape'
        else:
            encoding = 'utf-8-sig'
        filehandler.close()
        return encoding

  # 批量创建目录
    def mkdirs_once_many(self, path):
        path = os.path.normpath(path)  # 去掉路径最右侧的 \\ 、/
        path = path.replace('\\', '/') # 将所有的\\转为/，避免出现转义字符串

        head, tail = os.path.split(path)
        new_dir_path = ''  # 反转后的目录路径
        root = ''  #根目录

        if not os.path.isdir(path) and os.path.isfile(path):  # 如果path指向的是文件，则继续分解文件所在目录
            head, tail = os.path.split(head)

        if tail == '':
            return

        while tail:
            new_dir_path = new_dir_path + tail + '/'
            head, tail = os.path.split(head)
            root = head
        else:
            new_dir_path = root + new_dir_path

            # 批量创建目录
            new_dir_path = os.path.normpath(new_dir_path)
            head, tail = os.path.split(new_dir_path)
            temp = ''
            while tail:
                temp = temp + '/' + tail
                dir_path = root + temp
                if not os.path.isdir(dir_path):
                    os.mkdir(dir_path)
                head, tail = os.path.split(head)


    # 复制文件或目录到指定目录(非自身目录)
    def copy_dir_or_file(self, src, dest):
        if not os.path.exists(dest):
            print('目标路径：%s 不存在' % dest)
            return  [False, '目标路径：%s 不存在' % dest]
        elif not os.path.isdir(dest):
            print('目标路径：%s 不为目录' % dest)
            return   [False, '目标路径：%s 不为目录' % dest]
        elif src.replace('/', '\\').rstrip('\\') == dest.replace('/', '\\').rstrip('\\'):
            print('源路径和目标路径相同，无需复制')
            return [True,'源路径和目标路径相同，不需要复制']

        if not os.path.exists(src):
            print('源路径：%s 不存在' % src)
            return  [False, '源路径：%s 不存在' % src]

        # /E 复制目录和子目录，包括空的 /Y 无需确认，自动覆盖已有文件
        args = 'xcopy /YE ' + os.path.normpath(src) + ' ' + os.path.normpath(dest) # 注意：xcopy不支持 d:/xxx,只支持 d:\xxxx,所以要转换
        try:
            with subprocess.Popen(args, shell=True, universal_newlines = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
                output = proc.communicate()
                print('复制文件操作输出：%s' % str(output))
                if not output[1]:
                    print('复制目标文件|目录(%s) 到目标目录(%s)成功' % (src, dest))
                    return [True,'复制成功']
                else:
                    print('复制目标文件|目录(%s) 到目标目录(%s)失败:%s' % (src, dest, output[1]))
                    return  [False,'复制目标文件|目录(%s) 到目标目录(%s)失败:%s' % (src, dest, output[1])]
        except Exception as e:
            print('复制目标文件|目录(%s) 到目标目录(%s)失败 %s' % (src, dest, e))
            return  [False, '复制目标文件|目录(%s) 到目标目录(%s)失败 %s' % (src, dest, e)]

    # 删除指定目录及其子目录下的所有子文件,不删除目录
    def delete_file(self, dirpath):
        if not os.path.exists(dirpath):
            print('要删除的目标路径：%s 不存在' % dirpath)
            return  [False, '要删除的目标路径：%s 不存在' % dirpath]
        elif not os.path.isdir(dirpath):
            print('要删除的目标路径：%s 不为目录' % dirpath)
            return   [False, '要删除的目标路径：%s 不为目录' % dirpath]

        # 注意：同xcopy命令，del也不支持 d:/xxxx,Linux/Unix路径的写法，只支持d:\xxx windows路径的写法
        args = 'del /F/S/Q ' + os.path.normpath(dirpath)  # /F 强制删除只读文件。 /S 删除所有子目录中的指定的文件。 /Q 安静模式。删除前，不要求确认
        try:
            with subprocess.Popen(args, shell=True, universal_newlines = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
                output = proc.communicate()
                print('删除目标目录下的文件，操作输出：%s' % str(output))
                if not output[1]:
                    print('删除目标目录(%s)下的文件成功' % dirpath)
                    return [True,'删除成功']
                else:
                    print('删除目标目录(%s)下的文件失败：%s' % (dirpath, output[1]))
                    return [True,'删除目标目录(%s)下的文件失败：%s' % (dirpath, output[1])]
        except Exception as e:
            print('删除目标目录(%s)下的文失败:%s' % (dirpath,e))
            return  [False, '删除目标目录(%s)下的文失败:%s' % (dirpath,e)]

if __name__ == '__main__':
    # 测试
    from mysshclient import MySSHClient
    ssh_client = MySSHClient()
    ssh_client.connect(hostname='192.168.187.129', port=22, username='root', password='123456')
    ssh_client.exec_command('ls -l')

    # ssh_client.download_file('/root/dirForDownload/file', './test1.txt')
    # ssh_client.download_file('/root/dirForDownload/file', '.\test2.txt')
    # ssh_client.download_file('/root/dirForDownload/file', 'd:\\test3.txt')
    # ssh_client.download_file('/root/dirForDownload/file', 'd:\test4.txt')
    # ssh_client.download_file('/root/dirForDownload/file', 'd:\mytest4.txt')
    # ssh_client.download_file('/root/dirForDownload/file', 'd:/test5.txt')
    # ssh_client.download_file('/root/dirForDownload/file', 'd:\dir1\dir2\test6.txt')
    ssh_client.download_file('/app/PyOneKeyUpDownloadTest/eladmin-system-2.0.jar', 'F:/27Download/eladmin-system-2.0.jar')

    # ssh_client.upload_file('./test1.txt', '/root/test1.txt')
    # ssh_client.upload_file('d:\mytest4.txt', '/root/mytestfile.txt')
    # ssh_client.upload_file('d:\dir1\dir2\test6.txt', './test6.txt')
    ssh_client.upload_file('F:/27Download/HelloJava.java', '/app/test6.txt')
    ssh_client.close()