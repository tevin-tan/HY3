import datetime
import time
import unittest

from cases import SET, v_l
from com import base, login, custom


class DoneList(unittest.TestCase, base.Base, SET):
	"""已处理任务"""
	
	def setUp(self):
		self.env_file = "env.json"
		self.data_file = "data_xhd.json"
		base.Base.__init__(self, self.env_file, self.data_file)
		SET.__init__(self)
		self.se = SET()
		self.se.start_run()
	
	def tearDown(self):
		self.end_time = time.clock()
		self.case_using_time(self.begin_time, self.end_time)
		print(self.using_time)
		v_l.append({
			"name": self.case_name,
			"apply_code": self.apply_code,
			"result": self.run_result,
			"u_time": self.using_time,
			"s_time": self.s_time,
			"e_time": str(datetime.datetime.now()).split('.')[0]
			})
		self.se.end_run(v_l)
		self.page.driver.quit()
	
	def test_01_query_done_list(self):
		"""查询已处理任务列表"""
		self.case_name = custom.get_current_function_name()
		# 贷款产品信息
		custom.print_product_info(self.product_info)
		
		try:
			# 1 客户信息-业务基本信息
			if self.HAE.input_customer_base_info(self.page, self.data['applyVo']):
				self.log.info("录入基本信息完成")
			
			# 2 客户基本信息 - 借款人/共贷人/担保人信息
			self.HAE.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
			
			# 3 物业信息
			self.HAE.input_all_bbi_property_info(
					self.page,
					self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0],
				self.cust_name)
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
			if result != None:
				self.next_user_id = result
				self.log.info("完成流程监控查询")
				self.page.driver.quit()
			else:
				self.run_result = False
				self.log.error("流程监控查询出错！")
				raise AssertionError('流程监控查询出错！')
			
			# 审批
			page = login.Login(self.next_user_id)
			# 审批审核
			self.PT.approval_to_review(page, self.apply_code, u'分公司主管同意审批', 0, True)
			self.DL.query_done_list(page, self.apply_code)
			page.driver.quit()
		except Exception as e:
			self.run_result = False
			raise e
