# coding:utf-8
import os
import time

from selenium.common import exceptions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

from com import custom
from com.pobj.IntoCaseManage import HouseloanApplyEntry as Hae


class PendingTask(object):
	"""待处理任务"""
	
	def __init__(self):
		self.log = custom.mylog()
		self.HAE = Hae.HouseLoanApplyEntry()
	
	def query_task(self, page, condition):
		"""
			查询待处理任务
		:param page: 页面对象
		:param condition: applyCode
		:return: True/False
		"""
		
		self.log.info("查询查处理任务")
		
		try:
			page.driver.switch_to_default_content()
			# 打开任务中心
			time.sleep(1)
			page.driver.find_element_by_id('1DBCBC52791800014989140019301189').click()
			time.sleep(1)
			page.driver.find_element_by_name("/house/commonIndex/todoList").click()
			
			try:
				page.driver.switch_to_frame("bTabs_tab_house_commonIndex_todoList")
			except ec.NoSuchFrameException as e:
				raise e
			# 打开表单
			time.sleep(2)
			page.driver.find_element_by_id("frmQuery").click()
			# 选定申请编号搜索框
			page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").click()
			# 输入申请编号
			page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys(condition)
			# 点击查询按钮
			page.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/a[1]/span").click()
			time.sleep(2)
			t1 = page.driver.find_element_by_xpath('//*[@id="datagrid-row-r2-2-0"]/td[3]')
			if not t1.text:
				return False
			else:
				return True
		except ec.NoSuchFrameException as e:
			raise e
		finally:
			page.driver.quit()
	
	def approval_to_review(self, page, condition, remark, action=0, image=False):
		"""
			审批审核
		:param page:    页面对象
		:param condition:   applyCode
		:param remark:  审批审核意见
		:param action   0 通过， 1 回退， 2 取消， 3 拒绝
		:param image True 上传，False 不上传
		:return:
		"""
		# 打开任务中心
		page.driver.find_element_by_id('1DBCBC52791800014989140019301189').click()
		time.sleep(2)
		# 待处理任务
		page.driver.find_element_by_name("/house/commonIndex/todoList").click()
		time.sleep(2)
		# 切换iframe 待处理任务
		page.driver.switch_to_frame("bTabs_tab_house_commonIndex_todoList")
		#  打开表单
		time.sleep(1)
		page.driver.find_element_by_id("frmQuery").click()
		# 选定申请编号搜索框
		page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").click()
		# 输入申请编号
		time.sleep(1)
		page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys(condition)
		# 点击查询按钮
		page.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/a[1]/span").click()
		time.sleep(1)
		t1 = page.driver.find_element_by_xpath("//*[@id='datagrid-row-r2-2-0']/td[3]")
		time.sleep(2)
		if not t1.text:
			return False
		else:
			t1.click()
			time.sleep(1)
			page.driver.find_element_by_class_name("datagrid-btable").click()
			# 双击该笔案件
			ActionChains(page.driver).double_click(t1).perform()
			time.sleep(1)
			
			if action == 0:
				# 填写批核意见
				page.driver.find_element_by_class_name("container-fluid").click()
				time.sleep(1)
				page.driver.find_element_by_xpath("//*[@id=\"approve_opinion_form\"]/div[5]/div[2]").click()
				page.driver.find_element_by_xpath("//*[@id=\"remarkable\"]").send_keys(remark)
				if image:
					self.HAE.upload_image_file(
							page, "E:\\HouseLoanAutoPy3\\bin\\uploadtool.exe",
							"E:\\HouseLoanAutoPy3\\image\\2.jpg")
			elif action == 1:
				# 回退
				Select(page.driver.find_element_by_name("appResult")).select_by_visible_text(u"回退")
				Select(page.driver.find_element_by_name("nextActivitiId")).select_by_visible_text(u"风控专员录入")
				# 填写回退意见
				page.driver.find_element_by_id('remarkable2').send_keys(remark)
			elif action == 2:
				# 取消
				Select(page.driver.find_element_by_name("appResult")).select_by_visible_text(u"取消")
				Select(page.driver.find_element_by_name("resultReasonId")).select_by_value("02")
				# 填写意见
				page.driver.find_element_by_id('remarkable2').send_keys(remark)
			elif action == 3:
				# 拒绝
				Select(page.driver.find_element_by_name("appResult")).select_by_visible_text(u"拒绝")
				Select(page.driver.find_element_by_name("resultReasonId")).select_by_value("01")
				# 填写意见
				page.driver.find_element_by_id('remarkable2').send_keys(remark)
			else:
				self.log.error("输入的参数有误(0-3)!")
				raise ValueError('参数有误！')
			
			# 保存
			page.driver.find_element_by_xpath("//*[@id=\"apply_module_apply_save\"]/span/span/span[2]").click()
			time.sleep(1)
			page.driver.find_element_by_xpath("/html/body/div[5]/div[3]/a/span/span").click()  # 关闭弹窗
			
			# 提交
			page.driver.find_element_by_xpath("//*[@id='apply_module_apply_submit']/span/span/span[2]").click()
			time.sleep(1)
			page.driver.find_element_by_xpath('/html/body/div[5]/div[3]/a[1]').click()
			time.sleep(2)
			page.driver.find_element_by_xpath("/html/body/div[5]/div[3]/a").click()
			return True
	
	def special_approval(self, page, condition, remark):
		"""
		风控审批审核（特批）
		:param page:    页面对象
		:param condition:   applyCode
		:param remark:  审批审核意见
		:return:
		"""
		self.log.info("开始特批审核")
		try:
			# 打开任务中心
			page.driver.find_element_by_id("1DBCBC52791800014989140019301189").click()
			time.sleep(2)
			# 待处理任务
			page.driver.find_element_by_name("/house/commonIndex/todoList").click()
			time.sleep(2)
			try:
				page.driver.switch_to.frame("bTabs_tab_house_commonIndex_todoList")
			except ec.NoSuchFrameException as e:
				raise e
			
			# 打开表单
			time.sleep(1)
			page.driver.find_element_by_id("frmQuery").click()
			# 选定申请编号搜索框
			page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").click()
			# 输入申请编号
			time.sleep(1)
			page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys(condition)
			# 点击查询按钮
			page.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/a[1]/span").click()
			time.sleep(1)
			t1 = page.driver.find_element_by_xpath("//*[@id='datagrid-row-r2-2-0']/td[3]")
			time.sleep(2)
			if not t1.text:
				return False
			else:
				t1.click()
				time.sleep(1)
				page.driver.find_element_by_class_name("datagrid-btable").click()
				# 双击该笔案件
				ActionChains(page.driver).double_click(t1).perform()
				time.sleep(1)
				# 特批
				page.driver.find_element_by_xpath('//*[@id="approve_opinion_form"]/div[2]/div[5]/input').click()
				
				# 填写批核意见
				page.driver.find_element_by_class_name("container-fluid").click()
				time.sleep(1)
				page.driver.find_element_by_xpath("//*[@id=\"approve_opinion_form\"]/div[5]/div[2]").click()
				page.driver.find_element_by_xpath("//*[@id=\"remarkable\"]").send_keys(remark)
				
				# 保存
				page.driver.find_element_by_xpath("//*[@id=\"apply_module_apply_save\"]/span/span/span[2]").click()
				time.sleep(1)
				page.driver.find_element_by_xpath("/html/body/div[5]/div[3]/a/span/span").click()  # 关闭弹窗
				
				# 提交
				page.driver.find_element_by_xpath("//*[@id='apply_module_apply_submit']/span/span/span[2]").click()
				time.sleep(2)
				page.driver.find_element_by_xpath('/html/body/div[5]/div[3]/a[1]').click()
				time.sleep(2)
				page.driver.find_element_by_xpath("/html/body/div[5]/div[3]/a").click()
				return True
		except ec.NoSuchElementException as e:
			raise e
	
	def risk_approval_fallback(self, page, condition, option, remark):
		"""
		风控审批回退
		:param page:    页面对象
		:param condition:   applyCode
		:param option:   风控审批员列表
		:param remark:  审批审核意见
		:return:
		"""
		
		self.log.info("开始执行风控审批回退操作")
		try:
			# 打开任务中心
			page.driver.find_element_by_id('1DBCBC52791800014989140019301189').click()
			time.sleep(2)
			# 待处理任务
			page.driver.find_element_by_name("/house/commonIndex/todoList").click()
			time.sleep(2)
			try:
				page.driver.switch_to.frame("bTabs_tab_house_commonIndex_todoList")
			except ec.NoSuchFrameException as e:
				raise e
			# 打开表单
			time.sleep(1)
			page.driver.find_element_by_id("frmQuery").click()
			# 选定申请编号搜索框
			page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").click()
			# 输入申请编号
			time.sleep(1)
			page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys(condition)
			# 点击查询按钮
			page.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/a[1]/span").click()
			time.sleep(1)
			t1 = page.driver.find_element_by_xpath("//*[@id='datagrid-row-r2-2-0']/td[3]")
			time.sleep(2)
		except ec.NoSuchElementException as e:
			raise e
		if not t1.text:
			return False
		else:
			t1.click()
			time.sleep(1)
			try:
				page.driver.find_element_by_class_name("datagrid-btable").click()
				# 双击该笔案件
				ActionChains(page.driver).double_click(t1).perform()
				time.sleep(1)
				
				# 回退
				Select(page.driver.find_element_by_name("appResult")).select_by_visible_text(u"回退")
				Select(page.driver.find_element_by_name("nextActivitiId")).select_by_visible_text(option)
				# 填写回退意见
				page.driver.find_element_by_id('remarkable2').send_keys(remark)
				
				# 保存
				page.driver.find_element_by_xpath("//*[@id=\"apply_module_apply_save\"]/span/span/span[2]").click()
				time.sleep(1)
				page.driver.find_element_by_xpath("/html/body/div[5]/div[3]/a/span/span").click()  # 关闭弹窗
				
				# 提交
				page.driver.find_element_by_xpath("//*[@id='apply_module_apply_submit']/span/span/span[2]").click()
				time.sleep(2)
				page.driver.find_element_by_xpath('/html/body/div[5]/div[3]/a[1]').click()
				time.sleep(2)
				page.driver.find_element_by_xpath("/html/body/div[5]/div[3]/a").click()
				return True
			except ec.NoSuchElementException as e:
				raise e
	
	@staticmethod
	def task_search(page, condition):
		"""
			待处理任务查询
		:param page: 页面
		:param condition:  applyCode
		:return: 查询表格数据
		"""
		
		try:
			# 打开任务中心
			page.driver.find_element_by_id('1DBCBC52791800014989140019301189').click()
			time.sleep(2)
			# 待处理任务
			page.driver.find_element_by_name("/house/commonIndex/todoList").click()
			time.sleep(2)
		except ec.NoSuchElementException as e:
			raise e
		try:
			page.driver.switch_to_frame('bTabs_tab_house_commonIndex_todoList')
		except ec.NoSuchFrameException as e:
			raise e
		try:
			page.driver.find_element_by_id("frmQuery").click()
			time.sleep(1)
			# 选定申请编号搜索框
			page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").click()
			# 输入申请编号
			time.sleep(1)
			page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys(condition)
			# 点击查询按钮
			page.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/a[1]/span").click()
			time.sleep(1)
			res = page.driver.find_element_by_xpath("//*[@id='datagrid-row-r2-2-0']/td[3]")
			return res
		except ec.NoSuchElementException as e:
			raise e
	
	def compliance_audit(self, page, condition, upload=False):
		"""
		合规审查
		:param page: 页面对象
		:param condition: applyCode
		:param upload : True/False 是否上传影像
		:return:
		"""
		
		# 查询待处理任务
		t1 = self.task_search(page, condition)
		if not t1.text:
			self.log.error("can't found the task in the taskList")
			return False
		else:
			t1.click()
			# 双击该笔案件
			ActionChains(page.driver).double_click(t1).perform()
			page.driver.switch_to_frame("myIframeImage1")
			# 个人信息
			for i in range(1, 4):
				time.sleep(1)
				page.driver.find_element_by_xpath(
						'//*[@id="listVue"]/div[1]/form/div[' + str(i) + ']/div/div[3]/input').click()
			# 征信信息
			for i in range(1, 3):
				time.sleep(1)
				page.driver.find_element_by_xpath(
						'//*[@id="listVue"]/div[2]/form/div[' + str(i) + ']/div/div[3]/input').click()
			# 房贷信息
			for i in range(1, 3):
				time.sleep(1)
				page.driver.find_element_by_xpath(
						'//*[@id="listVue"]/div[3]/form/div[' + str(i) + ']/div/div[3]/input').click()
			# 贷款银行信息
			for i in range(1, 3):
				time.sleep(1)
				page.driver.find_element_by_xpath(
						'//*[@id="listVue"]/div[4]/form/div[' + str(i) + ']/div/div[3]/input').click()
		
		page.driver.switch_to.parent_frame()
		if upload is not False:
			try:
				page.driver.find_element_by_link_text("影像资料").click()
				try:
					page.driver.switch_to_frame('myIframeImage5')
				except ec.NoSuchFrameException as msg:
					raise msg
				# upload
				page.driver.find_element_by_class_name('img_upload_area').click()
				page.driver.find_element_by_id('browse').click()
				os.system("E:\\HouseLoanAutoPy3\\bin\\uploadtool.exe" + " " + "E:\\HouseLoanAutoPy3\\image\\2.jpg")
			except ec.NoSuchElementException as msg:
				raise ValueError(msg)
			finally:
				time.sleep(1)
				page.driver.switch_to.parent_frame()
		# 保存
		self.save(page)
		time.sleep(2)
		# 提交
		self.submit(page)
		time.sleep(2)
		page.driver.quit()
		return True
	
	@staticmethod
	def save(page):
		page.driver.find_element_by_xpath('//*[@id="apply_module_apply_save"]').click()
		page.driver.find_element_by_xpath(' /html/body/div[4]/div[3]/a').click()
	
	@staticmethod
	def submit(page):
		page.driver.find_element_by_xpath('//*[@id="apply_module_apply_submit"]').click()
		page.driver.find_element_by_xpath('/html/body/div[4]/div[3]/a').click()
	
	def part_warrant_apply(self, page, condition, flag=0):
		"""
			部分权证请款
		:param page: 页面对象
		:param condition:   applyCode
		:param flag
		:return:
		"""
		
		# 打开任务中心
		t1 = self.task_search(page, condition)
		if not t1.text:
			return False
		else:
			t1.click()
			# 双击
			ActionChains(page.driver).double_click(t1).perform()
			try:
				page.driver.switch_to_frame("myIframeImage1")  # 切换iframe
			except ec.NoSuchFrameException as e:
				raise e
			
			try:
				if flag == 0:
					# 第一次权证请款
					page.driver.find_element_by_xpath('//*[@id="warrantInfo"]/div[2]/div/input[4]').click()
					page.driver.find_element_by_id('splitLoanMoney').click()
					time.sleep(1)
					# 请款拆分明细
					page.driver.find_element_by_xpath('//*[@id="warrantSplitModel"]/div').click()
					time.sleep(1)
					page.driver.find_element_by_xpath(
							'//*[@id="warrantForm"]/div/table/tbody/tr[1]/td[1]/input').click()
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
				else:
					# save
					page.driver.switch_to.parent_frame()
					page.driver.find_element_by_id('second_warrant_save').click()
					page.driver.find_element_by_xpath('/html/body/div[2]/div[3]/a').click()
					time.sleep(1)
					# submit
					page.driver.find_element_by_id('second_warrant_apply').click()
					time.sleep(1)
					page.driver.find_element_by_xpath('/html/body/div[2]/div[3]/a[1]').click()
				
				return True
			except ec.NoSuchElementException as e:
				raise e
	
	def receipt_return(self, page, apply_code):
		"""
		回执提放审批审核
		:param page:
		:param apply_code:
		:return:
		"""
		
		t1 = self.task_search(page, apply_code)
		if not t1.text:
			return False
		else:
			t1.click()
			ActionChains(page.driver).double_click(t1).perform()
			try:
				page.driver.switch_to_frame("myIframeImage1")  # 切换iframe
			except ec.NoSuchFrameException as e:
				raise e
		page.driver.find_element_by_xpath('//*[@id="checkOpinion"]/textarea').send_keys("回执提放审批")
		# save
		page.driver.switch_to.parent_frame()
		page.driver.find_element_by_id("warrant_request_save").click()
		page.driver.find_element_by_xpath("/html/body/div[2]/div[3]/a").click()
		time.sleep(1)
		# submit
		page.driver.find_element_by_id('warrant_request_submit').click()
		page.driver.find_element_by_xpath('/html/body/div[2]/div[3]/a[1]').click()
		time.sleep(1)
		return True
