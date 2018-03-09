# coding:utf-8
import json
import config
import os
from com import login, custom
from com.idCardNumber import IdCardNumber as IDCard


class Base(object):
	"""基类"""
	
	def __init__(self, env_file, data_file):
		"""
		构造函数
		:param env_file:  环境配置文件
		:param data_file: 数据配置文件
		"""
		self.page = login.Login()
		self.apply_code = None
		self.next_user_id = None
		self.log = custom.mylog()
		self.data_file = data_file
		self.env_file = env_file
		self.treasurer = 'xn0007533'  # 资金主管账号
		
		# 环境初始化,解析环境
		res_env = self.init_env()
		self.number = res_env["number"]
		self.env = res_env["enviroment"]
		
		# 数据初始化
		res = self.init_data()
		self.data = res[0]
		self.custName = self.data['custInfoVo'][0]['custName']
		self.company = res[1]
		
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
	
	def init_env(self):
		"""
		环境初始化
		:return:
		"""
		try:
			rootdir = config.__path__[0]
			config_env = os.path.join(rootdir, self.env_file)
			try:
				with open(config_env, 'r', encoding='utf-8') as f:
					env_data = json.load(f)
				f.close()
				return env_data
			except IOError as e:
				raise e
		except Exception as e:
			self.log.error('load config error:', str(e))
			raise e
	
	def init_data(self):
		"""
		数据初始化
		:return: data, company
		"""
		filename = self.data_file
		data_source = custom.enviroment_change(filename, self.number, self.env)
		# 自动赋值
		self.set_value(data_source)
		return data_source
	
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
			data_source[0]['custInfoVo'][0]['phone'] = IDCard.createPhone()
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
