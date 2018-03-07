# coding: utf-8
import unittest
import json
import os
from com import common, contract
from com.login import Login
from com.custom import Log, enviroment_change, print_env


class UploadImageData(unittest.TestCase):
	"""影响资料上传"""
	
	def setUp(self):
		self.log = Log()
		try:
			import config
			rdir = config.__path__[0]
			config_env = os.path.join(rdir, 'env.json')
			print("config_env:" + config_env)
			with open(config_env, 'r', encoding='utf-8') as f:
				self.da = json.load(f)
				self.number = self.da["number"]
				self.env = self.da["enviroment"]
				self.exe = self.da["upload_exe"]
				self.image = self.da["image_jpg"]
			f.close()
			filename = "data_cwd.json"
			data, company = enviroment_change(filename, self.number, self.env)
			self.page = Login()
			
			# 录入的源数据
			self.data = data
			
			# 分公司选择
			self.company = company
			print_env(self.env, self.company)
			self.next_user_id = ""
		except Exception as e:
			self.log.error('load config error:', str(e))
			raise e
	
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
	
	def test_01_upload_image(self):
		"""房贷专员:上传权证资料"""
		
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.custName = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])[1]
		
		# 3 物业信息
		common.input_cwd_bbi_property_info(
				self.page, self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0]
				)
		# 上传影像资料
		res = common.upload_image_file(self.page, self.exe, self.image)
		if res:
			self.log.info("上传影像资料成功！")
		else:
			raise (res)
		
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		apply_code = common.get_applycode(self.page, self.custName)
		if apply_code:
			self.apply_code = apply_code
			self.log.info("申请件查询完成")
			print("apply_code:" + self.apply_code)
	
	def test_02_upload_image_delete(self):
		"""房贷专员删除权证资料"""
		
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.custName = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])[1]
		
		# 3 物业信息
		common.input_cwd_bbi_property_info(
				self.page, self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0]
				)
		# 删除影像资料
		res = common.upload_image_file(self.page, self.exe, self.image, True)
		if res:
			self.log.info("上传影像资料成功！")
		else:
			raise (res)
		
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		apply_code = common.get_applycode(self.page, self.custName)
		if apply_code:
			self.apply_code = apply_code
			self.log.info("申请件查询完成")
			print("apply_code:" + self.apply_code)
	
	def test_03_upload_many_image(self):
		"""专员-上传多张权证资料"""
		
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.custName = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])[1]
		
		# 3 物业信息
		common.input_cwd_bbi_property_info(
				self.page, self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0]
				)
		# 上传影像资料
		
		for i in range(0, 5):
			res = common.upload_image_file(self.page, self.exe, self.image)
			if res:
				self.log.info("上传第" + str(i) + "张影像资料成功！")
			else:
				raise (res)
		
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		apply_code = common.get_applycode(self.page, self.custName)
		if apply_code:
			self.apply_code = apply_code
			self.log.info("申请件查询完成")
			print("apply_code:" + self.apply_code)
	
	def test_04_branch_director_upload_image(self):
		"""分公司主管:上传权证资料"""
		
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.custName = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])[1]
		
		# 3 物业信息
		common.input_cwd_bbi_property_info(
				self.page, self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0]
				)
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		apply_code = common.get_applycode(self.page, self.custName)
		if apply_code:
			self.apply_code = apply_code
			self.log.info("申请件查询完成")
			print("apply_code:" + self.apply_code)
		
		self.next_user_id = common.get_next_user(self.page, self.apply_code)
		# Login
		page = Login(self.next_user_id)
		res = common.approval_to_review(page, self.apply_code, u'分公司主管同意审批', 0, True)
		if not res:
			self.log.error("can't find applycode")
			raise ValueError("can't find applycode")
		else:
			self.log.info("风控审批-分公司主管审批结束")
			self.next_user_id = common.get_next_user(page, self.apply_code)
	
	def test_05_branch_manage_upload_image(self):
		"""分公司经理-上传权证资料"""
		
		self.test_04_branch_director_upload_image()
		
		page = Login(self.next_user_id)
		# 审批并上传权证资料
		res = common.approval_to_review(page, self.apply_code, u'分公司经理同意审批', 0, True)
		if not res:
			self.log.error("can't find applycode")
			raise ValueError("can't find applycode")
		else:
			self.log.info("风控审批-分公司经理审批结束")
			self.next_user_id = common.get_next_user(page, self.apply_code)
	
	def test_06_area_manage_upload_image(self):
		"""区域经理-上传权证资料"""
		
		self.test_05_branch_manage_upload_image()
		
		# 区域审批审核，并上传资料
		page = Login(self.next_user_id)
		res = common.approval_to_review(page, self.apply_code, u'区域经理同意审批', 0, True)
		if not res:
			self.log.error("can't find applyCode")
			raise ValueError("can't find applyCode")
		else:
			self.log.info("风控审批-区域经理审批结束")
			self.next_user_id = common.get_next_user(page, self.apply_code)
	
	def test_07_senior_manager_upload_image(self):
		"""高级审批经理-上传权证资料"""
		
		self.test_06_area_manage_upload_image()
		
		# 高级审批审核，并上传资料
		page = Login(self.next_user_id)
		res = common.approval_to_review(page, self.apply_code, u'高级经理同意审批', 0, True)
		if not res:
			self.log.error("can't find applyCode")
			raise ValueError("can't find applyCode")
		else:
			self.log.info("风控审批-高级经理审批结束")
			self.next_user_id = common.get_next_user(page, self.apply_code)
	
	def test_08_compliance_Officer_original(self):
		"""合规审查员上传影像资料"""
		
		self.data['applyVo']['applyAmount'] = 2000000
		# ---------------------------------------------------------------------------------
		#                   1. 申请录入
		# ---------------------------------------------------------------------------------
		
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.custName = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])[1]
		
		# 3 物业信息
		common.input_cwd_bbi_property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		apply_code = common.get_applycode(self.page, self.custName)
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
			res = common.approval_to_review(page, apply_code, e, 0)
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
		
		res = contract.Contract(page, self.apply_code, rec_bank_info, 10)
		res.execute_sign()
		
		self.next_user_id = common.get_next_user(page, self.apply_code)
		
		# 合规审查
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 合规审查
		res = common.compliance_audit(page, self.apply_code, True)
		if res:
			self.log.info("合规审批结束")
			page.driver.quit()
		else:
			self.log.error("合规审查失败")
			raise ValueError("合规审查失败")
