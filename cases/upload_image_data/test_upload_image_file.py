# coding: utf-8
import unittest
import json
import os
from com import common
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
		except Exception as e:
			self.log.error('load config error:', str(e))
			raise e
	
	def tearDown(self):
		self.page.driver.quit()
	
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
		"""房贷专员删除影像资料"""
		
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
