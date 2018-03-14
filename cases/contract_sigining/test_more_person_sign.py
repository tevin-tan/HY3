# coding:utf-8

import unittest
from com import common, base
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
		
		self.before_contract_sign()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 签约
		common.make_signing(page, self.apply_code, self.rec_bank_info)
		self.log.info("签约完成")
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code)
	
	def test_two_person_sign(self):
		"""两人签约"""
		
		# 修改贷款金额
		self.update_product_amount(400000)
		self.before_contract_sign()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 两个人签约
		res = common.make_signing(page, self.apply_code, self.rec_bank_info, 2)
		if res:
			self.log.info("合同打印完成！")
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code)
	
	def test_03_three_person_sign(self):
		"""三人签约"""
		
		# 修改贷款金额
		self.update_product_amount(600000)
		self.before_contract_sign()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 两个人签约
		common.make_signing(page, self.apply_code, self.rec_bank_info, 3)
		self.log.info("合同打印完成")
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code)
	
	def test_04_four_person_sign(self):
		"""四人签约"""
		
		# ---------------------------------------------------------------------------------
		#                   1. 申请录入
		# ---------------------------------------------------------------------------------
		
		# 贷款金额
		self.update_product_amount(800000)
		self.before_contract_sign()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 两个人签约
		common.make_signing(page, self.apply_code, self.rec_bank_info, 4)
		self.log.info("合同打印完成")
		
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code)
	
	def test_05_five_person_sign(self):
		"""五人签约"""
		
		# 贷款金额
		self.update_product_amount(1000000)
		self.before_contract_sign()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 5个人签约
		common.make_signing(page, self.apply_code, self.rec_bank_info, 5)
		self.log.info("合同打印完成")
		
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code)
