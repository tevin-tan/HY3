# coding:utf-8
import time
import unittest
import os
# from HTMLTestRunner import HTMLTestRunner
from lib.HTMLTestRunnerCN import HTMLTestRunner

from cases.baseProcess import (
	test_gqt_input_data,
	test_eyt_input_data,
	test_xhd_input_data,
	test_suite_cwd
	)
from cases.IntoCases import test_into_case, test_fallback
from cases.contract_sigining import test_more_person_sign

if __name__ == "__main__":
	def set_reporter_path():
		# 定义报告存放路径以及格式
		# local_dir = os.path.dirname(os.getcwd())
		local_dir = os.getcwd()
		# local_dir = "E:\HouseLoanAutoPy3"
		print("local_dir: %s " % local_dir)
		# path = local_dir + "\\report\\" + now + "-result.html"
		path = local_dir + "\\report\\" + "index.html"
		print("path:", path)
		return local_dir, path
	
	
	# 按照一定格式获取当前时间
	now = time.strftime("%Y-%m-%d %H_%M_%S")
	PT = set_reporter_path()
	print("path:", PT)
	fp = open(PT[1], 'wb')
	#
	suite = unittest.TestSuite()
	# 构造测试套件
	# suite.addTest(test_eyt_input_data.EYT('test_eyt_01_base_info'))
	# suite.addTest(test_eyt_input_data.EYT('test_eyt_21_funds_raise'))
	# suite.addTest(test_eyt_input_data.EYT('test_eyt_01_base_info'))
	# suite.addTest(test_xhd_input_data.XHD('test_xhd_21_funds_raise'))
	
	suite.addTest(test_suite_cwd.CWD('test_cwd_01_base_info'))
	
	# suite.addTest(test_into_case.IntoCase('test_03_two_borrower'))
	# suite.addTest(test_fallback.fallback('test_02_branch_manager_reject'))
	
	# suite.addTest(test_more_person_sign.contractSign('test_03_three_person_sign'))
	
	runner = unittest.TextTestRunner()
	
	# 定义测试报告
	runner = HTMLTestRunner(
			stream=fp,
			title='测试报告',
			description='用例执行情况:')
	runner.run(suite)
	fp.close()  # 关闭测试报告
