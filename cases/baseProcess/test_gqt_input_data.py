# coding:utf-8

# --------------------------------------------------
# 过桥通录单流程
# ---------------------------------------------------

import unittest
import os
import json
from com import common
from com.login import Login
from com import custom
from com.custom import get_name, Log, enviroment_change


class GQT(unittest.TestCase):
	'''过桥通-1.0产品测试'''
	
	def setUp(self):
		self.page = Login()
		self.applyCode = ''
		self.next_user_id = ""
		self.cust_info = dict(
				_borrow_info=dict(
						custName=get_name(),
						idNum="360101199101011054",
						phone="13564789215",
						address=u"湖南长沙",
						companyName=u'小牛普惠管理有限公司',
						postName=u'工程师',
						workDate=u'2011-02-03',  # 入职日期
						workYear=5,  # 工作年限
						monthIncoming=15000  # 月均收入
						),
				_cust_base_info=dict(
						productName=u'过桥通-1.0(一线城市)',  # 贷款产品
						applyAmount=50000,  # 申请金额
						applyPeriod=10,  # 贷款天数
						branchManager=u"小明",
						branchManagerCode="xn111",
						teamGroup=u"A队",
						teamGroupCode="xn0001",
						teamManager=u"小王",
						teamManagerCode="xn0001",
						sale=u"王刚",
						saleCode="xn0002",
						monthIncome=3000,
						checkApprove=u"同意",
						)
				)
		
		self.loan_amount = 200000  # 拆分金额
		self.log = Log()
		
		try:
			import config
			rootdir = config.__path__[0]
			config_env = os.path.join(rootdir, 'env.json')
			# print("config_env:" + config_env)
			with open(config_env, 'r', encoding='utf-8') as f:
				self.da = json.load(f)
				self.number = self.da["number"]
				self.env = self.da["enviroment"]
			f.close()
			filename = "data_gqt.json"
			data, company = enviroment_change(filename, self.number, self.env)
			# 录入的源数据
			self.data = data
			# 分公司选择
			self.company = company
			custom.print_env(self.env, self.company)
		except Exception as e:
			print('load config error:', str(e))
			raise e
	
	def tearDown(self):
		self.page.quit()
	
	'''
		  过桥通案件数据录入
	'''
	
	def test_gqt_01_base_info(self):
		'''过桥通产品客户基本信息录入'''
		
		common.input_customer_base_info(self.page, self.cust_info['_cust_base_info'])
		self.log.info("客户基本信息录入结束")
	
	def test_gqt_02_input(self):
		'''过桥通产品借款人信息录入'''
		
		# 1 客户信息-业务基本信息
		common.input_customer_base_info(self.page, self.cust_info['_cust_base_info'])
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		common.input_customer_borrow_info(self.page, self.cust_info['_borrow_info'])
	
	def test_cwd_03_Property_info(self):
		'''物业信息录入'''
		
		# 1 客户信息-业务基本信息
		common.input_customer_base_info(self.page, self.cust_info['_cust_base_info'])
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		common.input_customer_borrow_info(self.page, self.cust_info['_borrow_info'])
		
		common.input_cwd_bbi_property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		
		self.log.info("录入物业信息结束")
	
	def test_gqt_04_applydata(self):
		'''申请件录入,提交'''
		
		# 1 客户信息-业务基本信息
		common.input_customer_base_info(self.page, self.data['applyVo'])
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.custName = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])[1]
		
		# 3 物业信息
		common.input_cwd_bbi_property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0], True, 'gqt')
		
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
	
	def test_gqt_05_get_applyCode(self):
		'''申请件查询'''
		
		self.test_gqt_04_applydata()
		applycode = common.get_applycode(self.page, self.custName)
		
		if applycode:
			self.log.info("申请件查询完成")
			self.applyCode = applycode
			return applycode, True
		else:
			return None, False
	
	def test_gqt_06_show_task(self):
		'''查看待处理任务列表'''
		
		self.test_gqt_05_get_applyCode()[0]
		next_id = common.process_monitor(self.page, self.applyCode)
		if next_id:
			self.log.info("下一个处理人:" + next_id)
			self.next_user_id = next_id
		else:
			raise ValueError("没有找到下一个处理人！")
		self.page.driver.quit()
		
		page = Login(self.next_user_id)
		
		res = common.query_task(page, self.applyCode)
		if res:
			self.log.info("查询待处理任务成功")
			return True
		else:
			return False
	
	def test_gqt_07_process_monitor(self):
		'''流程监控'''
		
		result = self.test_gqt_05_get_applyCode()  # 申请件查询
		res = common.process_monitor(self.page, result[0])  # l流程监控
		
		if not res:
			self.log.error("流程监控查询失败")
			raise AssertionError('流程监控查询失败')
		else:
			self.page.user_info['auth']["username"] = res  # 更新下一个登录人
			print(self.page.user_info['auth']["username"])
			self.next_user_id = res
			self.log.info("完成流程监控查询")
			return res, result[0]  # (下一个处理人ID, 申请件ID)
	
	def test_gqt_08_branch_supervisor_approval(self):
		'''分公司主管审批'''
		
		# 获取分公司登录ID
		res = self.test_gqt_07_process_monitor()
		print("userId:" + res[0])
		
		# 下一个处理人重新登录
		page = Login(res[0])
		
		# 审批审核
		res = common.approval_to_review(page, res[1], u'分公司主管同意审批')
		if not res:
			self.log.error("can't find applycode")
			raise ValueError("can't find applycode")
		
		# 查看下一步处理人
		next_id = common.process_monitor(page, self.applyCode)
		if not res:
			self.log.error("流程监控查询失败")
			raise AssertionError('流程监控查询失败')
		else:
			self.next_user_id = next_id
			self.log.info("风控审批-分公司主管审批结束")
			# 当前用户退出系统
			self.page.driver.quit()
			return next_id  # 下一步处理人ID
	
	def test_gqt_09_branch_manager_approval(self):
		'''分公司经理审批'''
		
		# 获取分公司经理登录ID
		next_id = self.test_gqt_08_branch_supervisor_approval()
		
		# 下一个处理人重新登录
		page = Login(next_id)
		
		# 审批审核
		res = common.approval_to_review(page, self.applyCode, u'分公司经理同意审批')
		if not res:
			self.log.error("can't find applycode")
			raise ValueError("can't find applycode")
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode)
		if not res:
			return False
		else:
			self.next_user_id = res
			self.log.info("风控审批-分公司经理审批结束")
			# 当前用户退出系统
			self.page.driver.quit()
			return res
	
	def test_gqt_10_regional_prereview(self):
		'''区域预复核审批'''
		
		# 获取区域预复核员ID
		next_id = self.test_gqt_09_branch_manager_approval()
		
		# 下一个处理人重新登录
		page = Login(next_id)
		
		# 审批审核
		res = common.approval_to_review(page, self.applyCode, u'区域预复核通过')
		if not res:
			raise ValueError("can't find applycode")
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode)
		if not res:
			return False
		else:
			self.next_user_id = res
			self.log.info("区域预复核审批结束")
			# 当前用户退出系统
			self.page.driver.quit()
			return res
	
	def test_gqt_11_manager_approval(self):
		'''审批经理审批'''
		
		# 获取审批经理ID
		next_id = self.test_gqt_10_regional_prereview()
		
		# 下一个处理人重新登录
		page = Login(next_id)
		
		# 审批审核
		res = common.approval_to_review(page, self.applyCode, u'审批经理审批')
		if not res:
			self.log.error("can't find applycode")
			raise ValueError("can't find applycode")
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode)
		if not res:
			return False
		else:
			self.next_user_id = res
			self.log.info("风控审批-审批经理审批结束")
			# 当前用户退出系统
			self.page.driver.quit()
			return res
	
	def test_gqt_12_contract_signing(self):
		'''签约'''
		
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
		common.make_signing(page, self.applyCode, rec_bank_info)
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode)
		if not res:
			return False
		else:
			self.next_user_id = res
			self.log.info("合同打印完成")
			# 当前用户退出系统
			self.page.driver.quit()
			return res
	
	def test_gqt_13_compliance_audit(self):
		'''合规审查'''
		
		# 获取下一步合同登录ID
		next_id = self.test_gqt_12_contract_signing()
		
		# 下一个处理人重新登录
		page = Login(next_id)
		
		# 合规审查
		res = common.compliance_audit(page, self.applyCode)
		if res:
			self.log.info("合规审批结束")
		else:
			self.log.error("合规审查失败")
	
	def test_gqt_14_authority_card_member_transact(self):
		'''权证办理'''
		
		# 合规审查
		self.test_gqt_13_compliance_audit()
		# 权证员登录
		page = Login(self.company["authority_member"]["user"])
		# 权证员上传权证信息
		common.authority_card_transact(page, self.applyCode, self.env)
		# common.authority_card_transact(page, "GZ20171213C06")
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode)
		if not res:
			self.log.error("上传权证资料失败")
			raise AssertionError('上传权证资料失败')
		else:
			self.log.info("权证办理完成")
			self.next_user_id = res
			# 当前用户退出系统
			page.driver.quit()
			self.page.driver.quit()
			return res
	
	def test_gqt_15_warrant_apply(self):
		'''权证请款-原件请款'''
		
		# 获取合同打印专员ID
		next_id = self.test_gqt_14_authority_card_member_transact()
		page = Login(next_id)
		# 权证请款
		res = common.warrant_apply(page, self.applyCode)
		if not res:
			self.log.error("权证请款失败！")
			raise AssertionError('权证请款失败！')
		else:
			self.log.info("完成权证请款")
		self.page.driver.quit()
	
	def test_gqt_16_finace_transact(self):
		'''财务办理'''
		
		# 权证请款
		self.test_gqt_15_warrant_apply()
		# 业务助理登录
		page = Login(self.company["business_assistant"]["user"])
		common.finace_transact(page, self.applyCode)
		self.log.info("完成财务办理")
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode, 1)
		if not res:
			return False
		else:
			self.next_user_id = res
			# 当前用户退出系统
			self.page.driver.quit()
			return res
	
	def test_gqt_17_finace_approve_branch_manager(self):
		'''财务分公司经理审批'''
		
		remark = u"财务分公司经理审批"
		
		# 下一个处理人
		self.test_gqt_16_finace_transact()
		page = Login(self.next_user_id)
		result = common.finace_approve(page, self.applyCode, remark)
		
		if not result:
			return False
		else:
			self.log.info("财务流程-分公司经理审批结束")
			# 查看下一步处理人
			res = common.process_monitor(page, self.applyCode, 1)
			if not res:
				return False
			else:
				self.next_user_id = res
				print("nextId:" + res)
				# 当前用户退出系统
				page.driver.quit()
				self.page.driver.quit()
				return res
	
	def test_gqt_18_finace_approve_risk_control_manager(self):
		'''财务风控经理审批'''
		
		remark = u'风控经理审批'
		
		self.test_gqt_17_finace_approve_branch_manager()
		page = Login(self.next_user_id)
		result = common.finace_approve(page, self.applyCode, remark)
		if result:
			self.log.info("财务流程-风控经理审批结束")
		else:
			self.log.error("Error: 风控经理审批出错！")
			raise AssertionError('风控经理审批出错')
		# page = Login('xn003625')
		# common.finace_approve(page, "CS20171215X14", remark)
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode, 1)
		if not res:
			return False
		else:
			self.next_user_id = res
			print("nextId:" + self.next_user_id)
			# 当前用户退出系统
			self.page.driver.quit()
			return res
	
	def test_gqt_19_funds_appprove(self):
		'''资金主管审批'''
		
		remark = u'资金主管审批'
		self.test_gqt_18_finace_approve_risk_control_manager()
		page = Login(self.next_user_id)
		result = common.finace_approve(page, self.applyCode, remark)
		if result:
			self.log.info("财务流程-资金主管审批结束")
		else:
			self.log.error("Error-资金主管审批报错！")
			raise AssertionError('资金主管审批报错!')
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode, 1)
		if not res:
			return False
		else:
			self.next_user_id = res
			print("nextId:" + self.next_user_id)
			# 当前用户退出系统
			self.page.driver.quit()
			return res
	
	def test_gqt_20_finace_approve_financial_accounting(self):
		'''财务会计审批'''
		
		remark = u'财务会计审批'
		
		self.test_gqt_19_funds_appprove()
		page = Login(self.next_user_id)
		result = common.finace_approve(page, self.applyCode, remark)
		if result:
			self.log.info("财务流程-财务会计审批结束")
		else:
			self.log.error("Error-财务会计审批报错！")
			raise AssertionError('Error-财务会计审批报错！')
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode, 1)
		if not res:
			return False
		else:
			self.next_user_id = res
			print("nextId:" + self.next_user_id)
			# 当前用户退出系统
			self.page.driver.quit()
			return res
	
	def test_gqt_21_finace_approve_financial_manager(self):
		'''财务经理审批'''
		
		remark = u'财务经理审批'
		
		self.test_gqt_20_finace_approve_financial_accounting()
		page = Login(self.next_user_id)
		res = common.finace_approve(page, self.applyCode, remark)
		if res:
			self.log.info("财务流程-财务经理审批结束")
		else:
			self.log.error("Error-财务经理审批出错！")
			raise AssertionError('Error-财务经理审批出错！')
	
	def test_gqt_22_funds_raise(self):
		'''资金主管募资审批'''
		
		remark = u'资金主管审批'
		
		self.test_gqt_21_finace_approve_financial_manager()
		page = Login('xn0007533')
		res = common.funds_raise(page, self.applyCode, remark)
		if res:
			self.log.info("募资流程-资金主管审批结束")
			self.page.driver.quit()
		else:
			self.log.error("Error-募资出错！")
			raise AssertionError('募资出错')


if __name__ == '__main__':
	unittest.main()
