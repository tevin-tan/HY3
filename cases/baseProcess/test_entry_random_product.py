# coding:utf-8
import datetime
import random
import time
import unittest

from cases import SET, v_l
from com import base, custom
from com.login import Login
from com.pobj.ContractSign import ContractSign as Cts
from config.product import product


class EntryRandomProduct(unittest.TestCase, base.Base, SET):
	"""任意产品进件"""
	
	def setUp(self):
		
		self.env_file = "env.json"
		self.data_file = "data_eyt.json"
		base.Base.__init__(self, self.env_file, self.data_file)
		SET.__init__(self)
		self.se = SET()
		self.se.start_run()
		
		pd = random.choice(product)
		print(pd)
		self.product_info.update(dict(name=pd['name']), period=str(pd['period']))
		# 设置产品
		self.data['applyVo']['productName'] = pd['name']
		self.data['applyVo']['applyPeriod'] = str(pd['period'])
	
	def tearDown(self):
		self.end_time = time.clock()
		self.case_using_time(self.begin_time, self.end_time)
		print(self.using_time)
		v_l.append({
			"name":       self.case_name,
			"apply_code": self.apply_code,
			"result":     self.run_result,
			"u_time":     self.using_time,
			"s_time":     self.s_time,
			"e_time":     str(datetime.datetime.now()).split('.')[0]
			})
		self.se.end_run(v_l)
		self.page.driver.quit()
	
	"""
		E押通案件数据录入
	"""
	
	def test_random_product_01_base_info(self):
		"""客户基本信息录入"""
		self.case_name = custom.get_current_function_name()
		
		try:
			# 打印贷款产品信息
			custom.print_product_info(self.product_info)
			if self.company['branchName'] not in self.city:
				# 非渠道城市进件
				self.HAE.input_customer_base_info(self.page, self.data['applyVo'])
			else:
				# 渠道城市非新产品
				if 'E押通-2.1' not in self.product_info['name']:
					self.HAE.input_customer_base_info(self.page, self.data['applyVo'])
				else:
					# 渠道城市新产品
					self.HAE.input_customer_base_info(self.page, self.data['applyVo'], True)
		except Exception as e:
			self.run_result = False
			raise e
	
	def test_random_product_02_borrowr_info(self):
		"""借款人/共贷人/担保人信息"""
		
		try:
			self.test_random_product_01_base_info()
			self.case_name = custom.get_current_function_name()
			res = self.HAE.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
			if res:
				self.log.info("录入借款人信息结束")
		except Exception as e:
			self.log.error("进件失败！")
			self.run_result = False
			raise e
	
	def test_random_product_03_Property_info(self):
		"""物业信息录入"""
		
		try:
			self.test_random_product_02_borrowr_info()
			self.case_name = custom.get_current_function_name()
			res = self.HAE.input_all_bbi_property_info(
				self.page,
				self.data['applyPropertyInfoVo'][0],
				self.data['applyCustCreditInfoVo'][0],
				self.cust_name,
				True
				)
			if res:
				self.log.info("录入物业信息结束")
			else:
				self.log.error('进件失败：录入物业信息出错！')
		except Exception as e:
			self.run_result = False
			raise e
	
	def test_random_product_04_applydata(self):
		"""申请件录入,提交"""
		
		try:
			self.test_random_product_03_Property_info()
			self.case_name = custom.get_current_function_name()
			self.HAE.submit(self.page)
		except Exception as e:
			self.run_result = False
			raise e
	
	def test_random_product_05_get_applyCode(self):
		"""申请件查询"""
		
		try:
			self.test_random_product_04_applydata()
			self.case_name = custom.get_current_function_name()
			applycode = self.AQ.get_applycode(self.page, self.cust_name)
			if applycode:
				self.log.info("申请件查询完成")
				self.apply_code = applycode
			else:
				self.log.error("can't get applyCode!")
				raise ValueError("can't get applyCode!")
		except Exception as e:
			self.run_result = False
			raise e
	
	def test_random_product_06_show_task(self):
		"""查看待处理任务列表"""
		
		try:
			self.test_random_product_05_get_applyCode()
			self.case_name = custom.get_current_function_name()
			next_id = self.PM.process_monitor(self.page, self.apply_code)
			if next_id:
				self.log.info("下一个处理人:" + next_id)
				self.next_user_id = next_id
			else:
				raise ValueError("没有找到下一个处理人！")
			self.page.driver.quit()
			
			page = Login(self.next_user_id)
			
			res = self.PT.query_task(page, self.apply_code)
			if res:
				self.log.info("待处理任务列表中存在该笔案件！")
			else:
				self.log.error("待处理任务列表中不存在该笔案件！")
				raise ValueError("查询失败")
		except Exception as e:
			self.run_result = False
			raise e
	
	def test_random_product_07_process_monitor(self):
		"""流程监控"""
		try:
			self.test_random_product_05_get_applyCode()  # 申请件查询
			self.case_name = custom.get_current_function_name()
			res = self.PM.process_monitor(self.page, self.apply_code)  # l流程监控
			if not res:
				raise ValueError("流程监控错误！")
			else:
				self.page.user_info['auth']["username"] = res  # 更新下一个登录人
				self.next_user_id = res
				self.log.info("next deal User: " + self.next_user_id)
		except Exception as e:
			self.run_result = False
			raise e
	
	def test_random_product_08_branch_supervisor_approval(self):
		"""分公司主管审批"""
		
		try:
			# 获取分公司登录ID
			self.test_random_product_07_process_monitor()
			self.case_name = custom.get_current_function_name()
			# 下一个处理人重新登录
			page = Login(self.next_user_id)
			
			# 审批审核
			self.PT.approval_to_review(page, self.apply_code, u'分公司主管同意审批', 0, True)
			
			# 查看下一步处理人
			next_id = self.PM.process_monitor(page, self.apply_code)
			if not next_id:
				raise AssertionError("没有找到下一个处理人")
			else:
				self.next_user_id = next_id
				self.log.info("下一个处理人：" + self.next_user_id)
				# 当前用户退出系统
				page.driver.quit()
		except Exception as e:
			self.run_result = False
			raise e
	
	def test_random_product_09_branch_manager_approval(self):
		"""分公司经理审批"""
		
		try:
			# 获取分公司经理登录ID
			self.test_random_product_08_branch_supervisor_approval()
			self.case_name = custom.get_current_function_name()
			# 下一个处理人重新登录
			page = Login(self.next_user_id)
			
			# 审批审核
			self.PT.approval_to_review(page, self.apply_code, u'分公司经理同意审批')
			
			# 查看下一步处理人
			res = self.PM.process_monitor(page, self.apply_code)
			if not res:
				raise AssertionError("没有找到下一个处理人")
			else:
				self.next_user_id = res
				self.log.info("下一个处理人: " + self.next_user_id)
				# 当前用户退出系统
				page.driver.quit()
		except Exception as e:
			self.run_result = False
			raise e
	
	def test_random_product_10_regional_prereview(self):
		"""区域预复核审批"""
		try:
			# 获取区域预复核员ID
			self.test_random_product_09_branch_manager_approval()
			self.case_name = custom.get_current_function_name()
			# 下一个处理人重新登录
			page = Login(self.next_user_id)
			
			# 审批审核
			res = self.PT.approval_to_review(page, self.apply_code, u'区域预复核通过')
			if not res:
				self.log.error("区域预复核失败")
				raise AssertionError("区域预复核失败")
			else:
				self.log.info("区域预复核审批完成！")
			
			# 查看下一步处理人
			res = self.PM.process_monitor(page, self.apply_code)
			if not res:
				self.log.error("Can't not found the next UserId")
				raise AssertionError("Can't not found the next UserId")
			else:
				self.next_user_id = res
				self.log.info("next_user_id %s", self.next_user_id)
				# 当前用户退出系统
				page.driver.quit()
		except Exception as e:
			self.run_result = False
			raise e
	
	def test_random_product_11_manager_approval(self):
		"""高级审批经理审批"""
		try:
			# 获取审批经理ID
			self.test_random_product_10_regional_prereview()
			self.case_name = custom.get_current_function_name()
			# 下一个处理人重新登录
			page = Login(self.next_user_id)
			
			# 审批审核
			self.PT.approval_to_review(page, self.apply_code, u'高级审批经理审批')
			
			# 查看下一步处理人
			res = self.PM.process_monitor(page, self.apply_code)
			if not res:
				raise AssertionError('没有找到下一个处理人')
			else:
				self.next_user_id = res
				self.next_user_id = res
				self.log.info("下一个处理人:" + res)
				# 当前用户退出系统
				page.driver.quit()
		except Exception as e:
			self.run_result = False
			raise e
	
	def test_random_product_12_contract_signing(self):
		"""签约"""
		
		# 收款银行信息
		rec_bank_info = dict(
			recBankNum='6210302082441017886',
			recPhone='13686467482',
			recBankProvince=u'湖南省',
			recBankDistrict=u'长沙',
			recBank=u'中国农业银行',
			recBankBranch=u'北京支行',
			)
		
		try:
			# 获取合同打印专员ID
			self.test_random_product_11_manager_approval()
			self.case_name = custom.get_current_function_name()
			# 下一个处理人重新登录
			page = Login(self.next_user_id)
			
			# 签约
			rc = Cts.ContractSign(page, self.apply_code, rec_bank_info)
			res = rc.execute_enter_borroers_bank_info()
			if res:
				rc.contract_submit()
			
			# 查看下一步处理人
			res = self.PM.process_monitor(page, self.apply_code)
			if not res:
				raise AssertionError('没有找到下一个处理人')
			else:
				self.next_user_id = res
				self.log.info("下一个处理人: " + self.next_user_id)
				# 当前用户退出系统
				page.driver.quit()
		except Exception as e:
			self.run_result = False
			raise e
	
	def test_random_product_13_compliance_audit(self):
		"""合规审查"""
		
		try:
			# 获取下一步合同登录ID
			self.test_random_product_12_contract_signing()
			self.case_name = custom.get_current_function_name()
			# 下一个处理人重新登录
			page = Login(self.next_user_id)
			
			# 合规审查
			res = self.PT.compliance_audit(page, self.apply_code)
			if res:
				self.log.info("合规审查通过")
			else:
				self.log.error("合规审查失败")
				raise AssertionError('合规审查失败')
			page.driver.quit()
		except Exception as e:
			self.run_result = False
			raise e
	
	def test_random_product_14_authority_card_member_transact(self):
		"""权证办理"""
		
		try:
			# 合规审查
			self.test_random_product_13_compliance_audit()
			self.case_name = custom.get_current_function_name()
			# 权证员登录
			page = Login(self.company["authority_member"]["user"])
			# 权证员上传权证信息
			rs = self.WM.authority_card_transact(page, self.apply_code, self.env)
			if not rs:
				self.log.error("上传权证信息失败")
				raise AssertionError('上传权证信息失败')
			
			# 查看下一步处理人
			res = self.PM.process_monitor(page, self.apply_code)
			if not res:
				self.log.error("权证办理-没找到下一步处理人")
				raise AssertionError('权证办理-没找到下一步处理人')
			else:
				self.next_user_id = res
				self.log.info("下一步处理人：%s", self.next_user_id)
				# 当前用户退出系统
				page.driver.quit()
		except BaseException as e:
			self.run_result = False
			raise e
	
	def test_random_product_15_warrant_apply(self):
		"""权证请款-原件请款"""
		
		# 获取合同打印专员ID
		self.test_random_product_14_authority_card_member_transact()
		self.case_name = custom.get_current_function_name()
		page = Login(self.next_user_id)
		# 权证请款
		res = self.WM.warrant_apply(page, self.apply_code)
		if res:
			self.log.info("权证请款成功")
			page.driver.quit()
		else:
			self.log.error("权证请款失败")
			raise AssertionError('权证请款失败')
	
	def test_random_product_16_finace_transact(self):
		"""财务办理"""
		
		# 权证请款
		self.test_random_product_15_warrant_apply()
		self.case_name = custom.get_current_function_name()
		# 业务助理登录
		page = Login(self.company["business_assistant"]["user"])
		rs = self.FA.finace_transact(page, self.apply_code)
		if not rs:
			self.log.error("财务办理失败")
			raise AssertionError('财务办理失败')
		
		# 查看下一步处理人
		res = self.PM.process_monitor(page, self.apply_code, 1)
		if not res:
			self.log.error("没有找到下一步处理人")
			raise AssertionError('没有找到下一步处理人')
		else:
			self.next_user_id = res
			self.log.info("下一步处理人：%s", self.next_user_id)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_random_product_17_finace_approval_branch_manager(self):
		"""财务分公司经理审批"""
		
		remark = u"财务分公司经理审批"
		
		# 下一个处理人
		self.test_random_product_16_finace_transact()
		self.case_name = custom.get_current_function_name()
		page = Login(self.next_user_id)
		result = self.FA.finace_approval(page, self.apply_code, remark)
		if not result:
			self.log.error("财务流程-分公司经理审批失败")
			raise AssertionError('财务流程-分公司经理审批失败')
		# 查看下一步处理人
		res = self.PM.process_monitor(page, self.apply_code, 1)
		if not res:
			self.log.error("没有找到下一步处理人")
			raise AssertionError('没有找到下一步处理人')
		else:
			self.next_user_id = res
			self.log.info("下一步处理人: %s", self.next_user_id)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_random_product_18_finace_approval_risk_control_manager(self):
		"""财务风控经理审批"""
		
		remark = u'风控经理审批'
		
		self.test_random_product_17_finace_approval_branch_manager()
		self.case_name = custom.get_current_function_name()
		page = Login(self.next_user_id)
		result = self.FA.finace_approval(page, self.apply_code, remark)
		if not result:
			self.log.error("财务流程-风控经理审批出错")
			raise AssertionError('财务流程-风控经理审批出错')
		else:
			self.log.info("财务流程-风控经理审批完成")
		
		# 查看下一步处理人
		res = self.PM.process_monitor(page, self.apply_code, 1)
		if not res:
			self.log.error("Can't found the next userId!")
			raise AssertionError("Can't found the next userId!")
		else:
			self.next_user_id = res
			self.log.info("下一步处理人:%s", self.next_user_id)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_random_product_19_finace_approval_financial_accounting(self):
		"""财务会计审批"""
		
		remark = u'财务会计审批'
		
		self.test_random_product_18_finace_approval_risk_control_manager()
		self.case_name = custom.get_current_function_name()
		page = Login(self.next_user_id)
		rs = self.FA.finace_approval(page, self.apply_code, remark)
		if not rs:
			self.log.error("财务流程-财务会计审批失败")
			raise AssertionError('财务流程-财务会计审批失败')
		else:
			self.log.info("财务流程-财务会计审批完成")
		
		# 查看下一步处理人
		res = self.PM.process_monitor(page, self.apply_code, 1)
		if not res:
			self.log.error("Can't found The next UserId")
			raise AssertionError("Can't found The next UserId")
		else:
			self.next_user_id = res
			self.log.info("nextId is %s", self.next_user_id)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_random_product_20_finace_approval_financial_manager(self):
		"""财务经理审批"""
		
		remark = u'财务经理审批'
		
		self.test_random_product_19_finace_approval_financial_accounting()
		
		self.case_name = custom.get_current_function_name()
		page = Login(self.next_user_id)
		res = self.FA.finace_approval(page, self.apply_code, remark)
		if not res:
			self.log.error("财务流程-财务经理审批失败")
			raise AssertionError('财务流程-财务经理审批失败')
		else:
			self.log.info("财务流程-财务经理审批完成")
			page.driver.quit()
	
	def test_random_product_21_funds_raise(self):
		"""募资-资金主管募资审批"""
		
		remark = u'资金主管审批'
		
		self.test_random_product_20_finace_approval_financial_manager()
		self.case_name = custom.get_current_function_name()
		page = Login(self.treasurer)
		res = self.RA.funds_raise(page, self.apply_code, remark)
		if not res:
			self.log.error("募资-资金主管审批失败")
			raise AssertionError('募资-资金主管审批失败')
		else:
			self.log.info("募资-资金主管审批完成!")
			self.page.driver.quit()


if __name__ == '__main__':
	unittest.main()
