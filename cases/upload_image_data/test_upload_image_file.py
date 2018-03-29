# coding: utf-8
import datetime
import time
import unittest

from cases import SET, v_l
from com import common, base, custom
from com.login import Login
from com.pobj.ContractSign import ContractSign


class UploadImageData(unittest.TestCase, base.Base, SET):
	"""影响资料上传"""

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
			"result": self.run_result,
			"u_time": self.using_time,
			"s_time": self.s_time,
			"e_time": str(datetime.datetime.now()).split('.')[0]
		})
		self.se.end_run(v_l)
		self.page.driver.quit()

	def test_01_upload_image(self):
		"""房贷专员:上传权证资料"""
		self.case_name = custom.get_current_function_name()
		try:
			custom.print_product_info(self.product_info)

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
			# 上传影像资料
			res = self.HAE.upload_image_file(self.page, self.exe, self.image)
			if res:
				self.log.info("上传影像资料成功！")
			else:
				self.run_result = False
				raise res

			# 提交
			self.HAE.submit(self.page)
			self.log.info("申请件录入完成提交")

			apply_code = self.AQ.get_applycode(self.page, self.cust_name)
			if apply_code:
				self.apply_code = apply_code
				self.log.info("申请件查询完成")
				print("apply_code:" + self.apply_code)
		except Exception as e:
			self.run_result = False
			raise e

	def test_02_upload_image_delete(self):
		"""房贷专员删除权证资料"""
		self.skipTest("图片定位困难")
		custom.print_product_info(self.product_info)
		custom.print_person_info(self.person_info)

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
		# 删除影像资料
		res = self.HAE.upload_image_file(self.page, self.exe, self.image, True)
		if res:
			self.log.info("上传影像资料成功！")
		else:
			raise res

		# 提交
		self.HAE.submit(self.page)
		self.log.info("申请件录入完成提交")

		apply_code = self.AQ.get_applycode(self.page, self.cust_name)
		if apply_code:
			self.apply_code = apply_code
			self.log.info("申请件查询完成")
			print("apply_code:" + self.apply_code)

	def test_03_upload_many_image(self):
		"""专员-上传多张权证资料"""
		self.case_name = custom.get_current_function_name()
		try:
			custom.print_product_info(self.product_info)
			custom.print_person_info(self.person_info)

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
			# 上传影像资料

			for i in range(0, 5):
				res = self.HAE.upload_image_file(self.page, self.exe, self.image)
				if res:
					self.log.info("上传第" + str(i) + "张影像资料成功！")
				else:
					self.run_result = False
					raise res

			# 提交
			self.HAE.submit(self.page)
			self.log.info("申请件录入完成提交")

			apply_code = self.AQ.get_applycode(self.page, self.cust_name)
			if apply_code:
				self.apply_code = apply_code
				self.log.info("申请件查询完成")
				print("apply_code:" + self.apply_code)
		except Exception as e:
			self.run_result = False
			raise e

	def test_04_branch_director_upload_image(self):
		"""分公司主管:上传权证资料"""

		try:
			self.case_name = custom.get_current_function_name()
			custom.print_product_info(self.product_info)
			custom.print_person_info(self.person_info)

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

			self.next_user_id = common.get_next_user(self.page, self.apply_code)
			# Login
			page = Login(self.next_user_id)
			res = self.PT.approval_to_review(page, self.apply_code, u'分公司主管同意审批', 0, True)
			if not res:
				self.run_result = False
				self.log.error("can't find applycode")
				raise ValueError("can't find applycode")
			else:
				self.log.info("风控审批-分公司主管审批结束")
				self.next_user_id = common.get_next_user(page, self.apply_code)
		except Exception as e:
			self.run_result = False
			raise e

	def test_05_branch_manage_upload_image(self):
		"""分公司经理-上传权证资料"""

		try:
			self.test_04_branch_director_upload_image()
			self.case_name = custom.get_current_function_name()

			page = Login(self.next_user_id)
			# 审批并上传权证资料
			res = self.PT.approval_to_review(page, self.apply_code, u'分公司经理同意审批', 0, True)
			if not res:
				self.run_result = False
				self.log.error("can't find applycode")
				raise ValueError("can't find applycode")
			else:
				self.log.info("风控审批-分公司经理审批结束")
				self.next_user_id = common.get_next_user(page, self.apply_code)
		except Exception as e:
			self.run_result = False
			raise e

	def test_06_area_manage_upload_image(self):
		"""区域经理-上传权证资料"""
		self.case_name = custom.get_current_function_name()
		try:
			self.test_05_branch_manage_upload_image()
			self.case_name = custom.get_current_function_name()
			# 区域审批审核，并上传资料
			page = Login(self.next_user_id)
			res = self.PT.approval_to_review(page, self.apply_code, u'区域经理同意审批', 0, True)
			if not res:
				self.run_result = False
				self.log.error("can't find applyCode")
				raise ValueError("can't find applyCode")
			else:
				self.log.info("风控审批-区域经理审批结束")
				self.next_user_id = common.get_next_user(page, self.apply_code)
		except Exception as e:
			self.run_result = False
			raise e

	def test_07_senior_manager_upload_image(self):
		"""高级审批经理-上传权证资料"""

		try:
			self.test_06_area_manage_upload_image()
			self.case_name = custom.get_current_function_name()
			# 高级审批审核，并上传资料
			page = Login(self.next_user_id)
			res = self.PT.approval_to_review(page, self.apply_code, u'高级经理同意审批', 0, True)
			if not res:
				self.log.error("can't find applyCode")
				raise ValueError("can't find applyCode")
			else:
				self.log.info("风控审批-高级经理审批结束")
				self.next_user_id = common.get_next_user(page, self.apply_code)
		except Exception as e:
			self.run_result = False
			raise e

	def test_08_compliance_Officer_original(self):
		"""合规审查员上传影像资料"""

		try:
			self.case_name = custom.get_current_function_name()
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
				self.page, self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0],
				self.cust_name)
			# 提交
			self.HAE.submit(self.page)
			self.log.info("申请件录入完成提交")

			apply_code = self.AQ.get_applycode(self.page, self.cust_name)
			if apply_code:
				self.apply_code = apply_code
				self.log.info("申请件查询完成")
				print("apply_code:" + self.apply_code)
			# 流程监控
			self.next_user_id = common.get_next_user(self.page, self.apply_code)

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

			# 下一个处理人重新登录
			page = Login(self.next_user_id)

			res = ContractSign.ContractSign(page, self.apply_code, self.rec_bank_info, 10)
			res.execute_sign()
			res.contract_submit()

			self.next_user_id = common.get_next_user(page, self.apply_code)

			# 合规审查
			# 下一个处理人重新登录
			page = Login(self.next_user_id)

			# 合规审查, 并上传影像资料
			res = self.PT.compliance_audit(page, self.apply_code, True)
			if res:
				self.log.info("合规审批结束")
				page.driver.quit()
			else:
				self.run_result = False
				self.log.error("合规审查失败")
				raise ValueError("合规审查失败")
		except Exception as e:
			self.run_result = False
			raise e
