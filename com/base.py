# coding:utf-8
import json
import os

import config.source_data
from com import common, custom, login
from com.idCardNumber import IdCardNumber as IDCard
from com.pobj.DoneListTask import ProcessedTask
from com.pobj.FinancialPendingTask import (
	FinancialApproval as Fa,
	RaiseApproval as Ra,
	)
from com.pobj.HouseRefuseList import RefuseList
from com.pobj.IntoCaseManage import HouseloanApplyEntry as Hae
from com.pobj.LendingConfirm import BaseDataPush
from com.pobj.TaskCenter import (
	ApplicationQuery as Aq,
	PendingTask as Pt,
	ProcessMonitor as Pm,
	)
from com.pobj.WarrantManage import WarrantManageList as Wm
from config import product


class Base(object):
	"""基类"""
	
	def __init__(self, env_file, data_file):
		"""
		构造函数
		:param env_file:  环境配置文件
		:param data_file: 数据配置文件
		"""
		
		self.city = ['东莞分公司', '南通分公司', '南京分公司', '无锡分公司', '苏州分公司', '常州分公司']
		self.using_time = None  # 执行时长
		self.apply_code = None
		self.next_user_id = None
		
		# 版本信息
		custom.print_version_info()
		self.log = custom.mylog()
		
		if env_file is not None:
			self.env_file = env_file
		else:
			return
		if data_file is not None:
			self.data_file = data_file
		else:
			return
		
		self.page = login.Login()
		
		# 环境初始化,解析环境
		self.__init_env()
		
		# 数据初始化
		self.__init_data()
		# 默认产品
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
		# 设置角色
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
		# 已处理任务列表：
		self.DL = ProcessedTask.ProcessedTask()
		# 基础数据同步
		self.BaseData = BaseDataPush.BaseDataPush()
	
	def __init_env(self):
		"""环境初始化"""
		try:
			r_dir = config.__path__[0]
			config_env = os.path.join(r_dir, self.env_file)
			try:
				with open(config_env, 'r', encoding='utf-8') as f:
					env_data = json.load(f)
			except IOError as e:
				raise e
		except Exception as e:
			self.log.error('load config error:', str(e))
			raise e
		
		self.number = env_data["number"]
		self.env = env_data["enviroment"]
		self.exe = env_data['upload_exe']
		self.image = env_data["image_jpg"]
		self.company = env_data[self.env]["company"][self.number]
	
	def __init_data(self):
		"""
		数据初始化, 根据产品的不同，读取不同的配置文件
		"""
		filename = self.data_file
		rd = config.source_data.__path__[0]
		data_config = os.path.join(rd, filename)
		
		with open(data_config, 'r', encoding='utf-8') as fd:
			data_source = json.load(fd)
		
		# 自动赋值
		self.set_value(data_source)
		self.data = data_source
		self.cust_name = self.data['custInfoVo'][0]['custName']
	
	@staticmethod
	def set_value(data_source):
		"""
		获取配置数据文件数据，并自动赋给任意值
		:param data_source:
		:return:
		"""
		if type(data_source) is dict:
			data_source['custInfoVo'][0]['custName'] = custom.get_name()
			data_source['custInfoVo'][0]['idNum'] = IDCard.getRandomIdNumber()[0]
			data_source['custInfoVo'][0]['phone'] = IDCard.create_phone()
			data_source['custInfoVo'][0]['address'] = IDCard.getRandomIdNumber()[1]
	
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
		
		try:
			# 打印贷款产品信息
			custom.print_product_info(self.product_info)
			if self.company['branchName'] not in self.city:
				# 非渠道城市进件
				self.HAE.input_customer_base_info(self.page, self.data['applyVo'])
			else:
				# 渠道城市非新产品
				if 'E押通-2.1' not in self.product_info['name']:
					self.HAE.input_customer_base_info(self.page, self.data['applyVo'])
				else:
					# 渠道城市新产品
					self.HAE.input_customer_base_info(self.page, self.data['applyVo'], True)
		except Exception as e:
			raise e
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.HAE.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
		
		# 3 物业信息
		self.HAE.input_all_bbi_property_info(
			self.page,
			self.data['applyPropertyInfoVo'][0],
			self.data['applyCustCreditInfoVo'][0],
			self.cust_name
			)
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
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
	
	def before_contract_sign(self, amount=1000000):
		"""签约前操作"""
		
		try:
			# 打印贷款产品信息
			custom.print_product_info(self.product_info)
			if self.company['branchName'] not in product.product_city or self.data['applyVo']['productName'] not in \
					product.product['YES']:
				# 非渠道城市进件
				self.HAE.input_customer_base_info(self.page, self.data['applyVo'])
			else:
				# 渠道城市新产品
				self.HAE.input_customer_base_info(self.page, self.data['applyVo'], True)
		except Exception as e:
			raise e
		
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
		result = self.PM.process_monitor(self.page, apply_code)
		if result != None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
		else:
			self.log.error("流程监控查询出错！")
			raise AssertionError('流程监控查询出错！')
		
		# ---------------------------------------------------------------------------------------
		# 	                        2. 风控审批流程
		# ---------------------------------------------------------------------------------------
		
		# 下一个处理人重新登录
		self.page = login.Login(self.next_user_id)
		
		list_mark = [
			"分公司主管审批",
			"分公司经理审批",
			"区域预复核审批",
			"高级审批经理审批",
			"风控总监审批",
			"首席风控官"
			]
		
		if amount > 2000000:
			for e in list_mark:
				res = self.PT.approval_to_review(self.page, self.apply_code, e, 0)
				self.risk_approval_result(res, e, self.page, self.apply_code)
				# 下一个处理人重新登录
				self.page = login.Login(self.next_user_id)
		elif 1500000 < amount <= 2000000:
			for e in list_mark[:5]:
				res1 = self.PT.approval_to_review(self.page, self.apply_code, e, 0)
				self.risk_approval_result(res1, e, self.page, self.apply_code)
				# 下一个处理人重新登录
				self.page = login.Login(self.next_user_id)
		else:
			count = 0
			for e in list_mark[:4]:
				if count == 3:
					if self.next_user_id != self.senior_manager:
						return
				res1 = self.PT.approval_to_review(self.page, self.apply_code, e, 0)
				self.risk_approval_result(res1, e, self.page, self.apply_code)
				count = count + 1
				# 下一个处理人重新登录
				self.page = login.Login(self.next_user_id)
	
	def risk_approval_result(self, res, mark, page, apply_code):
		"""
		校验风控审批结果
		:param res: 返回值传入
		:param mark: 角色
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
	
	def case_using_time(self, begin_time, end_time):
		run_time = end_time - begin_time
		m, s = divmod(run_time, 60)
		h, m = divmod(m, 60)
		if h != 0:
			self.using_time = str(h).split('.')[0] + 'h' + str(m).split('.')[0] + 'm' + str(s).split('.')[0] + 's'
		elif h == 0 and m != 0:
			self.using_time = str(m).split('.')[0] + 'm' + str(s).split('.')[0] + 's'
		elif h == 0 and m == 0:
			self.using_time = str(s)[:4] + 's'
		# self.using_time = str(run_time)[:5]
		return self.using_time
