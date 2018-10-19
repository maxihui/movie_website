import pymysql


def get_conn():
	"""
	建立数据库连接
	"""
	conn = pymysql.connect(
		host='localhost',
		user='root',
		password='12345678',
		db='imdb',
		charset='utf8',
		cursorclass=pymysql.cursors.DictCursor
		)
	return conn


def insert(sql):
	"""
	插入数据库操作，直接传入sql，因为在这里直接生成sql会有编码错误，所以直接传入整句sql
	"""
	conn = get_conn()
	cursor = conn.cursor()
	try:
		cursor.execute(sql)
		conn.commit()
	except Exception as e:
		print('error: %s'%e)
		print('-'*10)
		conn.rollback()
	finally:
		cursor.close()
		conn.close()


def select(table, squery):
	conn = get_conn()
	cursor = conn.cursor()
	sql = '''select * from %s where %s'''%(table, squery)
	try:
		# print(sql)
		cursor.execute(sql)
		return cursor.fetchone()
	except Exception as e:
		print(e,'\n----------')
		conn.rollback()
	finally:
		cursor.close()
		conn.close()


def select_all(table, squery):
	conn = get_conn()
	cursor = conn.cursor()
	sql = '''select * from %s where %s'''%(table, squery)
	try:
		# print(sql)
		cursor.execute(sql)
		return cursor.fetchall()
	except Exception as e:
		print(e,'\n----------')
		conn.rollback()
	finally:
		cursor.close()
		conn.close()


def update(table, squery):
	conn = get_conn()
	cursor = conn.cursor()
	sql = '''update %s set %s;'''%(table, squery)
	try:
		cursor.execute(sql)
		conn.commit()
		print('update successful.')
	except Exception as e:
		print('error: %s'%e)
		print('-'*10)
		conn.rollback()
	finally:
		cursor.close()
		conn.close()


def begin(sql, sql2, *args):
	conn = get_conn()
	cursor = conn.cursor()
	try:
		if args:
			sql3 = args[0]
			cursor.execute(sql)
			cursor.execute(sql2)
			cursor.execute(sql3)
			conn.commit()
		else:
			cursor.execute(sql)
			cursor.execute(sql2)
			conn.commit()
	except Exception as e:
		print('error: %s'%e)
		print('-'*10)
		conn.rollback()
	finally:
		cursor.close()
		conn.close()

def select_sql(sql):
	conn = get_conn()
	cursor = conn.cursor()
	try:
		# print(sql)
		cursor.execute(sql)
		return cursor.fetchone()
	except Exception as e:
		print(e,'\n----------')
		conn.rollback()
	finally:
		cursor.close()
		conn.close()


def select_asql(sql):
	conn = get_conn()
	cursor = conn.cursor()
	try:
		# print(sql)
		cursor.execute(sql)
		return cursor.fetchall()
	except Exception as e:
		print(e,'\n----------')
		conn.rollback()
	finally:
		cursor.close()
		conn.close()