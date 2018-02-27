# coding:utf-8
'''
	部分募资
'''

import unittest
import json
import os
from com import common
from com.login import Login
from com.custom import Log, enviroment_change


class PartRaise(unittest.TestCase):
	def setUp(self):
		try:
			import config
			rootdir = config.__path__[0]
			config_env = os.path.join(rootdir, 'env.json')
			print("config_env:" + config_env)
			with open(config_env, 'r', encoding='utf-8') as f:
				self.da = json.load(f)
				self.number = self.da["number"]
				self.env = self.da["enviroment"]
			
			filename = "data_cwd.json"
			data, company = enviroment_change(filename, self.number, self.env)
			self.page = Login()
			self.log = Log()
			
			# 录入的源数据
			self.data = data
			# 分公司选择
			self.company = company
		except Exception as e:
			self.log.error('load config error:', str(e))
			raise e
	
	def get_next_user(self, page, applycode):
		next_id = common.process_monitor(page, applycode)
		if next_id is None:
			raise ValueError("没有找到下一步处理人")
		else:
			self.next_user_id = next_id
			self.log.info("下一步处理人:" + next_id)
			# 当前用户退出系统
			self.page.driver.quit()
	
	def tearDown(self):
		self.page.driver.quit()
	
	def test_contract_signing(self):
		'''两人签约, 两个分别200000万'''
		
		# ---------------------------------------------------------------------------------
		#                   1. 申请录入
		# ---------------------------------------------------------------------------------
		
		self.data['applyVo']['applyAmount'] = 400000
		# 1 客户信息-业务基本信息
		if common.input_customer_base_info(self.page, self.data['applyVo']):
			self.log.info("录入基本信息完成")
		
		# 2 客户基本信息 - 借款人/共贷人/担保人信息
		self.custName = common.input_customer_borrow_info(self.page, self.data['custInfoVo'][0])[1]
		
		# 3 物业信息
		common.input_cwd_bbi_property_info(self.page, self.data['applyPropertyInfoVo'][0],
		                                   self.data['applyCustCreditInfoVo'][0])
		# 提交
		common.submit(self.page)
		self.log.info("申请件录入完成提交")
		
		applycode = common.get_applycode(self.page, self.custName)
		if applycode:
			self.applycode = applycode
			self.log.info("申请件查询完成")
			print("applycode:" + self.applycode)
		# 流程监控
		result = common.process_monitor(self.page, applycode)
		if result is not None:
			self.next_user_id = result
			self.log.info("完成流程监控查询")
		else:
			raise ValueError("流程监控查询出错！")
		
		# ---------------------------------------------------------------------------------------
		# 	                        2. 风控审批流程
		# ---------------------------------------------------------------------------------------
		
		# 下一个处理人重新登录
		page = Login(result)
		
		# 分公司主管审批
		res = common.approval_to_review(page, applycode, u'分公司主管审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise ValueError("审批失败")
		else:
			self.log.info("分公司主管审批通过！")
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 分公司经理审批
		res = common.approval_to_review(page, applycode, u'分公司经理审批通过', 0)
		if not res:
			self.log.error("审批失败")
			raise ValueError("审批失败")
		else:
			self.log.info("分公司经理审批通过！")
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 区域预复核审批
		res = common.approval_to_review(page, applycode, u'区域预复核审批通过', 0)
		if not res:
			self.log.error("区域预复核审批失败！")
			raise ValueError("区域预复核审批失败!")
		else:
			self.log.info("区域经理审批通过")
			self.get_next_user(page, applycode)
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 审批经理审批通过
		res = common.approval_to_review(page, applycode, u'审批经理审批通过', 0)
		if not res:
			self.log.error("审批经理审批失败！")
			raise ValueError("审批经理审批失败！")
		else:
			self.log.info("审批经理审批通过成功！")
			self.get_next_user(page, applycode)
		
		# -----------------------------------------------------------------------------
		# 	                        3. 合同打印
		# -----------------------------------------------------------------------------
		
		rec_bank_info = dict(
				recBankNum=self.data['houseCommonLoanInfoList'][0]['recBankNum'],
				recPhone=self.data['houseCommonLoanInfoList'][0]['recPhone'],
				recBankProvince=self.data['houseCommonLoanInfoList'][0]['recBankProvince'],
				recBankDistrict=self.data['houseCommonLoanInfoList'][0]['recBankDistrict'],
				recBank=self.data['houseCommonLoanInfoList'][0]['recBank'],
				recBankBranch=self.data['houseCommonLoanInfoList'][0]['recBankBranch'],
				)
		
		
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 两个人签约
		res = common.make_signing(page, self.applycode, rec_bank_info, 2)
		if res:
			self.log.info("合同打印完成！")
			# 查看下一步处理人
			self.get_next_user(page, applycode)
		
		# -----------------------------------------------------------------------------
		#                                合规审查
		# -----------------------------------------------------------------------------
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 合规审查
		res = common.compliance_audit(page, self.applycode)
		if res:
			self.log.info("合规审批结束")
			self.get_next_user(page, self.applycode)
		else:
			self.log.error("合规审查失败")
			raise ValueError("合规审查失败")
		
		# -----------------------------------------------------------------------------
		#                                权证办理
		# -----------------------------------------------------------------------------
		page = Login(self.company["authority_member"]["user"])
		# 权证员上传权证信息
		common.authority_card_transact(page, self.applycode, self.env)
		# 查看下一步处理人
		res = common.process_monitor(page, self.applycode)
		if not res:
			self.log.error("上传权证资料失败")
			raise ValueError("上传权证资料失败")
		else:
			self.log.info("权证办理完成")
			self.next_user_id = res
			self.get_next_user(page, self.applycode)
		# -----------------------------------------------------------------------------
		#                                权证请款
		# -----------------------------------------------------------------------------
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		res = common.warrant_apply(page, self.applycode)
		if not res:
			self.log.error("权证请款失败！")
			raise ValueError('权证请款失败！')
		else:
			self.log.info("完成权证请款")
			self.get_next_user(page, self.applycode)
