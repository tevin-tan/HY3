# coding:utf-8
import unittest
import json
import os
from com import common
from com.login import Login
from com import custom


class CWD(unittest.TestCase):
	'''车位贷流程用例'''
	
	def setUp(self):
		self.page = Login()
		self.applyCode = ''
		self.next_user_id = ""
		local_dir = os.getcwd()
		print("local_dir: %s " % local_dir)
		self.log = custom.Log()
		# 环境初始化
		# self._enviroment_change(0)
		try:
			import config
			rootdir = config.__path__[0]
			config_env = os.path.join(rootdir, 'env.json')
			print("config_env:" + config_env)
			with open(config_env, 'r', encoding='utf-8') as f:
				self.fd = f
				self.da = json.load(f)
				self.number = self.da["number"]
				self.env = self.da["enviroment"]
			
			f.close()
			filename = "data_cwd.json"
			data, company = custom.enviroment_change(filename, self.number, self.env)
			# 录入的源数据
			self.data = data
			# 分公司选择
			self.company = company
		except Exception as e:
			print('load config error:', str(e))
			raise ValueError("load config error")
	
	def _enviroment_change(self, i):
		'''
			环境切换
		:param i:   分公司序号  "0" 广州， "1" 长沙
		:return:
		'''
		# 导入数据
		import config
		rd = config.__path__[0]
		config_env = os.path.join(rd, 'env.json')
		data_config = os.path.join(rd, "data_cwd.json")
		with open(data_config, 'r') as f:
			self.data = json.load(f)
			print(self.data['applyVo']['productName'])
		
		# 环境变量, 切换分公司
		with open(config_env, 'r') as f1:
			self.env = json.load(f1)
			self.company = self.env["SIT"]["company"][i]
	
	def tearDown(self):
		self.fd.close()
		self.page.driver.quit()
	
	def skipTest(self, reason):
		pass
	
	def test_cwd_01_base_info(self):
		'''客户基本信息录入'''
		
		common.input_customer_base_info(self.page, self.data['applyVo'])
		self.log.info("客户基本信息录入结束")
	
	def test_cwd_02_borrowr_info(self):
		'''借款人/共贷人/担保人信息'''
		
		self.test_cwd_01_base_info()
		try:
			res = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])[1]
			if res:
				self.log.info("录入借款人信息结束")
		except Exception as e:
			self.log.error("Error:", e)
			raise
	
	def test_cwd_03_Property_info(self):
		'''物业信息录入'''
		
		self.test_cwd_02_borrowr_info()
		
		data1 = self.data['applyPropertyInfoVo'][0]
		data2 = self.data['applyCustCreditInfoVo'][0]
		
		res = common.input_cwd_bbi_Property_info(self.page, data1, data2, True)
		if res:
			self.log.info("录入物业信息结束")
		else:
			raise
	
	def test_cwd_04_applydata(self):
		'''申请件录入,提交'''
		
		# 1 客户信息-业务基本信息
		# log_to().info(u"客户基本信息录入")
		common.input_customer_base_info(self.page, self.data['applyVo'])
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		# log_to().info(u"借款人/共贷人信息录入")
		self.custName = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])[1]
		
		# 3 物业信息
		# log_to().info(u"物业基本信息录入")
		common.input_cwd_bbi_Property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0], True)
		
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
	
	def test_cwd_05_get_applyCode(self):
		'''申请件查询'''
		
		self.test_cwd_04_applydata()
		applycode = common.get_applycode(self.page, self.custName)
		
		if applycode:
			self.log.info("申请件查询完成")
			self.applyCode = applycode
		else:
			raise ValueError("申请件查询失败")
	
	def test_cwd_06_show_task(self):
		'''查看待处理任务列表'''
		
		self.test_cwd_05_get_applyCode()
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
		else:
			self.log.error("查询待处理任务失败！")
			raise ValueError("查询待处理任务失败")
	
	def test_cwd_07_process_monitor(self):
		'''流程监控'''
		
		self.test_cwd_05_get_applyCode()  # 申请件查询
		res = common.process_monitor(self.page, self.applyCode)  # l流程监控
		
		if not res:
			raise ValueError("流程监控查询出错！")
		else:
			self.page.user_info['auth']["username"] = res  # 更新下一个登录人
			print(self.page.user_info['auth']["username"])
			self.next_user_id = res
			self.log.info("完成流程监控查询")
		self.page.driver.quit()
	
	def test_cwd_08_branch_supervisor_approval(self):
		'''分公司主管审批'''
		
		# 获取分公司登录ID
		self.test_cwd_07_process_monitor()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批审核
		res = common.approval_to_review(page, self.applyCode, u'分公司主管同意审批')
		if not res:
			self.log.error("can't find applycode")
			raise ValueError("can't find applycode")
		else:
			self.log.info("风控审批-分公司主管审批结束")
		
		# 查看下一步处理人
		next_id = common.process_monitor(page, self.applyCode)
		if not res:
			raise ValueError("查询下一步处理人出错！")
		else:
			self.next_user_id = next_id
			self.log.info("下一个处理人：" + self.next_user_id)
			# 当前用户退出系统
			page.driver.quit()
	
	def test_cwd_09_branch_manager_approval(self):
		'''分公司经理审批'''
		
		# 获取分公司经理登录ID
		self.test_cwd_08_branch_supervisor_approval()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批审核
		res = common.approval_to_review(page, self.applyCode, u'分公司经理同意审批')
		if not res:
			raise ValueError("can't find applycode")
		else:
			self.log.info("风控审批-分公司经理审批结束")
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode)
		if not res:
			raise ValueError("查询下一步处理人出错！")
		else:
			self.next_user_id = res
			self.log.info("下一个处理人：" + self.next_user_id)
			# 当前用户退出系统
			page.driver.quit()
	
	def test_cwd_10_regional_prereview(self):
		'''区域预复核审批'''
		
		# 获取区域预复核员ID
		self.test_cwd_09_branch_manager_approval()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批审核
		res = common.approval_to_review(page, self.applyCode, u'区域预复核通过')
		if not res:
			custom.Log().error("can't find applycode")
			raise ValueError("can't find applycode")
		else:
			self.log.info("区域预复核审批结束")
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode)
		if not res:
			self.log.error("Can't found next user!")
			raise ValueError("没有找到下一个处理人")
		else:
			self.next_user_id = res
			self.log.info("下一步处理人：" + self.next_user_id)
			# 当前用户退出系统
			page.driver.quit()
	
	def test_cwd_11_manager_approval(self):
		'''高级审批经理审批'''
		
		# 获取审批经理ID
		self.test_cwd_10_regional_prereview()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批审核
		res = common.approval_to_review(page, self.applyCode, u'审批经理审批')
		if not res:
			custom.Log().ERROR("can't find applycode")
			raise ValueError("can't find applycode")
		else:
			self.log.info("风控审批-审批经理审批结束")
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode)
		if not res:
			self.log.error("Can't found next user!")
		else:
			self.next_user_id = res
			self.log.info("下一个处理人：" + self.next_user_id)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_cwd_12_contract_signing(self):
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
		self.test_cwd_11_manager_approval()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 签约
		common.make_signing(page, self.applyCode, rec_bank_info)
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode)
		if not res:
			self.log.error("Can't found next User!")
		else:
			self.next_user_id = res
			self.log.info("合同打印完成")
			self.log.info("Next deal User:" + self.next_user_id)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_cwd_13_compliance_audit(self):
		'''合规审查'''
		
		# 获取下一步合同登录ID
		self.test_cwd_12_contract_signing()
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 合规审查
		res = common.compliance_audit(page, self.applyCode)
		if res:
			self.log.info("合规审批结束")
		else:
			raise ValueError("合规审查失败")
		self.page.driver.quit()
	
	def test_cwd_14_authority_card_member_transact(self):
		'''权证办理'''
		
		# 合规审查
		self.test_cwd_13_compliance_audit()
		# 权证员登录
		page = Login(self.company["authority_member"]["user"])
		# 权证员上传权证信息
		common.authority_card_transact(page, self.applyCode)
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode)
		if not res:
			self.log.error("上传权证资料失败")
			raise ValueError("上传权证资料失败")
		else:
			self.log.info("权证办理完成")
			self.next_user_id = res
			self.log.info("Next deal user:" + self.next_user_id)
			# 当前用户退出系统
			page.driver.quit()
	
	def test_cwd_15_warrant_apply(self):
		'''权证请款-原件请款'''
		
		# 获取合同打印专员ID
		self.test_cwd_14_authority_card_member_transact()
		page = Login(self.next_user_id)
		# 权证请款
		res = common.warrant_apply(page, self.applyCode)
		if not res:
			raise ValueError("权证请款失败！")
		else:
			self.log.info("完成权证请款")
			page.driver.quit()
	
	def test_cwd_16_finace_transact(self):
		'''财务办理'''
		
		# 权证请款
		self.test_cwd_15_warrant_apply()
		# 业务助理登录
		page = Login(self.company["business_assistant"]["user"])
		common.finace_transact(page, self.applyCode)
		self.log.info("完成财务办理")
		# page = Login('xn052298')
		# common.finace_transact(page, 'CS20171215C02')
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode, 1)
		if not res:
			raise ValueError("Can't found Next User!")
		else:
			self.next_user_id = res
			self.log.info("Next deal User:" + self.next_user_id)
			# 当前用户退出系统
			page.driver.quit()
		self.page.driver.quit()
	
	def test_cwd_17_finace_approve_branch_manager(self):
		'''财务分公司经理审批'''
		
		remark = u"财务分公司经理审批"
		
		# 下一个处理人
		self.test_cwd_16_finace_transact()
		page = Login(self.next_user_id)
		result = common.finace_approve(page, self.applyCode, remark)
		
		if not result:
			raise result
		else:
			self.log.info("财务流程-分公司经理审批结束")
			# 查看下一步处理人
			res = common.process_monitor(page, self.applyCode, 1)
			if not res:
				raise ValueError("Can't found Next User!")
			else:
				self.next_user_id = res
				self.log.info("Next deal User:" + self.next_user_id)
				# 当前用户退出系统
				page.driver.quit()
				self.page.driver.quit()
	
	def test_cwd_18_finace_approve_risk_control_manager(self):
		'''财务风控经理审批'''
		
		remark = u'风控经理审批'
		
		self.test_cwd_17_finace_approve_branch_manager()
		page = Login(self.next_user_id)
		rs = common.finace_approve(page, self.applyCode, remark)
		if rs:
			self.log.info("财务流程-风控经理审批结束")
		else:
			raise ValueError("风控经理审批出错！")
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode, 1)
		if not res:
			raise ValueError("can't found Next User！")
		else:
			self.next_user_id = res
			self.log.info("nextId:" + self.next_user_id)
			# 当前用户退出系统
			page.driver.quit()
		self.page.driver.quit()
	
	def test_cwd_19_finace_approve_financial_accounting(self):
		'''财务会计审批'''
		
		remark = u'财务会计审批'
		
		self.test_cwd_18_finace_approve_risk_control_manager()
		page = Login(self.next_user_id)
		common.finace_approve(page, self.applyCode, remark)
		
		# 查看下一步处理人
		res = common.process_monitor(page, self.applyCode, 1)
		if not res:
			raise ValueError("Can't found next User!")
		else:
			self.log.info("财务流程-财务会计审批结束")
			self.next_user_id = res
			self.log.info("nextId:" + self.next_user_id)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def test_cwd_20_finace_approve_financial_manager(self):
		'''财务经理审批'''
		
		remark = u'财务经理审批'
		
		self.test_cwd_19_finace_approve_financial_accounting()
		page = Login(self.next_user_id)
		res = common.finace_approve(page, self.applyCode, remark)
		if res:
			self.log.info("财务流程-财务经理审批结束")
		else:
			raise ValueError("财务经理审批出错")
	
	def test_cwd_21_funds_raise(self):
		'''资金主管募资审批'''
		
		remark = u'资金主管审批'
		
		self.test_cwd_20_finace_approve_financial_manager()
		page = Login('xn0007533')
		res = common.funds_raise(page, self.applyCode, remark)
		if res:
			self.log.info("募资流程-资金主管审批结束")
			self.page.driver.quit()
		else:
			raise ValueError("募资流程出错")
