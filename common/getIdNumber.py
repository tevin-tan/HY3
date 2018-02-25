"""
	生成身份证号
	生成手机号
"""
import random
import datetime
from datetime import date
from datetime import timedelta
import os

base_dir = os.path.dirname(os.path.dirname(__file__))
DC_PATH = base_dir + "/common/districtcode.txt"


# 随机生成手机号码
def createPhone():
	prelist = [
		"130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152", "153",
		"155", "156", "157", "158", "159", "186", "187", "188"]
	return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))


# 随机生成身份证号
def getdistrictcode():
	with open(DC_PATH) as file:
		data = file.read()
		districtlist = data.split('\n')
	for node in districtlist:
		# print("node:", node)
		if node[10:11] != ' ':
			# 省市
			state = node[10:].strip()
		if node[10:11] == ' ' and node[12:13] != ' ':
			city = node[12:].strip()
		if node[10:11] == ' ' and node[12:13] == ' ':
			district = node[14:].strip()
			code = node[0:6]
			codelist.append({
				"state": state, "city": city, "district": district, "code": code
				})


def getValidateCheckout(id17):
	"""获得校验码算法"""
	weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 十七位数字本体码权重
	validate = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']  # mod11,对应校验码字符值
	
	sum = 0
	for i in range(0, len(id17)):
		sum = sum + int(id17[i]) * weight[i]
	mode = sum % 11
	return validate[mode]


def gennerator():
	global codelist
	codelist = []
	if not codelist:
		getdistrictcode()
	id = codelist[random.randint(0, len(codelist))]['code']  # 地区项
	id = id + str(random.randint(1930, 2013))  # 年份项
	da = date.today() + timedelta(days=random.randint(1, 366))  # 月份和日期项
	id = id + da.strftime('%m%d')
	id = id + str(random.randint(100, 300))  # ，顺序号简单处理
	
	checkOut = getValidateCheckout(id)
	id = id + str(checkOut)
	
	"""
		count = 0
		weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 权重项
		checkcode = {
			'0': '1', '1': '0', '2': 'X', '3': '9', '4': '8', '5': '7', '6': '6', '7': '5', '8': '5', '9': '3', '10': '2'
			}  # 校验码映射
		for i in range(0, len(id)):
			count = count + int(id[i]) * weight[i]
			id = id + checkcode[str(count % 11)]  # 算出校验码
	"""
	
	return id

print(createPhone())
print(gennerator())

# Todo
"""

def getRandomIdNumber(sex=1):
	#产生随机可用身份证号，sex = 1表示男性，sex = 0表示女性
	# 地址码产生
	from addr import addr  # 地址码
	addrInfo = random.randint(0, len(addr))  # 随机选择一个值
	addrId = addr[addrInfo][0]
	addrName = addr[addrInfo][1]
	idNumber = str(addrId)
	# 出生日期码
	start, end = "1960-01-01", "2000-12-30"  # 生日起止日期
	days = (datetime.datetime.strptime(end, "%Y-%m-%d") - datetime.datetime.strptime(start, "%Y-%m-%d")).days + 1
	birthDays = datetime.datetime.strftime(
		datetime.datetime.strptime(start, "%Y-%m-%d") + datetime.timedelta(random.randint(0, days)), "%Y%m%d")
	idNumber = idNumber + str(birthDays)
	# 顺序码
	for i in range(2):  # 产生前面的随机值
		n = random.randint(0, 9)  # 最后一个值可以包括
		idNumber = idNumber + str(n)
	# 性别数字码
	sexId = random.randrange(sex, 10, step=2)  # 性别码
	idNumber = idNumber + str(sexId)
	# 校验码
	checkOut = getValidateCheckout(idNumber)
	idNumber = idNumber + str(checkOut)
	return idNumber, addrName, addrId, birthDays, sex, checkOut

"""
