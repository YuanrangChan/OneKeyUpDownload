# coding:utf-8
# @Time    :2019/8/20 22:32
# @Author  :David Chan
# @Mail    :david@chan.com
# @Function:fileConfigureParser

__author__ = 'david'

import re

class FileConfigureParser:
	def __init__(self):
		self.host_list_in_order = [] #存放主机地址，用于控制执行顺序
		self.operation_object_dic = {} #存放对应主机的待执行操作|待上传文件|待下载文件

	def get_host_list_in_order(self):
		return self.host_list_in_order

	def get_operation_object_dic(self):
		return self.operation_object_dic

	def parser_configure(self,config_file):
		print('正在读取待操作对象配置信息')
		self.host_list_in_order = []
		self.operation_object_dic = {}

		file_for_parser_failure = open('./result/object_will_not_be_operate.txt','w',encoding='utf-8') #用于记录不会被执行的操作配置行
		file_for_parser_failure.write('----------不会被操作的对象----------\n')
		file_for_parser_failure.write('所在文件：%s\n'% config_file) #用于记录不会被执行的操作
		line_no = 0 #用于记录行号

		with open(config_file,'r',encoding='utf-8') as file:
			host = ''
			line = file.readline()
			line_no = 1
			while line:
				line = line.rstrip('\n')
				line = line.rstrip('\t')
				line = line.strip()

				if line.startswith('#'):#注释，跳过
					line = file.readline()
					continue
				elif re.findall('[\s*[\d]+\.[\d]+\.[\d]+\.[\d]+\s*]$',line) :#说明是主机IP，形如[192.168.1.21]
					host = line.lstrip('[')
					host = line.rstrip(']')
					host = line.strip(' ')

					self.host_list_in_order.append(host)
					self.operation_object_dic[host] = []
				elif line and host:#说明是待操作目标对
					object_operation = line.strip(' ')
					object_operation = object_operation.strip('\t')
					self.operation_object_dic[host].append(object_operation)
				elif line:
					file_for_parser_failure.write('第%s行：'%line_no)
					file_for_parser_failure.write(line)
					file_for_parser_failure.write('\n')
					file_for_parser_failure.flush()

				line = file.readline()
				line_no = line_no + 1

		file_for_parser_failure.close()
		print('待操作对应信息：',self.operation_object_dic)
		print('主机地址列表：',self.host_list_in_order)




