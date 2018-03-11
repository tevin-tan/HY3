# coding:utf-8

import unittest
from com import common, custom, base
from com.login import Login
from com.pobj.ContractSign import ContractSign as Cts


class XHD(unittest.TestCase, base.Base):
	"""循环贷流程用例"""
	
	def setUp(self):
		self.env_file = "env.json"
		self.data_file = "data_xhd.json"
		base.Base.__init__(self, self.env_file, self.data_file)
	
	def tearDown(self):
		self.page.driver.quit()
	
	"""
		循环贷案件数据录入
	"""
	
	def test_xhd_01_base_info(self):
		"""客户基本信息录入"""
		
		custom.print_product_info(self.product_info)
		res = self.HAE.input_customer_base_info(self.page, self.data['applyVo'])
		if not res:
			self.log.error("客户基本信息录入出错！")
			raise AssertionError('客户基本信息录入出错')
		else:
			self.log.info("客户基本信息录入完成！")
	
	def test_xhd_02_borrowr_info(self):
		"""借款人/共贷人/担保人信息"""
		
		self.test_xhd_01_base_info()
		try:
			res = self.HAE.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
			if res:
				self.log.info("录入借款人信息结束")
		except Exception as e:
			self.log.error("进件失败！:", e)
			raise e
	
	def test_xhd_03_Property_info(self):
		"""物业信息录入"""
		
		self.test_xhd_02_borrowr_info()
		
		try:
			res = self.HAE.input_all_bbi_property_info(
					self.page,
					self.data['applyPropertyInfoVo'][0],
					self.data['applyCustCreditInfoVo'][0],
					True
					)
			if res:
				self.log.info("录入物业信息结束")
			else:
				self.log.error('进件失败：录入物业信息出错！')
		except Exception as e:
			raise e
	
	def test_xhd_04_applydata(self):
		"""申请件录入,提交"""
		
		self.test_xhd_03_Property_info()
		# 提交
		self.HAE.submit(self.page)
	
	def test_xhd_05_get_applyCode(self):
		"""申请件查询"""
		
		self.test_xhd_04_applydata()
		applycode = self.AQ.get_applycode(self.page, self.custName)
		if applycode:
			self.log.info("申请件查询完成")
			self.apply_code = applycode
		else:
			self.log.error("Can't get applyCode!")
			raise AssertionError("Can't get applyCode!")
	
	def test_xhd_06_show_task(self):
		"""查看待处理任务列表"""
		
		self.test_xhd_05_get_applyCode()
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
			self.log.info("待处理任务查询ok")
			page.driver.quit()
		else:
			self.log.error("待处理任务查询fail")
			raise AssertionError('待处理任务查询fail')
	
	def test_xhd_07_process_monitor(self):
		"""流程监控"""
		
		self.test_xhd_05_get_applyCode()  # 申请件查询
		res = self.PM.process_monitor(self.page, self.apply_code)  # l流程监控
		
		if not res:
			raise AssertionError('流程监控出错！')
		else:
			self.page.user_info['auth']["username"] = res  # 更新下一个登录人
			self.next_user_id = res
			self.log.info("Next Deal User: " + self.next_user_id)
	
	def test_xhd_08_branch_supervisor_approval(self):
		"""分公司主管审批"""
		
		# 获取分公司登录ID
		self.test_xhd_07_process_monitor()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批审核
		self.PT.approval_to_review(page, self.apply_code, u'分公司主管同意审批')
		
		# 查看下一步处理人
		next_id = self.PM.process_monitor(page, self.apply_code)
		if not next_id:
			self.log.error("Can't Get Next User")
			raise AssertionError("get Next user error!")
		else:
			self.next_user_id = next_id
			self.log.info("Next Deal User: " + self.next_user_id)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_xhd_09_branch_manager_approval(self):
		"""分公司经理审批"""
		
		# 获取分公司经理登录ID
		self.test_xhd_08_branch_supervisor_approval()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批审核
		res = self.PT.approval_to_review(page, self.apply_code, u'分公司经理同意审批')
		if not res:
			self.log.error("风控-分公司审批失败")
			raise AssertionError('风控-分公司审批失败')
		else:
			self.log.info("风控-分公司经理完成!")
		
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code)
	
	def test_xhd_10_regional_prereview(self):
		"""区域预复核审批"""
		
		# 获取区域预复核员ID
		self.test_xhd_09_branch_manager_approval()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批审核
		rs = self.PT.approval_to_review(page, self.apply_code, u'区域预复核通过')
		if not rs:
			self.log.error("风控-区域预复核失败")
			raise AssertionError('风控-区域预复核失败')
		else:
			self.log.info("风控-区域预复核成功！")
		
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code)
	
	def test_xhd_11_manager_approval(self):
		"""高级审批经理审批"""
		
		# 获取审批经理ID
		self.test_xhd_10_regional_prereview()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批审核
		result = self.PT.approval_to_review(page, self.apply_code, u'高级审批经理审批')
		if not result:
			self.log.error("风控-高级审批经理审批失败")
			raise AssertionError('风控-高级审批经理审批失败')
		else:
			self.log.info("风控-高级审批经理审批完成")
		
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code)
	
	def test_xhd_12_contract_signing(self):
		"""签约"""
		
		rec_bank_info = dict(
				recBankNum=self.data['houseCommonLoanInfoList'][0]['recBankNum'],
				recPhone=self.data['houseCommonLoanInfoList'][0]['recPhone'],
				recBankProvince=self.data['houseCommonLoanInfoList'][0]['recBankProvince'],
				recBankDistrict=self.data['houseCommonLoanInfoList'][0]['recBankDistrict'],
				recBank=self.data['houseCommonLoanInfoList'][0]['recBank'],
				recBankBranch=self.data['houseCommonLoanInfoList'][0]['recBankBranch'],
				)
		
		# 获取合同打印专员ID
		self.test_xhd_11_manager_approval()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 签约
		# rs = common.make_signing(page, self.apply_code, rec_bank_info)
		rs = Cts.ContractSign(page, self.apply_code, rec_bank_info).execute_sign()
		if not rs:
			self.log.error("签约失败")
			raise AssertionError('签约失败')
		else:
			self.log.info("签约成功")
		
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code)
	
	def test_xhd_13_compliance_audit(self):
		"""合规审查"""
		
		# 获取下一步合同登录ID
		self.test_xhd_12_contract_signing()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 合规审查
		res = self.PT.compliance_audit(page, self.apply_code)
		if not res:
			self.log.error("合规审查失败")
			raise AssertionError("合规审查失败")
		else:
			self.log.info("合规审查成功")
			page.driver.quit()
	
	def test_xhd_14_authority_card_member_transact(self):
		"""权证办理"""
		
		# 合规审查
		self.test_xhd_13_compliance_audit()
		# 权证员登录
		page = Login(self.company["authority_member"]["user"])
		# 权证员上传权证信息
		res = self.WM.authority_card_transact(page, self.apply_code, self.env)
		if not res:
			self.log.error("权证员上传资料失败")
			raise AssertionError('权证员上传资料失败')
		else:
			self.log.info("权证员上传资料成功！")
		
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code)
	
	def test_xhd_15_warrant_apply(self):
		"""权证请款-原件请款"""
		
		# 获取合同打印专员ID
		self.test_xhd_14_authority_card_member_transact()
		page = Login(self.next_user_id)
		# 权证请款
		res = self.WM.warrant_apply(page, self.apply_code)
		if not res:
			self.log.error("权证请款失败")
			raise AssertionError('权证请款失败')
		else:
			self.log.info("权证请款成功")
			page.driver.quit()
	
	def test_xhd_16_finace_transact(self):
		"""财务办理"""
		
		# 权证请款
		self.test_xhd_15_warrant_apply()
		# 业务助理登录
		page = Login(self.company["business_assistant"]["user"])
		result = self.FA.finace_transact(page, self.apply_code)
		if not result:
			self.log.error("财务办理失败")
			raise AssertionError('财务办理失败')
		else:
			self.log.info("财务办理成功")
		
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code, 1)
	
	def test_xhd_17_finace_approval_branch_manager(self):
		"""财务分公司经理审批"""
		
		remark = u"财务分公司经理审批"
		
		# 下一个处理人
		self.test_xhd_16_finace_transact()
		page = Login(self.next_user_id)
		result = self.FA.finace_approval(page, self.apply_code, remark)
		if not result:
			raise AssertionError('审批失败！')
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code, 1)
	
	def test_xhd_18_finace_approval_risk_control_manager(self):
		"""财务风控经理审批"""
		
		remark = u'风控经理审批'
		
		self.test_xhd_17_finace_approval_branch_manager()
		page = Login(self.next_user_id)
		result = self.FA.finace_approval(page, self.apply_code, remark)
		if not result:
			self.log.error("财务-风控经理审批出错")
			raise AssertionError('财务-风控经理审批出错')
		else:
			self.log.info("财务-风控经理审批完成")
		
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code, 1)
	
	def test_xhd_19_finace_approval_financial_accounting(self):
		"""财务会计审批"""
		
		remark = u'财务会计审批'
		
		self.test_xhd_18_finace_approval_risk_control_manager()
		page = Login(self.next_user_id)
		result = self.FA.finace_approval(page, self.apply_code, remark)
		if not result:
			self.log.error("财务-财务会计审批出错！")
			raise AssertionError('财务-财务会计审批出错')
		else:
			self.log.info("财务-财务会计审批完成！")
		
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code, 1)
	
	def test_xhd_20_finace_approval_financial_manager(self):
		"""财务经理审批"""
		
		remark = u'财务经理审批'
		
		self.test_xhd_19_finace_approval_financial_accounting()
		page = Login(self.next_user_id)
		res = self.FA.finace_approval(page, self.apply_code, remark)
		if not res:
			self.log.error("财务-财务经理审批出错！")
			raise AssertionError('财务-财务经理审批出错')
		else:
			self.log.info("财务-财务经理审批完成！")
			page.driver.quit()
	
	def test_xhd_21_funds_raise(self):
		"""资金主管募资审批"""
		
		remark = u'资金主管审批'
		
		self.test_xhd_20_finace_approval_financial_manager()
		page = Login(self.treasurer)
		res = self.RA.funds_raise(page, self.apply_code, remark)
		if not res:
			self.log.error("募资-资金主管审批出错！")
			raise AssertionError('募资-资金主管审批出错!')
		else:
			self.log.info("募资-资金主管审批完成！")
			page.driver.quit()


if __name__ == '__main__':
	unittest.main()
