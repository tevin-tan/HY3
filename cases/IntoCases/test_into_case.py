# coding:utf-8
import unittest
import time
import json
import os
from com import common
from com import custom
from com.login import Login
from com.custom import Log, print_env


class IntoCase(unittest.TestCase):
	'''申请录入进件场景'''
	
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
			data, company = custom.enviroment_change(filename, self.number, self.env)
			self.page = Login()
			self.log = Log()
			
			self.evt = dict(
					data=data,
					company=company
					)
			print_env(self.env, self.evt['company'])
		except Exception as e:
			print('load config error:', str(e))
			raise e
	
	def tearDown(self):
		pass
	
	def test_01_one_borrower(self):
		'''单借款人'''
		
		name = custom.get_current_function_name()
		print("当前用例编号:" + name)
		# 录入一个借款人
		
		# 1 客户信息-业务基本信息
		common.input_customer_base_info(self.page, self.evt['data']['applyVo'])
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		common.input_customer_borrow_info(self.page, self.evt['data']['custInfoVo'][0])
		
		# 3 物业信息
		common.input_cwd_bbi_Property_info(self.page, self.evt['data']['applyPropertyInfoVo'][0],
		                                   self.evt['data']['applyCustCreditInfoVo'][0])
		
		# 提交
		common.submit(self.page)
		self.countTestCases()
	
	def test_02_two_borrower(self, n=2):
		# 录入两个借款人
		self.skipTest("xxxxx")
		# n = 2
		common.input_customer_base_info(self.page, self.evt['data']['applyVo'])
		
		if n == 1:
			# common.input_customer_borrow_info(self.page, self.evt['data']['custInfoVo'][0])
			# 添加借款人
			self.page.driver.find_element_by_xpath('//*[@id="tb"]/a[1]/span[2]').click()
			# 姓名
			self.page.driver.find_element_by_xpath(
					'//*[@id="datagrid-row-r1-2-0"]/td[4]/div/table/tbody/tr/td/input').send_keys(u" 小王")
			# 身份证
			self.page.driver.find_element_by_xpath(
					'//*[@id="datagrid-row-r1-2-0"]/td[5]/div/table/tbody/tr/td/input').send_keys("360101199101011054")
			
			# 受教育程度
			self.page.driver.find_element_by_id("_easyui_textbox_input3").click()
			self.page.driver.find_element_by_id('_easyui_combobox_i2_0').click()
			
			# 婚姻
			self.page.driver.find_element_by_xpath(
					'//*[@id="datagrid-row-r1-2-0"]/td[8]/div/table/tbody/tr/td/span/span/a').click()
			self.page.driver.find_element_by_id('_easyui_combobox_i3_3').click()
			
			# 家庭住址信息
			self.page.driver.find_element_by_id('_easyui_textbox_input5').send_keys("hhhhh")
			# phone
			self.page.driver.find_element_by_xpath(
					'//*[@id="datagrid-row-r1-2-0"]/td[10]/div/table/tbody/tr/td/input').send_keys("13683121234")
			# 单位名称
			self.page.driver.find_element_by_xpath(
					'//*[@id="datagrid-row-r1-2-0"]/td[11]/div/table/tbody/tr/td/input').send_keys('xxxxx')
			# 公司规模
			self.page.driver.find_element_by_id('_easyui_textbox_input6').click()
			self.page.driver.find_element_by_id('_easyui_combobox_i4_3').click()
			
			# 所属行业
			self.page.driver.find_element_by_id('_easyui_textbox_input7').click()
			self.page.driver.find_element_by_id('_easyui_combobox_i5_2').click()
			
			# 职位
			self.page.driver.find_element_by_id('_easyui_textbox_input9').send_keys("aaaaaa")
			# 日期
			self.page.driver.find_element_by_xpath(
					'//*[@id="datagrid-row-r1-2-0"]/td[16]/div/table/tbody/tr/td/input').send_keys('2017-09-01')
			# 工作年限
			self.page.driver.find_element_by_id('_easyui_textbox_input10').send_keys(10)
			# 月均收入
			self.page.driver.find_element_by_id('_easyui_textbox_input11').send_keys(10000)
			# 是否有社保
			self.page.driver.find_element_by_xpath(
					'//*[@id="datagrid-row-r1-2-0"]/td[19]/div/table/tbody/tr/td/input').click()
			# 确认
			self.page.driver.find_element_by_xpath('//*[@id="tb"]/a[3]/span[2]').click()
		elif n == 2:
			common.input_customer_borrow_info(self.page, self.evt['data']['custInfoVo'][0])
			self.page.driver.find_element_by_xpath('//*[@id="tb"]/a[1]/span[2]').click()
			self.page.driver.find_element_by_xpath(
					'//*[@id="datagrid-row-r1-2-1"]/td[4]/div/table/tbody/tr/td/input').send_keys(u"小黑")
			self.page.driver.find_element_by_xpath(
					'//*[@id="datagrid-row-r1-2-1"]/td[5]/div/table/tbody/tr/td/input').send_keys("360101199101011054")
			time.sleep(2)
			self.page.driver.find_element_by_id('_easyui_textbox_input14').click()
			self.page.driver.find_element_by_id('_easyui_combobox_i8_2').click()
			
			self.page.driver.find_element_by_id('_easyui_textbox_input15').click()
			self.page.driver.find_element_by_id('_easyui_combobox_i9_0').click()
			
			self.page.driver.find_element_by_id('_easyui_textbox_input16').send_keys("xxxaaaa")
			self.page.driver.find_element_by_xpath(
					'//*[@id="datagrid-row-r1-2-1"]/td[10]/div/table/tbody/tr/td/input').send_keys("13912341923")
			self.page.driver.find_element_by_xpath(
					'//*[@id="datagrid-row-r1-2-1"]/td[11]/div/table/tbody/tr/td/input').send_keys("yyyyyy")
			self.page.driver.find_element_by_id('_easyui_textbox_input17').click()
			self.page.driver.find_element_by_id('_easyui_combobox_i10_3').click()
			self.page.driver.find_element_by_id('_easyui_textbox_input18').click()
			self.page.driver.find_element_by_id('_easyui_combobox_i11_2').click()
			
			self.page.driver.find_element_by_id('_easyui_textbox_input20').send_keys("bbbbb")
			self.page.driver.find_element_by_xpath(
					'//*[@id="datagrid-row-r1-2-1"]/td[16]/div/table/tbody/tr/td/input').send_keys("2017-12-19")
			self.page.driver.find_element_by_id('_easyui_textbox_input21').send_keys(12)
			self.page.driver.find_element_by_id('_easyui_textbox_input22').send_keys(20000)
			
			self.page.driver.find_element_by_xpath(
					'//*[@id="datagrid-row-r1-2-1"]/td[19]/div/table/tbody/tr/td/input').click()
			
			# 确认
			self.page.driver.find_element_by_xpath('//*[@id="tb"]/a[3]/span[2]').click()
			
			# 关联关系信息
			self.page.driver.find_element_by_xpath('//*[@id="tbs"]/a[1]').click()
			self.page.driver.find_element_by_id('_easyui_textbox_input23').click()
			self.page.driver.find_element_by_id('_easyui_combobox_i12_0').click()
			
			self.page.driver.find_element_by_id('_easyui_textbox_input24').click()
			self.page.driver.find_element_by_id('_easyui_combobox_i13_1').click()
			
			self.page.driver.find_element_by_id('_easyui_textbox_input25').click()
			self.page.driver.find_element_by_id('_easyui_combobox_i14_0').click()
			self.page.driver.find_element_by_xpath('//*[@id="tb"]/a[3]/span[2]').click()
			
			# 保存
			self.page.driver.find_element_by_id('apply_module_apply_save').click()
			self.page.driver.find_element_by_xpath('/html/body/div[2]/div[3]/a').click()
	
	# 提交
	# self.page.driver.find_element_by_id('apply_module_apply_submit').click()
	
	
	def test_03_two_borrower(self):
		'''录入两个借款人'''
		
		name = custom.get_current_function_name()
		print("当前用例编号:" + name)
		# 录入基本信息
		common.input_customer_base_info(self.page, self.evt['data']['applyVo'])
		# 录入借款人/共贷人信息
		common.input_customer_borrow_info(self.page, self.evt['data']['custInfoVo'][0])
		common.input_more_borrower(self.page)
		# 录入业务基本信息
		common.input_cwd_bbi_Property_info(
				self.page,
				self.evt['data']['applyPropertyInfoVo'][0],
				self.evt['data']['applyCustCreditInfoVo'][0]
				)
		
		# 提交
		common.submit(self.page)
		self.page.driver.quit()
	
	def test_gqt_04_applydata(self):
		'''过桥通申请件录入,提交'''
		
		data, _ = custom.enviroment_change("data_gqt.json", self.number, self.env)
		
		self.evt['data'].update(data)
		# self.page = Login()
		
		# 1 客户信息-业务基本信息
		common.input_customer_base_info(self.page, self.evt['data']['applyVo'])
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		common.input_customer_borrow_info(self.page, self.evt['data']['custInfoVo'][0])
		common.input_more_borrower(self.page)
		
		# 3 物业信息
		common.input_cwd_bbi_Property_info(self.page, self.evt['data']['applyPropertyInfoVo'][0],
		                                   self.evt['data']['applyCustCreditInfoVo'][0], True, 'gqt')
		
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")


if __name__ == '__main__':
	
	ic = IntoCase()
# suite = unittest.TestSuite()
# suite.addTest(IntoCase('test_01_one_borrower'))
# runner = unittest.TextTestRunner()
# runner.run(suite)
