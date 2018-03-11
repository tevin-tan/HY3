# coding:utf-8
import time
from com import custom
from selenium.common import exceptions as ec


class ApplicationQuery(object):
	"""申请件查询"""
	
	def __init__(self):
		self.log = custom.mylog()
	
	def get_applycode(self, page, condition):
		"""
			获取APPLYCODE
		:param page:    页面对象
		:param condition:   录入客户姓名
		:return:    applyCode
		"""
		try:
			# 打开任务中心
			page._click_control(page.driver, "id", "1DBCBC52791800014989140019301189")
			time.sleep(1)
			# 申请件查询
			page.driver.find_element_by_name('/house/commonIndex/applySearch/index').click()
			time.sleep(2)
		except ec.ElementNotVisibleException as e:
			raise e
		try:
			# 切换iframe 申请件查询
			page.driver.switch_to_frame("bTabs_tab_house_commonIndex_applySearch_index")
		except ec.NoSuchFrameException as e:
			raise e.msg
		
		try:
			# 打开表单
			time.sleep(2)
			page.driver.find_element_by_class_name("main-form-table").click()
			time.sleep(2)
			page.driver.find_element_by_xpath("//*[@id='row-content']/div[2]/input").click()
			# # 根据条件查询录入案件
			page.driver.find_element_by_xpath("//*[@id='row-content']/div[2]/input").send_keys(condition)
			page.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/a[1]").click()
			time.sleep(1)
			# 第一个申请编号
			t1 = page.driver.find_element_by_xpath("//*[@id='datagrid-row-r2-2-0']/td[9]")
		except ec.NoSuchFrameException as e:
			raise e.msg
		
		if t1:
			# 获取申请编号
			self.log.info("applyCode: " + t1.text)
			return t1.text
		else:
			raise ValueError("Value error")
