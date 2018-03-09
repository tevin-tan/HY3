# coding:utf-8

"""
    通用方法
"""
import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from config.locator import loc_cust_info, loc_borrower
from selenium.common import exceptions as ec
from com.custom import get_name, mylog
from com import custom
# import common.getIdNumber as GT
from com.idCardNumber import IdCardNumber as IDCard

import datetime


def browser(arg="chrome"):
	"""
		 浏览器选择
	:param 默认chrome
	:return:
	"""
	
	if arg == "ie":
		driver = webdriver.Ie()
	elif arg == "chrome":
		driver = webdriver.Chrome()
	elif arg == "firefox":
		driver = webdriver.Firefox()
	else:
		raise ValueError("Can't support the kind of borrower!")
	
	return driver


def input_customer_base_info(page, data):
	"""
		客户基本信息录入
	:param page: 浏览器对象
	:param data: 数据字典，录入的基本数据
	:return:
	"""
	
	# 案件录入
	time.sleep(2)
	# 进件管理
	page._click_control(page.driver, "id", "1DCDFBEA96010001A2941A801EA02310")
	
	time.sleep(2)
	page._click_control(page.driver, "name", "/house/commonIndex/applyIndex/index")
	
	# 主界面
	try:
		# 切换表单(id="myIframe")或者(name="framing")
		# page.driver.switch_to.frame("myIframe") #切换到第一个frame
		page.driver.switch_to.frame("bTabs_tab_house_commonIndex_applyIndex_index")  # 切换到房贷申请录入iframe
	except ec.NoSuchFrameException as e:
		raise e.msg
	try:
		Select(page.driver.find_element_by_xpath(".//*[@id='apply_module_product_id']")).select_by_visible_text(
				data["productName"])  # 产品
	except ec.ElementNotVisibleException as e:
		raise e.msg
	
	try:
		page._send_data(page.driver, "id", loc_cust_info['je_id'], data["applyAmount"])  # 金额
		page._send_data(page.driver, "id", loc_cust_info['dkts_id'], data["applyPeriod"])  # 贷款天数
		page._send_data(page.driver, "id", loc_cust_info['fgsjlxm_id'], data["branchManager"])  # 分公司经理姓名:
		page._send_data(page.driver, "id", loc_cust_info['fgsjlgh_id'], data["branchManagerCode"])  # 分公司经理工号
		page._send_data(page.driver, "id", loc_cust_info['tdzb_id'], data["teamGroup"])  # 团队组别
		page._send_data(page.driver, "id", loc_cust_info['tdjlxm_id'], data["teamManager"])  # 团队经理姓名
		page._send_data(page.driver, "id", loc_cust_info['tdjlgh_id'], data["teamManagerCode"])  # 团队经理工号
		page._send_data(page.driver, "id", loc_cust_info['khjlxm_id'], data["sale"])  # 客户经理姓名
		page._send_data(page.driver, "id", loc_cust_info['khjlgh_id'], data["saleCode"])  # 客户经理工号
		page._send_data(page.driver, "id", loc_cust_info['lsyjsr_id'], data["monthIncome"])  # 流水月均收入
		page._send_data(page.driver, "name", loc_cust_info['zyyjbz_name'], data["checkApprove"])  # 专员意见备注
	except ec.NoSuchElementException as e:
		raise e.msg
	
	# 保存
	save(page)
	return True


def input_customer_borrow_info(page, data):
	"""
		客户基本信息 - 借款人/共贷人/担保人信息
	:param page 页面
	:param data 传入的数据
	:return:
	"""
	# custname = get_name()
	try:
		page._click_control(page.driver, "xpath", ".//*[@id='tb']/a[1]/span[2]")
		# Update  2017-12-27
		# 姓名元素变更，身份证号码变更
		page.driver.find_element_by_xpath(loc_borrower['jkrxm']).send_keys(data['custName'])  # 借款人姓名
		time.sleep(1)
		page._send_data(page.driver, "xpath", loc_borrower['sfzhm'], data["idNum"])  # 身份证号码
		# page._send_data(page.driver, "xpath", loc_borrower['sfzhm'], IDCard.getRandomIdNumber()[0])  # 身份证号码
		# 受教育程度
		page._click_control(page.driver, "id", loc_borrower['sjycd']['locate'])
		page._click_control(page.driver, "id", loc_borrower['sjycd']['value'])
		time.sleep(1)
		page._click_control(page.driver, "id", loc_borrower['hyzk']['locate'])  # 婚姻状况
		
		time.sleep(1)
		page._click_control(page.driver, "id", loc_borrower['hyzk']['value'])
		
		page._send_data(page.driver, "id", loc_borrower['jtdzxx'], data['address'])  # 家庭地址信息
		# page._send_data(page.driver, "id", loc_borrower['jtdzxx'], IDCard.getRandomIdNumber()[1])  # 家庭地址信息
		page._send_data(page.driver, "xpath", loc_borrower['xxfs'], data["phone"])  # 联系方式
		# page._send_data(page.driver, "xpath", loc_borrower['xxfs'], IDCard.createPhone())  # 联系方式
		page._send_data(page.driver, "xpath", loc_borrower['dwmc'], data["companyName"])  # 单位名称
		
		# 公司规模
		# page.driver.find_element_by_css_selector(loc_borrower['gsgm']['a']).click()
		# page.driver.find_element_by_xpath(loc_borrower['gsgm']['a']).click()
		# page._click_control(page.driver, "xpath", loc_borrower['gsgm']['b'])
		# page._click_control(page.driver, "xpath", loc_borrower['gsgm']['c'])
		
		# 此处用这个方法
		page._click_control(page.driver, "id", loc_borrower['gsgm']['locate'])
		page._click_control(page.driver, "id", loc_borrower['gsgm']['value'])
		
		# 所属行业
		page._click_control(page.driver, "id", loc_borrower['sshy']['locate'])
		page._click_control(page.driver, "id", loc_borrower['sshy']['value'])
		
		page._send_data(page.driver, "id", loc_borrower['zw'], data["postName"])  # 职位
		page._send_data(page.driver, "xpath", loc_borrower['rzrq'], data["workDate"])  # 入职日期
		page._send_data(page.driver, "id", loc_borrower['gzyx'], data['workYear'])  # 工作年限
		page._send_data(page.driver, "id", loc_borrower['yjsr'], data['monthIncoming'])  # 月均收入
		page.driver.find_element_by_css_selector("input[type=\"checkbox\"]").click()  # 是否有社保 Todo
		page.driver.find_element_by_xpath('//*[@id="tb"]/a[3]/span[2]').click()
		# 临时保存
		save(page)
		return True
	except ec.NoSuchElementException as e:
		mylog().error(e)
		raise e.msg


