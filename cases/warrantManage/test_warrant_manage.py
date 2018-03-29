# coding:utf-8

import datetime
import time
import unittest

from cases import SET, v_l
from com import common, base, custom
from com.login import Login
from com.pobj.ContractSign import ContractSign


class WarrantManage(unittest.TestCase, base.Base, SET):
	"""权证请款流程"""

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

	def test_01_warrantManage_original(self):
		"""权证原件请款"""
		self.case_name = custom.get_current_function_name()
		try:
			self.update_product_amount(2000000)
			# 1. 申请录入
			self.before_application_entry()
			# 2. 风控审批
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
				res = self.PT.approval_to_review(page, self.apply_code, e, 0)
				self.risk_approval_result(res, e, page, self.apply_code)
				# 下一个处理人重新登录
				page = Login(self.next_user_id)

			# -----------------------------------------------------------------------------
			# 	                        3. 合同打印
			# -----------------------------------------------------------------------------

			rc = ContractSign.ContractSign(page, self.apply_code, self.rec_bank_info, 10)
			res = rc.execute_sign()
			if res:
				rc.contract_submit()

			self.next_user_id = common.get_next_user(page, self.apply_code)

			# 下一个处理人重新登录
			page = Login(self.next_user_id)

			# 合规审查
			res = self.PT.compliance_audit(page, self.apply_code)
			if res:
				self.log.info("合规审批结束")
				page.driver.quit()
			else:
				self.run_result = False
				self.log.error("合规审查失败")
				raise ValueError("合规审查失败")

			# 权证办理
			# 权证员登录
			page = Login(self.company["authority_member"]["user"])
			# 权证员上传权证信息
			self.WM.authority_card_transact(page, self.apply_code, self.env)
			self.next_user_id = common.get_next_user(page, self.apply_code)

			page = Login(self.next_user_id)
			# 权证请款
			res = self.WM.warrant_apply(page, self.apply_code)
			if not res:
				self.run_result = False
				self.log.error("权证请款失败！")
				raise ValueError('权证请款失败！')
			else:
				self.log.info("完成权证请款")
				self.next_user_id = common.get_next_user(page, self.apply_code)
		except Exception as e:
			self.run_result = False
			raise e

	def test_02_warrantManage_part(self):
		"""部分权证请款"""
		self.case_name = custom.get_current_function_name()
		try:
			self.update_product_amount(400000)
			self.before_contract_sign()

			# -----------------------------------------------------------------------------
			# 	                        3. 合同打印
			# -----------------------------------------------------------------------------
			# next transcat person
			self.next_user_id = common.get_next_user(self.page, self.apply_code)

			# 下一个处理人重新登录
			page = Login(self.next_user_id)

			# 两个人签约
			rc = ContractSign.ContractSign(page, self.apply_code, self.rec_bank_info, 2)
			res = rc.execute_sign()
			if res:
				rc.contract_submit()
				self.log.info("合同打印完成！")
				# 查看下一步处理人
				self.next_user_id = common.get_next_user(page, self.apply_code)

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
				self.run_result = False
				self.log.error("合规审查失败")
				raise ValueError("合规审查失败")

			# -----------------------------------------------------------------------------
			#                                权证办理
			# -----------------------------------------------------------------------------
			page = Login(self.company["authority_member"]["user"])
			# 权证员上传权证信息
			res = self.WM.authority_card_transact(page, self.apply_code, self.env)
			if not res:
				self.run_result = False
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
				self.run_result = False
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
					self.run_result = False
					self.log.error(i + "失败")
					raise ValueError(i + '失败')
				else:
					self.log.info(i + "通过")
					self.next_user_id = common.get_next_user(page, self.apply_code)
		except Exception as e:
			self.run_result = False
			raise e
