import datetime
import time
import unittest

from cases import SET, v_l
from com import base, custom
from com.login import Login
from com.pobj.ContractSign import ContractSign as Cts


class AddContract(unittest.TestCase, base.Base, SET):
	"""多借款人签约"""
	
	def setUp(self):
		
		self.env_file = "env.json"
		self.data_file = "data_eyt.json"
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
			"result": self.run_result,
			"u_time": self.using_time,
			"s_time": self.s_time,
			"e_time": str(datetime.datetime.now()).split('.')[0]
			})
		self.se.end_run(v_l)
		self.page.driver.quit()
	
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
		self.case_name = custom.get_current_function_name()
		try:
			self.before_contract_sign(200000)
			# self.case_name = custom.get_current_function_name()
			# 下一个处理人重新登录
			page = Login(self.next_user_id)
			
			rc = Cts.ContractSign(page, self.apply_code, self.rec_bank_info)
			res = rc.execute_sign()
			if res:
				rc.contract_submit()
		except Exception as e:
			self.run_result = False
			raise e
	
	def test_02_2Person_contract(self):
		"""双人签约"""
		try:
			# 贷款金额
			self.update_product_amount(400000)
			self.before_contract_sign(400000)
			self.case_name = custom.get_current_function_name()
			# 下一个处理人重新登录
			page = Login(self.next_user_id)
			
			Cts.ContractSign(page, self.apply_code, self.rec_bank_info, 2)
		except Exception as e:
			self.run_result = False
			raise e
	
	def test_03_3Person_contract(self):
		"""三人签约"""
		
		try:
			# 贷款金额
			self.update_product_amount(600000)
			self.before_contract_sign(600000)
			self.case_name = custom.get_current_function_name()
			# 下一个处理人重新登录
			page = Login(self.next_user_id)
			
			Cts.ContractSign(page, self.apply_code, self.rec_bank_info, 3)
		except Exception as e:
			self.run_result = False
			raise e
	
	def test_04_4Person_contract(self):
		"""四人签约"""
		
		try:
			# 贷款金额
			self.update_product_amount(800000)
			self.before_contract_sign(800000)
			self.case_name = custom.get_current_function_name()
			# 下一个处理人重新登录
			page = Login(self.next_user_id)
			
			Cts.ContractSign(page, self.apply_code, self.rec_bank_info, 4).execute_sign()
		except Exception as e:
			self.run_result = False
			raise e
	
	def test_05_5Person_contract(self):
		"""五人签约"""
		
		try:
			# 贷款金额
			self.update_product_amount(1000000)
			self.before_contract_sign(1000000)
			self.case_name = custom.get_current_function_name()
			# 下一个处理人重新登录
			page = Login(self.next_user_id)
			
			Cts.ContractSign(page, self.apply_code, self.rec_bank_info, 5).execute_sign()
		except Exception as e:
			self.run_result = False
			raise e
	
	def test_06_6Person_contract(self):
		"""六人签约"""
		
		try:
			# 贷款金额
			self.update_product_amount(1200000)
			self.before_contract_sign(1200000)
			self.case_name = custom.get_current_function_name()
			# 下一个处理人重新登录
			page = Login(self.next_user_id)
			
			Cts.ContractSign(page, self.apply_code, self.rec_bank_info, 6).execute_sign()
		except Exception as e:
			self.run_result = False
			raise e
	
	def test_07_7Person_contract(self):
		"""七人签约"""
		
		try:
			
			# 贷款金额
			self.update_product_amount(1400000)
			self.before_contract_sign(1400000)
			self.case_name = custom.get_current_function_name()
			# 下一个处理人重新登录
			page = Login(self.next_user_id)
			
			Cts.ContractSign(page, self.apply_code, self.rec_bank_info, 7).execute_sign()
		except Exception as e:
			self.run_result = False
			raise e
	
	def test_08_10Person_contract(self):
		"""10人签约"""
		
		try:
			# 贷款金额
			self.update_product_amount(2000000)
			self.before_contract_sign(2000000)
			self.case_name = custom.get_current_function_name()
			# 下一个处理人重新登录
			page = Login(self.next_user_id)
			
			res = Cts.ContractSign(page, self.apply_code, self.rec_bank_info, 10)
			res.execute_sign()
		except Exception as e:
			self.run_result = False
			raise e
	
	def test_09_20Person_contract(self):
		"""20人签约
		"""
		
		try:
			# 贷款金额
			self.update_product_amount(4000000)
			self.before_contract_sign(4000000)
			self.case_name = custom.get_current_function_name()
			# 下一个处理人重新登录
			page = Login(self.next_user_id)
			
			res = Cts.ContractSign(page, self.apply_code, self.rec_bank_info, 20)
			res.execute_sign()
		except Exception as e:
			self.run_result = False
			raise e
