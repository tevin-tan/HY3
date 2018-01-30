# coding:utf-8

'''
    过桥通录单流程
'''

import random
import time
import os
import json
import unittest

from com import common
from com.login import Login
from com.custom import getName, Log, enviroment_change


class XHD(unittest.TestCase):
	'''循环贷流程用例'''
	
	def _init_params(self):
		self.cust_info = dict(
				_borrow_info=dict(
						custName=getName(),
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
						productName=u'循环贷-1.0',  # 贷款产品
						applyAmount=200000,  # 申请金额
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
		
		self.property_info = dict(
				propertyOwner=self.cust_info['_borrow_info']['custName'],
				propertyNo="ABCDEFG",
				)
	
	def setUp(self):
		self._init_params()
		self.page = Login()
		self.applyCode = ''
		self.log = Log()
		try:
			import config
			rootdir = config.__path__[0]
			config_env = os.path.join(rootdir, 'env.json')
			print("config_env:" + config_env)
			with open(config_env, 'r') as f:
				self.da = json.load(f)
				self.number = self.da["number"]
				self.env = self.da["enviroment"]
			
			filename = "data_cwd.json"
			data, company = enviroment_change(filename, self.number, self.env)
			# 录入的源数据
			self.data = data
			# 分公司选择
			self.company = company
		except Exception as e:
			print('load config error:', str(e))
			raise
	
	def tearDown(self):
		self.page.quit()
	
	'''
		  循环贷案件数据录入
	'''
	
	def test_xhd_01_base_info(self):
		'''客户基本信息录入'''
		res = common.input_customer_base_info(self.page, self.cust_info['_cust_base_info'])
		if not res:
			self.log.error("客户基本信息录入出错！")
			raise
		else:
			self.log.info("客户基本信息录入完成！")
	
	def test_xhd_02_borrowr_info(self):
		'''借款人/共贷人/担保人信息'''
		common.input_customer_base_info(self.page, self.cust_info['_cust_base_info'])
		common.input_customer_borrow_info(self.page, self.cust_info['_borrow_info'])
	
	def test_xhd_03_Property_info(self):
		'''物业信息录入'''
		common.input_customer_base_info(self.page, self.cust_info['_cust_base_info'])
		common.input_customer_borrow_info(self.page, self.cust_info['_borrow_info'])
		common.input_bbi_Property_info(self.page)
	
	def test_xhd_04_applydata(self):
		'''申请件录入,提交'''
		
		# 1 客户信息-业务基本信息
		# log_to().info(u"客户基本信息录入")
		common.input_customer_base_info(self.page, self.cust_info['_cust_base_info'])
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		# log_to().info(u"借款人/共贷人信息录入")
		self.custName = common.input_customer_borrow_info(self.page, self.cust_info['_borrow_info'])[1]
		
		# 3 物业信息
		# log_to().info(u"物业基本信息录入")
		common.input_bbi_Property_info(self.page)
		
		# 提交
		common.submit(self.page)
	
	def test_xhd_05_get_applyCode(self):
		'''申请件查询'''
		
		self.test_xhd_04_applydata()
		applycode = common.get_applycode(self.page, self.custName)
		if applycode:
			self.log.info("申请件查询完成")
			self.applyCode = applycode
		else:
			self.log.error("Can't get applyCode!")
			raise
	
	def test_xhd_06_show_task(self):
		'''查看待处理任务列表'''
		self.test_xhd_05_get_applyCode()
		next_id = common.process_monitor(self.page, self.applyCode)
		if next_id:
			self.log.info("下一个处理人:"+ next_id)
			self.next_user_id = next_id
		else:
			raise ValueError("没有找到下一个处理人！")
		self.page.driver.quit()
		
		page = Login(self.next_user_id)
		
		res = common.query_task(page, self.applyCode)
		if res:
			self.log.info("待处理任务查询ok")
		else:
			self.log.info("待处理任务查询fail")
			raise
	
	def test_xhd_07_process_monitor(self):
		'''流程监控'''
		
		self.test_xhd_05_get_applyCode()  # 申请件查询
		res = common.process_monitor(self.page, self.applyCode)  # l流程监控
		
		if not res:
			raise
		else:
			self.page.user_info['auth']["username"] = res  # 更新下一个登录人
			self.next_user_id = res
			self.log.info("Next Deal User: " + self.next_user_id)
	
	def test_xhd_08_branch_supervisor_approval(self):
		'''分公司主管审批'''
		
		# 获取分公司登录ID
		self.test_xhd_07_process_monitor()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批审核
		common.approval_to_review(page, self.applyCode, u'分公司主管同意审批')
		
		# 查看下一步处理人
		next_id = common.process_monitor(page, self.applyCode)
		if not next_id:
			self.log.error("Can't Get Next User")
			raise
		else:
			self.next_user_id = next_id
			self.log.info("Next Deal User: " + self.next_user_id)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_xhd_09_branch_manager_approval(self):
		'''分公司经理审批'''
		
		# 获取分公司经理登录ID
		self.test_xhd_08_branch_supervisor_approval()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批审核
		res = common.approval_to_review(page, self.applyCode, u'分公司经理同意审批')
		if not res:
			Log().error("风控-分公司审批失败")
			raise
		else:
			Log().info("风控-分公司经理完成!")
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode)
		if not res:
			Log().error("Can't found the next userId!")
			raise
		else:
			self.next_user_id = res
			Log().info("next User Id is :%s", res)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_xhd_10_regional_prereview(self):
		'''区域预复核审批'''
		
		# 获取区域预复核员ID
		self.test_xhd_09_branch_manager_approval()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批审核
		rs = common.approval_to_review(page, self.applyCode, u'区域预复核通过')
		if not rs:
			Log().error("风控-区域预复核失败")
			raise
		else:
			Log().info("风控-区域预复核成功！")
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode)
		if not res:
			self.log.error("Can't Get next User")
			raise
		else:
			self.next_user_id = res
			self.log.info("Next deal User:" + self.next_user_id)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_xhd_11_manager_approval(self):
		'''高级审批经理审批'''
		
		# 获取审批经理ID
		self.test_xhd_10_regional_prereview()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批审核
		result = common.approval_to_review(page, self.applyCode, u'高级审批经理审批')
		if not result:
			Log().error("风控-高级审批经理审批失败")
			raise
		else:
			Log().info("风控-高级审批经理审批完成")
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode)
		if not res:
			Log().error("Can't found Next userId!")
			raise
		else:
			self.next_user_id = res
			Log().info("next_user_id: %s", res)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_xhd_12_contract_signing(self):
		'''签约'''
		
		rec_bank_info = dict(
				recBankNum=self.data['houseCommonLoanInfoList'][0]['recBankNum'],
				recPhone=self.data['houseCommonLoanInfoList'][0]['recPhone'],
				recBankProvince=self.data['houseCommonLoanInfoList'][0]['recBankProvince'],
				recBankDistrict=self.data['houseCommonLoanInfoList'][0]['recBankDistrict'],
				recBank=self.data['houseCommonLoanInfoList'][0]['recBank'],
				recBankBranch=self.data['houseCommonLoanInfoList'][0]['recBankBranch'],
				)
		
		# 扣款银行信息
		rep_bank_info = dict(
				rep_name=u'习近平',
				rep_id_num='420101198201013526',
				rep_bank_code='6210302082441017886',
				rep_phone='13686467482',
				provice=u'湖南省',
				district=u'长沙',
				rep_bank_name=u'中国银行',
				rep_bank_branch_name=u'北京支行',
				)
		
		# 获取合同打印专员ID
		self.test_xhd_11_manager_approval()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 签约
		rs = common.make_signing(page, self.applyCode, rec_bank_info)
		if not rs:
			Log().error("签约失败")
			raise
		else:
			Log().info("签约成功")
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode)
		if not res:
			self.log.error("Can't Get Next User")
			raise
		else:
			self.next_user_id = res
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_xhd_13_compliance_audit(self):
		'''合规审查'''
		
		# 获取下一步合同登录ID
		self.test_xhd_12_contract_signing()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 合规审查
		res = common.compliance_audit(page, self.applyCode)
		if not res:
			Log().error("合规审查失败")
			raise
		else:
			Log().info("合规审查成功")
			self.page.driver.quit()
	
	def test_xhd_14_authority_card_member_transact(self):
		'''权证办理'''
		
		# print  u"申请编号:" + self.applyCode
		# 合规审查
		self.test_xhd_13_compliance_audit()
		# 权证员登录
		page = Login(self.company["authority_member"]["user"])
		# 权证员上传权证信息
		res = common.authority_card_transact(page, self.applyCode)
		if not res:
			Log().error("权证员上传资料失败")
			raise
		else:
			Log().info("权证员上传资料成功！")
		# common.authority_card_transact(page, "GZ20171213C06")
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode)
		if not res:
			Log().error("Can't found The next UserId!")
			raise
		else:
			self.next_user_id = res
			Log().info("Next UserId is :%s", res)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_xhd_15_warrant_apply(self):
		'''权证请款-原件请款'''
		
		# 获取合同打印专员ID
		self.test_xhd_14_authority_card_member_transact()
		page = Login(self.next_user_id)
		# 权证请款
		res = common.warrant_apply(page, self.applyCode)
		if not res:
			Log().error("权证请款失败")
			raise
		else:
			Log().info("权证请款成功")
	
	def test_xhd_16_finace_transact(self):
		'''财务办理'''
		
		# 权证请款
		self.test_xhd_15_warrant_apply()
		# 业务助理登录
		page = Login(self.company["business_assistant"]["user"])
		result = common.finace_transact(page, self.applyCode)
		if not result:
			Log().error("财务办理失败")
			raise
		else:
			Log().info("财务办理成功")
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode, 1)
		if not res:
			Log().error("Can't found the next user id")
			raise
		else:
			self.next_user_id = res
			Log().info("Next user Id is: %s", res)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_xhd_17_finace_approve_branch_manager(self):
		'''财务分公司经理审批'''
		
		remark = u"财务分公司经理审批"
		
		# 下一个处理人
		self.test_xhd_16_finace_transact()
		page = Login(self.next_user_id)
		result = common.finace_approve(page, self.applyCode, remark)
		if not result:
			raise
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode, 1)
		if not res:
			Log().error("Can't found the next user Id")
			raise
		else:
			self.next_user_id = res
			Log().info("Next user Id is: %s", res)
			print("nextId:" + res)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_xhd_18_finace_approve_risk_control_manager(self):
		'''财务风控经理审批'''
		
		remark = u'风控经理审批'
		
		self.test_xhd_17_finace_approve_branch_manager()
		page = Login(self.next_user_id)
		result = common.finace_approve(page, self.applyCode, remark)
		if not result:
			Log().error("财务-风控经理审批出错")
			raise
		else:
			Log().info("财务-风控经理审批完成")
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode, 1)
		if not res:
			Log().error("Can't found the next user id")
			raise
		else:
			self.next_user_id = res
			Log().info("nextId: %s", res)
			print("nextId:" + self.next_user_id)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_xhd_19_finace_approve_financial_accounting(self):
		'''财务会计审批'''
		
		remark = u'财务会计审批'
		
		self.test_xhd_18_finace_approve_risk_control_manager()
		page = Login(self.next_user_id)
		result = common.finace_approve(page, self.applyCode, remark)
		if not result:
			Log().error("财务-财务会计审批出错！")
			raise
		else:
			Log().info("财务-财务会计审批完成！")
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode, 1)
		if not res:
			Log().error("can't found The next user Id!")
			raise
		else:
			self.next_user_id = res
			print("nextId:" + self.next_user_id)
			Log().info("nextId :%s", res)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_xhd_20_finace_approve_financial_manager(self):
		'''财务经理审批'''
		
		remark = u'财务经理审批'
		
		self.test_xhd_19_finace_approve_financial_accounting()
		page = Login(self.next_user_id)
		res = common.finace_approve(page, self.applyCode, remark)
		if not res:
			Log().error("财务-财务经理审批出错！")
			raise
		else:
			Log().info("财务-财务经理审批完成！")
			self.page.driver.quit()
	
	def test_xhd_21_funds_raise(self):
		'''资金主管募资审批'''
		
		remark = u'资金主管审批'
		
		self.test_xhd_20_finace_approve_financial_manager()
		page = Login('xn0007533')
		res = common.funds_raise(page, self.applyCode, remark)
		if not res:
			Log().error("募资-资金主管审批出错！")
			raise
		else:
			Log().info("募资-资金主管审批完成！")
			self.page.driver.quit()


if __name__ == '__main__':
	unittest.main()
