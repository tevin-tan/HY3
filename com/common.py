# coding:utf-8

# ----------------------------
#     系统操作通用方法
# ----------------------------
import time

from selenium import webdriver
from selenium.common import exceptions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

from com.custom import get_name, mylog


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


# 申请录入保存
def save(page):
	page.driver.find_element_by_css_selector(
			"#apply_module_apply_save > span.l-btn-left > span.l-btn-text > span.a_text").click()
	time.sleep(1)
	# 弹窗关闭
	page.driver.find_element_by_xpath("html/body/div[2]/div[3]/a").click()  # 确认保存
	time.sleep(1)


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
		page.driver.switch_to_default_content()
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
