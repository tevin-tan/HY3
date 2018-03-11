# coding: utf-8

import time
from com import custom
from selenium.webdriver.common.action_chains import ActionChains


class FinancialApproval(object):
	"""财务审批"""
	
	def __init__(self):
		self.log = custom.mylog()
	
	def funds_raise(self, page, condition, remark):
		"""
			募资
		:param page:
		:param condition:
		:param remark:
		:return:
		"""
		
		self.log.info("发起募资申请")
		page._click_control(page.driver, "id", "1DBCBC52791800014989140019301189")
		page.driver.find_element_by_name('/house/commonIndex/financial/toDoList').click()
		page.driver.switch_to_frame('bTabs_tab_house_commonIndex_financial_toDoList')
		
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
		
		if res.text == condition:
			res.click()
			ActionChains(page.driver).double_click(res).perform()
			time.sleep(2)
			page.driver.switch_to_frame('myIframeImage1')
			page.driver.find_element_by_name('options').clear()
			page.driver.find_element_by_name('options').send_keys(remark)
			# save
			page.driver.switch_to.parent_frame()
			page.driver.find_element_by_xpath('//*[@id="financeRasing_save"]/span').click()
			page.driver.find_element_by_xpath('/html/body/div[3]/div[3]/a').click()
			# submit
			page.driver.find_element_by_xpath('//*[@id="financeRasing_submit"]/span').click()
			page.driver.find_element_by_xpath('/html/body/div[3]/div[3]/a[1]').click()
			
			return True
		else:
			self.log.error(u'财务待处理任务中没有找到申请编号')
			return False
