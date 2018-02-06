import config
import random
import os
import yaml
from stdnum import luhn


def getBankCardNumber():
	"""获取真是银行卡号"""
	
	rootdir = config.__path__[0]
	f1 = os.path.join(rootdir, 'bankNum')
	with open(f1, 'r', encoding='utf-8') as f:
		temp = yaml.load(f)
		# print(temp)
		
		while True:
			res = random.choice(temp['Number'])
			# 判断银行卡号是否有效
			if luhn.is_valid(res):
				break
		# print(res)
		f.close()
	return res


print(getBankCardNumber())
