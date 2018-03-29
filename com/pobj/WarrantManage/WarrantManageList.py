# coding: utf-8

import datetime
import random
import time

from selenium.common import exceptions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

from com import custom
from com.pobj.TaskCenter.PendingTask import PendingTask as Pt


class WarrantManage(object):
	"""权证办理"""
	
	def __init__(self):
		self.log = custom.mylog()
		self.PT = Pt()
	
	def warrant_apply(self, page, condition):
		"""
		权证请款
		:param page: 页面对象
		:param condition:   applyCode
		:return:
		"""
		
		self.log.info("开始权证请款")
		# 打开任务中心
		t1 = self.PT.task_search(page, condition)
		if not t1.text:
			return False
		else:
			t1.click()
			# 双击
			ActionChains(page.driver).double_click(t1).perform()
			time.sleep(2)
			try:
				page.driver.switch_to.frame("myIframeImage1")  # 切换iframe
			except ec.NoSuchFrameException as e:
				raise e.msg
			
			try:
				# 原件请款-拆分个体
				# page.driver.find_element_by_name('apply').click()
				page.driver.find_element_by_xpath('//*[@id="warrantInfo"]/div[2]/div/input[3]').click()
				page.driver.find_element_by_id('splitLoanMoney').click()
				time.sleep(1)
				# 请款拆分明细
				page.driver.find_element_by_xpath('//*[@id="warrantSplitModel"]/div').click()
				time.sleep(1)
				page.driver.find_element_by_xpath('//*[@id="warrantForm"]/div/table/tbody/tr/td[1]/input').click()
				time.sleep(1)
				
				# 确定
				page.driver.find_element_by_id('dialogSplitSure').click()
				# 保存
				page.driver.switch_to.parent_frame()
				time.sleep(1)
				page.driver.find_element_by_xpath('//*[@id="first_warrant_save"]/span').click()
				time.sleep(1)
				page.driver.find_element_by_xpath('/html/body/div[2]/div[3]/a').click()
				# 提交
				page.driver.find_element_by_id('first_warrant_apply').click()
				time.sleep(1)
				page.driver.find_element_by_xpath('/html/body/div[2]/div[3]/a[1]').click()
				time.sleep(1)
				page.driver.find_element_by_xpath('/html/body/div[2]/div[3]/a').click()
				
				# page.driver.quit()
				return True
			except ec.NoSuchElementException as e:
				raise e.msg
	
	# 原件请款
	def authority_card_transact(self, page, condition, env="SIT"):
		"""
		权证办理
		:param page: 页面
		:param condition: applyCode
		:param env 环境选择
		:return:
		"""
		
		self.log.info("开始权证办理")
		# 权证管理
		try:
			# page.driver.find_element_by_xpath("/html/body/header/ul/li[5]").click()
			if env == "SIT":
				page.driver.find_element_by_id("1DF1731576B000013DB03A40A8601B66").click()
			else:
				page.driver.find_element_by_id("1DF16C65668E000176ED2081C4D01896").click()
			time.sleep(1)
			page.driver.find_element_by_name("/house/commonIndex/warrantManageList").click()
			time.sleep(1)
		except ec.NoSuchElementException as e:
			raise e
		try:
			# 切换iframe
			page.driver.switch_to_frame('bTabs_tab_house_commonIndex_warrantManageList')
		except ec.NoSuchFrameException as e:
			raise e.msg
		try:
			# 点击查询按钮
			page.driver.find_element_by_id("frmQuery").click()
			# 选定申请编号搜索框
			page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").click()
			# 输入申请编号
			page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys(condition)
			# 点击查询按钮
			page.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/a[1]/span").click()
			time.sleep(2)
			res = page.driver.find_element_by_xpath('//*[@id="datagrid-row-r1-2-0"]/td[6]/div')
			time.sleep(1)
		except ec.ElementNotVisibleException as e:
			raise e.msg
		if res.text:
			res.click()
			try:
				page.driver.find_element_by_class_name("datagrid-btable").click()
				# 双击该笔案件
				ActionChains(page.driver).double_click(res).perform()
				time.sleep(2)
				page.driver.switch_to.frame('myIframeImage1')
				# 添加
				page.driver.find_element_by_xpath('//*[@id="gridtb0"]/div[1]/a[1]').click()
				time.sleep(2)
				# 选择日期
				Select(page.driver.find_element_by_xpath('//*[@id="status"]')).select_by_value('入库')
				js = "$('input[name=storageTime]').removeAttr('readonly')"
				page.driver.execute_script(js)
				page.driver.find_element_by_xpath('//*[@id="warrantForm"]/div/div[4]/div/div/input').send_keys(
						str(datetime.date.today()))
				number = random.randrange(1, 10000000000000)  # 抵押证件号
				page.driver.find_element_by_name('warrantsCode').send_keys(str(number))
				
				# 保存权证信息
				page.driver.find_element_by_id('saveContent').click()
				time.sleep(1)
				# 添加他项权证
				page.driver.find_element_by_xpath('//*[@id="gridtb0"]/div[1]/a[1]').click()
				time.sleep(2)
				Select(page.driver.find_element_by_xpath('//*[@id="credential"]')).select_by_value('DA06')  # 他项权证
				Select(page.driver.find_element_by_xpath('//*[@id="status"]')).select_by_value('入库')
				js = "$('input[name=storageTime]').removeAttr('readonly')"
				page.driver.execute_script(js)
				page.driver.find_element_by_xpath('//*[@id="warrantForm"]/div/div[4]/div/div/input').send_keys(
						str(datetime.date.today()))
				page.driver.execute_script("$('input[name=factDelvieryDate]').removeAttr('readonly')")
				page.driver.find_element_by_name('factDelvieryDate').send_keys(str(datetime.date.today()))
				page.driver.find_element_by_name('warrantsCode').send_keys(str(number))
				
				# 保存权证信息
				page.driver.find_element_by_id('saveContent').click()
				
				# 页面保存
				page.driver.switch_to.parent_frame()
				page.driver.find_element_by_id('warrant_save').click()
				page.driver.find_element_by_xpath('/html/body/div[2]/div[3]/a').click()
				time.sleep(1)
				# 页面提交
				page.driver.find_element_by_id('warrant_submit').click()
				time.sleep(1)
				page.driver.find_element_by_xpath('/html/body/div[2]/div[3]/a').click()
				time.sleep(1)
				page.driver.find_element_by_xpath('/html/body/div[2]/div[3]/a').click()
				return True
			except ec.NoSuchElementException as e:
				raise e.msg
		else:
			return False
	
	# 部分请款
	def authority_card_transact_2(self, page, condition, num, env="SIT"):
		"""
		权证办理
		:param page: 页面
		:param condition: applyCode
		:param env 环境选择
		:param num  1 第一次, 2 第二次
		:return:
		"""
		
		self.log.info("开始权证办理")
		# 权证管理
		try:
			if env == "SIT":
				page.driver.find_element_by_id("1DF1731576B000013DB03A40A8601B66").click()
			else:
				page.driver.find_element_by_id("1DF16C65668E000176ED2081C4D01896").click()
			time.sleep(1)
			page.driver.find_element_by_name("/house/commonIndex/warrantManageList").click()
			time.sleep(1)
		except ec.NoSuchElementException as e:
			raise e
		try:
			# 切换iframe
			page.driver.switch_to_frame('bTabs_tab_house_commonIndex_warrantManageList')
		except ec.NoSuchFrameException as e:
			raise e.msg
		try:
			# 点击查询按钮
			page.driver.find_element_by_id("frmQuery").click()
			# 选定申请编号搜索框
			page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").click()
			# 输入申请编号
			page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys(condition)
			# 点击查询按钮
			page.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/a[1]/span").click()
			time.sleep(2)
			res = page.driver.find_element_by_xpath('//*[@id="datagrid-row-r1-2-0"]/td[6]/div')
			time.sleep(1)
		except ec.ElementNotVisibleException as e:
			raise e.msg
		if res.text:
			res.click()
			try:
				page.driver.find_element_by_class_name("datagrid-btable").click()
				# 双击该笔案件
				ActionChains(page.driver).double_click(res).perform()
				time.sleep(2)
				page.driver.switch_to.frame('myIframeImage1')
				number = random.randrange(1, 10000000000000)  # 抵押证件号
				# 第一次
				if num == 1:
					# 添加
					page.driver.find_element_by_xpath('//*[@id="gridtb0"]/div[1]/a[1]').click()
					time.sleep(2)
					# 选择日期
					Select(page.driver.find_element_by_xpath('//*[@id="credential"]')).select_by_value('DA04')  # 抵押回执
					Select(page.driver.find_element_by_xpath('//*[@id="status"]')).select_by_value('入库')
					js = "$('input[name=storageTime]').removeAttr('readonly')"
					page.driver.execute_script(js)
					page.driver.find_element_by_xpath('//*[@id="warrantForm"]/div/div[4]/div/div/input').send_keys(
							str(datetime.date.today()))
					
					js = "$('input[name=preDeliveryDate]').removeAttr('readonly')"
					page.driver.execute_script(js)
					page.driver.find_element_by_xpath('//*[@id="warrantForm"]/div/div[5]/div/div/input').send_keys(
						'2020-12-31')
					page.driver.find_element_by_name('warrantsCode').send_keys(str(number))
					# 保存权证信息
					page.driver.find_element_by_id('saveContent').click()
				elif num == 2:
					time.sleep(1)
					# 添加他项权证
					page.driver.find_element_by_xpath('//*[@id="gridtb0"]/div[1]/a[1]').click()
					time.sleep(2)
					Select(page.driver.find_element_by_xpath('//*[@id="credential"]')).select_by_value('DA06')
					Select(page.driver.find_element_by_xpath('//*[@id="status"]')).select_by_value('入库')
					js = "$('input[name=storageTime]').removeAttr('readonly')"
					page.driver.execute_script(js)
					page.driver.find_element_by_xpath('//*[@id="warrantForm"]/div/div[4]/div/div/input').send_keys(
							str(datetime.date.today()))
					page.driver.execute_script("$('input[name=factDelvieryDate]').removeAttr('readonly')")
					page.driver.find_element_by_name('factDelvieryDate').send_keys(str(datetime.date.today()))
					page.driver.find_element_by_name('warrantsCode').send_keys(str(number))
					# 保存权证信息
					page.driver.find_element_by_id('saveContent').click()
				
				# 页面保存
				page.driver.switch_to.parent_frame()
				page.driver.find_element_by_id('warrant_save').click()
				page.driver.find_element_by_xpath('/html/body/div[2]/div[3]/a').click()
				time.sleep(1)
				# 页面提交
				page.driver.find_element_by_id('warrant_submit').click()
				time.sleep(1)
				page.driver.find_element_by_xpath('/html/body/div[2]/div[3]/a').click()
				time.sleep(1)
				page.driver.find_element_by_xpath('/html/body/div[2]/div[3]/a').click()
				# page.driver.find_element_by_xpath('/html/body/div[4]/div[3]/a').click()
				return True
			except ec.NoSuchElementException as e:
				raise e.msg
		else:
			return False
