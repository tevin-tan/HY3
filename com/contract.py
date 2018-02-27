import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from com.custom import get_name
from com.common import task_search
from selenium.common import exceptions as EC
# import common.getIdNumber as GT
from com.idCardNumber import IdCardNumber as IDCN
from common import getBankCard


class Contract():
	"""合同签约"""
	
	def __init__(self, page, condition, rec_bank_info, number=1):
		self.number = number
		self.page = page
		self.condition = condition
		self.rec_bank_info = rec_bank_info
		
		t1 = task_search(self.page, self.condition)
		if not t1.text:
			raise AssertionError('查询流程监控出错！')
		else:
			t1.click()
			ActionChains(self.page.driver).double_click(t1).perform()
			time.sleep(1)
			try:
				self.page.driver.switch_to_frame("myIframeImage1")  # 切换iframe
			except EC.NoSuchFrameException as e:
				raise e.msg
			# ----------------------------------------------------------------------------------------
			#                                 合同信息录入
			# ----------------------------------------------------------------------------------------
			try:
				Select(self.page.driver.find_element_by_name("signAddressProvince")).select_by_visible_text(u"陕西省")
				Select(self.page.driver.find_element_by_name("signAddressCity")).select_by_visible_text(u"咸阳市")
				Select(self.page.driver.find_element_by_name("signAddressDistinct")).select_by_visible_text(u"武功县")
			except EC.ElementNotSelectableException as e:
				raise e.msg
			try:
				self.page.driver.find_element_by_xpath('//*[@id="sign_module_form"]/div/div[3]/div[2]/input').send_keys(
						u"爱在心口难开")
				self.page.driver.find_element_by_xpath(
						'//*[@id="sign_module_form"]/div/div[4]/div[2]/textarea').send_keys(
						u'借款合同约定事项')
				self.page.driver.find_element_by_xpath(
						'//*[@id="sign_module_form"]/div/div[5]/div[2]/textarea').send_keys(
						u'签约备注信息')
			except EC.NoSuchElementException as e:
				raise e.msg
	
	def personal_information(self):
		"""主借人基本信息"""
		self.page.driver.find_element_by_class_name("signBaseAndInfo").click()
		match_str = '//*[starts-with(@id, "signPersonForm")]/'
		bank_str = '//*[starts-with(@id, "signBankFormperson")]/'
		# 拆分金额
		self.page.driver.find_element_by_xpath(match_str + '/table/tbody/tr[4]/td[4]/input').send_keys('200000')
		# 工作地点
		self.page.driver.find_element_by_xpath(match_str + '/table/tbody/tr[2]/td[8]/input').send_keys(
				u'北京')
		# 切换选定银行from
		# self.page.driver.find_element_by_xpath(bank_str + '/section[1]/div[2]/div[6]/input').send_keys(
		# 		self.rec_bank_info['recBankNum']) # 收款银行账号
		self.page.driver.find_element_by_xpath(bank_str + '/section[1]/div[2]/div[6]/input').send_keys(
				getBankCard.getBankCardNumber())  # 收款银行账号
		self.page.driver.find_element_by_xpath(bank_str + '/section[1]/div[2]/div[8]/input').send_keys(
				self.rec_bank_info['recPhone'])  # 银行预留电话
		
		self.page.driver.find_element_by_xpath(bank_str + '/section[1]/div[3]/div[4]/input').send_keys(
				self.rec_bank_info['recBankProvince'])  # 开户所在省
		self.page.driver.find_element_by_xpath(bank_str + '/section[1]/div[3]/div[6]/input').send_keys(
				self.rec_bank_info['recBankDistrict'])  # 开户行市县
		
		# ----------------------------------------------------------------------------------------
		# 选择银行类别
		self.page.driver.find_element_by_xpath(bank_str + '/section[1]/div[3]/div[2]/div/button/span[1]').click()
		time.sleep(1)
		# 中国农业银行，默认写死了xpath，方法不推荐，先这样处理
		self.page.driver.find_element_by_xpath(
				bank_str + '/section[1]/div[3]/div[2]/div/div/ul/li[4]/a/span[1]').click()
		
		# ----------------------------------------------------------------------------------------
		# 考虑用以下方法，但未成功
		# -----------------------------
		# sl = Select(self.page.driver.find_element_by_class_name('dropdown-menu open'))
		# s1 = self.page.driver.find_element_by_name('recBankNum1')
		# Select(s1).select_by_index(1)
		# Select(s1).select_by_value('0192')
		# Select(self.page.driver.find_element_by_name("recBankNum1")).select_by_visible_text(u'招商银行')
		# -----------------------------
		# 分支银行
		self.page.driver.find_element_by_xpath(bank_str + '/section[1]/div[3]/div[2]/input[3]').send_keys(
				self.rec_bank_info['recBankBranch'])
		
		# 与收款银行一致
		self.page.driver.find_element_by_xpath(bank_str + '/section[2]/div[1]/div/button').click()
		time.sleep(1)
	
	# 拆借人银行信息录入
	def add_first_person(self, personform, bankform):
		
		cust_name = get_name()
		self.page.driver.find_element_by_link_text(u"拆借人信息").click()
		self.page.driver.find_element_by_id('addLoanApartPerson').click()
		self.page.driver.find_element_by_id('apply_loanApart_info').click()
		self.page.driver.find_element_by_id("loanApartPersonForm0").click()
		# name
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[1]/td[2]/input').send_keys(cust_name)
		# phone
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[1]/td[4]/input').send_keys(
				IDCN.createPhone())
		# ID
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[1]/td[6]/input').send_keys(
				IDCN.getRandomIdNumber()[0])
		# age
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[1]/td[8]/input').send_keys("30")
		
		Select(self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[2]/td[2]/select')).select_by_visible_text(u'已婚')
		
		Select(self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[2]/td[4]/select')).select_by_visible_text(u'本科')
		
		Select(self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[2]/td[6]/select')).select_by_visible_text(u'建筑业')
		# 工作地点
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[2]/td[8]/input').send_keys(u"深圳")
		# 公司规模
		Select(self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[3]/td[2]/select')).select_by_visible_text(
				'100-300人')
		# 工作职位
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[3]/td[4]/input').send_keys(u"工程师")
		# 入职日期
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[3]/td[6]/input').send_keys("2017-08-21")
		# 工作年限
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[3]/td[8]/input').send_keys(10)
		# 月均收入
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[4]/td[2]/input').send_keys(100000)
		# 拆借金额
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[4]/td[4]/input').clear()
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[4]/td[4]/input').send_keys('200000')
		
		# 收扣款银行信息录入
		# self.page.driver.find_element_by_id('loanApartBankForm0').click()
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(bankform) + '"]/section[1]/div[2]/div[6]/input').send_keys(
				getBankCard.getBankCardNumber())
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(bankform) + '"]/section[1]/div[2]/div[8]/input').send_keys(
				IDCN.createPhone())
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(bankform) + '"]/section[1]/div[3]/div[2]/input[3]').send_keys(u'深圳支行')
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(bankform) + '"]/section[1]/div[3]/div[4]/input').send_keys(
				u'湖南省')
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(bankform) + '"]/section[1]/div[3]/div[6]/input').send_keys(
				u'长沙市')
		
		# 扣款银行
		self.page.driver.find_element_by_xpath('//*[@id="' + str(bankform) + '"]/section[2]/div[1]/div/button').click()
	
	# 添加其他拆借人
	def add_other_person(self, personform, bankform):
		cust_name = get_name()
		self.page.driver.find_element_by_id('addLoanApartPerson').click()
		self.page.driver.find_element_by_id(str(personform)).click()
		
		# name
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[1]/td[2]/input').send_keys(cust_name)
		# phone
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[1]/td[4]/input').send_keys(IDCN.createPhone())
		# ID
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[1]/td[6]/input').send_keys(
				IDCN.getRandomIdNumber()[0])
		# age
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[1]/td[8]/input').send_keys("30")
		
		Select(self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[2]/td[2]/select')).select_by_visible_text(u'已婚')
		
		Select(self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[2]/td[4]/select')).select_by_visible_text(u'本科')
		
		Select(self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[2]/td[6]/select')).select_by_visible_text(u'建筑业')
		# 工作地点
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[2]/td[8]/input').send_keys(u"深圳")
		# 公司规模
		Select(self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[3]/td[2]/select')).select_by_visible_text(
				'100-300人')
		# 工作职位
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[3]/td[4]/input').send_keys(u"工程师")
		# 入职日期
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[3]/td[6]/input').send_keys("2017-08-21")
		# 工作年限
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[3]/td[8]/input').send_keys(10)
		# 月均收入
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[4]/td[2]/input').send_keys(100000)
		# 拆借金额
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[4]/td[4]/input').clear()
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(personform) + '"]/table/tbody/tr[4]/td[4]/input').send_keys('200000')
		
		# 收扣款银行信息录入
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(bankform) + '"]/section[1]/div[2]/div[6]/input').send_keys(
				getBankCard.getBankCardNumber())
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(bankform) + '"]/section[1]/div[2]/div[8]/input').send_keys(
				IDCN.createPhone())
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(bankform) + '"]/section[1]/div[3]/div[2]/input[3]').send_keys(u'深圳支行')
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(bankform) + '"]/section[1]/div[3]/div[4]/input').send_keys(
				u'湖南省')
		self.page.driver.find_element_by_xpath(
				'//*[@id="' + str(bankform) + '"]/section[1]/div[3]/div[6]/input').send_keys(
				u'长沙市')
		
		# 扣款银行
		self.page.driver.find_element_by_xpath('//*[@id="' + str(bankform) + '"]/section[2]/div[1]/div/button').click()
	
	def contract_save(self):
		# 保存
		self.page.driver.switch_to.parent_frame()  # 切换到父iframe
		self.page.driver.find_element_by_xpath('//*[@id="contract_sign_save"]/span').click()
		time.sleep(1)
		self.page.driver.find_element_by_xpath('/html/body/div[5]/div[3]/a').click()  # 关闭弹窗
	
	def contract_submit(self):
		# 提交
		self.page.driver.find_element_by_xpath('//*[@id="contract_sign_submit"]/span').click()
		time.sleep(1)
		self.page.driver.find_element_by_xpath('/html/body/div[5]/div[3]/a').click()  # 确认合同打印
		time.sleep(2)
		self.page.driver.find_element_by_xpath('/html/body/div[5]/div[3]/a').click()  # 确认提交
		time.sleep(2)
		self.page.driver.find_element_by_xpath('/html/body/div[5]/div[3]/a').click()  # 确认
	
	def execute_sign(self):
		"""
			添加拆借人银行信息
		:return:
		"""
		
		"""
		if self.number == 1:
			self.personal_information()
		elif self.number == 2:
			self.personal_information()
			self.add_first_person("loanApartPersonForm0", "loanApartBankForm0")
		elif self.number == 3:
			self.personal_information()
			self.add_first_person("loanApartPersonForm0", "loanApartBankForm0")
			self.add_other_person("loanApartPersonForm1", "loanApartBankForm1")
		elif self.number == 4:
			self.personal_information()
			self.add_first_person("loanApartPersonForm0", "loanApartBankForm0")
			self.add_other_person("loanApartPersonForm1", "loanApartBankForm1")
			self.add_other_person("loanApartPersonForm2", "loanApartBankForm2")
		elif self.number == 5:
			self.personal_information()
			self.add_first_person("loanApartPersonForm0", "loanApartBankForm0")
			self.add_other_person("loanApartPersonForm1", "loanApartBankForm1")
			self.add_other_person("loanApartPersonForm2", "loanApartBankForm2")
			self.add_other_person("loanApartPersonForm3", "loanApartBankForm3")
		elif self.number == 6:
			self.personal_information()
			self.add_first_person("loanApartPersonForm0", "loanApartBankForm0")
			self.add_other_person("loanApartPersonForm1", "loanApartBankForm1")
			self.add_other_person("loanApartPersonForm2", "loanApartBankForm2")
			self.add_other_person("loanApartPersonForm3", "loanApartBankForm3")
			self.add_other_person("loanApartPersonForm4", "loanApartBankForm4")
		"""
		
		lf = "loanApartPersonForm"
		bf = "loanApartBankForm"
		if self.number == 0 or self.number == 1:
			self.personal_information()
		elif self.number == 2:
			self.personal_information()
			self.add_first_person(lf + "0", bf + "0")
		else:
			self.personal_information()
			self.add_first_person(lf + "0", bf + "0")
			count = 1
			for j in range(self.number, 2, -1):
				self.add_other_person(lf + str(count), bf + str(count))
				count = count + 1
		
		self.contract_save()
		self.contract_submit()
