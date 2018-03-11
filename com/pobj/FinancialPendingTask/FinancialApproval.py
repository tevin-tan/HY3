# coding: utf-8

import time
import datetime
from com import custom
from selenium.common import exceptions as ec
from selenium.webdriver.common.action_chains import ActionChains


class FinancialApproval(object):
	"""财务审批"""
	
	def __init__(self):
		self.log = custom.mylog()
	
	def finace_transact(self, page, condition):
		"""
		财务办理
		:param page: 页面对象
		:param condition:   applyCode
		:return:
		"""
		
		self.log.info("发起财务办理")
		# 财务放款申请列表
		try:
			page.driver.find_element_by_id('1DBCBC52791800014989140019301189')
			page.driver.find_element_by_name('/house/commonIndex/financeManageList').click()
			time.sleep(1)
			page.driver.switch_to_frame('bTabs_tab_house_commonIndex_financeManageList')
			# 选定申请编号搜索框
			page.driver.find_element_by_id("frmQuery").click()
			page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").click()
			# 输入申请编号
			time.sleep(1)
			page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys(condition)
			# 点击查询按钮
			page.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/a[1]/span").click()
			time.sleep(1)
			res = page.driver.find_element_by_xpath('//*[@id="datagrid-row-r1-2-0"]/td[5]/div')
		except ec.NoSuchElementException as e:
			raise e.msg
		if not res.text:
			return False
		else:
			res.click()
			ActionChains(page.driver).double_click(res).perform()
			time.sleep(2)
			try:
				page.driver.switch_to_frame('myIframeImage1')
			except ec.NoSuchFrameException as  e:
				raise e.msg
			page.driver.find_element_by_name('preLoaningDate').send_keys(str(datetime.date.today()))
			time.sleep(1)
			# 保存
			page.driver.switch_to.parent_frame()
			page.driver.find_element_by_xpath('//*[@id="financeApply_save"]/span').click()
			time.sleep(1)
			page.driver.find_element_by_xpath('/html/body/div[4]/div[3]/a').click()
			# 提交
			page.driver.find_element_by_xpath('//*[@id="financeApply_submit"]/span').click()
			return True
	
	def finace_approval(self, page, condition, remark):
		"""
		财务审批
		:param page: 页面对象
		:param condition: applyCode
		:param remark
		:return:
		"""
		
		self.log.info("发起财务审批")
		# 财务待处理任务
		try:
			page.driver.find_element_by_id('1DBCBC52791800014989140019301189')
			
			time.sleep(1)
			page.driver.find_element_by_name('/house/commonIndex/financial/toDoList').click()
			try:
				page.driver.switch_to_frame('bTabs_tab_house_commonIndex_financial_toDoList')
			except ec.NoSuchFrameException as e:
				raise e.msg
			
			# 选定申请编号搜索框
			page.driver.find_element_by_id("frmQuery").click()
			page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").click()
			# 输入申请编号
			time.sleep(1)
			page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys(condition)
			# 点击查询按钮
			page.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/a[1]/span").click()
			time.sleep(1)
			res = page.driver.find_element_by_xpath('//*[@id="datagrid-row-r1-2-0"]/td[7]/div')
		except ec.ElementNotVisibleException as e:
			raise e.msg
		
		if res.text == condition:
			res.click()
			ActionChains(page.driver).double_click(res).perform()
			time.sleep(2)
			page.driver.switch_to_frame('myIframeImage1')
			page.driver.find_element_by_id('remark').clear()
			page.driver.find_element_by_id('remark').send_keys(remark)
			# save
			page.driver.switch_to.parent_frame()
			page.driver.find_element_by_xpath('//*[@id="financeApply_save"]/span').click()
			time.sleep(1)
			page.driver.find_element_by_xpath('/html/body/div[4]/div[3]/a').click()
			# submit
			page.driver.find_element_by_xpath('//*[@id="financeApply_submit"]/span').click()
			time.sleep(2)
			return True
		else:
			self.log.error(u'财务待处理任务中没有找到申请编号')
			return False
