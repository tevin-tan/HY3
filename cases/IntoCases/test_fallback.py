# coding:utf-8
"""
	description: 回退，取消，拒绝场景
	Author: tsx
	date: 2018-1-15
"""
import unittest
from com import custom, base
from com.login import Login


class FallBack(unittest.TestCase, base.Base):
	"""风控回退/拒绝/取消场景"""
	
	def setUp(self):
		self.env_file = "env.json"
		self.data_file = "data_xhd.json"
		base.Base.__init__(self, self.env_file, self.data_file)
	
	def tearDown(self):
		pass
	
	def get_next_user(self, page, applycode):
		next_id = self.PM.process_monitor(page, applycode)
		if next_id is None:
			self.log.error("没有找到下一步处理人！")
			raise AssertionError("没有找到下一步处理人！")
		else:
			self.next_user_id = next_id
			self.log.info("下一步处理人:" + next_id)
			# 当前用户退出系统
			page.driver.quit()
	
	def test_01_branch_director_fallback(self):
		"""主管回退到申请录入"""
		
		"""
			1. 申请基本信息录入
		"""
		
		custom.print_product_info(self.product_info)
		custom.print_person_info(self.person_info)
		
		# 1 客户信息-业务基本信息
		if self.HAE.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.HAE.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		self.HAE.input_all_bbi_property_info(
				self.page, self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0])
		
		# 提交
		self.HAE.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applycode = self.AQ.get_applycode(self.page, self.custName)
		
		if applycode:
			self.applycode = applycode
			self.log.info("申请件查询完成:" + self.applycode)
		# 流程监控
		result = self.PM.process_monitor(self.page, applycode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		"""
			2. 风控回退
		"""
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司主管回退
		res = self.PT.approval_to_review(page, applycode, u'回退到申请录入', 1)
		if not res:
			self.log.error("回退失败")
			raise ValueError("回退失败")
		else:
			self.log.info(u'分公司主管回退成功！')
			self.get_next_user(page, applycode)
	
	def test_02_branch_manager_fallback(self):
		"""分公司经理回退到申请录入"""
		
		"""
			---------------------------------------------------------------------
									1. 申请基本信息录入
			---------------------------------------------------------------------
		"""
		
		custom.print_product_info(self.product_info)
		custom.print_person_info(self.person_info)
		
		# 1 客户信息-业务基本信息
		if self.HAE.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.HAE.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		self.HAE.input_all_bbi_property_info(
				self.page,
				self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0])
		
		# 提交
		self.HAE.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applycode = self.AQ.get_applycode(self.page, self.custName)
		
		if applycode:
			self.applycode = applycode
			self.log.info("申请件查询完成:" + self.applycode)
		# 流程监控
		result = self.PM.process_monitor(self.page, applycode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		"""
			------------------------------------------------------------
								2. 风控审批回退
			------------------------------------------------------------
		"""
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = self.PT.approval_to_review(page, applycode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info(u'分公司主管审批通过!')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		# 分公司经理回退
		res = self.PT.approval_to_review(page, applycode, u'分公司经理回退到申请录入', 1)
		if not res:
			self.log.error("回退失败")
			raise ValueError("回退失败")
		else:
			self.log.info(u'分公司经理回退到申请录入!')
			self.get_next_user(page, applycode)
	
	def test_03_regional_fallback(self):
		"""区域复核回退到申请录入"""
		
		"""
			---------------------------------------------------------------------
									1. 申请基本信息录入
			---------------------------------------------------------------------
		"""
		
		custom.print_product_info(self.product_info)
		custom.print_person_info(self.person_info)
		
		# 1 客户信息-业务基本信息
		if self.HAE.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.HAE.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		self.HAE.input_all_bbi_property_info(
				self.page,
				self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0])
		# 提交
		self.HAE.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applycode = self.AQ.get_applycode(self.page, self.custName)
		if applycode:
			self.applycode = applycode
			self.log.info("申请件查询完成:" + self.applycode)
		
		# 流程监控
		result = self.PM.process_monitor(self.page, applycode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		"""
			------------------------------------------------------------
								2. 风控审批回退
			------------------------------------------------------------
		"""
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = self.PT.approval_to_review(page, applycode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info(u'分公司主管审批通过！')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批通过
		res = self.PT.approval_to_review(page, applycode, u'分公司经理回退到申请录入', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info(u'分公司经理审批通过！')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核回退
		res = self.PT.approval_to_review(page, applycode, u'区域回退到申请录入', 1)
		if not res:
			self.log.error("回退失败")
			raise ValueError("回退失败")
		else:
			self.log.info(u'区域回退到申请录入成功!')
			self.get_next_user(page, applycode)
	
	def test_04_manage_fallback(self):
		"""高级审批经理回退到申请录入"""
		
		"""
			---------------------------------------------------------------------
									1. 申请基本信息录入
			---------------------------------------------------------------------
		"""
		
		custom.print_product_info(self.product_info)
		custom.print_person_info(self.person_info)
		
		# 1 客户信息-业务基本信息
		if self.HAE.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.HAE.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		self.HAE.input_all_bbi_property_info(
				self.page,
				self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0])
		# 提交
		self.HAE.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applycode = self.AQ.get_applycode(self.page, self.custName)
		if applycode:
			self.applycode = applycode
			self.log.info("申请件查询完成:" + self.applycode)
		# 流程监控
		result = self.PM.process_monitor(self.page, applycode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		"""
			------------------------------------------------------------
								2. 风控审批回退
			------------------------------------------------------------
		"""
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = self.PT.approval_to_review(page, applycode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info(u'分公司主管审批通过！')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = self.PT.approval_to_review(page, applycode, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info(u'分公司经理审批通过！')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = self.PT.approval_to_review(page, applycode, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise AssertionError('区域预复核审批失败！')
		else:
			self.log.info(u'区域预复核审批通过!')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批经理回退
		res = self.PT.approval_to_review(page, applycode, u'审批经理回退到申请录入成功', 1)
		if not res:
			self.log.error("审批经理回退失败！")
			raise AssertionError('审批经理回退失败！')
		else:
			self.log.info(u'审批经理回退到申请录入成功!')
			self.get_next_user(page, applycode)
	
	def test_05_risk_fallback(self):
		"""风控逐级回退"""
		
		"""
			---------------------------------------------------------------------
									1. 申请基本信息录入
			---------------------------------------------------------------------
		"""
		option = [u'区域预复核', u'分公司经理', u'分公司风控主管', u'风控专员录入']
		
		custom.print_product_info(self.product_info)
		custom.print_person_info(self.person_info)
		
		# 1 客户信息-业务基本信息
		if self.HAE.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.HAE.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		self.HAE.input_all_bbi_property_info(
				self.page,
				self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0])
		# 提交
		self.HAE.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applycode = self.AQ.get_applycode(self.page, self.custName)
		if applycode:
			self.applycode = applycode
			self.log.info("申请件查询完成:" + self.applycode)
		
		# 流程监控
		result = self.PM.process_monitor(self.page, applycode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		"""
			------------------------------------------------------------
								2. 风控审批回退
			------------------------------------------------------------
		"""
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		# 分公司主管审批
		res = self.PT.approval_to_review(page, applycode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info(u'分公司主管审批通过！')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		# 分公司经理审批
		res = self.PT.approval_to_review(page, applycode, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info(u'分公司经理审批通过！')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		# 区域预复核审批
		res = self.PT.approval_to_review(page, applycode, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise AssertionError('区域预复核审批失败！')
		else:
			self.log.info(u'区域预复核审批通过！')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		# 审批经理回退到区域预复核
		res = self.PT.risk_approval_fallback(page, applycode, option[0], u'回退到区域预复核')
		if not res:
			self.log.error("审批经理回退到区域预复核失败 ！")
			raise AssertionError('审批经理回退到区域预复核失败 ！')
		else:
			self.log.info(u'审批经理回退到区域预复核成功！')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		# 区域预复核回退到分公司经理
		res = self.PT.risk_approval_fallback(page, applycode, option[1], u'回退到分公司经理')
		if not res:
			self.log.error("区域预复核回退到分公司经理失败 ！")
			raise AssertionError('区域预复核回退到分公司经理失败 ！')
		else:
			self.log.info(u'区域预复核回退到分公司经理成功！')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		# 分公司经理回退到分公司主管
		res = self.PT.risk_approval_fallback(page, applycode, option[2], u'回退到分公司主管')
		if not res:
			self.log.error("分公司经理回退到分公司主管失败 ！")
			raise AssertionError('分公司经理回退到分公司主管失败 ！')
		else:
			self.log.info(u'区分公司经理回退到分公司主管成功！')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		# 分公司主管回退到申请录入
		res = self.PT.risk_approval_fallback(page, applycode, option[3], u'回退到申请录入')
		if not res:
			self.log.error("分公司主管回退到申请录入失败 ！")
			raise AssertionError('分公司主管回退到申请录入失败 ！')
		else:
			self.log.info(u'分公司主管回退到申请录入成功！')
			self.get_next_user(page, applycode)
	
	def test_01_branch_director_cancel(self):
		"""主管取消"""
		
		"""
			1. 申请基本信息录入
		"""
		custom.print_product_info(self.product_info)
		custom.print_person_info(self.person_info)
		
		# 1 客户信息-业务基本信息
		if self.HAE.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.HAE.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		self.HAE.input_all_bbi_property_info(
				self.page,
				self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0])
		
		# 提交
		self.HAE.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applycode = self.AQ.get_applycode(self.page, self.custName)
		
		if applycode:
			self.applycode = applycode
			self.log.info("申请件查询完成:" + self.applycode)
			print("applycode:" + self.applycode)
		# 流程监控
		result = self.PM.process_monitor(self.page, applycode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		"""
			2. 风控取消
		"""
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管取消
		res = self.PT.approval_to_review(page, applycode, u'主管取消', 2)
		if not res:
			self.log.error("分公司主管取消失败")
			raise AssertionError('分公司主管取消失败')
		else:
			self.log.info(u'主管取消！')
			self.get_next_user(page, applycode)
	
	def test_02_branch_manager_cancel(self):
		"""分公司经理取消"""
		
		"""
			---------------------------------------------------------------------
									1. 申请基本信息录入
			---------------------------------------------------------------------
		"""
		custom.print_product_info(self.product_info)
		custom.print_person_info(self.person_info)
		
		# 1 客户信息-业务基本信息
		if self.HAE.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.HAE.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		self.HAE.input_all_bbi_property_info(
				self.page,
				self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0])
		
		# 提交
		self.HAE.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applycode = self.AQ.get_applycode(self.page, self.custName)
		
		if applycode:
			self.applycode = applycode
			self.log.info("申请件查询完成:" + self.applycode)
			print("applycode:" + self.applycode)
		# 流程监控
		result = self.PM.process_monitor(self.page, applycode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		"""
			------------------------------------------------------------
								2. 风控审批回退
			------------------------------------------------------------
		"""
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = self.PT.approval_to_review(page, applycode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info(u'分公司主管审批通过!')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		# 分公司经理回退
		res = self.PT.approval_to_review(page, applycode, u'分公司经理取消', 2)
		if not res:
			self.log.error("分公司经理取消失败！")
			raise ValueError("分公司经理取消失败！")
		else:
			self.log.info(u'分公司经理取消!')
			self.get_next_user(page, applycode)
	
	def test_03_regional_cancel(self):
		"""区域复核取消"""
		
		"""
			---------------------------------------------------------------------
									1. 申请基本信息录入
			---------------------------------------------------------------------
		"""
		custom.print_product_info(self.product_info)
		custom.print_person_info(self.person_info)
		
		# 1 客户信息-业务基本信息
		if self.HAE.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.HAE.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		self.HAE.input_all_bbi_property_info(
				self.page,
				self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0])
		# 提交
		self.HAE.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applycode = self.AQ.get_applycode(self.page, self.custName)
		if applycode:
			self.applycode = applycode
			self.log.info("申请件查询完成:" + self.applycode)
		
		# 流程监控
		result = self.PM.process_monitor(self.page, applycode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		"""
			------------------------------------------------------------
								2. 风控审批取消
			------------------------------------------------------------
		"""
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = self.PT.approval_to_review(page, applycode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info(u'分公司主管审批通过！')
			self.get_next_user(page, applycode, )
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批通过
		res = self.PT.approval_to_review(page, applycode, u'分公司经理审批通过!', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info(u'分公司经理审批通过！')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核取消
		res = self.PT.approval_to_review(page, applycode, u'区域取消', 2)
		if not res:
			self.log.error("取消失败")
			raise AssertionError('取消失败')
		else:
			self.log.info(u'区域取消成功！')
			self.get_next_user(page, applycode)
	
	def test_04_manage_cancel(self):
		"""审批经理取消"""
		
		"""
			---------------------------------------------------------------------
									1. 申请基本信息录入
			---------------------------------------------------------------------
		"""
		custom.print_product_info(self.product_info)
		custom.print_person_info(self.person_info)
		
		# 1 客户信息-业务基本信息
		if self.HAE.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.HAE.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		self.HAE.input_all_bbi_property_info(
				self.page,
				self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0])
		# 提交
		self.HAE.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applycode = self.AQ.get_applycode(self.page, self.custName)
		if applycode:
			self.applycode = applycode
			self.log.info("申请件查询完成:" + self.applycode)
		# 流程监控
		result = self.PM.process_monitor(self.page, applycode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		"""
			------------------------------------------------------------
								2. 风控审批回退
			------------------------------------------------------------
		"""
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = self.PT.approval_to_review(page, applycode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info(u'分公司主管审批通过！')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = self.PT.approval_to_review(page, applycode, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info(u'分公司经理审批通过！')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = self.PT.approval_to_review(page, applycode, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise AssertionError('区域预复核审批失败！')
		else:
			self.log.info(u'区域预复核审批通过！')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批经理取消
		res = self.PT.approval_to_review(page, applycode, u'审审批经理取消成功', 2)
		if not res:
			self.log.error("审批经理取消失败！")
			raise AssertionError('审审批经理取消失败')
		else:
			self.log.info(u'审审批经理取消成功！')
			self.get_next_user(page, applycode)
	
	def test_01_branch_director_reject(self):
		"""主管拒绝"""
		
		"""
			1. 申请基本信息录入
		"""
		custom.print_product_info(self.product_info)
		custom.print_person_info(self.person_info)
		
		# 1 客户信息-业务基本信息
		if self.HAE.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.HAE.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		self.HAE.input_all_bbi_property_info(
				self.page,
				self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0])
		
		# 提交
		self.HAE.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applycode = self.AQ.get_applycode(self.page, self.custName)
		
		if applycode:
			self.applycode = applycode
			self.log.info("申请件查询完成:" + self.applycode)
		# 流程监控
		result = self.PM.process_monitor(self.page, applycode)
		if result is not None:
			self.next_user_id = result
			self.log.info("下一个处理人:" + self.next_user_id)
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		"""
			2. 风控拒绝
		"""
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司主管拒绝
		res = self.PT.approval_to_review(page, applycode, u'主管拒绝', 3)
		if not res:
			self.log.error("主管拒绝失败")
			raise AssertionError('主管拒绝失败')
		else:
			self.log.info('主管拒绝结束！')
		page.driver.close()
		
		# 高级审批经理登录
		page = Login(self.senior_manager)
		
		# 拒绝
		value = self.HRL.reconsideration(page, applycode)
		if value:
			self.log.info(u'主管拒绝成功，拒绝单已处于拒绝队列！')
			self.page.driver.quit()
		else:
			self.log.error(u'主管拒绝失败，拒绝队列未找到该笔单！')
			raise AssertionError('主管拒绝失败，拒绝队列未找到该笔单！')
	
	def test_01_branch_director_reject_pass(self):
		"""主管拒绝,并复议通过"""
		
		"""
			1. 申请基本信息录入
		"""
		custom.print_product_info(self.product_info)
		
		# 1 客户信息-业务基本信息
		if self.HAE.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.HAE.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		self.HAE.input_all_bbi_property_info(
				self.page,
				self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0])
		
		# 提交
		self.HAE.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applycode = self.AQ.get_applycode(self.page, self.custName)
		
		if applycode:
			self.applycode = applycode
			self.log.info("申请件查询完成:" + self.applycode)
		# 流程监控
		result = self.PM.process_monitor(self.page, applycode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		# --------------------------------------------------------------
		#               2. 风控拒绝
		# --------------------------------------------------------------
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管回退
		res = self.PT.approval_to_review(page, applycode, u'主管拒绝', 3)
		if not res:
			self.log.error("主管拒绝失败")
			raise AssertionError('主管拒绝失败')
		else:
			self.log.info(u'主管拒绝！')
		page.driver.close()
		
		# 高级审批经理登录
		page = Login(self.senior_manager)
		
		# 复议通过
		r1 = self.HRL.reconsideration(page, applycode, 1)
		if r1:
			self.log.info(u'主管拒绝成功，复议通过！')
			self.page.driver.quit()
		else:
			self.log.error(u'主管拒绝失败，复议出错！')
			raise AssertionError('主管拒绝失败，复议出错！')
	
	def test_01_branch_director_reject_fail(self):
		"""主管拒绝,并复议不通过"""
		
		"""
			1. 申请基本信息录入
		"""
		
		custom.print_product_info(self.product_info)
		custom.print_person_info(self.person_info)
		
		# 1 客户信息-业务基本信息
		if self.HAE.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.HAE.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		self.HAE.input_all_bbi_property_info(
				self.page,
				self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0])
		
		# 提交
		self.HAE.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applycode = self.AQ.get_applycode(self.page, self.custName)
		
		if applycode:
			self.applycode = applycode
			self.log.info("申请件查询完成! " + self.applycode)
		# 流程监控
		result = self.PM.process_monitor(self.page, applycode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		"""
			2. 风控拒绝
		"""
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管回退
		res = self.PT.approval_to_review(page, applycode, u'主管拒绝', 3)
		if not res:
			self.log.error("主管拒绝失败")
			raise AssertionError('主管拒绝失败，复议出错！')
		else:
			self.log.info(u'主管拒绝！')
		page.driver.close()
		
		# 高级审批经理登录
		page = Login(self.senior_manager)
		
		# 复议通过
		r1 = self.HRL.reconsideration(page, applycode, 2)
		if r1:
			self.log.info(u'主管拒绝成功，复议不通过成功！')
			self.page.driver.quit()
		else:
			self.log.error(u'主管拒绝失败，复议不通过出错！')
			raise AssertionError('主管拒绝失败，复议不通过出错！')
	
	def test_02_branch_manager_reject(self):
		"""分公司经理拒绝"""
		
		"""
			---------------------------------------------------------------------
									1. 申请基本信息录入
			---------------------------------------------------------------------
		"""
		custom.print_product_info(self.product_info)
		custom.print_person_info(self.person_info)
		
		# 1 客户信息-业务基本信息
		if self.HAE.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.HAE.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		self.HAE.input_all_bbi_property_info(
				self.page,
				self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0])
		
		# 提交
		self.HAE.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applycode = self.AQ.get_applycode(self.page, self.custName)
		
		if applycode:
			self.applycode = applycode
			self.log.info("申请件查询:" + self.applycode)
		# 流程监控
		self.get_next_user(self.page, applycode)
		
		"""
			------------------------------------------------------------
								2. 风控审批拒绝
			------------------------------------------------------------
		"""
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司主管审批
		res = self.PT.approval_to_review(page, applycode, u'分公司主管审批', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info(u'分公司主管审批通过!')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理拒绝
		res = self.PT.approval_to_review(page, applycode, u'分公司经理拒绝', 3)
		if not res:
			self.log.error("分公司经理拒绝失败！")
			raise AssertionError('分公司经理拒绝失败！')
		else:
			self.log.info(u'分公司经理拒绝！')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域经理拒绝
		res = self.PT.approval_to_review(page, applycode, u'区域经理拒绝', 3)
		if not res:
			self.log.error("区域经理拒绝失败！")
			raise AssertionError('区域经理拒绝失败！')
		else:
			self.log.info(u'区域经理拒绝成功！')
			self.get_next_user(page, self.applycode)
		
		# 下一步处理人登录
		page = Login(self.next_user_id)
		
		# 高级经理拒绝
		res = self.PT.approval_to_review(page, applycode, u'高级经理拒绝', 3)
		if not res:
			self.log.error("高级经理拒绝失败！")
			raise AssertionError('高级经理拒绝失败！')
		else:
			self.log.info(u'高级经理拒绝成功！')
		
		# 高级审批经理登录
		page = Login(self.senior_manager)
		
		# 拒绝
		value = self.HRL.reconsideration(page, applycode)
		if value:
			self.log.info(u'分公司经理拒成功，拒绝单已处于拒绝队列！')
			self.page.driver.quit()
		else:
			self.log.error(u'分公司经理拒绝失败，拒绝队列未找到该笔单！')
			raise AssertionError('分公司经理拒绝失败，拒绝队列未找到该笔单！')
	
	def test_02_branch_manager_reject_pass(self):
		"""分公司经理拒绝,并复议通过"""
		
		"""
			---------------------------------------------------------------------
									1. 申请基本信息录入
			---------------------------------------------------------------------
		"""
		custom.print_product_info(self.product_info)
		custom.print_person_info(self.person_info)
		
		# 1 客户信息-业务基本信息
		if self.HAE.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.HAE.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		self.HAE.input_all_bbi_property_info(
				self.page,
				self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0])
		
		# 提交
		self.HAE.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applycode = self.AQ.get_applycode(self.page, self.custName)
		
		if applycode:
			self.applycode = applycode
			self.log.info("申请件查询完成:" + self.applycode)
		else:
			self.log.info(u'获取applycode')
		self.get_next_user(self.page, self.applycode)
		"""
			------------------------------------------------------------
								2. 风控审批拒绝
			------------------------------------------------------------
		"""
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司主管审批
		res = self.PT.approval_to_review(page, applycode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info(u'分公司主管审批通过!')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理回退
		res = self.PT.approval_to_review(page, applycode, u'分公司经理拒绝', 3)
		if not res:
			self.log.error("分公司经理拒绝失败！")
			raise AssertionError('分公司经理拒绝失败！')
		else:
			self.log.info(u'分公司经理拒绝！')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域经理拒绝
		res = self.PT.approval_to_review(page, applycode, u'区域经理拒绝', 3)
		if not res:
			self.log.error("区域经理拒绝拒绝失败！")
			raise AssertionError('区域经理拒绝拒绝失败')
		else:
			self.log.info(u'区域经理拒绝！')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 高级经理拒绝
		res = self.PT.approval_to_review(page, applycode, u'高级经理拒绝', 3)
		if not res:
			self.log.error("高级经理拒绝失败！")
			raise AssertionError('高级经理拒绝失败！')
		else:
			self.log.info(u'高级经理拒绝成功！')
		
		# 高级审批经理登录
		page = Login(self.senior_manager)
		
		# 复议通过
		r1 = self.HRL.reconsideration(page, applycode, 1)
		if r1:
			self.log.info(u'分公司经理拒绝成功，复议通过！')
			self.page.driver.quit()
		else:
			self.log.error(u'分公司经理拒绝失败，复议出错！')
			raise AssertionError('分公司经理拒绝失败，复议出错！')
	
	def test_02_branch_manager_reject_fail(self):
		"""分公司经理拒绝,并复议不通过"""
		
		"""
			1. 申请基本信息录入
		"""
		custom.print_product_info(self.product_info)
		custom.print_person_info(self.person_info)
		
		# 1 客户信息-业务基本信息
		if self.HAE.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.HAE.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		self.HAE.input_all_bbi_property_info(
				self.page,
				self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0])
		
		# 提交
		self.HAE.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applycode = self.AQ.get_applycode(self.page, self.custName)
		
		if applycode:
			self.applycode = applycode
			self.log.info("申请件查询完成! " + self.applycode)
		# 流程监控
		result = self.PM.process_monitor(self.page, applycode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		"""
			2. 风控拒绝
		"""
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = self.PT.approval_to_review(page, applycode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info(u'分公司主管审批通过!')
			self.get_next_user(page, applycode)
		
		page = Login(self.next_user_id)
		# 分公司经理拒绝
		res = self.PT.approval_to_review(page, applycode, u'分公司经理拒绝', 3)
		if not res:
			self.log.error("分公司经理拒绝失败")
			raise AssertionError('分公司经理拒绝失败')
		else:
			self.log.info(u'分公司经理拒绝！')
		
		self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域经理拒绝
		res = self.PT.approval_to_review(page, applycode, u'区域经理拒绝', 3)
		if not res:
			self.log.error("区域经理拒绝拒绝失败！")
			raise ValueError("区域经理拒绝拒绝失败！")
		else:
			self.log.info(u'区域经理拒绝！')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 高级经理拒绝
		res = self.PT.approval_to_review(page, applycode, u'高级经理拒绝', 3)
		if not res:
			self.log.error("高级经理拒绝失败！")
			raise AssertionError('高级经理拒绝失败！')
		else:
			self.log.info(u'高级经理拒绝成功！')
		
		# 高级审批经理登录
		page = Login(self.senior_manager)
		
		# 复议通过
		r1 = self.HRL.reconsideration(page, applycode, 2)
		if r1:
			self.log.info(u'分公司经理拒绝成功，并复议不通过成功！')
			page.driver.quit()
		else:
			self.log.error(u'分公司经理拒绝成功，但复议不通过出错！')
			raise AssertionError('分公司经理拒绝成功，但复议不通过出错！')
	
	def test_03_regional_reject(self):
		"""区域复核拒绝"""
		
		"""
			---------------------------------------------------------------------
									1. 申请基本信息录入
			---------------------------------------------------------------------
		"""
		custom.print_product_info(self.product_info)
		custom.print_person_info(self.person_info)
		
		# 1 客户信息-业务基本信息
		if self.HAE.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.HAE.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		self.HAE.input_all_bbi_property_info(
				self.page,
				self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0])
		# 提交
		self.HAE.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applycode = self.AQ.get_applycode(self.page, self.custName)
		if applycode:
			self.applycode = applycode
			self.log.info("申请件查询完成:" + self.applycode)
		
		# 流程监控
		result = self.PM.process_monitor(self.page, applycode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		"""
			------------------------------------------------------------
								2. 风控审批拒绝
			------------------------------------------------------------
		"""
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = self.PT.approval_to_review(page, applycode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司主管审批通过")
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批通过
		res = self.PT.approval_to_review(page, applycode, u'分公司经理审批通过!', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info(u'分公司经理审批通过！')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核拒绝
		res = self.PT.approval_to_review(page, applycode, u'区域拒绝', 3)
		if not res:
			self.log.error("区域拒绝失败")
			raise AssertionError('区域拒绝失败')
		else:
			self.log.info("区域拒绝！")
			self.get_next_user(page, self.applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		res = self.PT.approval_to_review(page, applycode, u'高级经理拒绝', 3)
		if not res:
			self.log.error("高级经理拒绝失败")
			raise AssertionError('高级经理拒绝失败')
		else:
			self.log.info("高级经理拒绝拒绝成功！")
			page.driver.quit()
		
		# 高级审批经理登录
		page = Login(self.senior_manager)
		
		# 拒绝
		value = self.HRL.reconsideration(page, applycode)
		if value:
			self.log.info(u'区域拒绝成功，拒绝单已处于拒绝队列！')
			self.page.driver.quit()
		else:
			self.log.error(u'区域失败，拒绝队列未找到该笔单！')
			raise AssertionError('区域失败，拒绝队列未找到该笔单！')
	
	def test_03_regional_reject_pass(self):
		"""区域复核拒绝，并复议通过"""
		
		"""
			---------------------------------------------------------------------
									1. 申请基本信息录入
			---------------------------------------------------------------------
		"""
		custom.print_product_info(self.product_info)
		custom.print_person_info(self.person_info)
		
		# 1 客户信息-业务基本信息
		if self.HAE.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.HAE.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		self.HAE.input_all_bbi_property_info(
				self.page,
				self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0])
		# 提交
		self.HAE.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applycode = self.AQ.get_applycode(self.page, self.custName)
		if applycode:
			self.applycode = applycode
			self.log.info("申请件查询完成:" + self.applycode)
		
		# 流程监控
		result = self.PM.process_monitor(self.page, applycode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		"""
			------------------------------------------------------------
								2. 风控审批取消
			------------------------------------------------------------
		"""
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = self.PT.approval_to_review(page, applycode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info(u'分公司主管审批通过！')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批通过
		res = self.PT.approval_to_review(page, applycode, u'分公司经理审批通过!', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info(u'分公司经理审批通过！')
			self.get_next_user(page, applycode, )
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核取消
		res = self.PT.approval_to_review(page, applycode, u'区域拒绝', 3)
		if not res:
			self.log.error("区域拒绝失败")
			raise AssertionError('区域拒绝失败')
		else:
			self.log.info("区域拒绝！")
			self.get_next_user(page, self.applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		# 高级经理拒绝
		res = self.PT.approval_to_review(page, applycode, u'高级经理拒绝', 3)
		if not res:
			self.log.error("高级经理拒绝失败！")
			raise AssertionError('高级经理拒绝失败！')
		else:
			self.log.info(u'高级经理拒绝成功！')
			page.driver.quit()
		
		# 高级审批经理登录
		page = Login(self.senior_manager)
		
		# 复议通过
		r1 = self.HRL.reconsideration(page, applycode, 1)
		if r1:
			self.log.info(u'区域拒绝成功！复议通过！')
			self.page.driver.quit()
		else:
			self.log.error(u'区域拒绝失败，复议出错！')
			raise AssertionError('区域拒绝失败，复议出错！')
	
	def test_03_regional_reject_fail(self):
		"""区域复核拒绝，并复议不通过"""
		
		"""
			---------------------------------------------------------------------
									1. 申请基本信息录入
			---------------------------------------------------------------------
		"""
		custom.print_product_info(self.product_info)
		custom.print_person_info(self.person_info)
		
		# 1 客户信息-业务基本信息
		if self.HAE.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.HAE.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		self.HAE.input_all_bbi_property_info(
				self.page,
				self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0])
		# 提交
		self.HAE.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applycode = self.AQ.get_applycode(self.page, self.custName)
		if applycode:
			self.applycode = applycode
			self.log.info("申请件查询完成:" + self.applycode)
		
		# 流程监控
		result = self.PM.process_monitor(self.page, applycode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		"""
			------------------------------------------------------------
								2. 风控审批拒绝
			------------------------------------------------------------
		"""
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = self.PT.approval_to_review(page, applycode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info(u'分公司主管审批通过！')
		self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批通过
		res = self.PT.approval_to_review(page, applycode, u'分公司经理审批通过!', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info(u'分公司经理审批通过！')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核取消
		res = self.PT.approval_to_review(page, applycode, u'区域拒绝', 3)
		if not res:
			self.log.error("区域拒绝失败")
			raise AssertionError('区域拒绝失败')
		else:
			self.log.info("区域拒绝！")
			self.get_next_user(page, self.applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		res = self.PT.approval_to_review(page, applycode, u'高级经理拒绝', 3)
		if not res:
			self.log.error("高级经理失败")
			raise AssertionError('高级经理失败')
		else:
			self.log.info("高级经理拒绝成功！")
			page.driver.quit()
		
		# 高级审批经理登录
		page = Login(self.senior_manager)
		
		# 复议通过
		r1 = self.HRL.reconsideration(page, applycode, 2)
		if r1:
			self.log.info(u'区域拒绝成功，复议不通过成功！')
			self.page.driver.quit()
		else:
			self.log.error(u'区域拒绝成功，复议不通过出错！')
			raise AssertionError('区域拒绝成功，复议不通过出错！')
	
	def test_04_manage_reject(self):
		"""高级审批经理拒绝"""
		
		"""
			---------------------------------------------------------------------
									1. 申请基本信息录入
			---------------------------------------------------------------------
		"""
		custom.print_product_info(self.product_info)
		custom.print_person_info(self.person_info)
		
		# 1 客户信息-业务基本信息
		if self.HAE.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.HAE.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		self.HAE.input_all_bbi_property_info(
				self.page,
				self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0])
		# 提交
		self.HAE.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applycode = self.AQ.get_applycode(self.page, self.custName)
		if applycode:
			self.applycode = applycode
			self.log.info("申请件查询完成:" + self.applycode)
		
		# 流程监控
		result = self.PM.process_monitor(self.page, applycode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		# ------------------------------------------------------------
		# 2. 风控审批拒绝
		# ------------------------------------------------------------
		
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = self.PT.approval_to_review(page, applycode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info(u'分公司主管审批通过！')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = self.PT.approval_to_review(page, applycode, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info(u'分公司经理审批通过！')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = self.PT.approval_to_review(page, applycode, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise AssertionError('区域预复核审批失败！')
		else:
			self.log.info(u'区域预复核审批通过！')
			self.get_next_user(page, applycode, )
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		# 高级经理拒绝
		res = self.PT.approval_to_review(page, applycode, u'高级经理拒绝', 3)
		if not res:
			self.log.error("高级经理拒绝失败！")
			raise AssertionError('高级经理拒绝失败！')
		else:
			self.log.info(u'高级经理拒绝成功！')
			page.driver.quit()
		
		# 高级审批经理登录
		page = Login(self.senior_manager)
		
		# 拒绝
		value = self.HRL.reconsideration(page, applycode)
		if value:
			self.log.info(u'审批经理拒绝成功，拒绝单已处于拒绝队列！')
			self.page.driver.quit()
		else:
			self.log.error(u'审批经理拒绝失败，拒绝队列未找到该笔单！')
			raise AssertionError(u'审批经理拒绝失败，拒绝队列未找到该笔单！')
	
	def test_04_manage_reject_pass(self):
		"""高级审批经理拒绝,并复议通过"""
		
		"""
			---------------------------------------------------------------------
									1. 申请基本信息录入
			---------------------------------------------------------------------
		"""
		custom.print_product_info(self.product_info)
		custom.print_person_info(self.person_info)
		
		# 1 客户信息-业务基本信息
		if self.HAE.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.HAE.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		self.HAE.input_all_bbi_property_info(
				self.page,
				self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0])
		# 提交
		self.HAE.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applycode = self.AQ.get_applycode(self.page, self.custName)
		if applycode:
			self.applycode = applycode
			self.log.info("申请件查询完成:" + self.applycode)
		# 流程监控
		result = self.PM.process_monitor(self.page, applycode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		"""
			------------------------------------------------------------
								2. 风控审批回退
			------------------------------------------------------------
		"""
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = self.PT.approval_to_review(page, applycode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info(u'分公司主管审批通过！')
			self.get_next_user(page, applycode, )
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = self.PT.approval_to_review(page, applycode, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info(u'分公司经理审批通过！')
			self.get_next_user(page, applycode, )
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = self.PT.approval_to_review(page, applycode, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise AssertionError('区域预复核审批失败！')
		else:
			self.log.info(u'区域预复核审批通过!')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 高级经理拒绝
		res = self.PT.approval_to_review(page, applycode, u'高级经理拒绝', 3)
		if not res:
			self.log.error("高级经理拒绝失败！")
			raise AssertionError('高级经理拒绝失败！')
		else:
			self.log.info(u'高级经理拒绝成功！')
			page.driver.quit()
		
		# 高级审批经理登录
		page = Login(self.senior_manager)
		
		# 复议通过
		r1 = self.HRL.reconsideration(page, applycode, 1)
		if r1:
			self.log.info(u'复议通过！')
			self.page.driver.quit()
		else:
			self.log.error(u'复议出错！')
			raise AssertionError('复议出错！')
	
	def test_04_manage_reject_fail(self):
		"""高级审批经理拒绝,并复议不通过"""
		
		"""
			---------------------------------------------------------------------
									1. 申请基本信息录入
			---------------------------------------------------------------------
		"""
		custom.print_product_info(self.product_info)
		custom.print_person_info(self.person_info)
		
		# 1 客户信息-业务基本信息
		if self.HAE.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.HAE.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		self.HAE.input_all_bbi_property_info(
				self.page,
				self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0])
		# 提交
		self.HAE.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applycode = self.AQ.get_applycode(self.page, self.custName)
		if applycode:
			self.applycode = applycode
			self.log.info("申请件查询完成:" + self.applycode)
		# 流程监控
		result = self.PM.process_monitor(self.page, applycode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		"""
			------------------------------------------------------------
								2. 风控审批拒绝
			------------------------------------------------------------
		"""
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = self.PT.approval_to_review(page, applycode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info(u'分公司主管审批通过！')
			self.get_next_user(page, applycode, )
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = self.PT.approval_to_review(page, applycode, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info(u'分公司经理审批通过！')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = self.PT.approval_to_review(page, applycode, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise AssertionError('区域预复核审批失败！')
		else:
			self.log.info(u'区域预复核审批通过！')
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 高级经理拒绝
		res = self.PT.approval_to_review(page, applycode, u'高级经理拒绝', 3)
		if not res:
			self.log.error("高级经理拒绝失败！")
			raise AssertionError('高级经理拒绝失败！')
		else:
			self.log.info(u'高级经理拒绝成功！')
			page.driver.quit()
		
		# 高级审批经理登录
		page = Login(self.senior_manager)
		
		# 复议通过
		r1 = self.HRL.reconsideration(page, applycode, 2)
		if r1:
			self.log.info(u'复议不通过成功！')
			self.page.driver.quit()
		else:
			self.log.error(u'复议不通过出错！')
			raise AssertionError(u'复议不通过出错！')
