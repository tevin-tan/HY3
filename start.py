# coding:utf-8
import os
import time
import unittest
import yaml
import config
# from lib.HTMLTestRunner import HTMLTestRunner
from lib.HTMLTestRunnerCN import HTMLTestRunner
from cases.baseProcess import (
	test_suite_cwd,
	test_eyt_input_data,
	test_xhd_input_data,
	test_gqt_input_data,
	test_part_raise
	)
from cases.IntoCases import (
	test_into_case,
	test_fallback,
	test_special_approval
	)

from cases.contract_sigining import (
	test_more_person_sign,
	test_add_contract
	)

from cases.warrantManage import test_warrantManage
from cases.upload_image_data import test_upload_image_file

if __name__ == "__main__":
	
	def set_reporter_path():
		# 定义报告存放路径以及格式
		# local_dir = os.path.dirname(os.getcwd())
		local_dir = os.getcwd()
		print("local_dir: %s " % local_dir)
		# path = local_dir + "\\report\\" + now + "-result.html"
		path = local_dir + "\\report\\" + "index.html"
		return local_dir, path
	
	
	# 执行用例
	def run_case(element, case):
		if element is not None:
			for i in temp[element]:
				suite.addTest(case(i))
	
	
	# 按照一定格式获取当前时间
	now = time.strftime("%Y-%m-%d %H_%M_%S")
	PT = set_reporter_path()
	print("path:", PT)
	fp = open(PT[1], 'wb')
	
	# 创建测试套
	suite = unittest.TestSuite()
	
	suite_list = [
		'cwd',  # 车位贷
		'eyt',  # E押通
		'xhd',  # 循环贷
		'gqt',  # 过桥通
		'IntoCase',  # 申请录入进件场景
		'fallback',  # 回退场景
		'contract',  # 合同签约
		'AddContract',  # 添加拆借人签约
		"SPA",  # 特批
		"PartRaise",  # 部分募资
		"WarrantManage",  # 权证请款
		"UploadImageData",  # 上传影像资料
		]
	
	try:
		rdir = config.__path__[0]
		f1 = os.path.join(rdir, 'caseNumber.yaml')
		with open(f1, 'r', encoding='utf-8') as f:
			temp = yaml.load(f)
			for e in suite_list:
				if e == 'cwd':
					run_case(e, test_suite_cwd.CWD)
				elif e == 'eyt':
					run_case(e, test_eyt_input_data.EYT)
				elif e == 'xhd':
					run_case(e, test_xhd_input_data.XHD)
				elif e == 'gqt':
					run_case(e, test_gqt_input_data.GQT)
				elif e == 'IntoCase':
					run_case(e, test_into_case.IntoCase)
				elif e == 'fallback':
					run_case(e, test_fallback.FallBack)
				elif e == 'contract':
					run_case(e, test_more_person_sign.ContractSign)
				elif e == 'SPA':
					run_case(e, test_special_approval.SPA)
				elif e == 'AddContract':
					run_case(e, test_add_contract.AddContract)
				elif e == 'WarrantManage':
					run_case(e, test_warrantManage.WarrantManage)
				elif e == 'UploadImageData':
					run_case(e, test_upload_image_file.UploadImageData)
		print("f1:", f1)
		f.close()
	except Exception as e:
		print("Error: can't load file")
		raise e
	
	# 定义测试报告
	runner = HTMLTestRunner(stream=fp, title='测试报告', description='用例执行情况:')
	runner.run(suite)
	
	fp.close()  # 关闭测试报告
