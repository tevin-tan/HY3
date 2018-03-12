# coding:utf-8
import json
import config
import os
from com import login, custom, common
from com.idCardNumber import IdCardNumber as IDCard
from com.pobj.IntoCaseManage import HouseloanApplyEntry as Hae
from com.pobj.TaskCenter import (
	ApplicationQuery as Aq,
	PendingTask as Pt,
	ProcessMonitor as Pm,
	)
from com.pobj.WarrantManage import WarrantManageList as Wm
from com.pobj.FinancialPendingTask import (
	FinancialApproval as Fa,
	RaiseApproval as Ra,
	)
from com.pobj.HouseRefuseList import RefuseList


class Base(object):
	"""基类"""
	
	def __init__(self, env_file, data_file):
		"""
		构造函数
		:param env_file:  环境配置文件
		:param data_file: 数据配置文件
		"""
		self.page = login.Login()
		self.log = custom.mylog()
		
		self.apply_code = None
		self.next_user_id = None
		self.data_file = data_file
		self.env_file = env_file
		# 环境初始化,解析环境
		self.__init_env()
		
		# 数据初始化
		self.__init_data()
		
		self.product_info = dict(
				name=self.data['applyVo']['productName'],
				amount=self.data['applyVo']['applyAmount'],
				period=self.data['applyVo']['applyPeriod'],
				)
		
		self.person_info = dict(
				name=self.data['custInfoVo'][0]['custName'],
				idNum=self.data['custInfoVo'][0]['idNum'],
				phone=self.data['custInfoVo'][0]['phone'],
				address=self.data['custInfoVo'][0]['address']
				)
		self.rec_bank_info = dict(
				recBankNum=self.data['houseCommonLoanInfoList'][0]['recBankNum'],
				recPhone=self.data['houseCommonLoanInfoList'][0]['recPhone'],
				recBankProvince=self.data['houseCommonLoanInfoList'][0]['recBankProvince'],
				recBankDistrict=self.data['houseCommonLoanInfoList'][0]['recBankDistrict'],
				recBank=self.data['houseCommonLoanInfoList'][0]['recBank'],
				recBankBranch=self.data['houseCommonLoanInfoList'][0]['recBankBranch'],
				)
		
		# 信息输出
		custom.print_env_info(self.env, self.company)
		custom.print_person_info(self.person_info)
		
		self.__init__object()
		self.__user_define()
	
	def __user_define(self):
		self.treasurer = 'xn0007533'  # 资金主管账号
		self.senior_manager = 'xn003625'  # 高级审批经理
	
	def __init__object(self):
		"""
		页面对象实例化
		:return:
		"""
		
		# 房贷进件
		self.HAE = Hae.HouseLoanApplyEntry()
		# 申请件查询
		self.AQ = Aq.ApplicationQuery()
		# 待处理任务
		self.PT = Pt.PendingTask()
		# 流程监控
		self.PM = Pm.ProcessMonitor()
		# 权证办理
		self.WM = Wm.WarrantManage()
		# 财务流程
		self.FA = Fa.FinancialApproval()
		# 募资流程
		self.RA = Ra.FinancialApproval()
		# 房贷拒绝队列
		self.HRL = RefuseList.HouseRefuseLIst()
	
	def __init_env(self):
		"""环境初始化"""
		try:
			r_dir = config.__path__[0]
			config_env = os.path.join(r_dir, self.env_file)
			try:
				with open(config_env, 'r', encoding='utf-8') as f:
					env_data = json.load(f)
				f.close()
			except IOError as e:
				raise e
		except Exception as e:
			self.log.error('load config error:', str(e))
			raise e
		
		self.number = env_data["number"]
		self.env = env_data["enviroment"]
		self.exe = env_data['upload_exe']
		self.image = env_data["image_jpg"]
	
	def __init_data(self):
		"""
		数据初始化
		:return: data, company
		"""
		filename = self.data_file
		data_source = custom.enviroment_change(filename, self.number, self.env)
		# 自动赋值
		self.set_value(data_source)
		self.data = data_source[0]
		self.custName = self.data['custInfoVo'][0]['custName']
		self.company = data_source[1]
	
	@staticmethod
	def set_value(data_source):
		"""
		借款人信息自动赋值
		:param data_source:
		:return:
		"""
		if type(data_source) is tuple:
			data_source[0]['custInfoVo'][0]['custName'] = custom.get_name()
			data_source[0]['custInfoVo'][0]['idNum'] = IDCard.getRandomIdNumber()[0]
			data_source[0]['custInfoVo'][0]['phone'] = IDCard.create_phone()
			data_source[0]['custInfoVo'][0]['address'] = IDCard.getRandomIdNumber()[1]
	
	def update_product_amount(self, amount):
		"""
		修改贷款金额
		:param amount:
		:return:
		"""
		self.data['applyVo']['applyAmount'] = amount
		self.product_info.update(dict(amount=amount))
		custom.print_product_info(self.product_info)
	
	def before_application_entry(self):
		"""进件提交"""
		
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
		
		applycode = self.AQ.get_applycode(self.page, self.custName)
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
	
	def before_contract_sign(self):
		"""签约前操作"""
		
		# 1 客户信息-业务基本信息
		if self.HAE.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.HAE.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		self.HAE.input_all_bbi_property_info(
				self.page, self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0])
		# 提交
		self.HAE.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		apply_code = self.AQ.get_applycode(self.page, self.custName)
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
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		# ---------------------------------------------------------------------------------------
		# 	                        2. 风控审批流程
		# ---------------------------------------------------------------------------------------
		
		# 下一个处理人重新登录
		page = login.Login(self.next_user_id)
		
		list_mark = [
			"分公司主管审批",
			"分公司经理审批",
			"区域预复核审批",
			"高级审批经理审批",
			# "风控总监审批"
			]
		
		for e in list_mark:
			res = self.PT.approval_to_review(page, self.apply_code, e, 0)
			self.risk_approval_result(res, e, page, self.apply_code)
			# 下一个处理人重新登录
			page = login.Login(self.next_user_id)
	
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
