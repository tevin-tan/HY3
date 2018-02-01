# coding:utf-8

'''
    E押通录单流程
'''

import unittest
import os
import json
from com import common
from com.login import Login
from com import custom
from com.custom import (getName, logout, enviroment_change, Log, )


class EYT(unittest.TestCase):
	'''E押通-2.0产品测试'''
	
	def _init_params(self):
		self.cust_info = {
			'_cust_base_info': {
				'productName': u'E押通-2.0(二押)',  # 贷款产品
				'applyAmount': 200000,  # 申请金额
				'applyPeriod': 36,  # 贷款期数
				'branchManager': u"小明",
				'branchManagerCode': "xn111",
				'teamGroup': u"A队",
				"teamGroupCode": "xn0001",
				'teamManager': u"小王",
				'teamManagerCode': "xn0001",
				'sale': u"王刚",
				'saleCode': "xn0002",
				'monthIncome': 3000,
				'checkApprove': u"同意",
				},
			'_borrow_info': {
				'custName': getName(),
				'idNum': '360101199101011054',
				'phone': "13564789215",
				'address': u"湖南长沙",
				'companyName': u'小牛普惠管理有限公司',
				'postName': u'工程师',
				'workDate': u'2011-02-03',  # 入职日期
				'workYear': 5,  # 工作年限
				'monthIncoming': 15000  # 月均收入
				},
			'applyCode': '',
			'next_user_id': '',
			}
		self.loan_amount = 200000  # 拆分金额
		
		self.property_info = {
			'propertyOwner': self.cust_info['_borrow_info']['custName'],  # 产权人
			'propertyNo': 'EYT2017230',  # 房产证号
			'propertyStatus': True,  # 是否涉贷物业
			'propertyAge': 10,  # 房龄
			'propertyArea': 220,  # 建筑面积
			'registrationPrice': 333,  # 等级价
			'address': {
				'propertyAddressProvince': u'河北省',
				'propertyAddressCity': u'秦皇岛市',
				'propertyAddressDistinct': u'山海关区',
				'propertyAddressDetail': u'具体地址信息',
				},
			'evaluationSumAmount': 200,  # 评估公允价总值
			'evaluationNetAmount': 200,  # 评估公允价净值
			'slSumAmount': 202,  # 世联评估总值
			"slPrice": 203,  # 中介评估总值
			"agentSumAmout": 221,  # 中介评估净值
			"netSumAmount": 230,  # 网评总值
			"netAmount": 240,  # 网评净值
			"localSumAmount": 230,  # 当地评估总值
			"localNetValue": 290,  # 当地评估净值
			"remark": u"周边环境很好，带学位房，交通便利，风景秀丽.",  # 物业配套描述
			"localAssessmentOrigin": u'房产局',  # 当地评估来源
			"assessmentOrigin": u'世联行',  # 评估来源
			"evaluationCaseDescrip": u'好的没话说',  # 评估情况描述
			}
	
	def setUp(self):
		self._init_params()
		self.page = Login()
		self.applyCode = ""
		self.log = Log()
		
		try:
			import config
			rootdir = config.__path__[0]
			config_env = os.path.join(rootdir, 'env.json')
			print("config_env:" + config_env)
			with open(config_env, 'r', encoding='utf-8') as f:
				self.da = json.load(f)
				self.number = self.da["number"]
				self.env = self.da["enviroment"]
			f.close()
			filename = "data_cwd.json"
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
		  E押通案件数据录入
	'''
	
	def test_eyt_01_base_info(self):
		'''客户基本信息录入'''
		common.input_customer_base_info(self.page, self.cust_info['_cust_base_info'])
	
	def test_ety_02_borrowr_info(self):
		'''借款人/共贷人/担保人信息'''
		common.input_customer_base_info(self.page, self.cust_info['_cust_base_info'])
		common.input_customer_borrow_info(self.page, self.cust_info['_borrow_info'])
	
	def test_eyt_03_Property_info(self):
		'''物业信息录入'''
		common.input_customer_base_info(self.page, self.cust_info['_cust_base_info'])
		common.input_customer_borrow_info(self.page, self.cust_info['_borrow_info'])
		common.input_bbi_Property_info(self.page)
	
	def test_eyt_04_applydata(self):
		'''申请件录入,提交'''
		
		# 1 客户信息-业务基本信息
		# log_to().info(u"客户基本信息录入")
		common.input_customer_base_info(self.page, self.cust_info['_cust_base_info'])
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.custName = common.input_customer_borrow_info(self.page, self.cust_info['_borrow_info'])[1]
		
		# 3 物业信息
		# log_to().info(u"物业基本信息录入")
		common.input_bbi_Property_info(self.page)
		
		# 提交
		common.submit(self.page)
	
	def test_eyt_05_get_applyCode(self):
		'''申请件查询'''
		
		self.test_eyt_04_applydata()
		applycode = common.get_applycode(self.page, self.custName)
		if applycode:
			self.log.info("申请件查询完成")
			self.cust_info['applyCode'] = applycode
			self.applyCode = applycode
		else:
			self.log.error("can't get applyCode!")
			raise ValueError("can't get applyCode!")
	
	def test_eyt_06_show_task(self):
		'''查看待处理任务列表'''
		self.test_eyt_05_get_applyCode()
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
			self.log.info("待处理任务列表中存在该笔案件！")
		else:
			self.log.info("待处理任务列表中不存在该笔案件！")
			raise ValueError("待处理任务列表中不存在该笔案件")
	
	def test_eyt_07_process_monitor(self):
		'''流程监控'''
		self.test_eyt_05_get_applyCode()  # 申请件查询
		res = common.process_monitor(self.page, self.applyCode)  # l流程监控
		
		if not res:
			raise ValueError("流程监控错误！")
		else:
			self.page.user_info['auth']["username"] = res  # 更新下一个登录人
			print(self.page.user_info['auth']["username"])
			self.cust_info['next_user_id'] = res
			self.next_user_id = res
			self.log.info("next deal User: " + self.next_user_id)
	
	def test_eyt_08_branch_supervisor_approval(self):
		'''分公司主管审批'''
		
		# 获取分公司登录ID
		self.test_eyt_07_process_monitor()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批审核
		common.approval_to_review(page, self.applyCode, u'分公司主管同意审批')
		
		# 查看下一步处理人
		next_id = common.process_monitor(page, self.cust_info['applyCode'])
		if not next_id:
			raise AssertionError("没有找到下一个处理人")
		else:
			self.cust_info['next_user_id'] = next_id
			self.next_user_id = next_id
			self.log.info("下一个处理人：" + self.next_user_id)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_quit_system(self):
		'''退出系统'''
		logout(self.page.driver)
		self.page.driver.close()  # 关闭浏览器
	
	def test_eyt_09_branch_manager_approval(self):
		'''分公司经理审批'''
		
		# 获取分公司经理登录ID
		self.test_eyt_08_branch_supervisor_approval()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批审核
		common.approval_to_review(page, self.cust_info['applyCode'], u'分公司经理同意审批')
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.cust_info['applyCode'])
		if not res:
			raise AssertionError("没有找到下一个处理人")
		else:
			self.cust_info['next_user_id'] = res
			self.next_user_id = res
			self.log.info("下一个处理人: " + self.next_user_id)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_eyt_10_regional_prereview(self):
		'''区域预复核审批'''
		
		# 获取区域预复核员ID
		self.test_eyt_09_branch_manager_approval()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批审核
		res = common.approval_to_review(page, self.applyCode, u'区域预复核通过')
		if not res:
			Log().error("区域预复核失败")
			raise AssertionError("区域预复核失败")
		else:
			Log().info("区域预复核审批完成！")
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode)
		if not res:
			Log().error("Can't not found the next UserId")
			raise AssertionError("Can't not found the next UserId")
		else:
			self.next_user_id = res
			Log().info("next_user_id %s", self.next_user_id)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_eyt_11_manager_approval(self):
		'''高级审批经理审批'''
		
		# 获取审批经理ID
		self.test_eyt_10_regional_prereview()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批审核
		common.approval_to_review(page, self.applyCode, u'高级审批经理审批')
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode)
		if not res:
			raise AssertionError('没有找到下一个处理人')
		else:
			self.cust_info['next_user_id'] = res
			self.next_user_id = res
			self.log.info("下一个处理人:" + res)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_12_contract_signing(self):
		'''签约'''
		
		i_frame = 'bTabs_tab_house_commonIndex_todoList'
		# 收款银行信息
		rec_bank_info = dict(
				recBankNum='6210302082441017886',
				recPhone='13686467482',
				recBankProvince=u'湖南省',
				recBankDistrict=u'长沙',
				recBank=u'中国农业银行',
				recBankBranch=u'北京支行',
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
		self.test_eyt_11_manager_approval()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 签约
		common.make_signing(page, self.cust_info['applyCode'], rec_bank_info)
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.cust_info['applyCode'])
		if not res:
			raise AssertionError('没有找到下一个处理人')
		else:
			self.cust_info['next_user_id'] = res
			self.next_user_id = res
			self.log.info("下一个处理人: " + self.next_user_id)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_13_compliance_audit(self):
		'''合规审查'''
		
		# i_frame = 'bTabs_tab_house_commonIndex_todoList'
		# 获取下一步合同登录ID
		self.test_12_contract_signing()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 合规审查
		res = common.compliance_audit(page, self.cust_info['applyCode'])
		if res:
			Log().info("合规审查通过")
		else:
			Log().error("合规审查失败")
			raise AssertionError('合规审查失败')
		page.driver.quit()
	
	def test_eyt_14_authority_card_member_transact(self):
		'''权证办理'''
		
		# 合规审查
		self.test_13_compliance_audit()
		# 权证员登录
		page = Login(self.company["authority_member"]["user"])
		# 权证员上传权证信息
		rs = common.authority_card_transact(page, self.applyCode, self.env)
		if not rs:
			Log().error("上传权证信息失败")
			raise AssertionError('上传权证信息失败')
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode)
		if not res:
			Log().error("权证办理-没找到下一步处理人")
			raise AssertionError('权证办理-没找到下一步处理人')
		else:
			self.next_user_id = res
			Log().info("下一步处理人：%s", self.next_user_id)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_eyt_15_warrant_apply(self):
		'''权证请款-原件请款'''
		
		# 获取合同打印专员ID
		self.test_eyt_14_authority_card_member_transact()
		page = Login(self.next_user_id)
		# 权证请款
		res = common.warrant_apply(page, self.applyCode)
		if res:
			Log().info("权证请款成功")
		else:
			Log().error("权证请款失败")
			raise AssertionError('权证请款失败')
	
	def test_eyt_16_finace_transact(self):
		'''财务办理'''
		
		# 权证请款
		self.test_eyt_15_warrant_apply()
		# 业务助理登录
		page = Login(self.company["business_assistant"]["user"])
		rs = common.finace_transact(page, self.applyCode)
		if not rs:
			Log().error("财务办理失败")
			raise AssertionError('财务办理失败')
		
		# page = Login('xn052298')
		# common.finace_transact(page, 'CS20171215C02')
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode, 1)
		if not res:
			Log().error("没有找到下一步处理人")
			raise AssertionError('没有找到下一步处理人')
		else:
			self.next_user_id = res
			Log().info("下一步处理人：%s", self.next_user_id)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_eyt_17_finace_approve_branch_manager(self):
		'''财务分公司经理审批'''
		
		remark = u"财务分公司经理审批"
		
		# 下一个处理人
		self.test_eyt_16_finace_transact()
		page = Login(self.next_user_id)
		result = common.finace_approve(page, self.applyCode, remark)
		if not result:
			Log().error("财务流程-分公司经理审批失败")
			raise AssertionError('财务流程-分公司经理审批失败')
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode, 1)
		if not res:
			Log().error("没有找到下一步处理人")
			raise AssertionError('没有找到下一步处理人')
		else:
			self.next_user_id = res
			Log().info("下一步处理人: %s", self.next_user_id)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_eyt_18_finace_approve_risk_control_manager(self):
		'''财务风控经理审批'''
		
		remark = u'风控经理审批'
		
		self.test_eyt_17_finace_approve_branch_manager()
		page = Login(self.next_user_id)
		result = common.finace_approve(page, self.applyCode, remark)
		if not result:
			Log().error("财务流程-风控经理审批出错")
			raise AssertionError('财务流程-风控经理审批出错')
		else:
			Log().info("财务流程-风控经理审批完成")
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode, 1)
		if not res:
			Log().error("Can't found the next userId!")
			raise AssertionError("Can't found the next userId!")
		else:
			self.next_user_id = res
			Log().info("下一步处理人:%s", self.next_user_id)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_eyt_19_finace_approve_financial_accounting(self):
		'''财务会计审批'''
		
		remark = u'财务会计审批'
		
		self.test_eyt_18_finace_approve_risk_control_manager()
		page = Login(self.next_user_id)
		rs = common.finace_approve(page, self.applyCode, remark)
		if not rs:
			Log().error("财务流程-财务会计审批失败")
			raise AssertionError('财务流程-财务会计审批失败')
		else:
			Log().info("财务流程-财务会计审批完成")
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode, 1)
		if not res:
			Log().error("Can't found The next UserId")
			raise AssertionError("Can't found The next UserId")
		else:
			self.next_user_id = res
			Log().info("nextId is %s", self.next_user_id)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_eyt_20_finace_approve_financial_manager(self):
		'''财务经理审批'''
		
		remark = u'财务经理审批'
		
		self.test_eyt_19_finace_approve_financial_accounting()
		page = Login(self.next_user_id)
		res = common.finace_approve(page, self.applyCode, remark)
		if not res:
			Log().error("财务流程-财务经理审批失败")
			raise AssertionError('财务流程-财务经理审批失败')
		else:
			Log().info("财务流程-财务经理审批完成")
			self.page.driver.quit()
	
	def test_eyt_21_funds_raise(self):
		'''资金主管募资审批'''
		
		remark = u'资金主管审批'
		
		self.test_eyt_20_finace_approve_financial_manager()
		page = Login('xn0007533')
		res = common.funds_raise(page, self.applyCode, remark)
		if not res:
			Log().error("募资-资金主管审批失败")
			raise AssertionError('募资-资金主管审批失败')
		else:
			Log().info("募资-资金主管审批完成!")
			self.page.driver.quit()


if __name__ == '__main__':
	unittest.main()