# 输入多个借款人（待完善）
def input_more_borrower(page):
	"""
		客户基本信息 - 借款人/共贷人/担保人信息
	:param page 页面
	:param data 传入的数据
	"""
	
	try:
		page.driver.find_element_by_xpath('//*[@id="tb"]/a[1]/span[2]').click()
		# NAME
		page.driver.find_element_by_xpath(
				'//*[@id="datagrid-row-r1-2-1"]/td[5]/div/table/tbody/tr/td/input').send_keys(get_name())
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
				'//*[@id="datagrid-row-r1-2-1"]/td[11]/div/table/tbody/tr/td/input').send_keys(IDCard.createPhone())
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
		# 工作年限
		page.driver.find_element_by_id('_easyui_textbox_input21').send_keys(12)
		# 月均收入
		page.driver.find_element_by_id('_easyui_textbox_input22').send_keys(20000)
		# 是否有社保
		page.driver.find_element_by_xpath(
				'//*[@id="datagrid-row-r1-2-1"]/td[20]/div/table/tbody/tr/td/input').click()
		
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


# 业务基本信息- 输入物业信息(Basic business information-Property information)
def input_bbi_property_info(page):
	"""
		输入物业基本信息
	:param page: 页面对象
	:return:
	"""
	# 这步骤很关键，没有选中，则定位不到下面的元素
	try:
		t1 = page.driver.find_element_by_class_name("house-head-line")
		t1.click()
		page.driver.execute_script("window.scrollTo(1600, 0)")  # 页面滑动到顶部
		page.driver.find_element_by_link_text(u"业务基本信息").click()
	except ec.ElementNotVisibleException as e:
		mylog().error(e.msg)
		raise e
	
	try:
		page.driver.find_element_by_name("propertyOwner").clear()
		page.driver.find_element_by_name("propertyOwner").send_keys(get_name())  # 产权人
		page.driver.find_element_by_name("propertyNo").clear()
		page.driver.find_element_by_name("propertyNo").send_keys("gqt0132546")  # 房产证号
		
		# Todo
		time.sleep(3)
		page.driver.find_element_by_name("propertyStatus").click()  # 是否涉贷物业
		
		page.driver.find_element_by_name("propertyAge").click()
		page.driver.find_element_by_name("propertyAge").clear()
		page.driver.find_element_by_name("propertyAge").send_keys("10")  # 房龄
		
		page.driver.find_element_by_name("propertyArea").clear()
		page.driver.find_element_by_name("propertyArea").send_keys("100")  # 建筑面积
		
		page.driver.find_element_by_name("registrationPrice").clear()
		page.driver.find_element_by_name("registrationPrice").send_keys("200")  # 等级价
		
		try:
			# 地址
			Select(page.driver.find_element_by_name("propertyAddressProvince")).select_by_visible_text(u"河北省")
			Select(page.driver.find_element_by_name("propertyAddressCity")).select_by_visible_text(u"秦皇岛市")
			Select(page.driver.find_element_by_name("propertyAddressDistinct")).select_by_visible_text(u"山海关区")
			page.driver.find_element_by_id("propertyAddressDetail").clear()
			page.driver.find_element_by_id("propertyAddressDetail").send_keys(u"不知道在哪个地方")
		except ec.ElementNotVisibleException as e:
			raise e.msg
		
		page.driver.find_element_by_name("evaluationSumAmount").clear()
		page.driver.find_element_by_name("evaluationSumAmount").send_keys("200")  # 评估公允价总值
		page.driver.find_element_by_name("evaluationNetAmount").clear()
		page.driver.find_element_by_name("evaluationNetAmount").send_keys("201")  # 评估公允价净值
		page.driver.find_element_by_name("slSumAmount").clear()
		page.driver.find_element_by_name("slSumAmount").send_keys("202")  # 世联评估总值
		page.driver.find_element_by_name("slPrice").clear()
		page.driver.find_element_by_name("slPrice").send_keys("203")  # 世联评估净值
		page.driver.find_element_by_name("agentSumAmout").clear()
		page.driver.find_element_by_name("agentSumAmout").send_keys("204")  # 中介评估总值
		page.driver.find_element_by_name("agentNetAmount").clear()
		page.driver.find_element_by_name("agentNetAmount").send_keys("205")  # 中介评估净值
		page.driver.find_element_by_name("netSumAmount").clear()
		page.driver.find_element_by_name("netSumAmount").send_keys("206")  # 网评总值
		page.driver.find_element_by_name("netAmount").clear()
		page.driver.find_element_by_name("netAmount").send_keys("207")  # 网评净值
		page.driver.find_element_by_name("localSumAmount").clear()
		page.driver.find_element_by_name("localSumAmount").send_keys("208")  # 当地评估总值
		page.driver.find_element_by_name("localNetValue").clear()
		page.driver.find_element_by_name("localNetValue").send_keys("209")  # 当地评估净值
		page.driver.find_element_by_name("remark").clear()
		page.driver.find_element_by_name("remark").send_keys(u"周边环境良好")  # 物业配套描述
		page.driver.find_element_by_name("localAssessmentOrigin").clear()
		page.driver.find_element_by_name("localAssessmentOrigin").send_keys(u"房产局")  # 当地评估来源
		page.driver.find_element_by_name("assessmentOrigin").clear()
		page.driver.find_element_by_name("assessmentOrigin").send_keys(u"房产局")  # 评估来源
		page.driver.find_element_by_name("evaluationCaseDescrip").click()
		page.driver.find_element_by_name("localAssessmentOrigin").clear()
		page.driver.find_element_by_name("localAssessmentOrigin").send_keys(u"世联行")
		
		page.driver.find_element_by_name("evaluationCaseDescrip").clear()
		page.driver.find_element_by_name("evaluationCaseDescrip").send_keys(u"符合事实")  # 评估情况描述
		
		# 征信信息
		page.driver.find_element_by_link_text(u"征信信息").click()
		page.driver.find_element_by_name("loanIdNum").clear()
		page.driver.find_element_by_name("loanIdNum").send_keys(get_name())
		page.driver.find_element_by_name("creditOverdueNum").clear()
		page.driver.find_element_by_name("creditOverdueNum").send_keys("0")
		page.driver.find_element_by_name("queryLoanNum").clear()
		page.driver.find_element_by_name("queryLoanNum").send_keys("0")
		page.driver.find_element_by_name("loanOtherAmt").clear()
		page.driver.find_element_by_name("loanOtherAmt").send_keys("0")
		
		page.driver.find_element_by_link_text(u"网查信息").click()
		page.driver.find_element_by_class_name("remark").click()
		p1 = page.driver.find_element_by_xpath("//*[@id='apply_module_check_data_form']/div/div/textarea")
		p1.click()
		p1.send_keys(u"哈哈哈哈哈，无异常")
		
		page.driver.find_element_by_link_text(u"借款用途及回款来源").click()
		page.driver.find_element_by_id("apply_module_payment_source").send_keys(u"薪资回款")
		p2 = page.driver.find_element_by_xpath("//*[@id=\"apply_module_remark\"]")
		p2.click()
		p2.send_keys(u"无异常")
		
		page.driver.find_element_by_link_text(u"风控措施").click()
		page.driver.find_element_by_name("riskRemark").click()
		page.driver.find_element_by_name("riskRemark").send_keys(u"无异常")
		# 保存
		save(page)
	except ec.NoSuchElementException as e:
		raise e.msg


