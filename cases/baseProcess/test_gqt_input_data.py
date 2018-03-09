# coding:utf-8

# --------------------------------------------------
# 过桥通录单流程
# ---------------------------------------------------

import unittest
from com import common, custom, base
from com.login import Login


class GQT(unittest.TestCase, base.Base):
	"""过桥通-1.0产品测试"""
	
	def setUp(self):
		self.env_file = "env.json"
		self.data_file = "data_gqt.json"
		base.Base.__init__(self, self.env_file, self.data_file)
	
	def tearDown(self):
		self.page.driver.quit()
	
	"""
		过桥通案件数据录入
	"""
	
	def test_gqt_01_base_info(self):
		"""过桥通产品客户基本信息录入"""
		
		custom.print_product_info(self.product_info)
		common.input_customer_base_info(self.page, self.data['applyVo'])
		self.log.info("客户基本信息录入结束")
	
	def test_gqt_02_input(self):
		"""过桥通产品借款人信息录入"""
		
		self.test_gqt_01_base_info()
		try:
			res = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])
			if res:
				self.log.info("录入借款人信息结束")
		except Exception as e:
			self.log.error("进件失败！:", e)
			raise e
	
	def test_gqt_03_Property_info(self):
		"""物业信息录入"""
		
		self.test_gqt_02_input()
		try:
			res = common.input_all_bbi_property_info(
					self.page,
					self.data['applyPropertyInfoVo'][0],
					self.data['applyCustCreditInfoVo'][0],
					True,
					'gqt'  # 过桥通产品需填写垫资情况
					)
			if res:
				self.log.info("录入物业信息结束")
			else:
				self.log.error('进件失败：录入物业信息出错！')
		except Exception as e:
			raise e
	
	def test_gqt_04_applydata(self):
		"""申请件录入,提交"""
		
		self.test_gqt_03_Property_info()
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
	
	def test_gqt_05_get_applyCode(self):
		"""申请件查询"""
		
		self.test_gqt_04_applydata()
		applycode = common.get_applycode(self.page, self.custName)
		
		if applycode:
			self.log.info("申请件查询完成")
			self.apply_code = applycode
		else:
			raise ValueError("applyCode error!")
	
	def test_gqt_06_show_task(self):
		"""查看待处理任务列表"""
		
		self.test_gqt_05_get_applyCode()
		next_id = common.process_monitor(self.page, self.apply_code)
		if next_id:
			self.log.info("下一个处理人:" + next_id)
			self.next_user_id = next_id
		else:
			raise ValueError("没有找到下一个处理人！")
		self.page.driver.quit()
		
		page = Login(self.next_user_id)
		
		res = common.query_task(page, self.apply_code)
		if res:
			self.log.info("查询待处理任务成功")
			page.driver.quit()
		else:
			raise ValueError("查询任务失败！")
	
	def test_gqt_07_process_monitor(self):
		"""流程监控"""
		
		self.test_gqt_05_get_applyCode()  # 申请件查询
		res = common.process_monitor(self.page, self.apply_code)  # l流程监控
		
		if not res:
			self.log.error("流程监控查询失败")
			raise AssertionError('流程监控查询失败')
		else:
			self.page.user_info['auth']["username"] = res  # 更新下一个登录人
			self.next_user_id = res
			self.log.info("next deal User: " + self.next_user_id)
			self.log.info("完成流程监控查询")
			self.page.driver.quit()
	
	def test_gqt_08_branch_supervisor_approval(self):
		"""分公司主管审批"""
		
		self.test_gqt_07_process_monitor()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批审核
		res = common.approval_to_review(page, self.apply_code, u'分公司主管同意审批')
		if not res:
			self.log.error("can't find applycode")
			raise ValueError("can't find applycode")
		
		# 查看下一步处理人
		next_id = common.process_monitor(page, self.apply_code)
		if not res:
			self.log.error("流程监控查询失败")
			raise AssertionError('流程监控查询失败')
		else:
			self.next_user_id = next_id
			self.log.info("风控审批-分公司主管审批结束")
			self.log.info("下一个处理人：" + self.next_user_id)
			page.driver.quit()
	
	def test_gqt_09_branch_manager_approval(self):
		"""分公司经理审批"""
		
		# 获取分公司经理登录ID
		self.test_gqt_08_branch_supervisor_approval()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批审核
		res = common.approval_to_review(page, self.apply_code, u'分公司经理同意审批')
		if not res:
			self.log.error("can't find applycode")
			raise ValueError("can't find applycode")
		
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code)
	
	def test_gqt_10_regional_prereview(self):
		"""区域预复核审批"""
		
		# 获取区域预复核员ID
		self.test_gqt_09_branch_manager_approval()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批审核
		res = common.approval_to_review(page, self.apply_code, u'区域预复核通过')
		if not res:
			raise ValueError("can't find applycode")
		
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code)
	
	def test_gqt_11_manager_approval(self):
		"""审批经理审批"""
		
		# 获取审批经理ID
		self.test_gqt_10_regional_prereview()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批审核
		res = common.approval_to_review(page, self.apply_code, u'高级审批经理审批')
		if not res:
			self.log.error("can't find applycode")
			raise ValueError("can't find applycode")
		
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code)
	
	def test_gqt_12_contract_signing(self):
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
		next_id = self.test_gqt_11_manager_approval()
		
		# 下一个处理人重新登录
		page = Login(next_id)
		
		# 签约
		common.make_signing(page, self.apply_code, rec_bank_info)
		
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code)
	
	def test_gqt_13_compliance_audit(self):
		"""合规审查"""
		
		# 获取下一步合同登录ID
		self.test_gqt_12_contract_signing()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 合规审查
		res = common.compliance_audit(page, self.apply_code)
		if res:
			self.log.info("合规审批结束")
			page.driver.quit()
		else:
			self.log.error("合规审查失败")
	
	def test_gqt_14_authority_card_member_transact(self):
		"""权证办理"""
		
		# 合规审查
		self.test_gqt_13_compliance_audit()
		# 权证员登录
		page = Login(self.company["authority_member"]["user"])
		# 权证员上传权证信息
		common.authority_card_transact(page, self.apply_code, self.env)
		# 查看下一步处理人
		res = common.process_monitor(page, self.apply_code)
		if not res:
			self.log.error("上传权证资料失败")
			raise AssertionError('上传权证资料失败')
		else:
			self.log.info("权证办理完成")
			self.next_user_id = res
			# 当前用户退出系统
			page.driver.quit()
	
	def test_gqt_15_warrant_apply(self):
		"""权证请款-原件请款"""
		
		# 获取合同打印专员ID
		self.test_gqt_14_authority_card_member_transact()
		page = Login(self.next_user_id)
		# 权证请款
		res = common.warrant_apply(page, self.apply_code)
		if not res:
			self.log.error("权证请款失败！")
			raise AssertionError('权证请款失败！')
		else:
			self.log.info("完成权证请款")
		self.page.driver.quit()
	
	def test_gqt_16_finace_transact(self):
		"""财务办理"""
		
		# 权证请款
		self.test_gqt_15_warrant_apply()
		# 业务助理登录
		page = Login(self.company["business_assistant"]["user"])
		result = common.finace_transact(page, self.apply_code)
		if result:
			self.log.info("完成财务办理")
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.apply_code, 1)
		if not res:
			raise ValueError('查询下一步处理人出错！')
		else:
			self.next_user_id = res
			# 当前用户退出系统
			page.driver.quit()
	
	def test_gqt_17_finace_approve_branch_manager(self):
		"""财务分公司经理审批"""
		
		remark = u"财务分公司经理审批"
		
		# 下一个处理人
		self.test_gqt_16_finace_transact()
		page = Login(self.next_user_id)
		result = common.finace_approve(page, self.apply_code, remark)
		
		if not result:
			raise ValueError('财务经理审批失败')
		else:
			self.log.info("财务流程-分公司经理审批结束")
		
		self.next_user_id = common.get_next_user(page, self.apply_code, 1)
	
	def test_gqt_18_finace_approve_risk_control_manager(self):
		"""财务风控经理审批"""
		
		remark = u'风控经理审批'
		
		self.test_gqt_17_finace_approve_branch_manager()
		page = Login(self.next_user_id)
		result = common.finace_approve(page, self.apply_code, remark)
		if result:
			self.log.info("财务流程-风控经理审批结束")
		else:
			self.log.error("Error: 风控经理审批出错！")
			raise AssertionError('风控经理审批出错')
		
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code, 1)
	
	def test_gqt_19_funds_appprove(self):
		"""资金主管审批"""
		
		remark = u'资金主管审批'
		self.test_gqt_18_finace_approve_risk_control_manager()
		page = Login(self.next_user_id)
		result = common.finace_approve(page, self.apply_code, remark)
		if result:
			self.log.info("财务流程-资金主管审批结束")
		else:
			self.log.error("Error-资金主管审批报错！")
			raise AssertionError('资金主管审批报错!')
		
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code, 1)
	
	def test_gqt_20_finace_approve_financial_accounting(self):
		"""财务会计审批"""
		
		remark = u'财务会计审批'
		
		self.test_gqt_19_funds_appprove()
		page = Login(self.next_user_id)
		result = common.finace_approve(page, self.apply_code, remark)
		if result:
			self.log.info("财务流程-财务会计审批结束")
		else:
			self.log.error("Error-财务会计审批报错！")
			raise AssertionError('Error-财务会计审批报错！')
		
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code, 1)
	
	def test_gqt_21_finace_approve_financial_manager(self):
		"""财务经理审批"""
		
		remark = u'财务经理审批'
		
		self.test_gqt_20_finace_approve_financial_accounting()
		page = Login(self.next_user_id)
		res = common.finace_approve(page, self.apply_code, remark)
		if res:
			self.log.info("财务流程-财务经理审批结束")
			page.driver.quit()
		else:
			self.log.error("Error-财务经理审批出错！")
			raise AssertionError('Error-财务经理审批出错！')
	
	def test_gqt_22_funds_raise(self):
		"""资金主管募资审批"""
		
		remark = u'资金主管审批'
		
		self.test_gqt_21_finace_approve_financial_manager()
		page = Login(self.treasurer)
		res = common.funds_raise(page, self.apply_code, remark)
		if res:
			self.log.info("募资流程-资金主管审批结束")
			page.driver.quit()
		else:
			self.log.error("Error-募资出错！")
			raise AssertionError('募资出错')


if __name__ == '__main__':
	unittest.main()
