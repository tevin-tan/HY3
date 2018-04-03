import cx_Oracle

connection = cx_Oracle.connect('xndb', 'L6vz5vFwcWur', '10.15.14.89:1521/xndev')
# pprint(connection)

apply_id = '30260'
cursor = connection.cursor()
# cursor.execute(
# 	"SELECT * FROM  HOUSE_COMMON_LOAN_INFO WHERE APPLY_ID=" + apply_id
# )
# cursor.execute(
# 	"UPDATE house_common_loan_info t SET t.pay_date=sysdate, t.status='LOAN_PASS' WHERE t.apply_id= '39117'",
# 	)

apply_code = 'GZ20180330C14'

sql = "UPDATE house_common_loan_info t SET t.pay_date=sysdate, t.status='' \
WHERE t.apply_id= (SELECT t.apply_id FROM house_apply_info t \
WHERE t.apply_code =" + "'" + apply_code + "'" + ")"

cursor.execute(sql)
connection.commit()
# print(cursor.fetchall()[0])
# pprint(cursor.fetchall())

# 一次返回所有结果集
# res = cursor.fetchall()
# for r in res:
# 	print(r)
# print(cursor.description)

# 一次返回一行
# row = cursor.fetchone()
# print(row)


# for i in cursor:
# 	pprint(i)
# 	pprint(cursor.description)

cursor.close()
connection.close()
