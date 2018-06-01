# coding:utf-8
import datetime
import time

from com import custom, xlsx

v_l = []


class SET(object):
	def __init__(self):
		# self.city = ['东莞分公司', '南通分公司', '南京分公司', '无锡分公司', '苏州分公司', '常州分公司']
		self.run_result = True
		self.case_name = None
		self.begin_time = time.clock()
		self.s_time = str(datetime.datetime.now()).split('.')[0]
		self.xlsx = None
	
	def start_run(self):
		self.xlsx = xlsx.XLS()
	
	def end_run(self, v_l):
		# temp = custom.delete_duplicated_element_from_mix_list(v_l)
		temp = custom.delete_duplicated_element_from_list(v_l)
		self.xlsx.test_03(temp)
		self.xlsx.end()
