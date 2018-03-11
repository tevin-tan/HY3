import unittest
from com.login import Login
from com import custom, base
from com.pobj.ContractSign import ContractSign as Cts


class AddContract(unittest.TestCase, base.Base):
	"""多借款人签约"""
	
	def setUp(self):
		
		self.env_file = "env.json"
		self.data_file = "data_eyt.json"
		base.Base.__init__(self, self.env_file, self.data_file)
	
	def tearDown(self):
		self.page.driver.quit()
	
	def before_application_entry(self):
		""" 申请件录入"""
		
		# 贷款产品信息
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
			self.apply_code = applycode
			self.log.info("申请件查询完成")
			print("applycode:" + self.apply_code)
		# 流程监控
		result = self.PM.process_monitor(self.page, self.apply_code)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
	
	def before_risk_approval(self, amount):
		"""风控审批"""
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司主管审批
		res = self.PT.approval_to_review(page, self.apply_code, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司主管审批通过！")
			self.get_next_user(page, self.apply_code)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = self.PT.approval_to_review(page, self.apply_code, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司经理审批通过！")
			self.get_next_user(page, self.apply_code)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = self.PT.approval_to_review(page, self.apply_code, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise AssertionError('区域预复核审批失败！')
		else:
			self.log.info("区域预复核审批通过")
			self.get_next_user(page, self.apply_code)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批经理审批通过
		res = self.PT.approval_to_review(page, self.apply_code, u'审批经理审批通过', 0)
		if not res:
			self.log.error("审批经理审批失败！")
			raise AssertionError('审批经理审批失败!')
		else:
			self.log.info("审批经理审批通过成功！")
			self.get_next_user(page, self.apply_code)
		
		if amount > 1500000 & amount <= 2000000:
			# 下一个处理人重新登录
			page = Login(self.next_user_id)
			
			# 风控总监
			res = self.PT.approval_to_review(page, self.apply_code, u'风控总监审批通过', 0)
			if not res:
				self.log.error("审风控总监审批失败！")
				raise AssertionError('审风控总监审批失败!')
			else:
				self.log.info("风控总监审批通过成功！")
				self.get_next_user(page, self.apply_code)
		
		if amount > 2000000:
			
			# 下一个处理人重新登录
			page = Login(self.next_user_id)
			
			# 风控总监
			res = self.PT.approval_to_review(page, self.apply_code, u'首席风控官审批通过', 0)
			if not res:
				self.log.error("首席风控官审批失败！")
				raise AssertionError('首席风控官审批失败!')
			else:
				self.log.info("首席风控官审批通过成功!")
				self.get_next_user(page, self.apply_code)
	
	def get_next_user(self, page, applycode):
		next_id = self.PM.process_monitor(page, applycode)
		if next_id is None:
			self.log.error("没有找到下一步处理人！")
			raise AssertionError('没有找到下一步处理人！')
		else:
			self.next_user_id = next_id
			self.log.info("下一步处理人:" + next_id)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_01_1person_contract(self):
		"""单人签约"""
		
		self.before_application_entry()
		self.before_risk_approval(200000)
		
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
		
		Cts.ContractSign(page, self.apply_code, rec_bank_info).execute_sign()
	
	def test_02_2Person_contract(self):
		"""双人签约"""
		
		# 贷款金额
		self.update_product_amount(400000)
		self.before_application_entry()
		self.before_risk_approval(400000)
		
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
		
		Cts.ContractSign(page, self.apply_code, rec_bank_info, 2)
	
	def test_03_3Person_contract(self):
		"""三人签约"""
		# 贷款金额
		self.update_product_amount(600000)
		self.before_application_entry()
		self.before_risk_approval(600000)
		
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
		
		Cts.ContractSign(page, self.apply_code, rec_bank_info, 3)
	
	def test_04_4Person_contract(self):
		"""四人签约"""
		
		# 贷款金额
		self.update_product_amount(800000)
		self.before_application_entry()
		self.before_risk_approval(800000)
		
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
		
		Cts.ContractSign(page, self.apply_code, rec_bank_info, 4).execute_sign()
	
	def test_05_5Person_contract(self):
		"""五人签约"""
		
		# 贷款金额
		self.update_product_amount(1000000)
		self.before_application_entry()
		self.before_risk_approval(1000000)
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
		
		Cts.ContractSign(page, self.apply_code, rec_bank_info, 5).execute_sign()
	
	def test_06_6Person_contract(self):
		"""六人签约"""
		
		# 贷款金额
		self.update_product_amount(1200000)
		self.before_application_entry()
		self.before_risk_approval(1200000)
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
		
		Cts.ContractSign(page, self.apply_code, rec_bank_info, 6).execute_sign()
	
	def test_07_7Person_contract(self):
		"""七人签约"""
		
		# 贷款金额
		self.update_product_amount(1400000)
		self.before_application_entry()
		self.before_risk_approval(1400000)
		
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
		
		Cts.ContractSign(page, self.apply_code, rec_bank_info, 7).execute_sign()
	
	def test_08_10Person_contract(self):
		"""10人签约"""
		
		# 贷款金额
		self.update_product_amount(2000000)
		self.before_application_entry()
		self.before_risk_approval(2000000)
		
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
		
		res = Cts.ContractSign(page, self.apply_code, rec_bank_info, 10)
		res.execute_sign()
	
	def test_09_20Person_contract(self):
		"""20人签约
		"""
		
		# 贷款金额
		self.update_product_amount(4000000)
		self.before_application_entry()
		self.before_risk_approval(4000000)
		
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
		
		res = Cts.ContractSign(page, self.apply_code, rec_bank_info, 20)
		res.execute_sign()
