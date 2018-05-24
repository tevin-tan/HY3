# coding:utf-8

import time
import unittest

from selenium.common import exceptions as ec

from com import custom, database
from selenium.webdriver.common.action_chains import ActionChains

class BaseDataPush(unittest.TestCase):
	"""基础数据同步"""
	
	def __init__(self):
		self.log = custom.mylog()
		self.db = database.DB()
	
	def update_data_loan_success(self, sql_one, sql_two):
		"""修改放款成功"""
		
		# 修改house_common_loan_info表status = loan_pass
		self.db.sql_execute(sql_one)
		# 修改house_funds_info表 funds_status=21
		self.db.sql_execute(sql_two)
		
		# 提交
		self.db.sql_commit()
		time.sleep(3)
	
	def push_data_to_financial(self, page, apply_code):
		"""推送数据给财务"""
		
		self.log.info('开启数据同步推送')
		try:
			page.driver.find_element_by_id('1DBCBC52CF2E00012CB2184841703370').click()
			time.sleep(1)
			page.driver.find_element_by_name('/house/financial/financialIndex').click()
		except ec.NoSuchElementException as e:
			raise e
		try:
			page.driver.switch_to_frame('bTabs_tab_house_financial_financialIndex')
		except ec.NoSuchFrameException as e:
			raise e
		
		# 查询案件
		time.sleep(1)
		page.driver.find_element_by_name("applyCode").send_keys(apply_code)
		time.sleep(1)
		page.driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/a[1]').click()
		time.sleep(1)
		res = page.driver.find_element_by_xpath('//*[@id="datagrid-row-r1-2-0"]/td[10]/div')
		print(res.text)
		if res.text is not None:
			res.click()
			# ActionChains(page.driver).double_click(res).perform()
			page.driver.find_element_by_xpath('//*[@id="push"]').click()
			time.sleep(1)
			page.driver.find_element_by_xpath('/html/body/div[5]/div[3]/a').click()
			
