import cx_Oracle
from pprint import pprint

connection = cx_Oracle.connect('xndb', 'L6vz5vFwcWur', '10.15.14.89:1521/xndev')
# pprint(connection)

cursor = connection.cursor()
cursor.execute(
		"SELECT * FROM APP_RESULT WHERE APPLY_ID = (SELECT APPLY_ID FROM HOUSE_APPLY_INFO WHERE APPLY_CODE = 'GZ20171030E33') ORDER BY  HANDL_TIME",
		)

pprint(cursor.fetchall())


# res = cursor.fetchall()
# for r in res:
# 	print r
# cursor.close()
# connection.close()


# for i in cursor:
# 	pprint(i)
# pprint(cursor.description)
# row = cursor.fetchone()
# print row
