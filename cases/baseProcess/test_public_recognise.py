import unittest

from com.login import Login


class PublicSetupAccount(unittest.TestCase):
	"""对公认账"""
	
	def setUp(self):
		pass
	
	def test_for_public_recognise(self):
		page = Login('xn071385')
		page.driver.find_element_by_id('1DF1A2778FE0000148CBDE1D1A006F00').click()
		page.driver.find_element_by_xpath('//*[@id="1DF1A2778FE0000148CBDE1D1A006F00"]/ul/li[1]').click()
		name = '红色法拉利'
		page.driver.switch_to.frame('bTabs_tab_house_commonIndex_wait_index')
		page.driver.find_element_by_name('factRepayName').click()
		page.driver.find_element_by_name('factRepayName').send_keys(name)
		money = '5000'
		page.driver.find_element_by_name('receiptAmount').send_keys(money)
		page.driver.find_element_by_name('receiptDateStart').send_keys('2018-05-29')
		page.driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/a[1]').click()
		page.driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/a[1]').click()
		page.driver.find_element_by_xpath('//*[@id="table_box"]/div/div/div[1]/div[2]/div[2]').click()
		res = page.driver.find_element_by_xpath('//*[@id="datagrid-row-r2-2-0"]/td[6]/div')
		print(res.text)
		page.driver.find_element_by_xpath('//*[@id="datagrid-row-r2-2-0"]/td[18]/div/button').click()
		# page.driver.find_element_by_xpath('//*[@id="contractNo"]').click()
		# page.driver.find_element_by_xpath('//*[@id="contractNo"]').send_keys('assss')
		page.driver.find_element_by_xpath('//*[@id="admitsModal"]/div/div/div[3]/button[2]').click()
		page.driver.find_element_by_xpath('//*[@id="admitsMoneyAllotModal"]/div/div/div[3]/button[2]').click()
	
	def tearDown(self):
		pass
