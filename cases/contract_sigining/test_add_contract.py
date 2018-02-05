import unittest
import json
import os
from com import common
from com.login import Login
from com import custom, contract
from com.custom import Log, enviroment_change


class AddContract(unittest.TestCase):
	'''多借款人签约'''
	
	def setUp(self):
		try:
			import config
			rootdir = config.__path__[0]
			config_env = os.path.join(rootdir, 'env.json')
			print("config_env:" + config_env)
			with open(config_env, 'r', encoding='utf-8') as f:
				self.da = json.load(f)
				self.number = self.da["number"]
				self.env = self.da["enviroment"]
			f.close()
			filename = "data_cwd.json"
			data, company = enviroment_change(filename, self.number, self.env)
			self.page = Login()
			self.log = Log()
			
			# 录入的源数据
			self.data = data
			# 分公司选择
			self.company = company
			custom.print_env(self.env, self.company)
		
		except Exception as e:
			self.log.error('load config error:', str(e))
			raise e
	
	def tearDown(self):
		self.page.driver.quit()
	
	def get_next_user(self, page, applyCode):
		next_id = common.process_monitor(page, applyCode)
		if next_id is None:
			self.log.error("没有找到下一步处理人！")
			raise AssertionError('没有找到下一步处理人！')
		else:
			self.next_user_id = next_id
			self.log.info("下一步处理人:" + next_id)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_01_1person_contract(self):
		'''单人签约'''
		
		# ---------------------------------------------------------------------------------
		#                   1. 申请录入
		# ---------------------------------------------------------------------------------
		
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.custName = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])[1]
		
		# 3 物业信息
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成")
			print("applyCode:" + self.applyCode)
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		# ---------------------------------------------------------------------------------------
		# 	                        2. 风控审批流程
		# ---------------------------------------------------------------------------------------
		
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applyCode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司主管审批通过！")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = common.approval_to_review(page, applyCode, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司经理审批通过！")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = common.approval_to_review(page, applyCode, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise AssertionError('区域预复核审批失败！')
		else:
			self.log.info("区域预复核审批通过")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批经理审批通过
		res = common.approval_to_review(page, applyCode, u'审批经理审批通过', 0)
		if not res:
			self.log.error("审批经理审批失败！")
			raise AssertionError('审批经理审批失败!')
		else:
			self.log.info("审批经理审批通过成功！")
			self.get_next_user(page, applyCode)
		
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
		
		# 扣款银行信息
		rep_bank_info = dict(
				rep_name=u'习近平',
				rep_id_num='420101198201013526',
				rep_bank_code='6210302082441017886',
				rep_phone='13686467482',
				provice=u'湖南省',
				district=u'长沙',
				rep_bank_name=u'中国银行',
				rep_bank_branch_name=u'北京支行',
				)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		contract.Contract(page, self.applyCode, rec_bank_info).execute_sign()
	
	def test_02_2Person_contract(self):
		'''双人签约'''
		self.data['applyVo']['applyAmount'] = 400000
		# ---------------------------------------------------------------------------------
		#                   1. 申请录入
		# ---------------------------------------------------------------------------------
		
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.custName = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])[1]
		
		# 3 物业信息
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成")
			print("applyCode:" + self.applyCode)
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		# ---------------------------------------------------------------------------------------
		# 	                        2. 风控审批流程
		# ---------------------------------------------------------------------------------------
		
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applyCode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司主管审批通过！")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = common.approval_to_review(page, applyCode, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司经理审批通过！")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = common.approval_to_review(page, applyCode, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise AssertionError('区域预复核审批失败！')
		else:
			self.log.info("区域预复核审批通过")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批经理审批通过
		res = common.approval_to_review(page, applyCode, u'审批经理审批通过', 0)
		if not res:
			self.log.error("审批经理审批失败！")
			raise AssertionError('审批经理审批失败!')
		else:
			self.log.info("审批经理审批通过成功！")
			self.get_next_user(page, applyCode)
		
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
		
		# 扣款银行信息
		rep_bank_info = dict(
				rep_name=u'习近平',
				rep_id_num='420101198201013526',
				rep_bank_code='6210302082441017886',
				rep_phone='13686467482',
				provice=u'湖南省',
				district=u'长沙',
				rep_bank_name=u'中国银行',
				rep_bank_branch_name=u'北京支行',
				)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		contract.Contract(page, self.applyCode, rec_bank_info, 2)
	
	def test_03_3Person_contract(self):
		'''三人签约'''
		self.data['applyVo']['applyAmount'] = 600000
		
		# ---------------------------------------------------------------------------------
		#                   1. 申请录入
		# ---------------------------------------------------------------------------------
		
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.custName = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])[1]
		
		# 3 物业信息
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成")
			print("applyCode:" + self.applyCode)
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		# ---------------------------------------------------------------------------------------
		# 	                        2. 风控审批流程
		# ---------------------------------------------------------------------------------------
		
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applyCode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司主管审批通过！")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = common.approval_to_review(page, applyCode, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司经理审批通过！")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = common.approval_to_review(page, applyCode, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise AssertionError('区域预复核审批失败！')
		else:
			self.log.info("区域预复核审批通过")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批经理审批通过
		res = common.approval_to_review(page, applyCode, u'审批经理审批通过', 0)
		if not res:
			self.log.error("审批经理审批失败！")
			raise AssertionError('审批经理审批失败!')
		else:
			self.log.info("审批经理审批通过成功！")
			self.get_next_user(page, applyCode)
		
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
		
		# 扣款银行信息
		rep_bank_info = dict(
				rep_name=u'习近平',
				rep_id_num='420101198201013526',
				rep_bank_code='6210302082441017886',
				rep_phone='13686467482',
				provice=u'湖南省',
				district=u'长沙',
				rep_bank_name=u'中国银行',
				rep_bank_branch_name=u'北京支行',
				)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		contract.Contract(page, self.applyCode, rec_bank_info, 3)
	
	def test_04_4Person_contract(self):
		'''四人签约'''
		
		self.data['applyVo']['applyAmount'] = 800000
		# ---------------------------------------------------------------------------------
		#                   1. 申请录入
		# ---------------------------------------------------------------------------------
		
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.custName = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])[1]
		
		# 3 物业信息
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成")
			print("applyCode:" + self.applyCode)
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		# ---------------------------------------------------------------------------------------
		# 	                        2. 风控审批流程
		# ---------------------------------------------------------------------------------------
		
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applyCode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司主管审批通过！")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = common.approval_to_review(page, applyCode, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司经理审批通过！")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = common.approval_to_review(page, applyCode, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise AssertionError('区域预复核审批失败！')
		else:
			self.log.info("区域预复核审批通过")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批经理审批通过
		res = common.approval_to_review(page, applyCode, u'审批经理审批通过', 0)
		if not res:
			self.log.error("审批经理审批失败！")
			raise AssertionError('审批经理审批失败!')
		else:
			self.log.info("审批经理审批通过成功！")
			self.get_next_user(page, applyCode)
		
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
		
		# 扣款银行信息
		rep_bank_info = dict(
				rep_name=u'习近平',
				rep_id_num='420101198201013526',
				rep_bank_code='6210302082441017886',
				rep_phone='13686467482',
				provice=u'湖南省',
				district=u'长沙',
				rep_bank_name=u'中国银行',
				rep_bank_branch_name=u'北京支行',
				)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		contract.Contract(page, self.applyCode, rec_bank_info, 4).execute_sign()
	
	def test_05_5Person_contract(self):
		'''五人签约'''
		
		self.data['applyVo']['applyAmount'] = 1000000
		# ---------------------------------------------------------------------------------
		#                   1. 申请录入
		# ---------------------------------------------------------------------------------
		
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.custName = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])[1]
		
		# 3 物业信息
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成")
			print("applyCode:" + self.applyCode)
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		# ---------------------------------------------------------------------------------------
		# 	                        2. 风控审批流程
		# ---------------------------------------------------------------------------------------
		
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applyCode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司主管审批通过！")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = common.approval_to_review(page, applyCode, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司经理审批通过！")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = common.approval_to_review(page, applyCode, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise AssertionError('区域预复核审批失败！')
		else:
			self.log.info("区域预复核审批通过")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批经理审批通过
		res = common.approval_to_review(page, applyCode, u'审批经理审批通过', 0)
		if not res:
			self.log.error("审批经理审批失败！")
			raise AssertionError('审批经理审批失败!')
		else:
			self.log.info("审批经理审批通过成功！")
			self.get_next_user(page, applyCode)
		
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
		
		# 扣款银行信息
		rep_bank_info = dict(
				rep_name=u'习近平',
				rep_id_num='420101198201013526',
				rep_bank_code='6210302082441017886',
				rep_phone='13686467482',
				provice=u'湖南省',
				district=u'长沙',
				rep_bank_name=u'中国银行',
				rep_bank_branch_name=u'北京支行',
				)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		contract.Contract(page, self.applyCode, rec_bank_info, 5).execute_sign()
	
	def test_06_6Person_contract(self):
		'''六人签约'''
		self.data['applyVo']['applyAmount'] = 1200000
		# ---------------------------------------------------------------------------------
		#                   1. 申请录入
		# ---------------------------------------------------------------------------------
		
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.custName = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])[1]
		
		# 3 物业信息
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成")
			print("applyCode:" + self.applyCode)
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		# ---------------------------------------------------------------------------------------
		# 	                        2. 风控审批流程
		# ---------------------------------------------------------------------------------------
		
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applyCode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司主管审批通过！")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = common.approval_to_review(page, applyCode, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司经理审批通过！")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = common.approval_to_review(page, applyCode, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise AssertionError('区域预复核审批失败！')
		else:
			self.log.info("区域预复核审批通过")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批经理审批通过
		res = common.approval_to_review(page, applyCode, u'审批经理审批通过', 0)
		if not res:
			self.log.error("审批经理审批失败！")
			raise AssertionError('审批经理审批失败!')
		else:
			self.log.info("审批经理审批通过成功！")
			self.get_next_user(page, applyCode)
		
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
		
		# 扣款银行信息
		rep_bank_info = dict(
				rep_name=u'习近平',
				rep_id_num='420101198201013526',
				rep_bank_code='6210302082441017886',
				rep_phone='13686467482',
				provice=u'湖南省',
				district=u'长沙',
				rep_bank_name=u'中国银行',
				rep_bank_branch_name=u'北京支行',
				)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		contract.Contract(page, self.applyCode, rec_bank_info, 6).execute_sign()
	
	def test_07_7Person_contract(self):
		'''七人签约'''
		self.data['applyVo']['applyAmount'] = 1400000
		# ---------------------------------------------------------------------------------
		#                   1. 申请录入
		# ---------------------------------------------------------------------------------
		
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.custName = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])[1]
		
		# 3 物业信息
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成")
			print("applyCode:" + self.applyCode)
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		# ---------------------------------------------------------------------------------------
		# 	                        2. 风控审批流程
		# ---------------------------------------------------------------------------------------
		
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applyCode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司主管审批通过！")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = common.approval_to_review(page, applyCode, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司经理审批通过！")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = common.approval_to_review(page, applyCode, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise AssertionError('区域预复核审批失败！')
		else:
			self.log.info("区域预复核审批通过")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批经理审批通过
		res = common.approval_to_review(page, applyCode, u'审批经理审批通过', 0)
		if not res:
			self.log.error("审批经理审批失败！")
			raise AssertionError('审批经理审批失败!')
		else:
			self.log.info("审批经理审批通过成功！")
			self.get_next_user(page, applyCode)
		
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
		
		# 扣款银行信息
		rep_bank_info = dict(
				rep_name=u'习近平',
				rep_id_num='420101198201013526',
				rep_bank_code='6210302082441017886',
				rep_phone='13686467482',
				provice=u'湖南省',
				district=u'长沙',
				rep_bank_name=u'中国银行',
				rep_bank_branch_name=u'北京支行',
				)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		contract.Contract(page, self.applyCode, rec_bank_info, 7).execute_sign()
	
	def test_08_10Person_contract(self):
		'''10人签约'''
		
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
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成")
			print("applyCode:" + self.applyCode)
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		# ---------------------------------------------------------------------------------------
		# 	                        2. 风控审批流程
		# ---------------------------------------------------------------------------------------
		
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applyCode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司主管审批通过！")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = common.approval_to_review(page, applyCode, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司经理审批通过！")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = common.approval_to_review(page, applyCode, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise AssertionError('区域预复核审批失败！')
		else:
			self.log.info("区域预复核审批通过")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 高级审批经理审批通过
		res = common.approval_to_review(page, applyCode, u'审批经理审批通过', 0)
		if not res:
			self.log.error("审批经理审批失败！")
			raise AssertionError('审批经理审批失败!')
		else:
			self.log.info("审批经理审批通过成功！")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 风控总监
		res = common.approval_to_review(page, applyCode, u'风控总监审批通过', 0)
		if not res:
			self.log.error("审风控总监审批失败！")
			raise AssertionError('审风控总监审批失败!')
		else:
			self.log.info("风控总监审批通过成功！")
			self.get_next_user(page, applyCode)
		
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
		
		res = contract.Contract(page, self.applyCode, rec_bank_info, 10)
		res.execute_sign()
	
	def test_08_20Person_contract(self):
		'''20人签约'''
		
		self.data['applyVo']['applyAmount'] = 4000000
		# ---------------------------------------------------------------------------------
		#                   1. 申请录入
		# ---------------------------------------------------------------------------------
		
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.custName = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])[1]
		
		# 3 物业信息
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applyCode = common.get_applycode(self.page, self.custName)
		if applyCode:
			self.applyCode = applyCode
			self.log.info("申请件查询完成")
			print("applyCode:" + self.applyCode)
		# 流程监控
		result = common.process_monitor(self.page, applyCode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		# ---------------------------------------------------------------------------------------
		# 	                        2. 风控审批流程
		# ---------------------------------------------------------------------------------------
		
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applyCode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司主管审批通过！")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = common.approval_to_review(page, applyCode, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise AssertionError('审批失败')
		else:
			self.log.info("分公司经理审批通过！")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = common.approval_to_review(page, applyCode, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise AssertionError('区域预复核审批失败！')
		else:
			self.log.info("区域预复核审批通过")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 高级审批经理审批通过
		res = common.approval_to_review(page, applyCode, u'审批经理审批通过', 0)
		if not res:
			self.log.error("审批经理审批失败！")
			raise AssertionError('审批经理审批失败!')
		else:
			self.log.info("审批经理审批通过成功！")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 风控总监
		res = common.approval_to_review(page, applyCode, u'风控总监审批通过', 0)
		if not res:
			self.log.error("审风控总监审批失败！")
			raise AssertionError('审风控总监审批失败!')
		else:
			self.log.info("风控总监审批通过成功！")
			self.get_next_user(page, applyCode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 风控总监
		res = common.approval_to_review(page, applyCode, u'首席风控官审批通过', 0)
		if not res:
			self.log.error("首席风控官审批失败！")
			raise AssertionError('首席风控官审批失败!')
		else:
			self.log.info("首席风控官审批通过成功!")
			self.get_next_user(page, applyCode)
		
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
		
		res = contract.Contract(page, self.applyCode, rec_bank_info, 20)
		res.execute_sign()
