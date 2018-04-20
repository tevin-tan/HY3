# coding:utf-8
import datetime
import time
import unittest

from cases import SET, v_l
from com import common, base, custom, database
from com.login import Login
from com.pobj.ContractSign import ContractSign as Cts


class PartRaise(unittest.TestCase, base.Base, SET):
	"""部分请款募资"""

	def setUp(self):
		self.env_file = "env.json"
		self.data_file = "data_cwd.json"
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

	def test_01_part_receipt_director_approval(self):
		"""400000元部分请款，回执分公司主管审批"""

		# ---------------------------------------------------------------------------------
		#                   1. 申请录入
		# ---------------------------------------------------------------------------------
		self.case_name = custom.get_current_function_name()
		self.update_product_amount(400000)

		# 1 客户信息-业务基本信息
		if self.HAE.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")

		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.HAE.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])

		# 3 物业信息
		self.HAE.input_all_bbi_property_info(
			self.page, self.data['applyPropertyInfoVo'][0],
			self.data['applyCustCreditInfoVo'][0],
			self.cust_name
			)
		# 提交
		self.HAE.submit(self.page)
		self.log.info("申请件录入完成提交")

		apply_code = self.AQ.get_applycode(self.page, self.cust_name)
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
			# "高级审批经理审批"
			]

		for e in list_mark:
			res = self.PT.approval_to_review(page, apply_code, e, 0)
			self.risk_approval_result(res, e, page, apply_code)
			# 下一个处理人重新登录
			page = Login(self.next_user_id)
		
		if self.next_user_id is self.senior_manager:
			res = self.PT.approval_to_review(page, apply_code, '高级审批经理', 0)
			self.risk_approval_result(res, '高级审批经理', page, apply_code)
		else:
			# -----------------------------------------------------------------------------
			# 	                        3. 合同打印
			# -----------------------------------------------------------------------------
			
			# 两个人签约
			rc = Cts.ContractSign(page, self.apply_code, self.rec_bank_info, 2)
			res = rc.execute_enter_borroers_bank_info()
			if res:
				rc.contract_submit()
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
			res = self.WM.authority_card_transact_2(page, self.apply_code, 1, self.env)
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
			page = Login(self.next_user_id)
			rec = self.PT.receipt_return(page, self.apply_code)
			if not rec:
				self.log.error("回执分公司主管审批失败")
				raise ValueError('失败')
			else:
				self.log.info("回执分公司主管审批通过")
				self.next_user_id = common.get_next_user(page, self.apply_code)

	def test_02_part_receipt_manage_approval(self):
		"""回执分公司经理审批"""

		self.test_01_part_receipt_director_approval()
		self.case_name = custom.get_current_function_name()
		page = Login(self.next_user_id)
		rec = self.PT.receipt_return(page, self.apply_code)
		if not rec:
			self.log.error("回执审批经理审批失败")
			raise ValueError('失败')
		else:
			self.log.info("回执审批经理审批通过")
			self.next_user_id = common.get_next_user(page, self.apply_code)

	def test_03_receipt_first_approval(self):
		"""第一次回执放款申请"""
		self.test_02_part_receipt_manage_approval()
		self.case_name = custom.get_current_function_name()
		page = Login(self.next_user_id)
		rec = self.PT.receipt_return(page, self.apply_code)
		if not rec:
			self.log.error("第一次回执放款申请失败")
			raise ValueError('失败')
		else:
			self.log.info("第一次回执放款申请通过")
			self.next_user_id = common.get_next_user(page, self.apply_code)

	def test_04_part_finace_transact(self):
		"""部分请款-财务办理"""

		# 权证请款
		self.test_03_receipt_first_approval()
		self.case_name = custom.get_current_function_name()
		# 业务助理登录
		page = Login(self.company["business_assistant"]["user"])
		rs = self.FA.finace_transact(page, self.apply_code)
		if not rs:
			self.log.error("财务办理失败")
			raise AssertionError('财务办理失败')
		else:
			self.log.info("财务办理结束！")
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code, 1)

	def test_05_part_finace_branch_manage_aproval(self):
		"""财务分公司经理审批"""
		remark = u"财务分公司经理审批"

		self.test_04_part_finace_transact()
		self.case_name = custom.get_current_function_name()
		page = Login(self.next_user_id)
		result = self.FA.finace_approval(page, self.apply_code, remark)
		if not result:
			self.log.error("财务流程-分公司经理审批失败")
			raise AssertionError('财务流程-分公司经理审批失败')
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code, 1)

	def test_06_part_finace_approval_risk_control_manager(self):
		"""财务风控经理审批"""

		remark = u'风控经理审批'

		self.test_05_part_finace_branch_manage_aproval()
		self.case_name = custom.get_current_function_name()
		page = Login(self.next_user_id)
		result = self.FA.finace_approval(page, self.apply_code, remark)
		if not result:
			self.log.error("财务流程-风控经理审批出错")
			raise AssertionError('财务流程-风控经理审批出错')
		else:
			self.log.info("财务流程-风控经理审批完成")

		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code, 1)

	def test_07_part_finace_approval_financial_accounting(self):
		"""财务会计审批"""

		remark = u'财务会计审批'

		self.test_06_part_finace_approval_risk_control_manager()
		self.case_name = custom.get_current_function_name()
		page = Login(self.next_user_id)
		rs = self.FA.finace_approval(page, self.apply_code, remark)
		if not rs:
			self.log.error("财务流程-财务会计审批失败")
			raise AssertionError('财务流程-财务会计审批失败')
		else:
			self.log.info("财务流程-财务会计审批完成")

		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code, 1)

	def test_08_part_finace_approval_financial_manager(self):
		"""财务经理审批"""

		remark = u'财务经理审批'

		self.test_07_part_finace_approval_financial_accounting()
		self.case_name = custom.get_current_function_name()
		page = Login(self.next_user_id)
		res = self.FA.finace_approval(page, self.apply_code, remark)
		if not res:
			self.log.error("财务流程-财务经理审批失败")
			raise AssertionError('财务流程-财务经理审批失败')
		else:
			self.log.info("财务流程-财务经理审批完成")
			page.driver.quit()

	def test_09_part_funds_raise(self):
		"""资金主管募资审批"""

		remark = u'资金主管审批'

		self.test_08_part_finace_approval_financial_manager()
		self.case_name = custom.get_current_function_name()
		page = Login(self.treasurer)
		res = self.RA.funds_raise(page, self.apply_code, remark)
		if not res:
			self.log.error("募资-资金主管审批失败")
			raise AssertionError('募资-资金主管审批失败')
		else:
			self.log.info("募资-资金主管审批完成!")
			page.driver.quit()

	def test_10_part_authority_card_second_deal(self):
		"""第二次权证办理"""
		self.test_09_part_funds_raise()
		self.case_name = custom.get_current_function_name()
		page = Login(self.company["authority_member"]["user"])

		# 修改数据库，将第一次请款修改为放款成功，然后才能发起第二次权证请款，否则第二次权证办理不能跟提交
		db = database.DB()

		sql_1 = "UPDATE house_common_loan_info t SET t.pay_date=sysdate, t.status='LOAN_PASS' \
		WHERE t.apply_id= (SELECT t.apply_id FROM house_apply_info t \
		WHERE t.apply_code =" + "'" + self.apply_code + "'" + ")"

		contract_no = self.apply_code + '-3-02-1'

		sql_2 = "UPDATE house_funds_info t SET t.Funds_Status = 21  \
		WHERE t.apply_id = (SELECT t.apply_id FROM house_apply_info t \
		WHERE t.apply_code = " + "'" + self.apply_code + "'" + ")" + "AND CONTRACT_NO =" + "'" + contract_no + "'"

		db.sql_execute(sql_1)
		db.sql_execute(sql_2)
		db.sql_commit()
		time.sleep(3)

		# 权证员上传权证信息
		res = self.WM.authority_card_transact_2(page, self.apply_code, 2, self.env)
		if not res:
			self.log.error("上传权证资料失败")
			raise ValueError("上传权证资料失败")
		else:
			self.log.info("权证办理完成")
			self.next_user_id = common.get_next_user(page, self.apply_code)

	def test_11_part_warrent_request_money(self):
		"""第二次权证请款"""

		self.test_10_part_authority_card_second_deal()
		self.case_name = custom.get_current_function_name()
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		# 部分请款
		res = self.PT.part_warrant_apply(page, self.apply_code, 1)
		if not res:
			self.log.error("权证请款失败！")
			raise ValueError('权证请款失败！')
		else:
			self.log.info("完成权证请款")
			self.next_user_id = common.get_next_user(page, self.apply_code)

	def test_12_part_finace_transact_second(self):
		"""第二次财务办理"""

		self.test_11_part_warrent_request_money()
		self.case_name = custom.get_current_function_name()
		# 业务助理登录
		page = Login(self.company["business_assistant"]["user"])
		rs = self.FA.finace_transact(page, self.apply_code)
		if not rs:
			self.log.error("财务办理失败")
			raise AssertionError('财务办理失败')
		else:
			self.log.info("财务办理结束！")
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code, 2)

	def test_13_part_finace_branch_manage_aproval_second(self):
		"""第二次财务分公司主管审批"""
		remark = u"财务分公司经理审批"

		self.test_12_part_finace_transact_second()
		self.case_name = custom.get_current_function_name()
		page = Login(self.next_user_id)
		result = self.FA.finace_approval(page, self.apply_code, remark)
		if not result:
			self.log.error("财务流程-分公司经理审批失败")
			raise AssertionError('财务流程-分公司经理审批失败')
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code, 2)

	def test_14_part_finace_approval_risk_control_manager(self):
		"""第二次财务风控经理审批"""
		remark = u'风控经理审批'

		self.test_13_part_finace_branch_manage_aproval_second()
		self.case_name = custom.get_current_function_name()
		page = Login(self.next_user_id)
		result = self.FA.finace_approval(page, self.apply_code, remark)
		if not result:
			self.log.error("财务流程-风控经理审批出错")
			raise AssertionError('财务流程-风控经理审批出错')
		else:
			self.log.info("财务流程-风控经理审批完成")

		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code, 2)

	def test_15_part_finace_approval_financial_accounting_second(self):
		"""第二次财务会计审批"""

		remark = u'财务会计审批'

		self.test_14_part_finace_approval_risk_control_manager()
		self.case_name = custom.get_current_function_name()
		page = Login(self.next_user_id)
		rs = self.FA.finace_approval(page, self.apply_code, remark)
		if not rs:
			self.log.error("财务流程-财务会计审批失败")
			raise AssertionError('财务流程-财务会计审批失败')
		else:
			self.log.info("财务流程-财务会计审批完成")

		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code, 2)

	def test_16_finace_approval_financial_manager_second(self):
		"""财务经理审批"""

		remark = u'财务经理审批'

		self.test_15_part_finace_approval_financial_accounting_second()
		self.case_name = custom.get_current_function_name()
		page = Login(self.next_user_id)
		res = self.FA.finace_approval(page, self.apply_code, remark)
		if not res:
			self.log.error("财务流程-财务经理审批失败")
			raise AssertionError('财务流程-财务经理审批失败')
		else:
			self.log.info("财务流程-财务经理审批完成")
			page.driver.quit()

	def test_17_part_funds_raise_second(self):
		"""第二次募资发起"""

		remark = u'资金主管审批'

		self.test_16_finace_approval_financial_manager_second()
		self.case_name = custom.get_current_function_name()
		page = Login(self.treasurer)
		res = self.RA.funds_raise(page, self.apply_code, remark)
		if not res:
			self.log.error("募资-资金主管审批失败")
			raise AssertionError('募资-资金主管审批失败')
		else:
			self.log.info("募资-资金主管审批完成!")
			self.page.driver.quit()
