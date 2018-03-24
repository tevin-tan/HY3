# coding:utf-8
"""
	Desc: 特批
	Author: tsx
	Date: 2018-1-24
"""

import datetime
import time
import unittest

from cases import SET, v_l
from com import custom, base
from com.login import Login


class SPA(unittest.TestCase, base.Base, SET):
	"""特批"""
	
	def setUp(self):
		self.env_file = "env.json"
		self.data_file = "data_xhd.json"
		base.Base.__init__(self, self.env_file, self.data_file)
		SET.__init__(self)
		self.se = SET()
		self.se.start_run()
	
	def get_next_user(self, page, applycode):
		next_id = self.PM.process_monitor(page, applycode)
		if next_id is None:
			self.log.error("没有找到下一步处理人！")
			raise AssertionError('没有找到下一步处理人！')
		else:
			self.next_user_id = next_id
			self.log.info("下一步处理人:" + next_id)
			# 当前用户退出系统
			page.driver.quit()
	
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
	
	def test_01_region_special_approval(self):
		"""区域李伟波特批"""
		self.case_name = custom.get_current_function_name()
		custom.print_product_info(self.product_info)
		try:
			self.before_application_entry()
			"""
				------------------------------------------------------------
									2. 风控审批-区域特批
				------------------------------------------------------------
			"""
			# 下一个处理人重新登录
			page = Login(self.next_user_id)
			
			# 分公司主管审批
			res = self.PT.approval_to_review(page, self.apply_code, u'分公司主管审批通过', 0)
			if not res:
				self.run_result = False
				self.log.error("审批失败")
				raise AssertionError('审批失败')
			else:
				self.log.info(u'分公司主管审批通过！')
				self.get_next_user(page, self.apply_code)
			
			# 下一个处理人重新登录
			page = Login(self.next_user_id)
			
			# 分公司经理审批通过
			res = self.PT.approval_to_review(page, self.apply_code, u'分公司经理回退到申请录入', 0)
			if not res:
				self.run_result = False
				self.log.error("审批失败")
				raise AssertionError('审批失败')
			else:
				self.log.info(u'分公司经理审批通过！')
				self.get_next_user(page, self.apply_code)
			
			# 下一个处理人重新登录
			page = Login(self.next_user_id)
			
			if self.next_user_id != 'xn004754':
				# 区域特批
				res = self.PT.approval_to_review(page, self.apply_code, u'区域审批经理审批', 0)
				if not res:
					self.run_result = False
					self.log.error("区域审批经理审批失败")
					raise AssertionError('区域审批经理审批失败')
				else:
					self.log.info(u'区域审批经理审批成功!')
					self.get_next_user(page, self.apply_code)
			else:
				r = self.PT.special_approval(page, self.apply_code, u'区域特批')
				if not r:
					self.run_result = False
					self.log.error('区域特批出错！')
					raise AssertionError('区域特批出错！')
				else:
					self.log.info('区域特批通过！')
					page.driver.quit()
		except Exception as e:
			self.run_result = False
			raise e
	
	def test_02_manage_special_approval(self):
		"""高级经理特批"""
		try:
			self.test_01_region_special_approval()
			self.case_name = custom.get_current_function_name()
			page = Login(self.next_user_id)
			r = self.PT.special_approval(page, self.apply_code, u'高级经理特批')
			if not r:
				self.run_result = False
				self.log.error('高级经理特批出错！')
				raise AssertionError('高级经理特批出错！')
			else:
				self.log.info('高级经理特批通过！')
				self.get_next_user(page, self.apply_code)
				page.driver.quit()
		except Exception as e:
			self.run_result = False
			raise e
	
	def test_03_risk_director_special_approval(self):
		"""区域特批，风控总监特批终审"""
		
		try:
			self.test_02_manage_special_approval()
			self.case_name = custom.get_current_function_name()
			page = Login(self.next_user_id)
			r = self.PT.special_approval(page, self.apply_code, u'风控总监特批')
			if not r:
				self.log.error('风控总监特批出错！')
				raise AssertionError('风控总监特批出错！')
			else:
				self.log.info('风控总监特批通过！')
				self.get_next_user(page, self.apply_code)
				page.driver.quit()
		except Exception as e:
			self.run_result = False
			raise e
