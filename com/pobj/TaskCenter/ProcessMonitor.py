# coding:utf-8
import time
from com import custom
from selenium.common import exceptions as ec
from selenium.webdriver.common.action_chains import ActionChains


class ProcessMonitor(object):
	"""流程监控"""
	
	def __init__(self):
		self.log = custom.mylog()
	
	def process_monitor(self, page, condition, stage=0):
		"""
			流程监控
		:param page: 页面
		:param condition: applyCode
		:param stage  0,1,2  对应风控、财务、募资
		:return: 下一个处理人登录 ID
		"""
		try:
			time.sleep(1)
			page.driver.switch_to_default_content()
			# 打开任务中心
			page._click_control(page.driver, "id", "1DBCBC52791800014989140019301189")
			time.sleep(1)
			# 流程监控
			page.driver.find_element_by_name("/house/commonIndex/processMonitor").click()
			time.sleep(2)
			
			#  切换frame
			try:
				page.driver.switch_to_frame("bTabs_tab_house_commonIndex_processMonitor")
				time.sleep(1)
			except ec.NoSuchFrameException as e:
				raise e
			# 输入搜索条件
			page.driver.find_element_by_name("process_search").click()
			time.sleep(1)
			page.driver.find_element_by_xpath("//*[@id='applyCode']").click()
			page.driver.find_element_by_xpath("//*[@id='applyCode']").send_keys(condition)
			time.sleep(1)
			# 点击查询
			page.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/a[1]/span").click()
			time.sleep(1)
			# 校验查询结果
			res = page.driver.find_element_by_xpath("//*[@id='datagrid-row-r4-2-0']/td[5]/div")
			time.sleep(2)
			if not res.text:
				return False
			else:
				res.click()
				# page.driver.find_element_by_class_name("datagrid-btable").click()
				page.driver.find_element_by_name('process_search').click()
				# 双击该笔案件
				ActionChains(page.driver).double_click(res).perform()
				time.sleep(1)
				role = ""
				next_user_id = ""
				if stage == 0:
					res = page.driver.find_element_by_class_name("datagrid-btable")
					rcount = res.find_elements_by_tag_name("tr")  # 取表格的行数
					for i in range(1, len(rcount)):
						role = page.driver.find_element_by_xpath('//*[@id="datagrid-row-r1-2-%s"]/td[1]/div' % i).text
						time.sleep(1)
					self.log.info("下一个处理节点:" + role)  # 返回节点所有值
					# 下一步处理人ID
					next_user_id = page.driver.find_element_by_xpath(
							'//*[@id="datagrid-row-r1-2-%s"]/td[4]/div' % (len(rcount) - 1)).text
				elif stage == 1:
					page.driver.find_element_by_id('firstLoanA').click()
					page.driver.find_element_by_class_name('datagrid-view2')
					res = page.driver.find_element_by_xpath(
							'//*[@id="profile"]/div/div/div/div/div[2]/div[2]/table/tbody')
					rcount = res.find_elements_by_tag_name("tr")
					for i in range(1, len(rcount)):
						role = page.driver.find_element_by_xpath('//*[@id="datagrid-row-r4-2-%s"]/td[1]/div' % i).text
						time.sleep(1)
					self.log.info("下一个处理环节:" + role)  # 返回节点所有值
					next_user_id = page.driver.find_element_by_xpath(
							'//*[@id="datagrid-row-r4-2-%s"]/td[4]/div' % (len(rcount) - 1)).text
				elif stage == 2:
					# 第二次放款
					page.driver.find_element_by_id('secondLoanLi').click()
					page.driver.find_element_by_class_name("datagrid-btable")
					res = page.driver.find_element_by_xpath('//*[@id="settings"]/div/div/div/div/div[2]/div[2]/table')
					rcount = res.find_elements_by_tag_name("tr")  # 取表格的行数
					for i in range(1, len(rcount)):
						role = page.driver.find_element_by_xpath('//*[@id="datagrid-row-r8-2-%s"]/td[1]/div' % i).text
						time.sleep(1)
					self.log.info("下一个处理节点:" + role)  # 返回节点所有值
					# 下一步处理人ID
					next_user_id = page.driver.find_element_by_xpath(
							'//*[@id="datagrid-row-r8-2-%s"]/td[4]/div' % (len(rcount) - 1)).text
		except ec.NoSuchElementException as e:
			raise e
		finally:
			page.driver.quit()
		return next_user_id
