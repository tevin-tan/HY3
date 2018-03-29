# coding:utf-8
import time

from com import custom


class HouseRefuseLIst(object):
	"""房贷拒绝队列"""
	
	def __init__(self):
		self.log = custom.mylog()
	
	def reconsideration(self, page, applycode, action=0):
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
		time.sleep(1)
		page.driver.find_element_by_name('applyCode').send_keys(applycode)
		time.sleep(1)
		page.driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/a[1]').click()  # 查询
		time.sleep(1)
		if action == 0:
			page.driver.find_element_by_id('frmQuery').click()
			t1 = page.driver.find_element_by_xpath('//*[@id="datagrid-row-r1-2-0"]/td[13]/div')
			if t1.text != "":
				self.log.info("拒绝案件:" + t1.text)
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
			self.log.error("param wrong!")
			return False
