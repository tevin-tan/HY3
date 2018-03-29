import time


class TimeOut(object):
	"""用例耗时"""
	
	def __init__(self):
		self.using_time = None
	
	def __call__(self, func):
		def _call(*args, **kw):
			begin_time = time.clock()
			func(*args, **kw)
			end_time = time.clock()
			runtime = end_time - begin_time
			print('ran %s cost %.3f s' % (func.__name__, runtime))
		
		# self.using_time = str(runtime)[:6]
		
		return _call


class BSS(object):
	@TimeOut()  # 直接进行调用
	def runfunc(self):
		time.sleep(3)
		print('runfunc running')

# bs = bss()
# bs.runfunc()

# t = TimeOut()
# print(t.using_time)
