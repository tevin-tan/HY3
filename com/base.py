# coding:utf-8
import json
import config
import os
from com import login, custom
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
