# coding:utf-8

import os
import unittest

import yaml

import config
from com import base, login
from com.pobj.ContractSign import ContractSign as Cts


class ElectronicContract(unittest.TestCase, base.Base):
	def setUp(self):
		self.env_file = "env.json"
		self.data_file = "data_xhd.json"
		base.Base.__init__(self, self.env_file, self.data_file)
		
		rdir = config.__path__[0]
		pth = os.path.join(rdir, 'hostinfo')
		with open(pth, 'r', encoding='utf-8') as f:
			temp = yaml.load(f)
			self.host_ip = temp['SIT']['IP']
			self.port = temp['SIT']['port']
			self.host_name = temp['SIT']['username']
			self.host_password = temp['SIT']['password']
		f.close()
	
	def tearDown(self):
		self.page.driver.quit()
	
	def test_01_contract_sgin(self):
		"""电子签约"""
		# 1. 签约前步骤
		self.before_contract_sign()
		
		# 2. 获取短信验证码
		execmd = ' cd /web/apache-tomcat-7.0.69/logs; tail -10 catalina.out  > 1.txt ; ' \
		         'cat 1.txt | grep "短信" | awk -F"验证码：" \'{print $2}\' ' \
		         '| awk -F\'，\' \'{print $1}\' | tail -1'
		
		# ssh.sshclient_execmd(self.host_ip, self.port, self.host_name, self.host_password, cmd)
		
		# 3. 短信签约
		rs = Cts.ContractSign(self.page, self.apply_code, self.rec_bank_info)
		rs.send_message(self.host_ip, self.port, self.host_name, self.host_password, execmd)
	
	def test_02_delete_contract_sign(self):
		"""删除电子签约"""
		
		# 1. 签约
		self.test_01_contract_sgin()
		
		# 2. 删除
		page = login.Login(self.next_user_id)
		# 删除电子签章
		rs = Cts.ContractSign(page, self.apply_code, self.rec_bank_info)
		rs.delete_contract_sign(page, self.apply_code)
		page.driver.quit()
