# coding:utf-8

import cx_Oracle


class DB(object):
	def __init__(self):
		self.db_user = 'xndb'
		self.db_password = 'L6vz5vFwcWur'
		self.IP = '10.15.14.89'
		self.port = '1521'
		self.connection = None
		self.cursor = None

		self._create_connection()

	# connection = cx_Oracle.connect('xndb', 'L6vz5vFwcWur', '10.15.14.89:1521/xndev')

	def _create_connection(self):
		# 创建链接
		try:
			self.connection = cx_Oracle.connect(self.db_user, self.db_password, self.IP + ":" + self.port + '/xndev')
			self.cursor = self.connection.cursor()
		except ConnectionAbortedError.errno as e:
			raise e

	def shutdown(self):
		self.cursor.close()
		self.connection.close()

	def sql_execute(self, sql):
		# 执行sql语句
		self.cursor.execute(sql)

	def sql_commit(self):
		self.connection.commit()
