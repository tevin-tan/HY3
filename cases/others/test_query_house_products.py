# coding:utf-8
import datetime
import os
import time
import unittest

import xlsxwriter

from cases import SET, v_l
from com import database
from com.base import Base


class QueryProdcut(unittest.TestCase, Base, SET):
	"""查询房贷产品"""
	
	def setUp(self):
		self.env_file = None
		self.data_file = None
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
	
	def test_query_all_enable_product(self):
		"""查询房贷所有的已启动的产品"""
		
		self.log.info("查询房贷所有的已启动的产品")
		db = database.DB()
		sql = """
		SELECT NAME
		FROM BASE_PRODUCT
			WHERE PRODUCT_TYPE_ID = '4003156770' AND STATUS = 'enable'
		"""
		
		db.sql_execute(sql)
		res = db.sql_print()
		
		import report
		r_dir = report.__path__[0]
		l_p = os.path.join(r_dir, 'product.xlsx')
		workbook = xlsxwriter.Workbook(l_p)
		worksheet = workbook.add_worksheet()
		
		lth = res.__len__()
		fm = workbook.add_format({
			'align': 'center',
			})
		worksheet.write(0, 0, "序号")
		worksheet.write(0, 1, "名称")
		for i in range(1, lth):
			worksheet.write(i, 0, i, fm)
			worksheet.write(i, 1, res[i])
	
	def test_query_all_disable_product(self):
		"""查询房贷所有的已停用的产品"""
		
		self.log.info("查询房贷所有的已启动的产品")
		db = database.DB()
		sql = """
		SELECT NAME
		FROM BASE_PRODUCT
			WHERE PRODUCT_TYPE_ID = '4003156770' AND STATUS = 'disable'
		"""
		
		db.sql_execute(sql)
		db.sql_print()
