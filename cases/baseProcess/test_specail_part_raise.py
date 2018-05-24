# coding:utf-8
import datetime
import time
import unittest

from cases import SET, v_l
from com import common, custom, database
from com.base import Base
from com.login import Login
from com.pobj.ContractSign import ContractSign as Cts


class SpecaiPartRaise(unittest.TestCase, Base, SET):
	"""特别的募资场景"""
	
	def setUp(self):
		self.env_file = "env.json"
		self.data_file = "data_eyt.json"
		Base.__init__(self, self.env_file, self.data_file)
		SET.__init__(self)
		self.se = SET()
		self.se.start_run()
	
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
	
	def test_01_specail_part_raise(self):
		"""第一次全额请款，第二次为0"""
		self.case_name = custom.get_current_function_name()
		# ------------合同打印-------------
		try:
			self.before_contract_sign(200000)
			rc = Cts.ContractSign(self.page, self.apply_code, self.rec_bank_info)
			res = rc.execute_enter_borroers_bank_info()
			if res:
				rc.contract_submit()  # 提交
		except Exception as e:
			self.run_result = False
			raise e
		self.next_user_id = common.get_next_user(self.page, self.apply_code)
		
		# ------------合规审查------------------
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 合规审查
		res = self.PT.compliance_audit(page, self.apply_code)
		if res:
			self.log.info("合规审批结束")
			page.driver.quit()
		else:
			raise ValueError("合规审查失败")
		
		# ------------权证办理----------------
		page = Login(self.company["authority_member"]["user"])
		# 权证员上传权证信息
		res = self.WM.authority_card_transact_2(page, self.apply_code, 1, self.env)
		if not res:
			raise ValueError("上传权证资料失败")
		else:
			self.log.info("权证办理完成")
			self.next_user_id = common.get_next_user(page, self.apply_code)
		
		# ------------权证请款----------------
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		# 部分请款
		res = self.PT.part_warrant_apply(page, self.apply_code, 0)
		if not res:
			raise AssertionError('权证请款失败！')
		else:
			self.log.info("完成权证请款")
			self.next_user_id = common.get_next_user(page, self.apply_code)
		
		# 权证审批流程
		roles = ['回执分公司主管', '回执审批经理审批', '回执业务助理处理']
		
		for i in roles:
			page = Login(self.next_user_id)
			rec = self.PT.receipt_return(page, self.apply_code)
			if not rec:
				self.log.error(i + "审批失败")
				raise ValueError('失败')
			else:
				self.log.info(i + "审批通过")
				self.next_user_id = common.get_next_user(page, self.apply_code)
		
		# ------------财务流程----------------------
		page = Login(self.company["business_assistant"]["user"])
		rs = self.FA.finace_transact(page, self.apply_code)
		if not rs:
			self.log.error("财务办理失败")
			raise AssertionError('财务办理失败')
		else:
			self.log.info("财务办理结束！")
		# 查看下一步处理人
		self.next_user_id = common.get_next_user(page, self.apply_code, 1)
		
		role2 = ['分公司经理审', '风控经理', '财务会计', '财务经理']
		
		for e in role2:
			self.case_name = custom.get_current_function_name()
			page = Login(self.next_user_id)
			result = self.FA.finace_approval(page, self.apply_code, e + '审批通过')
			if not result:
				raise AssertionError(e + '审批失败')
			# 查看下一步处理人
			self.next_user_id = common.get_next_user(page, self.apply_code, 1)
		
		# ----------发起募资-----------------------------
		page = Login(self.treasurer)
		res = self.RA.funds_raise(page, self.apply_code, '第一次资金主管募资发起')
		if not res:
			self.log.error("募资-资金主管审批失败")
			raise AssertionError('募资-资金主管审批失败')
		else:
			self.log.info("募资-资金主管审批完成!")
			page.driver.quit()
		
		# 修改数据表为放款成功！
		db = database.DB()
		
		sql_1 = "UPDATE house_common_loan_info t SET t.pay_date=sysdate, t.status='LOAN_PASS' \
				WHERE t.apply_id= (SELECT t.apply_id FROM house_apply_info t \
				WHERE t.apply_code =" + "'" + self.apply_code + "'" + ")"
		
		contract_no = self.apply_code + '-3-02-1'
		
		sql_2 = "UPDATE house_funds_info t SET t.Funds_Status = 21  \
				WHERE t.apply_id = (SELECT t.apply_id FROM house_apply_info t \
				WHERE t.apply_code = " + "'" + self.apply_code + "'" + ")" + "AND CONTRACT_NO =" + "'" + contract_no + "'"
		
		db.sql_execute(sql_1)
		db.sql_execute(sql_2)
		db.sql_commit()
		time.sleep(3)
		
		# ----------第二次权证办理-----------------------------
		
		page = Login(self.company["authority_member"]["user"])
		# 权证员上传权证信息
		res = self.WM.authority_card_transact_2(page, self.apply_code, 2, self.env)
		if not res:
			self.log.error("上传权证资料失败")
			raise ValueError("上传权证资料失败")
		else:
			self.log.info("权证办理完成")
			self.next_user_id = common.get_next_user(page, self.apply_code)
		
		# ---------第二次权证请款--------------------------------
		# 下一个处理人重新登录
		page = Login(self.next_user_id)
		
		# 第二次请款金额为0
		res = self.PT.part_warrant_apply(page, self.apply_code, 2)
		if not res:
			raise ValueError('第二次权证请款金额为0请款流程出错！')
		else:
			self.log.info("第二次权证请款金额为0请款流程ok！")
		self.next_user_id = common.get_next_user(page, self.apply_code)
		page.driver.quit()
		
		# --------------------------回执审批流程---------------------
		page = Login(self.next_user_id)
		rec = self.PT.receipt_return(page, self.apply_code)
		if not rec:
			self.log.error("审批失败")
			raise ValueError('失败')
		else:
			
			self.log.info("审批通过,放款成功")
			page.driver.quit()
