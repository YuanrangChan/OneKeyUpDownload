# coding:utf-8
# @Time    :2019/8/20 23:07
# @Author  :David Chan
# @Mail    :david@chan.com
# @Function:uploadFile

__author__ = 'david'

import os
import time

from hostConfig import HostConfigParser
from fileTraversal import FileTraversal
from mysshclient import MySSHClient
from fileConfigureParser import FileConfigureParser

class UploadFile:
	def __init__(self):
		self.file_traversal = FileTraversal()
		self.host_set_for_upload_success = set() #存放成功上传的主机地址

	def upload_file(self):
		rootpath_for_upload = self.file_traversal.get_rootpath_for_upload() #获取本地待上传文件所在根目录
		print('待上传文件所在根目录为：%s' % rootpath_for_upload)

		file_configure_parser = FileConfigureParser()

		file_for_upload_success = open('./result/result_for_upload_success.txt','w',encoding='utf-8') #用于记录下载成功的文件
		file_for_upload_failure = open('./result/result_for_upload_failure.txt','w',encoding='utf-8') #用于记录下载失败的文件

		print('正在解析/conf/file_for_upload.txt文件')
		file_configure_parser.parser_configure('./conf/file_for_upload.txt')

		host_list_in_order = file_configure_parser.get_host_list_in_order()
		operation_object_dic = file_configure_parser.get_operation_object_dic()

		try:
			hostConfig = HostConfigParser().get_host_config() #获取主机配置信息
		except Exception as e:
			print('获取主机配置信息失败：%s。提取结束运行\n,烦检查配置文件host_config.conf是否配置正确\n' % e)
			exit()
		host_list = hostConfig.sections() #获取配置信息中，主机节点列表

		ssh_client = MySSHClient()
		for host in host_list_in_order:
			if host in host_list:
				print('正在获取主机信息：%s' % host)
				port,username,password = int(hostConfig[host]['port']),hostConfig[host]['username'],hostConfig[host]['password']
				ssh_client.connect(port,username,password)

				for object_info in operation_object_dic[host]:
					run_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()) #记录执行时间
					localpath,remotepath = object_info.split('|')
					localpath  = localpath.strip(' ')
					remotepath = remotepath.strip(' ')

					localpath = rootpath_for_upload + localpath
					print('正在检查待上传文件[%s]是否为目录...' % localpath)
					if os.path.isdir(localpath):
						print('路径%s为目录，不支持' % localpath)
						file_for_upload_failure.write('操作类型：上传文件\n')
						file_for_upload_failure.write('执行时间：%s\n' % run_time)
						file_for_upload_failure.write('上传信息：\n' + host +' ' +remotepath)
						file_for_upload_failure.write('\n失败原因：不支持目录的上传')
						file_for_upload_failure.write('\n--------------------华丽分割线--------------------\n\n')
						file_for_upload_failure.flush()
						continue
					else:
						line = host  + '|' + localpath + '|' + remotepath
						run_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()) #记录执行时间
						result = ssh_client.upload_file(localpath,remotepath)
						if result[0]:
							print('执行成功，正在记录到日志文件')
							file_for_upload_success.write('操作类型：上传文件\n')
							file_for_upload_success.write('执行时间：%s\n' % run_time)
							file_for_upload_success.write('上传信息：\n' + host + ' ' + remotepath)
							file_for_upload_success.write('\n--------------------华丽分割线--------------------\n\n')
							file_for_upload_success.flush()
						else:
							print('执行失败：%s，正在记录到结果文件' % result[1])
							file_for_upload_failure.write('操作类型：上传文件\n')
							file_for_upload_failure.write('执行时间：%s\n' % run_time)
							file_for_upload_failure.write('上传信息：\n' + line)
							file_for_upload_failure.write('\n失败原因：' + result[1])
							file_for_upload_failure.write('\n--------------------华丽分割线--------------------\n\n')
							file_for_upload_failure.flush()
				ssh_client.close()
			else:
				print('主机配置信息不存在')
				file_for_upload_failure.write('操作类型：上传文件\n')
				file_for_upload_failure.write('执行时间：%s\n' % run_time)
				file_for_upload_failure.write('上传信息：\n' + line)
				file_for_upload_failure.write('\n失败原因：主机配置信息不存在')
				file_for_upload_failure.write('\n--------------------华丽分割线--------------------\n\n')
				file_for_upload_failure.flush()

		file_for_upload_success.close()
		file_for_upload_failure.close()
		print('--------------------------上传完毕--------------------------')

	def exec_linux_command(self):
		file_configure_parser = FileConfigureParser()

		file_for_exec_success = open('./result/result_for_exec_success.txt','w',encoding='utf-8') #用于记录命令执行成功的文件
		file_for_exec_failure = open('./result/result_for_exec_failure.txt','w',encoding='utf-8') #用于记录命令执行失败的文件

		print('正在解析/conf/file_for_linux_operation.txt文件')
		file_configure_parser.parser_configure('./conf/file_for_linux_operation.txt')

		host_list_in_order = file_configure_parser.get_host_list_in_order()
		operation_object_dic = file_configure_parser.get_operation_object_dic()
		for host in host_list_in_order[:]:
			if host not in self.host_set_for_upload_success:
				host_list_in_order.remove(host)


		try:
			hostConfig = HostConfigParser().get_host_config() #获取主机配置信息
		except Exception as e:
			print('获取主机配置信息失败：%s,提取结束运行\n,烦请检查配置文件host_config.conf是否配置正确\n' % e)
			exit()
		host_list = hostConfig.sections() #获取配置信息中，主机节点列表

		ssh_client = MySSHClient()
		for host in host_list_in_order:
			if host in host_list:
				print('正在获取主机信息：%s' % host)
				port,username,password = int(hostConfig[host]['port']),hostConfig[host]['username'],hostConfig[host]['password']
				ssh_client.connect(host,port,username,password)

				for command in operation_object_dic[host]:
					run_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()) #记录执行时间
					result = ssh_client.exec_command(command)
					if result[0]:
						print('执行成功，正在记录到日志文件')
						file_for_exec_success.write('操作类型：执行命令\n')
						file_for_exec_success.write('执行时间：%s\n' % run_time)
						file_for_exec_success.write('执行信息：\n' + host + ' ' + command)
						file_for_exec_success.write('\n--------------------华丽分割线--------------------\n\n')
						file_for_exec_success.flush()
					else:
						print('执行失败：%s,正在记录到结果文件' % result[1])
						file_for_exec_failure.write('操作类型：执行命令\n')
						file_for_exec_failure.write('执行时间：%s\n' % run_time)
						file_for_exec_failure.write('执行信息：\n' + host + ' ' + command)
						file_for_exec_failure.write('\n失败原因：' + result[1])
						file_for_exec_failure.write('\n--------------------华丽分割线--------------------\n\n')
						file_for_exec_failure.flush()
			else:
				print('主机配置信息不存在')
				file_for_exec_failure.write('操作类型：执行命令\n')
				file_for_exec_failure.write('执行时间：%s\n' % run_time)
				file_for_exec_failure.write('执行信息：\n' + host + ' ' + command)
				file_for_exec_failure.write('失败原因：主机配置信息不存在')
				file_for_exec_failure.write('\n--------------------华丽分割线--------------------\n\n')
				file_for_exec_failure.flush()
			ssh_client.close()

		file_for_exec_success.close()
		file_for_exec_failure.close()






































