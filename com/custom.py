# coding:utf-8

import logging
import inspect
import random
import json
import os


def print_env(env, company):
	print('*' * 100)
	print(' ' * 40 + '当前环境:' + env)
	print(' ' * 40 + '当前公司:' + company['branchName'])
	print(' ' * 40 + '风控专员:' + company['Commissioner']['user'])
	print(' ' * 42 + '权证员:' + company['authority_member']['user'])
	print(' ' * 40 + '业务助理:' + company['business_assistant']['user'])
	print('*' * 100)


def Log():
	"""定义logger级别"""
	
	logging.basicConfig(
			level=logging.INFO,
			format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
			datefmt='%a, %d %b %Y %H:%M:%S',
			# filename='myapp.log',
			filemode='w')
	
	return logging


def get_name():
	"""
		获取随机姓名
	:return: name
	"""
	family_names = [
		"赵", "钱", "孙", "李", "周", "吴", "郑", "王", "冯", "陈",
		"褚", "卫", "蒋", "沈", "韩", "杨", "朱", "秦", "尤", "许",
		"何", "吕", "施", "张", "孔", "曹", "严", "华", "金", "魏",
		"陶", "姜", "戚", "谢", "邹", "喻", "柏", "水", "窦", "章",
		"云", "苏", "潘", "葛", "奚", "范", "彭", "郎", "鲁", "韦",
		"昌", "马", "苗", "凤", "花", "方", "俞", "任", "袁", "柳",
		"酆", "鲍", "史", "唐", "费", "廉", "岑", "薛", "雷", "贺",
		"倪", "汤", "滕", "殷", "罗", "毕", "郝", "邬", "安", "常",
		"乐", "于", "时", "傅", "皮", "卞", "齐", "康", "伍", "余",
		"元", "卜", "顾", "孟", "平", "黄", "和", "穆", "萧", "尹"
		]
	
	last_names = [
		"子璇", "淼", "国栋", "夫子", "瑞堂", "甜", "敏", "尚", "国贤", "贺祥", "晨涛",
		"昊轩", "易轩", "益辰", "益帆", "益冉", "瑾春", "瑾昆", "春齐", "杨", "文昊",
		"东东", "雄霖", "浩晨", "熙涵", "溶溶", "冰枫", "欣欣", "宜豪", "欣慧", "建政",
		"美欣", "淑慧", "文轩", "文杰", "欣源", "忠林", "榕润", "欣汝", "慧嘉", "新建",
		"建林", "亦菲", "林", "冰洁", "佳欣", "涵涵", "禹辰", "淳美", "泽惠", "伟洋",
		"涵越", "润丽", "翔", "淑华", "晶莹", "凌晶", "苒溪", "雨涵", "嘉怡", "佳毅",
		"子辰", "佳琪", "紫轩", "瑞辰", "昕蕊", "萌", "明远", "欣宜", "泽远", "欣怡",
		"佳怡", "佳惠", "晨茜", "晨璐", "运昊", "汝鑫", "淑君", "晶滢", "润莎", "榕汕",
		"佳钰", "佳玉", "晓庆", "一鸣", "语晨", "添池", "添昊", "雨泽", "雅晗", "雅涵",
		"清妍", "诗悦", "嘉乐", "晨涵", "天赫", "玥傲", "佳昊", "天昊", "萌萌", "若萌"
		]
	
	i = random.randint(0, 99)
	f_name = family_names[i]
	j = random.randint(0, 99)
	l_name = last_names[j]
	name = f_name + l_name
	return name


def logout(driver):
	driver.find_element_by_xpath("/html/body/header/div[2]").click()


def enviroment_change(filename, number=0, enviroment="SIT"):
	"""
		环境切换
	:param enviroment: SIT/UAT
	:param number:  "0" 广州分公司; "1" 长沙分公司
	:return:    录入的数据， 所选分公司
	"""
	
	try:
		import config
		rd = config.__path__[0]
		data_config = os.path.join(rd, filename)
		env_config = os.path.join(rd, 'env.json')
		print("data_config:" + data_config)
		
		with open(data_config, 'r', encoding='utf-8') as fd:
			data = json.load(fd)
		
		# 环境变量, 切换分公司
		with open(env_config, 'r', encoding='utf-8') as f1:
			env = json.load(f1)
			company = env[enviroment]["company"][number]
		
		return data, company
	except Exception as e:
		print("config error:" + str(e))
		raise


def get_current_function_name():
	"""
		获取当前方法的名字
	:return:
	"""
	return inspect.stack()[1][3]


def hello():
	pwd = os.getcwd()
	father_path = os.path.abspath(os.path.dirname(pwd) + os.path.sep + ".")
	with open(father_path + "/config/env.json", 'r', encoding='utf-8') as f1:
		env = json.load(f1)
		print(env)
	
	dir = os.path.dirname(os.getcwd())
	print(dir + "/config/env.json")


if __name__ == '__main__':
	# dr = webdriver.Chrome()
	# dr.get("http://www.baidu.com")
	# dr.quit()
	#
	# logger = log_to()
	# logger.debug('This is debug message')
	# logger.info('This is info message')
	# logger.warning('This is warning message')
	
	hello()
