#!/usr/bin/env/ python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import sys
from uploadFile import UploadFile
from downloadFile import DownloadFile
from mysshclient import MySSHClient


if __name__ == '__main__':
    print('--------------------------开始运行--------------------------')
    if sys.argv[1] == '1':
        DownloadFile().download_file()
    elif sys.argv[1] == '2':
        upload_file_tool = UploadFile()
        upload_file_tool.upload_file()
        upload_file_tool.exec_linux_command() #需要在file_for_linux_operation.txt配置执行的linux命令
        # #连接服务器进行远程部署
        # ssh_client = MySSHClient()
        # ssh_client.connect(hostname='150.109.5.241',port=2202,username='appdeploy',password='Sf@deploy!@#')
        # command = '/home/appdeploy/saas-dds/tcs/expect_scp.sh'
        # ssh_client.exec_command(command)
        # ssh_client.close()
    else:
        print('启动参数错误，结束运行')


#这样执行是成功的
# if __name__ == '__main__':
#     print('--------------------------开始运行--------------------------')
#     runmode = 1
#     ssh_client = MySSHClient()
#     # ssh_client.connect(hostname='150.109.5.241',port=2202,username='appdeploy',password='Sf@deploy!@#')
#     ssh_client.connect(hostname='192.168.187.129',port=22,username='root',password='123456')
#     # if sys.argv[1] == '1':
#     if runmode == 1:
#         ssh_client.download_file('/app/PyOneKeyUpDownloadTest/eladmin-system-2.0.jar', 'F:/27Download/eladmin-system-2.0.jar')
#     # elif sys.argv[1] == '2':
#     elif runmode == 2:
#         ssh_client.upload_file('F:/27Download/HelloJava.java', '/app/test6.txt')
#         command = 'ls -al'
#         ssh_client.exec_command(command) #需要在file_for_linux_operation.txt配置执行的linux命令
#         # #连接服务器进行远程部署
#         # ssh_client = MySSHClient()
#         # ssh_client.connect(hostname='150.109.5.241',port=2202,username='appdeploy',password='Sf@deploy!@#')
#         # command = '/home/appdeploy/saas-dds/tcs/expect_scp.sh'
#         # ssh_client.exec_command(command)
#         # ssh_client.close()
#     else:
#         print('启动参数错误，结束运行')



# #!/usr/bin/env/ python
# # -*- coding:utf-8 -*-

# __author__ = 'laifuyu'

# from downloadFile import DownloadFile

# if __name__ == '__main__':
    # print('--------------------------开始运行--------------------------')
    # DownloadFile().download_file()
