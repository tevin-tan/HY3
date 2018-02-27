# coding:utf-8
'''
	Desc: 特批
	Author: tsx
	Date: 2018-1-24
'''

import unittest
import json
import os
from com import common
from com.login import Login
from com.custom import Log, enviroment_change, print_env


class SPA(unittest.TestCase):
	'''特批'''
	
	def setUp(self):
		self.log = Log()
		try:
			import config
			rootdir = config.__path__[0]
			config_env = os.path.join(rootdir, 'env.json')
			self.log.info("config_env:" + config_env)
			with open(config_env, 'r', encoding='utf-8') as f:
				self.da = json.load(f)
				self.number = self.da["number"]
				self.env = self.da["enviroment"]
			f.close()
			filename = "data_eyt.json"
			data, company = enviroment_change(filename, self.number, self.env)
			self.page = Login()
			
			# 录入的源数据
			self.data = data
			# 分公司选择
			self.company = company
			print_env(self.env, self.company)
		except Exception as e:
			self.log.error('load config error:', str(e))
			raise
	
	def get_next_user(self, page, applycode):
		next_id = common.process_monitor(page, applycode)
		if next_id is None:
			self.log.error("没有找到下一步处理人！")
			raise AssertionError('没有找到下一步处理人！')
		else:
			self.next_user_id = next_id
			self.log.info("下一步处理人:" + next_id)
			# 当前用户退出系统
			page.driver.quit()
	
	def tearDown(self):
		self.page.driver.quit()
	
	def test_01_region_special_approval(self):
		'''区域李伟波特批'''
		
		'''
			---------------------------------------------------------------------
									1. 申请基本信息录入
			---------------------------------------------------------------------
		'''
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.custName = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])[1]
		
		# 3 物业信息
		common.input_cwd_bbi_property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		self.log.info("主借人:" + self.custName)
		applycode = common.get_applycode(self.page, self.custName)
		
		if applycode:
			self.applycode = applycode
			self.log.info("申请件查询完成:" + self.applycode)
		else:
			self.log.error("申请件查询失败！")
			raise AssertionError('申请件查询失败！')
		
		# 流程监控
		result = common.process_monitor(self.page, applycode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		'''
			------------------------------------------------------------
								2. 风控审批-区域特批
			------------------------------------------------------------
		'''
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applycode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info(u'分公司主管审批通过！')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批通过
		res = common.approval_to_review(page, applycode, u'分公司经理回退到申请录入', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info(u'分公司经理审批通过！')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		if self.next_user_id != 'xn004754':
			# 区域特批
			res = common.approval_to_review(page, applycode, u'区域审批经理审批', 0)
			if not res:
				self.log.error("区域审批经理审批失败")
				raise AssertionError('区域审批经理审批失败')
			else:
				self.log.info(u'区域审批经理审批成功!')
				self.get_next_user(page, applycode)
		else:
			r = common.special_approval(page, self.applycode, u'区域特批')
			if not r:
				self.log.error('区域特批出错！')
				raise AssertionError('区域特批出错！')
			else:
				self.log.info('区域特批通过！')
				page.driver.quit()
	
	def test_02_manage_special_approval(self):
		'''高级经理特批'''
		
		self.test_01_region_special_approval()
		
		page = Login(self.next_user_id)
		r = common.special_approval(page, self.applycode, u'高级经理特批')
		if not r:
			self.log.error('高级经理特批出错！')
			raise AssertionError('高级经理特批出错！')
		else:
			self.log.info('高级经理特批通过！')
			self.get_next_user(page, self.applycode)
			page.driver.quit()
	
	def test_03_risk_director_special_approval(self):
		'''区域特批，风控总监特批终审'''
		
		self.test_02_manage_special_approval()
		
		page = Login(self.next_user_id)
		r = common.special_approval(page, self.applycode, u'风控总监特批')
		if not r:
			self.log.error('风控总监特批出错！')
			raise AssertionError('风控总监特批出错！')
		else:
			self.log.info('风控总监特批通过！')
			self.get_next_user(page, self.applycode)
			page.driver.quit()
