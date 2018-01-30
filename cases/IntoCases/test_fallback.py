# coding:utf-8
'''
	description: 回退，取消，拒绝场景
	Author: tsx
	date: 2018-1-15
'''
import unittest
import time
import json
import os
from com import common
from com.login import Login
from com.custom import Log, enviroment_change


class fallback(unittest.TestCase):
	'''风控回退/拒绝/取消场景'''
	
	def setUp(self):
		try:
			import config
			rootdir = config.__path__[0]
			config_env = os.path.join(rootdir, 'env.json')
			print("config_env:" + config_env)
			with open(config_env, 'r') as f:
				self.da = json.load(f)
				self.number = self.da["number"]
				self.env = self.da["enviroment"]
			
			filename = "data_cwd.json"
			data, company = enviroment_change(filename, self.number, self.env)
			self.page = Login()
			self.log = Log()
			
			# 录入的源数据
			self.data = data
			# 分公司选择
			self.company = company
		except Exception as e:
			self.log.error('load config error:', str(e))
			raise
	
	def tearDown(self):
		pass
	
	def get_next_user(self, page, applyCode):
		next_id = common.process_monitor(page, applyCode)
		if next_id is None:
			self.log.error("没有找到下一步处理人！")
			raise
		else:
			self.next_user_id = next_id
			self.log.info("下一步处理人:" + next_id)
			# 当前用户退出系统
			page.driver.quit()
	
	def test_01_branch_director_fallback(self):
		'''主管回退到申请录入'''
		
		'''
			1. 申请基本信息录入
		'''
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.custName = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])[1]
		
		# 3 物业信息
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成:" + self.applyCode)
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise
		
		'''
			2. 风控回退
		'''
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司主管回退
		res = common.approval_to_review(page, applyCode, u'回退到申请录入', 1)
		if not res:
			self.log.error("回退失败")
			raise ValueError("回退失败")
		else:
			self.log.info(u'分公司主管回退成功！')
			self.get_next_user(page, applyCode)
	
	def test_02_branch_manager_fallback(self):
		'''分公司经理回退到申请录入'''
		
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
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成:" + self.applyCode)
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise
		
		'''
			------------------------------------------------------------
								2. 风控审批回退
			------------------------------------------------------------
		'''
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applyCode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise
		else:
			self.log.info(u'分公司主管审批通过!')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		# 分公司经理回退
		res = common.approval_to_review(page, applyCode, u'分公司经理回退到申请录入', 1)
		if not res:
			self.log.error("回退失败")
			raise ValueError("回退失败")
		else:
			self.log.info(u'分公司经理回退到申请录入!')
			self.get_next_user(page, applyCode)
	
	def test_03_regional_fallback(self):
		'''区域复核回退到申请录入'''
		
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
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成:" + self.applyCode)
		
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise
		
		'''
			------------------------------------------------------------
								2. 风控审批回退
			------------------------------------------------------------
		'''
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applyCode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise
		else:
			self.log.info(u'分公司主管审批通过！')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批通过
		res = common.approval_to_review(page, applyCode, u'分公司经理回退到申请录入', 0)
		if not res:
			self.log.error("审批失败")
			raise
		else:
			self.log.info(u'分公司经理审批通过！')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核回退
		res = common.approval_to_review(page, applyCode, u'区域回退到申请录入', 1)
		if not res:
			self.log.error("回退失败")
			raise ValueError("回退失败")
		else:
			self.log.info(u'区域回退到申请录入成功!')
			self.get_next_user(page, applyCode)
	
	def test_04_manage_fallback(self):
		'''高级审批经理回退到申请录入'''
		
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
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成:" + self.applyCode)
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise
		
		'''
			------------------------------------------------------------
								2. 风控审批回退
			------------------------------------------------------------
		'''
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applyCode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise
		else:
			self.log.info(u'分公司主管审批通过！')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = common.approval_to_review(page, applyCode, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise
		else:
			self.log.info(u'分公司经理审批通过！')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = common.approval_to_review(page, applyCode, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise
		else:
			self.log.info(u'区域预复核审批通过!')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批经理回退
		res = common.approval_to_review(page, applyCode, u'审批经理回退到申请录入成功', 1)
		if not res:
			self.log.error("审批经理回退失败！")
			raise
		else:
			self.log.info(u'审批经理回退到申请录入成功!')
			self.get_next_user(page, applyCode)
	
	def test_05_risk_fallback(self):
		'''风控逐级回退'''
		
		'''
			---------------------------------------------------------------------
									1. 申请基本信息录入
			---------------------------------------------------------------------
		'''
		option = [u'区域预复核', u'分公司经理', u'分公司风控主管', u'风控专员录入']
		
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.custName = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])[1]
		
		# 3 物业信息
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成:" + self.applyCode)
		
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise
		
		'''
			------------------------------------------------------------
								2. 风控审批回退
			------------------------------------------------------------
		'''
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		# 分公司主管审批
		res = common.approval_to_review(page, applyCode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise
		else:
			self.log.info(u'分公司主管审批通过！')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		# 分公司经理审批
		res = common.approval_to_review(page, applyCode, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise
		else:
			self.log.info(u'分公司经理审批通过！')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		# 区域预复核审批
		res = common.approval_to_review(page, applyCode, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise
		else:
			self.log.info(u'区域预复核审批通过！')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		# 审批经理回退到区域预复核
		res = common.risk_approval_fallback(page, applyCode, option[0], u'回退到区域预复核')
		if not res:
			self.log.error("审批经理回退到区域预复核失败 ！")
			raise
		else:
			self.log.info(u'审批经理回退到区域预复核成功！')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		# 区域预复核回退到分公司经理
		res = common.risk_approval_fallback(page, applyCode, option[1], u'回退到分公司经理')
		if not res:
			self.log.error("区域预复核回退到分公司经理失败 ！")
			raise
		else:
			self.log.info(u'区域预复核回退到分公司经理成功！')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		# 分公司经理回退到分公司主管
		res = common.risk_approval_fallback(page, applyCode, option[2], u'回退到分公司主管')
		if not res:
			self.log.error("分公司经理回退到分公司主管失败 ！")
			raise
		else:
			self.log.info(u'区分公司经理回退到分公司主管成功！')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		# 分公司主管回退到申请录入
		res = common.risk_approval_fallback(page, applyCode, option[3], u'回退到申请录入')
		if not res:
			self.log.error("分公司主管回退到申请录入失败 ！")
			raise
		else:
			self.log.info(u'分公司主管回退到申请录入成功！')
			self.get_next_user(page, applyCode)
	
	def test_01_branch_director_cancel(self):
		'''主管取消'''
		
		'''
			1. 申请基本信息录入
		'''
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.custName = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])[1]
		
		# 3 物业信息
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成:" + self.applyCode)
			print("applyCode:" + self.applyCode)
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise
		
		'''
			2. 风控取消
		'''
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管回退
		res = common.approval_to_review(page, applyCode, u'主管取消', 2)
		if not res:
			self.log.error("分公司主管取消失败")
			raise
		else:
			self.log.info(u'主管取消！')
			self.get_next_user(page, applyCode)
	
	def test_02_branch_manager_cancel(self):
		'''分公司经理取消'''
		
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
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成:" + self.applyCode)
			print("applyCode:" + self.applyCode)
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise
		
		'''
			------------------------------------------------------------
								2. 风控审批回退
			------------------------------------------------------------
		'''
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applyCode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise
		else:
			self.log.info(u'分公司主管审批通过!')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		# 分公司经理回退
		res = common.approval_to_review(page, applyCode, u'分公司经理取消', 2)
		if not res:
			self.log.error("分公司经理取消失败！")
			raise ValueError("分公司经理取消失败！")
		else:
			self.log.info(u'分公司经理取消!')
			self.get_next_user(page, applyCode)
	
	def test_03_regional_cancel(self):
		'''区域复核取消'''
		
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
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成:" + self.applyCode)
		
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise
		
		'''
			------------------------------------------------------------
								2. 风控审批取消
			------------------------------------------------------------
		'''
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applyCode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise
		else:
			self.log.info(u'分公司主管审批通过！')
			self.get_next_user(page, applyCode, )
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批通过
		res = common.approval_to_review(page, applyCode, u'分公司经理审批通过!', 0)
		if not res:
			self.log.error("审批失败")
			raise
		else:
			self.log.info(u'分公司经理审批通过！')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核取消
		res = common.approval_to_review(page, applyCode, u'区域取消', 2)
		if not res:
			self.log.error("取消失败")
			raise
		else:
			self.log.info(u'区域取消成功！')
			self.get_next_user(page, applyCode)
	
	def test_04_manage_cancel(self):
		'''审批经理取消'''
		
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
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成:" + self.applyCode)
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise
		
		'''
			------------------------------------------------------------
								2. 风控审批回退
			------------------------------------------------------------
		'''
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applyCode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise
		else:
			self.log.info(u'分公司主管审批通过！')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = common.approval_to_review(page, applyCode, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise
		else:
			self.log.info(u'分公司经理审批通过！')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = common.approval_to_review(page, applyCode, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise
		else:
			self.log.info(u'区域预复核审批通过！')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批经理取消
		res = common.approval_to_review(page, applyCode, u'审审批经理取消成功', 2)
		if not res:
			self.log.error("审审批经理取消失败！")
			raise
		else:
			self.log.info(u'审审批经理取消成功！')
			self.get_next_user(page, applyCode)
	
	def test_01_branch_director_reject(self):
		'''主管拒绝'''
		
		'''
			1. 申请基本信息录入
		'''
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.custName = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])[1]
		
		# 3 物业信息
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成:" + self.applyCode)
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("下一个处理人:" + self.next_user_id)
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise
		
		'''
			2. 风控拒绝
		'''
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司主管拒绝
		res = common.approval_to_review(page, applyCode, u'主管拒绝', 3)
		if not res:
			self.log.error("主管拒绝失败")
			raise
		else:
			self.log.info('主管拒绝结束！')
		page.driver.close()
		
		# 高级审批经理登录
		page = Login('xn003625')
		
		# 拒绝
		value = common.reconsideration(page, applyCode)
		if value:
			self.log.info(u'主管拒绝成功，拒绝单已处于拒绝队列！')
			self.page.driver.quit()
		else:
			self.log.error(u'主管拒绝失败，拒绝队列未找到该笔单！')
			raise
	
	def test_01_branch_director_reject_pass(self):
		'''主管拒绝,并复议通过'''
		
		'''
			1. 申请基本信息录入
		'''
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.custName = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])[1]
		
		# 3 物业信息
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成:" + self.applyCode)
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise
		
		# --------------------------------------------------------------
		#               2. 风控拒绝
		# --------------------------------------------------------------
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管回退
		res = common.approval_to_review(page, applyCode, u'主管拒绝', 3)
		if not res:
			self.log.error("主管拒绝失败")
			raise
		else:
			self.log.info(u'主管拒绝！')
		page.driver.close()
		
		# 高级审批经理登录
		page = Login('xn003625')
		
		# 复议通过
		r1 = common.reconsideration(page, applyCode, 1)
		if r1:
			self.log.info(u'主管拒绝成功，复议通过！')
			self.page.driver.quit()
		else:
			self.log.error(u'主管拒绝失败，复议出错！')
			raise
	
	def test_01_branch_director_reject_fail(self):
		'''主管拒绝,并复议不通过'''
		
		'''
			1. 申请基本信息录入
		'''
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.custName = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])[1]
		
		# 3 物业信息
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成! " + self.applyCode)
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise
		
		'''
			2. 风控拒绝
		'''
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管回退
		res = common.approval_to_review(page, applyCode, u'主管拒绝', 3)
		if not res:
			self.log.error("主管拒绝失败")
			raise
		else:
			self.log.info(u'主管拒绝！')
		page.driver.close()
		
		# 高级审批经理登录
		page = Login('xn003625')
		
		# 复议通过
		r1 = common.reconsideration(page, applyCode, 2)
		if r1:
			self.log.info(u'主管拒绝成功，复议不通过成功！')
			self.page.driver.quit()
		else:
			self.log.error(u'主管拒绝失败，复议不通过出错！')
			raise
	
	def test_02_branch_manager_reject(self):
		'''分公司经理拒绝'''
		
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
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询:" + self.applyCode)
		# 流程监控
		self.get_next_user(self.page, applyCode)
		
		'''
			------------------------------------------------------------
								2. 风控审批拒绝
			------------------------------------------------------------
		'''
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applyCode, u'分公司主管审批', 0)
		if not res:
			self.log.error("审批失败")
			raise
		else:
			self.log.info(u'分公司主管审批通过!')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理拒绝
		res = common.approval_to_review(page, applyCode, u'分公司经理拒绝', 3)
		if not res:
			self.log.error("分公司经理拒绝失败！")
			raise
		else:
			self.log.info(u'分公司经理拒绝！')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域经理拒绝
		res = common.approval_to_review(page, applyCode, u'区域经理拒绝', 3)
		if not res:
			self.log.error("区域经理拒绝失败！")
			raise
		else:
			self.log.info(u'区域经理拒绝成功！')
			self.get_next_user(page, self.applyCode)
		
		#  下一步处理人登录
		page = Login(self.next_user_id)
		
		# 高级经理拒绝
		res = common.approval_to_review(page, applyCode, u'高级经理拒绝', 3)
		if not res:
			self.log.error("高级经理拒绝失败！")
			raise
		else:
			self.log.info(u'高级经理拒绝成功！')
		
		# 高级审批经理登录
		page = Login('xn003625')
		
		# 拒绝
		value = common.reconsideration(page, applyCode)
		if value:
			self.log.info(u'分公司经理拒成功，拒绝单已处于拒绝队列！')
			self.page.driver.quit()
		else:
			self.log.error(u'分公司经理拒绝失败，拒绝队列未找到该笔单！')
			raise
	
	def test_02_branch_manager_reject_pass(self):
		'''分公司经理拒绝,并复议通过'''
		
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
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成:" + self.applyCode)
		else:
			self.log.info(u'获取applyCode')
		self.get_next_user(self.page, self.applyCode)
		'''
			------------------------------------------------------------
								2. 风控审批拒绝
			------------------------------------------------------------
		'''
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applyCode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise
		else:
			self.log.info(u'分公司主管审批通过!')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理回退
		res = common.approval_to_review(page, applyCode, u'分公司经理拒绝', 3)
		if not res:
			self.log.error("分公司经理拒绝失败！")
			raise
		else:
			self.log.info(u'分公司经理拒绝！')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域经理拒绝
		res = common.approval_to_review(page, applyCode, u'区域经理拒绝', 3)
		if not res:
			self.log.error("区域经理拒绝拒绝失败！")
			raise
		else:
			self.log.info(u'区域经理拒绝！')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 高级经理拒绝
		res = common.approval_to_review(page, applyCode, u'高级经理拒绝', 3)
		if not res:
			self.log.error("高级经理拒绝失败！")
			raise
		else:
			self.log.info(u'高级经理拒绝成功！')
		
		# 高级审批经理登录
		page = Login('xn003625')
		
		# 复议通过
		r1 = common.reconsideration(page, applyCode, 1)
		if r1:
			self.log.info(u'分公司经理拒绝成功，复议通过！')
			self.page.driver.quit()
		else:
			self.log.error(u'分公司经理拒绝失败，复议出错！')
			raise
	
	def test_02_branch_manager_reject_fail(self):
		'''分公司经理拒绝,并复议不通过'''
		
		'''
			1. 申请基本信息录入
		'''
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.custName = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])[1]
		
		# 3 物业信息
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成! " + self.applyCode)
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise
		
		'''
			2. 风控拒绝
		'''
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applyCode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise
		else:
			self.log.info(u'分公司主管审批通过!')
			self.get_next_user(page, applyCode)
		
		page = Login(self.next_user_id)
		# 分公司经理拒绝
		res = common.approval_to_review(page, applyCode, u'分公司经理拒绝', 3)
		if not res:
			self.log.error("分公司经理拒绝失败")
			raise
		else:
			self.log.info(u'分公司经理拒绝！')
		
		self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域经理拒绝
		res = common.approval_to_review(page, applyCode, u'区域经理拒绝', 3)
		if not res:
			self.log.error("区域经理拒绝拒绝失败！")
			raise ValueError("区域经理拒绝拒绝失败！")
		else:
			self.log.info(u'区域经理拒绝！')
			self.get_next_user(page, applyCode)
			
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 高级经理拒绝
		res = common.approval_to_review(page, applyCode, u'高级经理拒绝', 3)
		if not res:
			self.log.error("高级经理拒绝失败！")
			raise
		else:
			self.log.info(u'高级经理拒绝成功！')
		
		# 高级审批经理登录
		page = Login('xn003625')
		
		# 复议通过
		r1 = common.reconsideration(page, applyCode, 2)
		if r1:
			self.log.info(u'分公司经理拒绝成功，并复议不通过成功！')
			page.driver.quit()
		else:
			self.log.error(u'分公司经理拒绝成功，但复议不通过出错！')
			raise
	
	def test_03_regional_reject(self):
		'''区域复核拒绝'''
		
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
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成:" + self.applyCode)
		
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise
		
		'''
			------------------------------------------------------------
								2. 风控审批拒绝
			------------------------------------------------------------
		'''
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applyCode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise
		else:
			self.log.info("分公司主管审批通过")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批通过
		res = common.approval_to_review(page, applyCode, u'分公司经理审批通过!', 0)
		if not res:
			self.log.error("审批失败")
			raise
		else:
			self.log.info(u'分公司经理审批通过！')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核拒绝
		res = common.approval_to_review(page, applyCode, u'区域拒绝', 3)
		if not res:
			self.log.error("区域拒绝失败")
			raise
		else:
			self.log.info("区域拒绝！")
			self.get_next_user(page, self.applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		res = common.approval_to_review(page, applyCode, u'高级经理拒绝', 3)
		if not res:
			self.log.error("高级经理拒绝失败")
			raise
		else:
			self.log.info("高级经理拒绝拒绝成功！")
			page.driver.quit()
			
		# 高级审批经理登录
		page = Login('xn003625')
		
		# 拒绝
		value = common.reconsideration(page, applyCode)
		if value:
			self.log.info(u'区域拒绝成功，拒绝单已处于拒绝队列！')
			self.page.driver.quit()
		else:
			self.log.error(u'区域失败，拒绝队列未找到该笔单！')
			raise
	
	def test_03_regional_reject_pass(self):
		'''区域复核拒绝，并复议通过'''
		
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
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成:" + self.applyCode)
		
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise
		
		'''
			------------------------------------------------------------
								2. 风控审批取消
			------------------------------------------------------------
		'''
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applyCode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise
		else:
			self.log.info(u'分公司主管审批通过！')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批通过
		res = common.approval_to_review(page, applyCode, u'分公司经理审批通过!', 0)
		if not res:
			self.log.error("审批失败")
			raise
		else:
			self.log.info(u'分公司经理审批通过！')
			self.get_next_user(page, applyCode, )
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核取消
		res = common.approval_to_review(page, applyCode, u'区域拒绝', 3)
		if not res:
			self.log.error("区域拒绝失败")
			raise
		else:
			self.log.info("区域拒绝！")
			self.get_next_user(page, self.applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		# 高级经理拒绝
		res = common.approval_to_review(page, applyCode, u'高级经理拒绝', 3)
		if not res:
			self.log.error("高级经理拒绝失败！")
			raise
		else:
			self.log.info(u'高级经理拒绝成功！')
			page.driver.quit()
		
		
		# 高级审批经理登录
		page = Login('xn003625')
		
		# 复议通过
		r1 = common.reconsideration(page, applyCode, 1)
		if r1:
			self.log.info(u'区域拒绝成功！复议通过！')
			self.page.driver.quit()
		else:
			self.log.error(u'区域拒绝失败，复议出错！')
			raise
	
	def test_03_regional_reject_fail(self):
		'''区域复核拒绝，并复议不通过'''
		
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
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成:" + self.applyCode)
		
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise
		
		'''
			------------------------------------------------------------
								2. 风控审批拒绝
			------------------------------------------------------------
		'''
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applyCode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise
		else:
			self.log.info(u'分公司主管审批通过！')
		self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批通过
		res = common.approval_to_review(page, applyCode, u'分公司经理审批通过!', 0)
		if not res:
			self.log.error("审批失败")
			raise
		else:
			self.log.info(u'分公司经理审批通过！')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核取消
		res = common.approval_to_review(page, applyCode, u'区域拒绝', 3)
		if not res:
			self.log.error("区域拒绝失败")
			raise
		else:
			self.log.info("区域拒绝！")
			self.get_next_user(page, self.applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		res = common.approval_to_review(page, applyCode, u'高级经理拒绝', 3)
		if not res:
			self.log.error("高级经理失败")
			raise
		else:
			self.log.info("高级经理拒绝成功！")
			page.driver.quit()
		
		# 高级审批经理登录
		page = Login('xn003625')
		
		# 复议通过
		r1 = common.reconsideration(page, applyCode, 2)
		if r1:
			self.log.info(u'区域拒绝成功，复议不通过成功！')
			self.page.driver.quit()
		else:
			self.log.error(u'区域拒绝成功，复议不通过出错！')
			raise
	
	def test_04_manage_reject(self):
		'''审批经理拒绝'''
		
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
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成:" + self.applyCode)
		
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise
		
		# ------------------------------------------------------------
		# 2. 风控审批拒绝
		# ------------------------------------------------------------
		
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applyCode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise
		else:
			self.log.info(u'分公司主管审批通过！')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = common.approval_to_review(page, applyCode, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise
		else:
			self.log.info(u'分公司经理审批通过！')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = common.approval_to_review(page, applyCode, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise
		else:
			self.log.info(u'区域预复核审批通过！')
			self.get_next_user(page, applyCode, )
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		# 高级经理拒绝
		res = common.approval_to_review(page, applyCode, u'高级经理拒绝', 3)
		if not res:
			self.log.error("高级经理拒绝失败！")
			raise
		else:
			self.log.info(u'高级经理拒绝成功！')
			page.driver.quit()
		
		# 高级审批经理登录
		page = Login('xn003625')
		
		# 拒绝
		value = common.reconsideration(page, applyCode)
		if value:
			self.log.info(u'审批经理拒绝成功，拒绝单已处于拒绝队列！')
			self.page.driver.quit()
		else:
			self.log.error(u'审批经理拒绝失败，拒绝队列未找到该笔单！')
			raise
	
	def test_04_manage_reject_pass(self):
		'''审批经理拒绝,并复议通过'''
		
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
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成:" + self.applyCode)
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise
		
		'''
			------------------------------------------------------------
								2. 风控审批回退
			------------------------------------------------------------
		'''
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applyCode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise
		else:
			self.log.info(u'分公司主管审批通过！')
			self.get_next_user(page, applyCode, )
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = common.approval_to_review(page, applyCode, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise
		else:
			self.log.info(u'分公司经理审批通过！')
			self.get_next_user(page, applyCode, )
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = common.approval_to_review(page, applyCode, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise
		else:
			self.log.info(u'区域预复核审批通过!')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 高级经理拒绝
		res = common.approval_to_review(page, applyCode, u'高级经理拒绝', 3)
		if not res:
			self.log.error("高级经理拒绝失败！")
			raise
		else:
			self.log.info(u'高级经理拒绝成功！')
			page.driver.quit()
		
		# 高级审批经理登录
		page = Login('xn003625')
		
		# 复议通过
		r1 = common.reconsideration(page, applyCode, 1)
		if r1:
			self.log.info(u'复议通过！')
			self.page.driver.quit()
		else:
			self.log.error(u'复议出错！')
			raise
	
	def test_04_manage_reject_fail(self):
		'''审批经理拒绝,并复议不通过'''
		
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
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成:" + self.applyCode)
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise
		
		'''
			------------------------------------------------------------
								2. 风控审批拒绝
			------------------------------------------------------------
		'''
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applyCode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise
		else:
			self.log.info(u'分公司主管审批通过！')
			self.get_next_user(page, applyCode, )
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = common.approval_to_review(page, applyCode, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise
		else:
			self.log.info( u'分公司经理审批通过！')
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = common.approval_to_review(page, applyCode, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise
		else:
			self.log.info(u'区域预复核审批通过！')
			self.get_next_user(page, applyCode )
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 高级经理拒绝
		res = common.approval_to_review(page, applyCode, u'高级经理拒绝', 3)
		if not res:
			self.log.error("高级经理拒绝失败！")
			raise
		else:
			self.log.info(u'高级经理拒绝成功！')
			page.driver.quit()
		
		# 高级审批经理登录
		page = Login('xn003625')
		
		# 复议通过
		r1 = common.reconsideration(page, applyCode, 2)
		if r1:
			self.log.info(u'复议不通过成功！')
			self.page.driver.quit()
		else:
			self.log.error(u'复议不通过出错！')
			raise
