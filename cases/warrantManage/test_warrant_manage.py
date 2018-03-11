# coding:utf-8

import unittest
from com import common, base
from com.login import Login
from com.pobj.ContractSign import ContractSign


class WarrantManage(unittest.TestCase, base.Base):
	"""权证请款流程"""
	
	def setUp(self):
		self.env_file = "env.json"
		self.data_file = "data_eyt.json"
		base.Base.__init__(self, self.env_file, self.data_file)
	
	def tearDown(self):
		self.page.driver.quit()
	
	def risk_approval_result(self, res, mark, page, apply_code):
		"""
		校验风控审批结果
		:param res: 返回值传入
		:param page: 页面对象
		:param apply_code: 申请件code
		:return:
		"""
		if not res:
			self.log.error(mark + ",审批失败")
			raise ValueError(mark + ",审批失败")
		else:
			self.log.info(mark + ",审批通过")
			self.next_user_id = common.get_next_user(page, apply_code)
	
	def test_01_warrantManage_original(self):
		"""权证原件请款"""
		
		self.update_product_amount(2000000)
		# ---------------------------------------------------------------------------------
		#                   1. 申请录入
		# ---------------------------------------------------------------------------------
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
		
		apply_code = self.AQ.get_applycode(self.page, self.custName)
		if apply_code:
			self.apply_code = apply_code
			self.log.info("申请件查询完成")
			print("apply_code:" + self.apply_code)
		# 流程监控
		result = self.PM.process_monitor(self.page, apply_code)
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
		page = Login(self.next_user_id)
		
		list_mark = [
			"分公司主管审批",
			"分公司经理审批",
			"区域预复核审批",
			"高级审批经理审批",
			"风控总监审批"
			]
		
		for e in list_mark:
			res = self.PT.approval_to_review(page, apply_code, e, 0)
			self.risk_approval_result(res, e, page, apply_code)
			# 下一个处理人重新登录
			page = Login(self.next_user_id)
		
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
		
		res = ContractSign.ContractSign(page, self.apply_code, rec_bank_info, 10)
		res.execute_sign()
		
		self.next_user_id = common.get_next_user(page, self.apply_code)
		
		# 合规审查
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 合规审查
		res = self.PT.compliance_audit(page, self.apply_code)
		if res:
			self.log.info("合规审批结束")
			page.driver.quit()
		else:
			self.log.error("合规审查失败")
			raise ValueError("合规审查失败")
		
		# 权证办理
		# 权证员登录
		page = Login(self.company["authority_member"]["user"])
		# 权证员上传权证信息
		self.WM.authority_card_transact(page, self.apply_code, self.env)
		
		page = Login(self.next_user_id)
		# 权证请款
		res = self.WM.warrant_apply(page, self.apply_code)
		if not res:
			self.log.error("权证请款失败！")
			raise ValueError('权证请款失败！')
		else:
			self.log.info("完成权证请款")
			self.next_user_id = common.get_next_user(page, self.apply_code)
	
	def test_02_warrantManage_part(self):
		"""部分权证请款"""
		
		# ---------------------------------------------------------------------------------
		#                   1. 申请录入
		# ---------------------------------------------------------------------------------
		
		self.update_product_amount(400000)
		
		# 1 客户信息-业务基本信息
		if self.HAE.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.HAE.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		self.HAE.input_all_bbi_property_info(
				self.page, self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0]
				)
		# 提交
		self.HAE.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		apply_code = self.AQ.get_applycode(self.page, self.custName)
		if apply_code:
			self.apply_code = apply_code
			self.log.info("申请件查询完成")
			print("apply_code:" + self.apply_code)
		# 流程监控
		result = self.PM.process_monitor(self.page, apply_code)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
		else:
			raise ValueError("流程监控查询出错！")
		
		# ---------------------------------------------------------------------------------------
		# 	                        2. 风控审批流程
		# ---------------------------------------------------------------------------------------
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		list_mark = [
			"分公司主管审批",
			"分公司经理审批",
			"区域预复核审批",
			"高级审批经理审批"
			]
		
		for e in list_mark:
			res = self.PT.approval_to_review(page, apply_code, e, 0)
			self.risk_approval_result(res, e, page, apply_code)
			# 下一个处理人重新登录
			page = Login(self.next_user_id)
		
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
		# next transcat person
		self.next_user_id = common.get_next_user(page, self.apply_code)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 两个人签约
		res = ContractSign.ContractSign(page, self.apply_code, rec_bank_info, 2).execute_sign()
		if res:
			self.log.info("合同打印完成！")
			# 查看下一步处理人
			self.next_user_id = common.get_next_user(page, apply_code)
		
		# -----------------------------------------------------------------------------
		#                                合规审查
		# -----------------------------------------------------------------------------
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 合规审查
		res = self.PT.compliance_audit(page, self.apply_code)
		if res:
			self.log.info("合规审批结束")
			page.driver.quit()
		else:
			self.log.error("合规审查失败")
			raise ValueError("合规审查失败")
		
		# -----------------------------------------------------------------------------
		#                                权证办理
		# -----------------------------------------------------------------------------
		page = Login(self.company["authority_member"]["user"])
		# 权证员上传权证信息
		res = self.WM.authority_card_transact(page, self.apply_code, self.env)
		if not res:
			self.log.error("上传权证资料失败")
			raise ValueError("上传权证资料失败")
		else:
			self.log.info("权证办理完成")
			self.next_user_id = common.get_next_user(page, self.apply_code)
		
		# -----------------------------------------------------------------------------
		#                                权证请款
		# -----------------------------------------------------------------------------
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		# 部分请款
		res = self.PT.part_warrant_apply(page, self.apply_code)
		if not res:
			self.log.error("权证请款失败！")
			raise ValueError('权证请款失败！')
		else:
			self.log.info("完成权证请款")
			self.next_user_id = common.get_next_user(page, self.apply_code)
		
		# -----------------------------------------------------------------------------
		#                                回执提放审批审核，回执分公司主管审批
		# -----------------------------------------------------------------------------
		receipt_lst = ['回执分公司主管审批', '回执审批经理审批', '第一次回执放款申请']
		
		for i in receipt_lst:
			page = Login(self.next_user_id)
			rec = self.PT.receipt_return(page, self.apply_code)
			if not rec:
				self.log.error(i + "失败")
				raise ValueError(i + '失败')
			else:
				self.log.info(i + "通过")
				self.next_user_id = common.get_next_user(page, self.apply_code)