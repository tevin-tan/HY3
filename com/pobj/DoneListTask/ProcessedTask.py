# coding:utf-8

import time

from selenium.common import exceptions as ec

from com import custom


class ProcessedTask(object):
	"""
	已处理任务列表
	"""
	
	def __init__(self):
		self.log = custom.mylog()
	
	def query_done_list(self, page, apply_code):
		"""查询已处理任务列表"""
		
		page.driver.switch_to_default_content()
		try:
			page.driver.find_element_by_id("1DBCBC52791800014989140019301189").click()
			time.sleep(1)
			page.driver.find_element_by_name('/house/commonIndex/doneList').click()
		except ec.NoSuchElementException as e:
			raise e
		try:
			page.driver.switch_to.frame('bTabs_tab_house_commonIndex_doneList')
		except ec.NoSuchFrameException as e:
			raise e
		
		page.driver.find_element_by_id("frmQuery").click()
		# 选定申请编号搜索框
		page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").click()
		# 输入申请编号
		page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys(apply_code)
		# 点击查询按钮
		page.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/a[1]/span").click()
		time.sleep(2)
		t1 = page.driver.find_element_by_xpath('//*[@id="datagrid-row-r2-2-0"]/td[3]')
		if not t1.text:
			raise ValueError("not found applyCode")
		else:
			if t1.text == apply_code:
				self.log.info("查询已处理任务成功！")
			else:
				self.log.error("查询已处理任务失败：查询结果与搜索条件不一致")
				raise ValueError("查询失败")
