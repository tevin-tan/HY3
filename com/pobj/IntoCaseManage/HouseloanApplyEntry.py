# coding:utf-8

import datetime
import os
import time

from selenium.common import exceptions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

from com import custom
from com.idCardNumber import IdCardNumber as IDCard
from config.locator import loc_cust_info, loc_borrower


class HouseLoanApplyEntry(object):
	"""房贷申请录入"""

	def __init__(self):
		self.log = custom.mylog()

	# self.log.info("房贷申请录入")
	
	def input_customer_base_info(self, page, data, flag=False):
		"""
			客户基本信息录入
		:param page: 浏览器对象
		:param data: 数据字典，录入的基本数据
		:param flag: True, 新产品， False 老产品
		:return:
		"""

		# 案件录入
		time.sleep(2)
		# 进件管理
		self.click_control(page.driver, "id", "1DCDFBEA96010001A2941A801EA02310")

		time.sleep(2)
		self.click_control(page.driver, "name", "/house/commonIndex/applyIndex/index")

		# 主界面
		try:
			# 切换表单(id="myIframe")或者(name="framing")
			page.driver.switch_to_frame("bTabs_tab_house_commonIndex_applyIndex_index")  # 切换到房贷申请录入iframe
		except ec.NoSuchFrameException as e:
			raise e.msg
		try:
			Select(page.driver.find_element_by_xpath(".//*[@id='apply_module_product_id']")).select_by_visible_text(
				data["productName"])  # 产品
		except ec.ElementNotVisibleException as e:
			raise e.msg

		try:
			self._send_data(page.driver, "id", loc_cust_info['je_id'], data["applyAmount"])  # 金额
			self._send_data(page.driver, "id", loc_cust_info['dkts_id'], data["applyPeriod"])  # 贷款天数
			self._send_data(page.driver, "id", loc_cust_info['fgsjlxm_id'], data["branchManager"])  # 分公司经理姓名:
			self._send_data(page.driver, "id", loc_cust_info['fgsjlgh_id'], data["branchManagerCode"])  # 分公司经理工号
			self._send_data(page.driver, "id", loc_cust_info['tdzb_id'], data["teamGroup"])  # 团队组别
			self._send_data(page.driver, "id", loc_cust_info['tdjlxm_id'], data["teamManager"])  # 团队经理姓名
			self._send_data(page.driver, "id", loc_cust_info['tdjlgh_id'], data["teamManagerCode"])  # 团队经理工号
			self._send_data(page.driver, "id", loc_cust_info['khjlxm_id'], data["sale"])  # 客户经理姓名
			self._send_data(page.driver, "id", loc_cust_info['khjlgh_id'], data["saleCode"])  # 客户经理工号
			self._send_data(page.driver, "id", loc_cust_info['lsyjsr_id'], data["monthIncome"])  # 流水月均收入
			self._send_data(page.driver, "name", loc_cust_info['zyyjbz_name'], data["checkApprove"])  # 专员意见备注
			if flag:
				s2 = Select(page.driver.find_element_by_xpath('//*[@id="apply_module_channel_name_key"]'))
				s2.select_by_index(0)
		except ec.NoSuchElementException as e:
			raise e.msg

		# 保存
		self.save(page)
		return True

	def input_customer_borrow_info(self, page, data):
		"""
			客户基本信息 - 借款人/共贷人/担保人信息
		:param page 页面
		:param data 传入的数据
		:return:
		"""

		try:
			self.click_control(page.driver, "xpath", ".//*[@id='tb']/a[1]/span[2]")
			# Update  2017-12-27
			# 姓名元素变更，身份证号码变更
			page.driver.find_element_by_xpath(loc_borrower['jkrxm']).send_keys(data['custName'])  # 借款人姓名
			time.sleep(1)
			self._send_data(page.driver, "xpath", loc_borrower['sfzhm'], data["idNum"])  # 身份证号码
			# 受教育程度
			self.click_control(page.driver, "id", loc_borrower['sjycd']['locate'])
			self.click_control(page.driver, "id", loc_borrower['sjycd']['value'])
			time.sleep(1)
			self.click_control(page.driver, "id", loc_borrower['hyzk']['locate'])  # 婚姻状况

			time.sleep(1)
			self.click_control(page.driver, "id", loc_borrower['hyzk']['value'])

			self._send_data(page.driver, "id", loc_borrower['jtdzxx'], data['address'])  # 家庭地址信息
			self._send_data(page.driver, "xpath", loc_borrower['xxfs'], data["phone"])  # 联系方式
			self._send_data(page.driver, "xpath", loc_borrower['dwmc'], data["companyName"])  # 单位名称

			# 公司规模
			# page.driver.find_element_by_css_selector(loc_borrower['gsgm']['a']).click()
			# page.driver.find_element_by_xpath(loc_borrower['gsgm']['a']).click()
			# self.click_control(page.driver, "xpath", loc_borrower['gsgm']['b'])
			# self.click_control(page.driver, "xpath", loc_borrower['gsgm']['c'])

			# 此处用这个方法
			self.click_control(page.driver, "id", loc_borrower['gsgm']['locate'])
			self.click_control(page.driver, "id", loc_borrower['gsgm']['value'])

			# 所属行业
			self.click_control(page.driver, "id", loc_borrower['sshy']['locate'])
			self.click_control(page.driver, "id", loc_borrower['sshy']['value'])

			self._send_data(page.driver, "id", loc_borrower['zw'], data["postName"])  # 职位
			self._send_data(page.driver, "xpath", loc_borrower['rzrq'], data["workDate"])  # 入职日期
			self._send_data(page.driver, "id", loc_borrower['gzyx'], data['workYear'])  # 工作年限
			self._send_data(page.driver, "id", loc_borrower['yjsr'], data['monthIncoming'])  # 月均收入
			# page.driver.find_element_by_css_selector("input[type=\"checkbox\"]").click()  # 是否有社保
			page.driver.find_element_by_css_selector(
				'#datagrid-row-r1-2-0 > td:nth-child(20) > div > table > tbody > tr > td > input[type="checkbox"]').click()  # 是否有社保

			page.driver.find_element_by_xpath('//*[@id="tb"]/a[3]/span[2]').click()
			# 临时保存
			self.save(page)
			return True
		except ec.NoSuchElementException as e:
			self.log.error(e)
			raise e.msg
		# 申请录入保存

	@staticmethod
	def save(page):
		page.driver.find_element_by_css_selector(
			"#apply_module_apply_save > span.l-btn-left > span.l-btn-text > span.a_text").click()
		time.sleep(1)
		# 弹窗关闭
		page.driver.find_element_by_xpath("html/body/div[2]/div[3]/a").click()  # 确认保存
		time.sleep(1)

	def submit(self, page):
		self.log.info("申请件提交")
		page.driver.find_element_by_id("apply_module_apply_submit").click()
		page.driver.find_element_by_xpath('/html/body/div[2]/div[3]/a[1]').click()
		time.sleep(3)
		page.driver.find_element_by_xpath("html/body/div[2]/div[3]/a").click()

	def click_control(self, driver, how="xpath", locate=None):
		try:
			if self.is_element_present(driver, how, locate):
				driver.find_element(how, locate).click()
				time.sleep(1)
		except ec.NoSuchElementException as e:
			raise e

	def _send_data(self, driver, how, locate="xpath", value=None):
		try:
			if self.is_element_present(driver, how, locate):
				element = driver.find_element(how, locate)
				element.clear()
				element.click()
				element.send_keys(value)
				time.sleep(1)
		except ec.NoSuchElementException as e:
			raise e

	@staticmethod
	def is_element_present(driver, how, what):
		try:
			driver.find_element(by=how, value=what)
		except ec.NoSuchElementException as e:
			print(e.msg)
			return False
		return True

	def input_all_bbi_property_info(
			self, page, data, apply_cust_credit_info, name, associated=False,
			product_name=None):
		"""
			物业信息录入
		:param page: 页面对象
		:param data: 传入的数据对象
		:param apply_cust_credit_info: 征信数据
		:param name: 客户姓名
		:param associated  关联世联
		:param product_name 过桥通 / 非过桥通
		:return:
		"""

		# 这步骤很关键，没有选中，则定位不到下面的元素
		try:
			t1 = page.driver.find_element_by_class_name("house-head-line")
			t1.click()
			page.driver.execute_script("window.scrollTo(1600, 0)")  # 页面滑动到顶部
			page.driver.find_element_by_link_text(u"业务基本信息").click()
		except ec.ElementNotVisibleException as e:
			self.log.error(e.msg)
			return False
		try:
			page.driver.find_element_by_name("propertyOwner").clear()
			page.driver.find_element_by_name("propertyOwner").send_keys(name)  # 产权人
			page.driver.find_element_by_name("propertyNo").clear()
			page.driver.find_element_by_name("propertyNo").send_keys(data['propertyNo'])  # 房产证号

			time.sleep(2)
			page.driver.find_element_by_name("propertyStatus").click()  # 是否涉贷物业

			page.driver.find_element_by_name("propertyAge").click()
			page.driver.find_element_by_name("propertyAge").clear()
			page.driver.find_element_by_name("propertyAge").send_keys(data['propertyAge'])  # 房龄

			page.driver.find_element_by_name("propertyArea").clear()
			page.driver.find_element_by_name("propertyArea").send_keys(data['propertyArea'])  # 建筑面积

			page.driver.find_element_by_name("registrationPrice").clear()
			page.driver.find_element_by_name("registrationPrice").send_keys(data['registrationPrice'])  # 等级价

			# 地址
			Select(page.driver.find_element_by_name("propertyAddressProvince")).select_by_visible_text(
				data['propertyAddressProvince'])
			Select(page.driver.find_element_by_name("propertyAddressCity")).select_by_visible_text(
				data['propertyAddressCity'])
			Select(page.driver.find_element_by_name("propertyAddressDistinct")).select_by_visible_text(
				data['propertyAddressDistinct'])
			page.driver.find_element_by_id("propertyAddressDetail").clear()
			page.driver.find_element_by_id("propertyAddressDetail").send_keys(data['propertyAddressDetails'])

			page.driver.find_element_by_name("evaluationSumAmount").clear()
			page.driver.find_element_by_name("evaluationSumAmount").send_keys(data['evaluationSumAmount'])  # 评估公允价总值
			page.driver.find_element_by_name("evaluationNetAmount").clear()
			page.driver.find_element_by_name("evaluationNetAmount").send_keys(data['evaluationNetAmount'])  # 评估公允价净值
			page.driver.find_element_by_name("slSumAmount").clear()
			page.driver.find_element_by_name("slSumAmount").send_keys(data['slSumAmount'])  # 世联评估总值
			page.driver.find_element_by_name("slPrice").clear()
			page.driver.find_element_by_name("slPrice").send_keys(data['slPrice'])  # 世联评估净值
			page.driver.find_element_by_name("agentSumAmout").clear()
			page.driver.find_element_by_name("agentSumAmout").send_keys(data['agentSumAmout'])  # 中介评估总值
			page.driver.find_element_by_name("agentNetAmount").clear()
			page.driver.find_element_by_name("agentNetAmount").send_keys(data['agentNetAmount'])  # 中介评估净值
			page.driver.find_element_by_name("netSumAmount").clear()
			page.driver.find_element_by_name("netSumAmount").send_keys(data['netSumAmount'])  # 网评总值
			page.driver.find_element_by_name("netAmount").clear()
			page.driver.find_element_by_name("netAmount").send_keys(data['netAmount'])  # 网评净值
			page.driver.find_element_by_name("localSumAmount").clear()
			page.driver.find_element_by_name("localSumAmount").send_keys(data['localSumAmount'])  # 当地评估总值
			page.driver.find_element_by_name("localNetValue").clear()
			page.driver.find_element_by_name("localNetValue").send_keys(data['localNetValue'])  # 当地评估净值
			page.driver.find_element_by_name("remark").clear()
			page.driver.find_element_by_name("remark").send_keys(data['remark'])  # 物业配套描述
			page.driver.find_element_by_name("localAssessmentOrigin").clear()
			page.driver.find_element_by_name("localAssessmentOrigin").send_keys(data['localAssessmentOrigin'])  # 当地评估来源
			page.driver.find_element_by_name("assessmentOrigin").clear()
			page.driver.find_element_by_name("assessmentOrigin").send_keys(data['assessmentOrigin'])  # 评估来源
			page.driver.find_element_by_name("localAssessmentOrigin").clear()
			page.driver.find_element_by_name("localAssessmentOrigin").send_keys(data['localAssessmentOrigin'])

			page.driver.find_element_by_name("evaluationCaseDescrip").clear()
			page.driver.find_element_by_name("evaluationCaseDescrip").send_keys(data['evaluationCaseDescrip'])  # 评估情况描述

			if associated:
				page.driver.find_element_by_link_text('关联').click()
				time.sleep(1)
				# page.driver.find_element_by_id('evaRalationModal').click()

				try:
					page.driver.find_element_by_xpath('//*[@id="evaRalationModal"]').click()
					assert page.driver.find_element_by_id('myModalLabel').text == '世联关联列表'
					page.driver.find_element_by_id('admitsSearchForm').click()
				except ec.ElementNotVisibleException as e:
					raise e.msg
				# 硬关联
				t3 = page.driver.find_element_by_xpath('//*[@id="evaRalationModal"]/div/div/div[2]')
				ActionChains(page.driver).double_click(t3).perform()
			# # 搜索条件
			# page.driver.find_element_by_name('cityName').send_keys(u'长沙市')
			# page.driver.find_element_by_name('constructionName').send_keys(u'金帆小区')
			# page.driver.find_element_by_name('buildingName').send_keys('10')
			# page.driver.find_element_by_name('houseName').send_keys('101')
			# # 查询
			# page.driver.find_element_by_xpath('//*[@id="admitsSearchForm"]/div[6]/button[1]').click()
			# time.sleep(1)
			# page.driver.find_element_by_xpath(
			# 	'//*[@id="evaRalationModal"]/div/div/div[2]/div[2]/div/div/div[1]/div[2]/div[2]/table').click()
			# page.driver.find_element_by_id('evaRalationBtn').click()
			# time.sleep(1)
			time.sleep(2)
			# 征信信息
			page.driver.find_element_by_link_text("征信信息").click()
			page.driver.find_element_by_name("loanIdNum").clear()
			page.driver.find_element_by_name("loanIdNum").send_keys(apply_cust_credit_info['loanIdNum'])
			page.driver.find_element_by_name("creditOverdueNum").clear()
			page.driver.find_element_by_name("creditOverdueNum").send_keys(apply_cust_credit_info['creditOverdueNum'])
			page.driver.find_element_by_name("queryLoanNum").clear()
			page.driver.find_element_by_name("queryLoanNum").send_keys(apply_cust_credit_info['queryLoanNum'])
			page.driver.find_element_by_name("loanOtherAmt").clear()
			page.driver.find_element_by_name("loanOtherAmt").send_keys(apply_cust_credit_info['loanOtherAmt'])

			if product_name == 'gqt':
				page.driver.find_element_by_link_text("垫资情况").click()
				# 基本情况
				Select(page.driver.find_element_by_name("loaningType")).select_by_value("DA01")
				page.driver.find_element_by_name('oldBankBranch').send_keys(u"南山科技园支行")
				page.driver.find_element_by_name('oldBankPhone').send_keys('13801349321')
				page.driver.find_element_by_name('oldBankManager').send_keys(u"朱小通")
				page.driver.find_element_by_name('newBankBranch').send_keys(u'民治支行')
				page.driver.find_element_by_name('newBankManager').send_keys(u'易健')
				page.driver.find_element_by_name('newBankPhone').send_keys('13901234123')
				# 贷款情况
				page.driver.find_element_by_link_text('贷款情况').click()
				page.driver.find_element_by_name('validDate').send_keys('2020-01-01')
				page.driver.find_element_by_name('bankAppRemark').send_keys(u'无异常')
				page.driver.find_element_by_name('checkAppCondition').send_keys(u'无异常')
				page.driver.find_element_by_name('paymentAccount').send_keys('121334')
				# 交易情况
				page.driver.find_element_by_link_text('交易情况').click()
				page.driver.find_element_by_name('tradeDate').send_keys('2018-01-01')
				page.driver.find_element_by_name('tradeSumAmount').send_keys('1000000')
				page.driver.find_element_by_name('deposit').send_keys('800000')
				page.driver.find_element_by_name('fundSupervisionAmount').send_keys('800000')

			# 网查信息
			page.driver.find_element_by_link_text(u"网查信息").click()
			page.driver.find_element_by_class_name("remark").click()
			p1 = page.driver.find_element_by_xpath("//*[@id='apply_module_check_data_form']/div/div/textarea")
			p1.click()
			p1.send_keys(u"哈哈哈哈哈，无异常")

			# 借款用途及回款来源
			page.driver.find_element_by_link_text(u"借款用途及回款来源").click()
			page.driver.find_element_by_id("apply_module_payment_source").send_keys(u"薪资回款")
			p2 = page.driver.find_element_by_xpath("//*[@id=\"apply_module_remark\"]")
			p2.click()
			p2.send_keys(u"无异常")

			# 风控措施
			page.driver.find_element_by_link_text(u"风控措施").click()
			page.driver.find_element_by_name("riskRemark").click()
			page.driver.find_element_by_name("riskRemark").send_keys(u"无异常")
			# 保存
			self.save(page)
			return True
		except ec.NoSuchElementException as e:
			self.log.error(e.msg)
			return False

	def upload_image_file(self, page, exe, image, delete=None):
		"""
		上传影像资料
		:param page:
		:param exe: 可执行文件
		:param image: 上传文件
		:param delete: 是否删除图片
		:return:
		"""

		self.log.info("开始上传影像资料")
		try:
			page.driver.find_element_by_link_text("影像资料").click()
			try:
				page.driver.switch_to_frame('myIframeImages')
			except ec.NoSuchFrameException as msg:
				raise msg
			# upload
			page.driver.find_element_by_class_name('img_upload_area').click()
			page.driver.find_element_by_id('browse').click()
			os.system(exe + " " + image)
			# os.system('E:\\HouseLoanAutoPy3\\bin\\uploadtool.exe "E:\\HouseLoanAutoPy3\\image\\2.jpg"')

			# Todo 图片名称随机变动，不好处理
			if delete:
				t_time = custom.get_current_day()[0]
				t_s = t_time.split(":")[0].replace("-", "/").replace(" ", "/")
				print(t_s)
				# match_str = '//*[starts-with(@id, "signPersonForm")]/'
				jpg_name = '//*[ends-with(@id, "jpg")]'
				# jpg_name = 'substring(@id, string-length(@id) - string-length("jpg") +1) = "jpg"'

				se = page.driver.find_element_by_xpath(
					'//*[@id="checkhttp://uat-img.xnph66.com/AttachFiles/loanbefore/' + t_s + jpg_name)
				# se = page.driver.find_element_by_xpath(jpg_name)
				se.click()
				# delete image
				page.driver.find_element_by_id('deleteItems').click()
				# confirm
				page.driver.find_element_by_xpath('/html/body/div[2]/div[3]/a[1]').click()
			return True
		except ec.NoSuchElementException as msg:
			raise ValueError(msg)
		finally:
			time.sleep(1)
			page.driver.switch_to.parent_frame()

	def input_more_borrower(self, page):
		"""
		客户基本信息 - 借款人/共贷人/担保人信息
		:param page 页面
		"""
		self.log.info("录入多个借款人")
		try:
			page.driver.find_element_by_xpath('//*[@id="tb"]/a[1]/span[2]').click()
			# NAME
			page.driver.find_element_by_xpath(
				'//*[@id="datagrid-row-r1-2-1"]/td[5]/div/table/tbody/tr/td/input').send_keys(custom.get_name())
			time.sleep(1)
			# IDNUMBER
			page.driver.find_element_by_xpath(
				'//*[@id="datagrid-row-r1-2-1"]/td[6]/div/table/tbody/tr/td/input').send_keys(
				IDCard.getRandomIdNumber()[0])
			time.sleep(1)
			# 受教育程度
			page.driver.find_element_by_id('_easyui_textbox_input14').click()
			page.driver.find_element_by_id('_easyui_combobox_i8_2').click()
			# 婚姻状况
			page.driver.find_element_by_id('_easyui_textbox_input15').click()
			page.driver.find_element_by_id('_easyui_combobox_i9_0').click()
			# 家庭住址信息
			page.driver.find_element_by_id('_easyui_textbox_input16').send_keys(IDCard.getRandomIdNumber()[1])
			# 联系方式
			page.driver.find_element_by_xpath(
				'//*[@id="datagrid-row-r1-2-1"]/td[11]/div/table/tbody/tr/td/input').send_keys(
				IDCard.create_phone())
			time.sleep(1)
			# 单位名称
			page.driver.find_element_by_xpath(
				'//*[@id="datagrid-row-r1-2-1"]/td[12]/div/table/tbody/tr/td/input').send_keys("小牛资本投资股份有限公司")
			time.sleep(1)
			# 公司规模
			page.driver.find_element_by_id('_easyui_textbox_input17').click()
			page.driver.find_element_by_id('_easyui_combobox_i10_3').click()
			# 所属行业
			page.driver.find_element_by_id('_easyui_textbox_input18').click()
			page.driver.find_element_by_id('_easyui_combobox_i11_2').click()
			# 职位
			page.driver.find_element_by_id('_easyui_textbox_input20').send_keys("总裁助理")
			# 入职日期
			page.driver.find_element_by_xpath(
				'//*[@id="datagrid-row-r1-2-1"]/td[17]/div/table/tbody/tr/td/input').send_keys(
				str(datetime.date.today()))
			time.sleep(1)
			# 工作年限
			page.driver.find_element_by_id('_easyui_textbox_input21').send_keys(12)
			time.sleep(1)
			# 月均收入
			page.driver.find_element_by_id('_easyui_textbox_input22').send_keys(20000)
			time.sleep(1)
			# 是否有社保
			page.driver.find_element_by_xpath(
				'//*[@id="datagrid-row-r1-2-1"]/td[20]/div/table/tbody/tr/td/input').click()
			time.sleep(1)
			page.driver.find_element_by_xpath(
				'//*[@id="datagrid-row-r1-2-1"]/td[21]/div/table/tbody/tr/td/input').click()
			# 确认
			page.driver.find_element_by_xpath('//*[@id="tb"]/a[3]/span[2]').click()
		except ec.NoSuchElementException as e:
			raise e.msg

		# ----------------------------------------------------------------------
		#                       关联关系信息
		# ----------------------------------------------------------------------
		try:
			page.driver.find_element_by_xpath('//*[@id="tbs"]/a[1]').click()

			page.driver.find_element_by_id('_easyui_textbox_input23').click()
			page.driver.find_element_by_id('_easyui_combobox_i12_0').click()

			page.driver.find_element_by_id('_easyui_textbox_input24').click()
			page.driver.find_element_by_id('_easyui_combobox_i13_1').click()

			page.driver.find_element_by_id('_easyui_textbox_input25').click()
			page.driver.find_element_by_id('_easyui_combobox_i14_0').click()

			# 确认
			page.driver.find_element_by_xpath('//*[@id="tbs"]/a[3]').click()

			# 保存
			page.driver.find_element_by_id('apply_module_apply_save').click()
			page.driver.find_element_by_xpath('/html/body/div[2]/div[3]/a').click()
		except ec.NoSuchElementException as e:
			raise e.msg
