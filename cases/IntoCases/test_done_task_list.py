import unittest

from com import base, login, custom


class DoneList(unittest.TestCase, base.Base):
	"""已处理任务"""
	
	def setUp(self):
		self.env_file = "env.json"
		self.data_file = "data_xhd.json"
		base.Base.__init__(self, self.env_file, self.data_file)
	
	def tearDown(self):
		self.page.driver.quit()
	
	def test_01_query_done_list(self):
		"""查询已处理任务列表"""
		
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
		
		applycode = self.AQ.get_applycode(self.page, self.cust_name)
		if applycode:
			self.apply_code = applycode
			self.log.info("申请件查询完成")
			print("applycode:" + self.apply_code)
		# 流程监控
		result = self.PM.process_monitor(self.page, self.apply_code)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		# 审批
		page = login.Login(self.next_user_id)
		# 审批审核
		self.PT.approval_to_review(page, self.apply_code, u'分公司主管同意审批', 0, True)
		self.DL.query_done_list(page, self.apply_code)
		page.driver.quit()
