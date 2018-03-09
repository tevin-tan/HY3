# coding:utf-8

import unittest
from com import common, custom, base
from com.login import Login


class ContractSign(unittest.TestCase, base.Base):
	"""合同签约"""
	
	def setUp(self):
		self.env_file = "env.json"
		self.data_file = "data_xhd.json"
		base.Base.__init__(self, self.env_file, self.data_file)
	
	def tearDown(self):
		self.page.driver.quit()
	
	def test_one_person_sign(self):
		"""单人签约"""
		
		# ---------------------------------------------------------------------------------
		#                   1. 申请录入
		# ---------------------------------------------------------------------------------
		
		# 打印贷款产品信息
		custom.print_product_info(self.product_info)
		
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		common.input_all_bbi_property_info(
				self.page,
				self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		apply_code = common.get_applycode(self.page, self.custName)
		if apply_code:
			self.apply_code = apply_code
			self.log.info("申请件查询完成")
			print("apply_code:" + self.apply_code)
		
		# 下一步处理人
		self.next_user_id = common.get_next_user(self.page, self.apply_code)
		# ---------------------------------------------------------------------------------------
		# 	                        2. 风控审批流程
		# ---------------------------------------------------------------------------------------
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司主管审批
		res = common.approval_to_review(page, apply_code, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司主管审批通过！")
		self.next_user_id = common.get_next_user(page, apply_code)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = common.approval_to_review(page, apply_code, u'分公司经理回退到申请录入', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司经理审批通过！")
		self.next_user_id = common.get_next_user(page, apply_code)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = common.approval_to_review(page, apply_code, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise AssertionError('区域预复核审批失败！')
		else:
			self.log.info("区域预复核审批通过")
		self.next_user_id = common.get_next_user(page, apply_code)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批经理审批通过
		res = common.approval_to_review(page, apply_code, u'审批经理审批通过', 0)
		if not res:
			self.log.error("审批经理审批失败！")
			raise AssertionError('审批经理审批失败!')
		else:
			self.log.info("审批经理审批通过成功！")
		self.next_user_id = common.get_next_user(page, apply_code)
		
		# -----------------------------------------------------------------------------
		# 	                        3. 合同打印
		# -----------------------------------------------------------------------------
		rec_bank_info = dict(
				recBankNum=self.data['houseCommonLoanInfoList'][0]['recBankNum'],
				recPhone=self.data['houseCommonLoanInfoList'][0]['recPhone'],
				recBankProvince=self.data['houseCommonLoanInfoList'][0]['recBankProvince'],
				recBankDistrict=self.data['houseCommonLoanInfoList'][0]['recBankDistrict'],
				recBank=self.data['houseCommonLoanInfoList'][0]['recBank'],
				recBankBranch=self.data['houseCommonLoanInfoList'][0]['recBankBranch'],
				)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 签约
		common.make_signing(page, self.apply_code, rec_bank_info)
		self.log.info("签约完成")
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, apply_code)
	
	def test_two_person_sign(self):
		"""两人签约"""
		
		# ---------------------------------------------------------------------------------
		#                   1. 申请录入
		# ---------------------------------------------------------------------------------
		# 修改贷款金额
		self.update_product_amount(400000)
		
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		common.input_all_bbi_property_info(
				self.page, self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		apply_code = common.get_applycode(self.page, self.custName)
		if apply_code:
			self.apply_code = apply_code
			self.log.info("申请件查询完成")
			print("apply_code:" + self.apply_code)
		# 流程监控
		result = common.process_monitor(self.page, apply_code)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		# ---------------------------------------------------------------------------------------
		# 	                        2. 风控审批流程
		# ---------------------------------------------------------------------------------------
		
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, apply_code, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司主管审批通过！")
		self.next_user_id = common.get_next_user(page, apply_code)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = common.approval_to_review(page, apply_code, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司经理审批通过！")
		self.next_user_id = common.get_next_user(page, apply_code)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = common.approval_to_review(page, apply_code, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise AssertionError('区域预复核审批失败！')
		else:
			self.log.info("区域经理审批通过")
		self.next_user_id = common.get_next_user(page, apply_code)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批经理审批通过
		res = common.approval_to_review(page, apply_code, u'审批经理审批通过', 0)
		if not res:
			self.log.error("审批经理审批失败！")
			raise AssertionError('审批经理审批失败！')
		else:
			self.log.info("审批经理审批通过成功！")
		self.next_user_id = common.get_next_user(page, apply_code)
		
		# -----------------------------------------------------------------------------
		# 	                        3. 合同打印
		# -----------------------------------------------------------------------------
		
		rec_bank_info = dict(
				recBankNum=self.data['houseCommonLoanInfoList'][0]['recBankNum'],
				recPhone=self.data['houseCommonLoanInfoList'][0]['recPhone'],
				recBankProvince=self.data['houseCommonLoanInfoList'][0]['recBankProvince'],
				recBankDistrict=self.data['houseCommonLoanInfoList'][0]['recBankDistrict'],
				recBank=self.data['houseCommonLoanInfoList'][0]['recBank'],
				recBankBranch=self.data['houseCommonLoanInfoList'][0]['recBankBranch'],
				)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 两个人签约
		res = common.make_signing(page, self.apply_code, rec_bank_info, 2)
		if res:
			self.log.info("合同打印完成！")
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, apply_code)
	
	def test_03_three_person_sign(self):
		"""三人签约"""
		
		# ---------------------------------------------------------------------------------
		#                   1. 申请录入
		# ---------------------------------------------------------------------------------
		
		# 修改贷款金额
		self.update_product_amount(600000)
		
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		common.input_all_bbi_property_info(
				self.page, self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		apply_code = common.get_applycode(self.page, self.custName)
		if apply_code:
			self.apply_code = apply_code
			self.log.info("申请件查询完成")
			print("apply_code:" + self.apply_code)
		# 流程监控
		result = common.process_monitor(self.page, apply_code)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		# ---------------------------------------------------------------------------------------
		# 	                        2. 风控审批流程
		# ---------------------------------------------------------------------------------------
		
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, apply_code, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司主管审批通过")
		self.next_user_id = common.get_next_user(page, apply_code)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = common.approval_to_review(page, apply_code, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司经理审批通过！")
		self.next_user_id = common.get_next_user(page, apply_code)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = common.approval_to_review(page, apply_code, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise AssertionError('区域预复核审批失败！')
		else:
			self.log.info("区域经理审批通过！")
		self.next_user_id = common.get_next_user(page, apply_code)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批经理审批通过
		res = common.approval_to_review(page, apply_code, u'审批经理审批通过', 0)
		if not res:
			self.log.error("审批经理审批失败！")
			raise AssertionError('审批经理审批失败！')
		else:
			self.log.info("高级审批经理审批成功！")
		self.next_user_id = common.get_next_user(page, apply_code)
		
		# -----------------------------------------------------------------------------
		# 	                        3. 合同打印
		# -----------------------------------------------------------------------------
		
		rec_bank_info = dict(
				recBankNum=self.data['houseCommonLoanInfoList'][0]['recBankNum'],
				recPhone=self.data['houseCommonLoanInfoList'][0]['recPhone'],
				recBankProvince=self.data['houseCommonLoanInfoList'][0]['recBankProvince'],
				recBankDistrict=self.data['houseCommonLoanInfoList'][0]['recBankDistrict'],
				recBank=self.data['houseCommonLoanInfoList'][0]['recBank'],
				recBankBranch=self.data['houseCommonLoanInfoList'][0]['recBankBranch'],
				)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 两个人签约
		common.make_signing(page, self.apply_code, rec_bank_info, 3)
		self.log.info("合同打印完成")
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, apply_code)
	
	def test_04_four_person_sign(self):
		"""四人签约"""
		
		# ---------------------------------------------------------------------------------
		#                   1. 申请录入
		# ---------------------------------------------------------------------------------
		
		# 贷款金额
		self.update_product_amount(800000)
		
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		common.input_all_bbi_property_info(
				self.page, self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		apply_code = common.get_applycode(self.page, self.custName)
		if apply_code:
			self.apply_code = apply_code
			self.log.info("申请件查询完成")
			print("apply_code:" + self.apply_code)
		# 流程监控
		result = common.process_monitor(self.page, apply_code)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		# ---------------------------------------------------------------------------------------
		# 	                        2. 风控审批流程
		# ---------------------------------------------------------------------------------------
		
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, apply_code, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司主管审批通过")
		self.next_user_id = common.get_next_user(page, apply_code)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = common.approval_to_review(page, apply_code, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司经理审批通过！")
		self.next_user_id = common.get_next_user(page, apply_code)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = common.approval_to_review(page, apply_code, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise AssertionError('区域预复核审批失败！')
		else:
			self.log.info("区域经理审批通过！")
		self.next_user_id = common.get_next_user(page, apply_code)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批经理审批通过
		res = common.approval_to_review(page, apply_code, u'审批经理审批通过', 0)
		if not res:
			self.log.error("审批经理审批失败！")
			raise AssertionError('审批经理审批失败！')
		else:
			self.log.info("高级审批经理审批成功！")
		self.next_user_id = common.get_next_user(page, apply_code)
		
		# -----------------------------------------------------------------------------
		# 	                        3. 合同打印
		# -----------------------------------------------------------------------------
		
		rec_bank_info = dict(
				recBankNum=self.data['houseCommonLoanInfoList'][0]['recBankNum'],
				recPhone=self.data['houseCommonLoanInfoList'][0]['recPhone'],
				recBankProvince=self.data['houseCommonLoanInfoList'][0]['recBankProvince'],
				recBankDistrict=self.data['houseCommonLoanInfoList'][0]['recBankDistrict'],
				recBank=self.data['houseCommonLoanInfoList'][0]['recBank'],
				recBankBranch=self.data['houseCommonLoanInfoList'][0]['recBankBranch'],
				)
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 两个人签约
		common.make_signing(page, self.apply_code, rec_bank_info, 4)
		self.log.info("合同打印完成")
		
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, apply_code)
	
	def test_05_five_person_sign(self):
		"""五人签约"""
		
		# ---------------------------------------------------------------------------------
		#                   1. 申请录入
		# ---------------------------------------------------------------------------------
		
		# 贷款金额
		self.update_product_amount(1000000)
		
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		common.input_all_bbi_property_info(
				self.page, self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		apply_code = common.get_applycode(self.page, self.custName)
		if apply_code:
			self.apply_code = apply_code
			self.log.info("申请件查询完成")
			print("apply_code:" + self.apply_code)
		# 流程监控
		result = common.process_monitor(self.page, apply_code)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		# ---------------------------------------------------------------------------------------
		# 	                        2. 风控审批流程
		# ---------------------------------------------------------------------------------------
		
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, apply_code, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司主管审批通过")
		self.next_user_id = common.get_next_user(page, apply_code)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = common.approval_to_review(page, apply_code, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司经理审批通过！")
		self.next_user_id = common.get_next_user(page, apply_code)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = common.approval_to_review(page, apply_code, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise AssertionError('区域预复核审批失败！')
		else:
			self.log.info("区域经理审批通过！")
		self.next_user_id = common.get_next_user(page, apply_code)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批经理审批通过
		res = common.approval_to_review(page, apply_code, u'审批经理审批通过', 0)
		if not res:
			self.log.error("审批经理审批失败！")
			raise AssertionError('审批经理审批失败！')
		else:
			self.log.info("高级审批经理审批成功！")
		self.next_user_id = common.get_next_user(page, apply_code)
		
		# -----------------------------------------------------------------------------
		# 	                        3. 合同打印
		# -----------------------------------------------------------------------------
		
		rec_bank_info = dict(
				recBankNum=self.data['houseCommonLoanInfoList'][0]['recBankNum'],
				recPhone=self.data['houseCommonLoanInfoList'][0]['recPhone'],
				recBankProvince=self.data['houseCommonLoanInfoList'][0]['recBankProvince'],
				recBankDistrict=self.data['houseCommonLoanInfoList'][0]['recBankDistrict'],
				recBank=self.data['houseCommonLoanInfoList'][0]['recBank'],
				recBankBranch=self.data['houseCommonLoanInfoList'][0]['recBankBranch'],
				)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 两个人签约
		common.make_signing(page, self.apply_code, rec_bank_info, 5)
		self.log.info("合同打印完成")
		
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, apply_code)