def input_all_bbi_property_info(page, data, apply_cust_credit_info, associated=False, product_name=None):
	"""
		车位贷物业信息录入
	:param page: 页面对象
	:param data: 传入的数据对象
	:param apply_cust_credit_info: 征信数据
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
		mylog().error(e.msg)
		return False
	
	try:
		page.driver.find_element_by_name("propertyOwner").clear()
		# page.driver.find_element_by_name("propertyOwner").send_keys(data['propertyOwner'])  # 产权人
		page.driver.find_element_by_name("propertyOwner").send_keys(get_name())  # 产权人
		page.driver.find_element_by_name("propertyNo").clear()
		page.driver.find_element_by_name("propertyNo").send_keys(data['propertyNo'])  # 房产证号
		
		# Todo
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
			page.driver.find_element_by_id('evaRalationModal').click()
			
			# 搜索条件
			page.driver.find_element_by_name('cityName').send_keys(u'长沙市')
			page.driver.find_element_by_name('constructionName').send_keys(u'金帆小区')
			page.driver.find_element_by_name('buildingName').send_keys('10')
			page.driver.find_element_by_name('houseName').send_keys('101')
			# 查询
			page.driver.find_element_by_xpath('//*[@id="admitsSearchForm"]/div[6]/button[1]').click()
			time.sleep(1)
			page.driver.find_element_by_xpath(
					'//*[@id="evaRalationModal"]/div/div/div[2]/div[2]/div/div/div[1]/div[2]/div[2]/table').click()
			page.driver.find_element_by_id('evaRalationBtn').click()
			time.sleep(1)
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
		save(page)
		return True
	except ec.NoSuchElementException as e:
		mylog().error(e.msg)
		return False


# 申请件查询，获取applyCode
def get_applycode(page, condition):
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
		# page.driver.find_element_by_xpath("/html/body/header/ul/li[2]/ul/li[4]").click()
		page.driver.find_element_by_name('/house/commonIndex/applySearch/index').click()
		time.sleep(2)
	except ec.ElementNotVisibleException as e:
		raise e
	try:
		# 切换iframe 申请件查询
		page.driver.switch_to.frame("bTabs_tab_house_commonIndex_applySearch_index")
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
		mylog().info("applyCode: " + t1.text)
		return t1.text
	else:
		raise ValueError("Value error")


# 待处理任务查询
def query_task(page, condition):
	"""
		查询待处理任务
	:param page: 页面对象
	:param condition: applyCode
	:return: True/False
	"""
	
	try:
		page.driver.switch_to.default_content()
		# 打开任务中心
		page._click_control(page.driver, "id", "1DBCBC52791800014989140019301189")
		time.sleep(1)
		# 待处理任务
		# page.driver.find_element_by_xpath("/html/body/header/ul/li[2]/ul/li[2]").click()
		page.driver.find_element_by_name("/house/commonIndex/todoList").click()
		
		try:
			# 切换iframe 待处理任务
			page.driver.switch_to.frame("bTabs_tab_house_commonIndex_todoList")
		except ec.NoSuchFrameException as e:
			raise e.msg
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
		t1 = page.driver.find_element_by_xpath("//*[@id='datagrid-row-r2-2-0']/td[9]")
	except ec.NoSuchFrameException as e:
		raise e.msg
	
	if not t1.text:
		return False
	else:
		return True


# 流程监控
def process_monitor(page, condition, stage=0):
	"""
		流程监控
	:param page: 页面
	:param condition: applyCode
	:param stage  0,1,2  对应风控、财务、募资
	:return: 下一个处理人登录 ID
	"""
	try:
		time.sleep(1)
		page.driver.switch_to.default_content()
		# 打开任务中心
		page._click_control(page.driver, "id", "1DBCBC52791800014989140019301189")
		time.sleep(1)
		# 流程监控
		page.driver.find_element_by_name("/house/commonIndex/processMonitor").click()
		time.sleep(2)
		
		#  切换frame
		try:
			page.driver.switch_to.frame("bTabs_tab_house_commonIndex_processMonitor")
			time.sleep(1)
		except ec.NoSuchFrameException as msg:
			raise (msg)
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
				mylog().info("下一个处理节点:" + role)  # 返回节点所有值
				# 下一步处理人ID
				next_user_id = page.driver.find_element_by_xpath(
						'//*[@id="datagrid-row-r1-2-%s"]/td[4]/div' % (len(rcount) - 1)).text
			elif stage == 1:
				page.driver.find_element_by_id('firstLoanA').click()
				# page.driver.find_element_by_xpath('//*[@id="profile"]/div/div/div/div/div[2]').click()
				page.driver.find_element_by_class_name('datagrid-view2')
				res = page.driver.find_element_by_xpath('//*[@id="profile"]/div/div/div/div/div[2]/div[2]/table/tbody')
				rcount = res.find_elements_by_tag_name("tr")
				for i in range(1, len(rcount)):
					role = page.driver.find_element_by_xpath('//*[@id="datagrid-row-r4-2-%s"]/td[1]/div' % i).text
					time.sleep(1)
				mylog().info("下一个处理环节:" + role)  # 返回节点所有值
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
				mylog().info("下一个处理节点:" + role)  # 返回节点所有值
				# 下一步处理人ID
				next_user_id = page.driver.find_element_by_xpath(
						'//*[@id="datagrid-row-r8-2-%s"]/td[4]/div' % (len(rcount) - 1)).text
	except ec.NoSuchElementException as msg:
		raise (msg)
	finally:
		page.driver.quit()
	return next_user_id


# 申请录入保存
def save(page):
	page.driver.find_element_by_css_selector(
			"#apply_module_apply_save > span.l-btn-left > span.l-btn-text > span.a_text").click()
	time.sleep(1)
	# 弹窗关闭
	page.driver.find_element_by_xpath("html/body/div[2]/div[3]/a").click()  # 确认保存
	time.sleep(1)


# 申请录入提交
def submit(page):
	page.driver.find_element_by_id("apply_module_apply_submit").click()
	page.driver.find_element_by_xpath('/html/body/div[2]/div[3]/a[1]').click()
	time.sleep(3)
	page.driver.find_element_by_xpath("html/body/div[2]/div[3]/a").click()


# 审批审核
def approval_to_review(page, condition, remark, action=0, image=False):
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
	page._click_control(page.driver, "id", "1DBCBC52791800014989140019301189")
	time.sleep(2)
	# 待处理任务
	# page.driver.find_element_by_xpath("/html/body/header/ul/li[2]/ul/li[2]").click()
	page.driver.find_element_by_name("/house/commonIndex/todoList").click()
	time.sleep(2)
	# 切换iframe 待处理任务
	page.driver.switch_to.frame("bTabs_tab_house_commonIndex_todoList")
	#  打开表单
	time.sleep(1)
	page.driver.find_element_by_id("frmQuery").click()
	# 选定申请编号搜索框
	page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").click()
	# 输入申请编号
	time.sleep(1)
	page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys(condition)
	# page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys("GZ20171116C05")
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
				upload_image_file(page, "E:\\HouseLoanAutoPy3\\lib\\uploadtool.exe",
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
			mylog().error("输入的参数有误(0-3)!")
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


# 特批
def special_approval(page, condition, remark):
	"""
		审批审核（特批）
	:param page:    页面对象
	:param condition:   applyCode
	:param remark:  审批审核意见
	:return:
	"""
	# 打开任务中心
	page._click_control(page.driver, "id", "1DBCBC52791800014989140019301189")
	time.sleep(2)
	# 待处理任务
	# page.driver.find_element_by_xpath("/html/body/header/ul/li[2]/ul/li[2]").click()
	page.driver.find_element_by_name("/house/commonIndex/todoList").click()
	time.sleep(2)
	# 切换iframe 待处理任务
	page.driver.switch_to.frame("bTabs_tab_house_commonIndex_todoList")
	#  打开表单
	time.sleep(1)
	page.driver.find_element_by_id("frmQuery").click()
	# 选定申请编号搜索框
	page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").click()
	# 输入申请编号
	time.sleep(1)
	page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys(condition)
	# page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys("CS20180201C23")
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


# 风控审批回退
def risk_approval_fallback(page, condition, option, remark):
	"""
		审批审核
	:param page:    页面对象
	:param condition:   applyCode
	:param remark:  审批审核意见
	:return:
	"""
	
	try:
		# 打开任务中心
		page._click_control(page.driver, "id", "1DBCBC52791800014989140019301189")
		time.sleep(2)
		# 待处理任务
		page.driver.find_element_by_name("/house/commonIndex/todoList").click()
		time.sleep(2)
		# 切换iframe 待处理任务
		page.driver.switch_to.frame("bTabs_tab_house_commonIndex_todoList")
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
	except ec.NoSuchElementException as e:
		raise e.msg
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
			raise e.msg


def make_signing(page, condition, rec_bank_info, number=1):
	"""
		合同打印
	:param page:    页面对象
	:param condition:   applyCode
	:param rec_bank_info:   收款银行
	:param number：  签约人个数
	:return:
	"""
	
	# 查询待处理任务
	t1 = task_search(page, condition)
	time.sleep(1)
	if not t1.text:
		return False
	else:
		t1.click()
		# 双击该笔案件
		ActionChains(page.driver).double_click(t1).perform()
		time.sleep(1)
		page.driver.switch_to_frame("myIframeImage1")  # 切换iframe
		# ----------------------------------------------------------------------------------------
		#                                 合同信息录入
		# ----------------------------------------------------------------------------------------
		Select(page.driver.find_element_by_name("signAddressProvince")).select_by_visible_text(u"陕西省")
		Select(page.driver.find_element_by_name("signAddressCity")).select_by_visible_text(u"咸阳市")
		Select(page.driver.find_element_by_name("signAddressDistinct")).select_by_visible_text(u"武功县")
		page.driver.find_element_by_xpath('//*[@id="sign_module_form"]/div/div[3]/div[2]/input').send_keys(u"爱在心口难开")
		page.driver.find_element_by_xpath('//*[@id="sign_module_form"]/div/div[4]/div[2]/textarea').send_keys(
				u'借款合同约定事项')
		page.driver.find_element_by_xpath('//*[@id="sign_module_form"]/div/div[5]/div[2]/textarea').send_keys(u'签约备注信息')
		
		# ----------------------------------------------------------------------------------------
		#                                 拆借人个人信息及收款银行信息录入
		# ----------------------------------------------------------------------------------------
		
		# 主借人银行信息录入
		def main_borrower(page):
			page.driver.find_element_by_class_name("signBaseAndInfo").click()
			match_str = '//*[starts-with(@id, "signPersonForm")]/'
			bank_str = '//*[starts-with(@id, "signBankFormperson")]/'
			# 拆分金额
			page.driver.find_element_by_xpath(match_str + '/table/tbody/tr[4]/td[4]/input').send_keys('200000')
			# 工作地点
			page.driver.find_element_by_xpath(match_str + '/table/tbody/tr[2]/td[8]/input').send_keys(
					u'北京')
			# 切换选定银行from
			page.driver.find_element_by_xpath(bank_str + '/section[1]/div[2]/div[6]/input').send_keys(
					rec_bank_info['recBankNum'])  # 收款银行账号
			page.driver.find_element_by_xpath(bank_str + '/section[1]/div[2]/div[8]/input').send_keys(
					rec_bank_info['recPhone'])  # 银行预留电话
			
			page.driver.find_element_by_xpath(bank_str + '/section[1]/div[3]/div[4]/input').send_keys(
					rec_bank_info['recBankProvince'])  # 开户所在省
			page.driver.find_element_by_xpath(bank_str + '/section[1]/div[3]/div[6]/input').send_keys(
					rec_bank_info['recBankDistrict'])  # 开户行市县
			
			# ----------------------------------------------------------------------------------------
			# 选择银行类别
			page.driver.find_element_by_xpath(bank_str + '/section[1]/div[3]/div[2]/div/button/span[1]').click()
			time.sleep(1)
			# 中国农业银行，默认写死了xpath，方法不推荐，先这样处理
			page.driver.find_element_by_xpath(bank_str + '/section[1]/div[3]/div[2]/div/div/ul/li[4]/a/span[1]').click()
			
			# ----------------------------------------------------------------------------------------
			
			# 考虑用以下方法，但未成功
			# -----------------------------
			# sl = Select(page.driver.find_element_by_class_name('dropdown-menu open'))
			# s1 = page.driver.find_element_by_name('recBankNum1')
			# Select(s1).select_by_index(1)
			# Select(s1).select_by_value('0192')
			
			# Select(page.driver.find_element_by_name("recBankNum1")).select_by_visible_text(u'招商银行')
			# -----------------------------
			
			# 分支银行
			page.driver.find_element_by_xpath(bank_str + '/section[1]/div[3]/div[2]/input[3]').send_keys(
					rec_bank_info['recBankBranch'])
			
			# 与收款银行一致
			page.driver.find_element_by_xpath(bank_str + '/section[2]/div[1]/div/button').click()
			time.sleep(1)
		
		# 拆借人银行信息录入
		def add_first_person(page, personform, bankform):
			
			custname = get_name()
			page.driver.find_element_by_link_text(u"拆借人信息").click()
			page.driver.find_element_by_id('addLoanApartPerson').click()
			time.sleep(1)
			page.driver.find_element_by_id('apply_loanApart_info').click()
			page.driver.find_element_by_id("loanApartPersonForm0").click()
			# name
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[1]/td[2]/input').send_keys(custname)
			# phone
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[1]/td[4]/input').send_keys("13512342341")
			# ID
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[1]/td[6]/input').send_keys("610124198703042140")
			# age
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[1]/td[8]/input').send_keys("30")
			
			Select(page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[2]/td[2]/select')).select_by_visible_text(u'已婚')
			
			Select(page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[2]/td[4]/select')).select_by_visible_text(u'本科')
			
			Select(page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[2]/td[6]/select')).select_by_visible_text(u'建筑业')
			# 工作地点
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[2]/td[8]/input').send_keys(u"深圳")
			# 公司规模
			Select(page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[3]/td[2]/select')).select_by_visible_text(
					'100-300人')
			# 工作职位
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[3]/td[4]/input').send_keys(u"工程师")
			# 入职日期
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[3]/td[6]/input').send_keys("2017-08-21")
			# 工作年限
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[3]/td[8]/input').send_keys(10)
			# 月均收入
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[4]/td[2]/input').send_keys(100000)
			# 拆借金额
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[4]/td[4]/input').clear()
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[4]/td[4]/input').send_keys('200000')
			
			# 收扣款银行信息录入
			# page.driver.find_element_by_id('loanApartBankForm0').click()
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(bankform) + '"]/section[1]/div[2]/div[6]/input').send_keys(
					"6217582600007330589")
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(bankform) + '"]/section[1]/div[2]/div[8]/input').send_keys(
					'13891213212')
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(bankform) + '"]/section[1]/div[3]/div[2]/input[3]').send_keys(u'深圳支行')
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(bankform) + '"]/section[1]/div[3]/div[4]/input').send_keys(
					u'湖南省')
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(bankform) + '"]/section[1]/div[3]/div[6]/input').send_keys(
					u'长沙市')
			
			# 扣款银行
			page.driver.find_element_by_xpath('//*[@id="' + str(bankform) + '"]/section[2]/div[1]/div/button').click()
		
		def add_other_person(page, personform, bankform):
			custname = get_name()
			page.driver.find_element_by_id('addLoanApartPerson').click()
			page.driver.find_element_by_id(str(personform)).click()
			
			# name
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[1]/td[2]/input').send_keys(custname)
			# phone
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[1]/td[4]/input').send_keys("13512342341")
			# ID
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[1]/td[6]/input').send_keys("610124198703042140")
			# age
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[1]/td[8]/input').send_keys("30")
			
			Select(page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[2]/td[2]/select')).select_by_visible_text(u'已婚')
			
			Select(page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[2]/td[4]/select')).select_by_visible_text(u'本科')
			
			Select(page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[2]/td[6]/select')).select_by_visible_text(u'建筑业')
			# 工作地点
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[2]/td[8]/input').send_keys(u"深圳")
			# 公司规模
			Select(page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[3]/td[2]/select')).select_by_visible_text(
					'100-300人')
			# 工作职位
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[3]/td[4]/input').send_keys(u"工程师")
			# 入职日期
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[3]/td[6]/input').send_keys("2017-08-21")
			# 工作年限
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[3]/td[8]/input').send_keys(10)
			# 月均收入
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[4]/td[2]/input').send_keys(100000)
			# 拆借金额
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[4]/td[4]/input').clear()
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(personform) + '"]/table/tbody/tr[4]/td[4]/input').send_keys('200000')
			
			# 收扣款银行信息录入
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(bankform) + '"]/section[1]/div[2]/div[6]/input').send_keys(
					"6217582600007330589")
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(bankform) + '"]/section[1]/div[2]/div[8]/input').send_keys(
					'13891213212')
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(bankform) + '"]/section[1]/div[3]/div[2]/input[3]').send_keys(u'深圳支行')
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(bankform) + '"]/section[1]/div[3]/div[4]/input').send_keys(
					u'湖南省')
			page.driver.find_element_by_xpath(
					'//*[@id="' + str(bankform) + '"]/section[1]/div[3]/div[6]/input').send_keys(
					u'长沙市')
			
			# 扣款银行
			page.driver.find_element_by_xpath('//*[@id="' + str(bankform) + '"]/section[2]/div[1]/div/button').click()
		
		# ----------------------------------------------------------------------------------------------------------
		#                                       新增拆借人
		# ----------------------------------------------------------------------------------------------------------
		
		if number == 1:
			main_borrower(page)
		elif number == 2:
			main_borrower(page)
			add_first_person(page, "loanApartPersonForm0", "loanApartBankForm0")
		elif number == 3:
			main_borrower(page)
			add_first_person(page, "loanApartPersonForm0", "loanApartBankForm0")
			add_other_person(page, "loanApartPersonForm1", "loanApartBankForm1")
		elif number == 4:
			main_borrower(page)
			add_first_person(page, "loanApartPersonForm0", "loanApartBankForm0")
			add_other_person(page, "loanApartPersonForm1", "loanApartBankForm1")
			add_other_person(page, "loanApartPersonForm2", "loanApartBankForm2")
		elif number == 5:
			main_borrower(page)
			add_first_person(page, "loanApartPersonForm0", "loanApartBankForm0")
			add_other_person(page, "loanApartPersonForm1", "loanApartBankForm1")
			add_other_person(page, "loanApartPersonForm2", "loanApartBankForm2")
			add_other_person(page, "loanApartPersonForm3", "loanApartBankForm3")
		
		# 保存
		page.driver.switch_to.parent_frame()  # 切换到父iframe
		page.driver.find_element_by_xpath('//*[@id="contract_sign_save"]/span').click()
		time.sleep(1)
		page.driver.find_element_by_xpath('/html/body/div[5]/div[3]/a').click()  # 关闭弹窗
		
		# 提交
		page.driver.find_element_by_xpath('//*[@id="contract_sign_submit"]/span').click()
		time.sleep(1)
		page.driver.find_element_by_xpath('/html/body/div[5]/div[3]/a').click()  # 确认合同打印
		time.sleep(2)
		page.driver.find_element_by_xpath('/html/body/div[5]/div[3]/a').click()  # 确认提交
		time.sleep(2)
		page.driver.find_element_by_xpath('/html/body/div[5]/div[3]/a').click()  # 确认
		
		return True


def compliance_audit(page, condition, upload=False):
	"""
		合规审查
	:param page: 页面对象
	:param condition: applyCode
	:return:
	"""
	
	# 查询待处理任务
	t1 = task_search(page, condition)
	if not t1.text:
		mylog().error("can't found the task in the taskList")
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
	if not False:
		try:
			page.driver.find_element_by_link_text("影像资料").click()
			try:
				page.driver.switch_to_frame('myIframeImage5')
			except ec.NoSuchFrameException as msg:
				raise (msg)
			# upload
			page.driver.find_element_by_class_name('img_upload_area').click()
			page.driver.find_element_by_id('browse').click()
			
			os.system("E:\\HouseLoanAutoPy3\\lib\\uploadtool.exe" + " " + "E:\\HouseLoanAutoPy3\\image\\2.jpg")
		except ec.NoSuchElementException as msg:
			raise ValueError(msg)
		finally:
			time.sleep(1)
			page.driver.switch_to.parent_frame()
	
	# 保存
	
	page.driver.find_element_by_xpath('//*[@id="apply_module_apply_save"]').click()
	page.driver.find_element_by_xpath(' /html/body/div[4]/div[3]/a').click()
	
	# 提交
	page.driver.find_element_by_xpath('//*[@id="apply_module_apply_submit"]').click()
	page.driver.find_element_by_xpath('/html/body/div[4]/div[3]/a').click()
	
	page.driver.quit()
	return True


def task_search(page, condition):
	"""
		待处理任务查询
	:param page: 页面
	:param condition:  applyCode
	:return: 查询表格数据
	"""
	
	try:
		# 打开任务中心
		page._click_control(page.driver, "id", "1DBCBC52791800014989140019301189")
		time.sleep(1)
		# 待处理任务
		page.driver.find_element_by_name("/house/commonIndex/todoList").click()
		time.sleep(2)
	except ec.NoSuchElementException as e:
		raise e.msg
	try:
		# 切换iframe
		page.driver.switch_to.frame('bTabs_tab_house_commonIndex_todoList')
	# page.driver.switch_to.frame(frame)
	except ec.NoSuchFrameException as e:
		raise e.msg
	try:
		page.driver.find_element_by_id("frmQuery").click()
		time.sleep(1)
		# 选定申请编号搜索框
		page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").click()
		# 输入申请编号
		time.sleep(1)
		page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys(condition)
		# page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys("GZ20171207E19")
		# 点击查询按钮
		page.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/a[1]/span").click()
		time.sleep(1)
		res = page.driver.find_element_by_xpath("//*[@id='datagrid-row-r2-2-0']/td[3]")
		return res
	except ec.NoSuchElementException as e:
		raise e.msg


def authority_card_transact(page, condition, env="SIT"):
	"""
		权证办理
	:param page: 页面
	:param condition: applyCode
	:param env 环境选择
	:return:
	"""
	
	# 权证管理
	try:
		# page.driver.find_element_by_xpath("/html/body/header/ul/li[5]").click()
		if env == "SIT":
			page.driver.find_element_by_id("1DF1731576B000013DB03A40A8601B66").click()
		else:
			page.driver.find_element_by_id("1DF16C65668E000176ED2081C4D01896").click()
		time.sleep(1)
		page.driver.find_element_by_name("/house/commonIndex/warrantManageList").click()
		time.sleep(2)
	except ec.NoSuchElementException as e:
		raise e
	try:
		# 切换iframe
		page.driver.switch_to.frame('bTabs_tab_house_commonIndex_warrantManageList')
	except ec.NoSuchFrameException as e:
		raise e.msg
	try:
		# 点击查询按钮
		page.driver.find_element_by_id("frmQuery").click()
		# 选定申请编号搜索框
		page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").click()
		# 输入申请编号
		page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys(condition)
		# page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys("GZ20171212C02")
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
			page.driver.switch_to.frame('myIframeImage1')
			# 添加
			page.driver.find_element_by_xpath('//*[@id="gridtb0"]/div[1]/a[1]').click()
			time.sleep(2)
			# 选择日期
			js = "$('input[name=storageTime]').removeAttr('readonly')"
			page.driver.execute_script(js)
			page.driver.find_element_by_xpath('//*[@id="warrantForm"]/div/div[4]/div/div/input').send_keys(
					str(datetime.date.today()))
			
			page.driver.find_element_by_name('warrantsCode').send_keys("12346689adbcdd")
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


def warrant_apply(page, condition):
	"""
		权证请款
	:param page: 页面对象
	:param condition:   applyCode
	:return:
	"""
	
	# 打开任务中心
	t1 = task_search(page, condition)
	if not t1.text:
		return False
	else:
		t1.click()
		# 双击
		ActionChains(page.driver).double_click(t1).perform()
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


def finace_transact(page, condition):
	"""
		财务办理
	:param page: 页面对象
	:param condition:   applyCode
	:return:
	"""
	
	# 打开任务中心
	# 财务放款申请列表
	try:
		page._click_control(page.driver, "id", "1DBCBC52791800014989140019301189")
		page.driver.find_element_by_name('/house/commonIndex/financeManageList').click()
		time.sleep(1)
		page.driver.switch_to.frame('bTabs_tab_house_commonIndex_financeManageList')
		# 选定申请编号搜索框
		page.driver.find_element_by_id("frmQuery").click()
		page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").click()
		# 输入申请编号
		time.sleep(1)
		page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys(condition)
		# page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys("CS20171214X07")
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
			page.driver.switch_to.frame('myIframeImage1')
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


def finace_approve(page, condition, remark):
	"""
		财务审批
	:param page: 页面对象
	:param condition: applyCode
	:return:
	"""
	
	# 财务待处理任务
	try:
		page._click_control(page.driver, "id", "1DBCBC52791800014989140019301189")
		time.sleep(1)
		page.driver.find_element_by_name('/house/commonIndex/financial/toDoList').click()
		try:
			page.driver.switch_to.frame('bTabs_tab_house_commonIndex_financial_toDoList')
		except ec.NoSuchFrameException as e:
			raise e.msg
		
		# 选定申请编号搜索框
		page.driver.find_element_by_id("frmQuery").click()
		page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").click()
		# 输入申请编号
		time.sleep(1)
		page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys(condition)
		# page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys("CS20171215X06")
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
		page.driver.switch_to.frame('myIframeImage1')
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
		logging.error(u'财务待处理任务中没有找到申请编号')
		return False


def funds_raise(page, condition, remark):
	"""
		募资
	:param page:
	:param condition:
	:param remark:
	:return:
	"""
	page._click_control(page.driver, "id", "1DBCBC52791800014989140019301189")
	page.driver.find_element_by_name('/house/commonIndex/financial/toDoList').click()
	page.driver.switch_to.frame('bTabs_tab_house_commonIndex_financial_toDoList')
	
	# 选定申请编号搜索框
	page.driver.find_element_by_id("frmQuery").click()
	page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").click()
	# 输入申请编号
	time.sleep(1)
	page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys(condition)
	# page.driver.find_element_by_xpath("//*[@id='row-content']/div[1]/input").send_keys("CS20171221C03")
	# 点击查询按钮
	page.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/a[1]/span").click()
	time.sleep(1)
	res = page.driver.find_element_by_xpath('//*[@id="datagrid-row-r1-2-0"]/td[7]/div')
	
	if res.text == condition:
		res.click()
		ActionChains(page.driver).double_click(res).perform()
		time.sleep(2)
		page.driver.switch_to.frame('myIframeImage1')
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
		logging.error(u'财务待处理任务中没有找到申请编号')
		return False


def reconsideration(page, applycode, action=0):
	"""
		高级经理复议拒绝的单
	:param page: 页面对象
	:param applycode: 申请code
	:param action: 0 拒绝; 1 复议通过; 2 复议拒绝
	:return:
	"""
	
	page.driver.find_element_by_id('1DCDFBEA96010001A2941A801EA02310').click()
	# 拒绝队列
	page.driver.find_element_by_name("/house/commonIndex/refuseList").click()
	# iframe
	page.driver.switch_to_frame('bTabs_tab_house_commonIndex_refuseList')
	page.driver.find_element_by_name('applyCode').send_keys(applycode)
	time.sleep(1)
	page.driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/a[1]').click()  # 查询
	time.sleep(1)
	if action == 0:
		page.driver.find_element_by_id('frmQuery').click()
		t1 = page.driver.find_element_by_xpath('//*[@id="datagrid-row-r1-2-0"]/td[13]/div')
		if t1.text != "":
			mylog().info("拒绝案件:" + t1.text)
			return True
		else:
			return False
	elif action == 1:
		page.driver.find_element_by_id('frmQuery').click()
		page.driver.find_element_by_xpath('//*[@id="datagrid-row-r1-2-0"]').click()
		page.driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/a[4]').click()
		page.driver.find_element_by_xpath('/html/body/div[5]/div[3]/a[1]').click()
		return True
	elif action == 2:
		page.driver.find_element_by_id('frmQuery').click()
		page.driver.find_element_by_xpath('//*[@id="datagrid-row-r1-2-0"]').click()
		page.driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/a[3]').click()
		page.driver.find_element_by_xpath('/html/body/div[5]').click()
		time.sleep(1)
		page.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[4]/input').send_keys(u"不通过！")
		time.sleep(1)
		page.driver.find_element_by_xpath('/html/body/div[5]/div[3]/a[1]').click()
		time.sleep(1)
		page.driver.find_element_by_xpath('/html/body/div[5]/div[3]/a').click()
		time.sleep(1)
		page.driver.find_element_by_xpath('/html/body/div[5]/div[3]/a').click()
		return True
	else:
		mylog().error("param wrong!")
		return False


def get_next_user(page, applycode, stage=0):
	"""
	获取下一个处理人
	:param page: 页面对象
	:param applycode: 申请件code
	:return:
	"""
	next_id = process_monitor(page, applycode, stage)
	if next_id is None:
		raise ValueError("没有找到下一步处理人")
	else:
		next_user_id = next_id
		mylog().info("下一步处理人:" + next_id)
		# 当前用户退出系统
		page.driver.quit()
	return next_user_id


def receipt_return(page, apply_code):
	"""
	回执提放审批审核
	:param page:
	:param apply_code:
	:return:
	"""
	
	t1 = task_search(page, apply_code)
	if not t1.text:
		return False
	else:
		t1.click()
		ActionChains(page.driver).double_click(t1).perform()
		try:
			page.driver.switch_to.frame("myIframeImage1")  # 切换iframe
		except ec.NoSuchFrameException as e:
			raise e.msg
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


def part_warrant_apply(page, condition, flag=0):
	"""
		部分权证请款
	:param page: 页面对象
	:param condition:   applyCode
	:return:
	"""
	
	# 打开任务中心
	t1 = task_search(page, condition)
	if not t1.text:
		return False
	else:
		t1.click()
		# 双击
		ActionChains(page.driver).double_click(t1).perform()
		try:
			page.driver.switch_to.frame("myIframeImage1")  # 切换iframe
		except ec.NoSuchFrameException as e:
			raise e.msg
		
		try:
			if flag == 0:
				# 第一次权证请款
				page.driver.find_element_by_xpath('//*[@id="warrantInfo"]/div[2]/div/input[4]').click()
				page.driver.find_element_by_id('splitLoanMoney').click()
				time.sleep(1)
				# 请款拆分明细
				page.driver.find_element_by_xpath('//*[@id="warrantSplitModel"]/div').click()
				time.sleep(1)
				page.driver.find_element_by_xpath('//*[@id="warrantForm"]/div/table/tbody/tr[1]/td[1]/input').click()
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
			raise e.msg


def upload_image_file(page, exe, image, delete=None):
	"""
	上传影像资料
	:param page:
	:return:
	"""
	try:
		page.driver.find_element_by_link_text("影像资料").click()
		try:
			page.driver.switch_to_frame('myIframeImages')
		except ec.NoSuchFrameException as msg:
			raise (msg)
		# upload
		page.driver.find_element_by_class_name('img_upload_area').click()
		page.driver.find_element_by_id('browse').click()
		os.system(exe + " " + image)
		# os.system('E:\\HouseLoanAutoPy3\\lib\\uploadtool.exe "E:\\HouseLoanAutoPy3\\image\\2.jpg"')
		
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
