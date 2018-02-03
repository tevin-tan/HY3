import time, random

ARR = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
LAST = ('1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2')


def makeNew():
	u''' 随机生成新的18为身份证号码 '''
	
	t = time.localtime()[0]
	x = '%02d%02d%02d%04d%02d%02d%03d' % (
		random.randint(10, 99),
		random.randint(1, 99),
		random.randint(1, 99),
		random.randint(t - 80, t - 18),
		random.randint(1, 12),
		random.randint(1, 28),
		random.randint(1, 999))
	y = 0
	for i in range(17):
		y += int(x[i]) * ARR[i]
	
	return '%s%s' % (x, LAST[y % 11])


def isTrue(arg):
	u''' 验证身份证号码是否真实号码 '''
	# print(u'请输入身份证号码')
	# x1 = input('?')
	x1 = arg
	xlen = len(x1)
	if xlen != 18 and xlen != 15:
		return u'身份证号码长度错误'
	
	try:
		if xlen == 18:
			x2 = x1[6:14]
			x3 = time.strptime(x2, '%Y%m%d')
			if x2 < '19000101' or x3 > time.localtime():
				return u'时间错误，超过允许的时间范围'
		else:
			x2 = time.strptime(x1[6:12], '%y%m%d')
	except:
		return u'时间错误，非合法时间'
	
	if xlen == 18:
		y = 0
		for i in range(17):
			y += int(x1[i]) * ARR[i]
		
		if LAST[y % 11] != x1[-1].upper():
			return u'验证码错误'
	
	return u'YES'


def old2new():
	u''' 15位身份证号码转换为18位身份证号码 '''
	print(u'请输入15位老身份证号码')
	x1 = input('?')
	if len(x1) != 15:
		return u'身份证号码输入错误，身份证号码长度不为15位'
	
	oldcard = '%s19%s' % (x1[:6], x1[6:])
	y = 0
	for i in range(17):
		y += int(oldcard[i]) * ARR[i]
	
	return '%s%s' % (oldcard, LAST[y % 11])


if __name__ == '__main__':
	res = makeNew()
	print(res)
	
	rs = isTrue(res)
	print(rs)
