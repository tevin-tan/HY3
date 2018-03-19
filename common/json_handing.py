# coding:utf-8

import json
import re


class h_json():
	def parse_json(self, filename):
		""" Parse a JSON file
			First remove comments and then use the json module package
			Comments look like :
				// ...
			or
				/*
				...
				*/
		"""
		res = []
		f = open(filename)
		all_lines = f.readlines()
		# 去除形如 // 但不包括 http:// ip_addr 的注释
		for line in all_lines:
			l = self.strip_comment(line)
			res.append(l)
		result = []
		comment = False
		# 去除形如 /* */的注释
		for l in res:
			if l.find("/*") != -1:
				comment = True
			if not comment:
				result.append(l)
			if l.find("*/") != -1:
				comment = False
		# 若直接使用 json.loads(str(res)) 会报 "ValueError: No JSON object could be decoded"
		str_res = ""
		for i in result:
			str_res += i
		return json.loads(str_res)
	
	def strip_comment(self, line):
		# 匹配IP地址的正则表达式
		ip_re = re.compile('[0-9]+(?:\.[0-9]+){0,3}')
		index = line.find("//")
		if index == -1:
			return line
		line_str = line[index]
		if ip_re.search(line_str):
			return line[:index + 16] + self.strip_comment(line[index + 17:])
		else:
			return line[:index] + self.strip_comment(line_str)
