import time
from bs4 import BeautifulSoup as bs
from random import randint
from pymysql import escape_string

import request
import mysqlcom as mysql

'''
数据库
mgenre  分类表
migenre 地址表
midata 详情地址表 
minformation 信息表
minformation_mtype 关联表（分类和信息）
'''


dns = 'http://www.imdb.cn/'
base_url = 'http://www.imdb.cn/Sections/Genre/Drama'

def save_html(url):
	"""
	获取首页中的所有分类链接，保存到数据库
	"""

	h = request.get_html(url)

	soup = bs(h, 'lxml')
	items_list = soup.find('div', class_='ss-1').find('span').find_all('a')
	for items in items_list:
		item = {}
		item['title'] = items.text
		item['name'] = items['href'].split('/')[-1]
		item['addr'] = dns + items['href']
		item['flag'] = 1
		# content = tuple(item.values())
		data_tup = (data['title'], data['name'], data['addr'], data['flag'])
		sql = '''insert into %s (title, name, addr, flag) values %s'''%('mgenre', data_tup)

		# mysql.insert(sql)
		print('insert information successful.')
	print('data save successful.')


def get_html():
	"""
	获取分类表分类地址，填充分类地址中的地址到地址表中
	要点： 数据库的查询去重，获取完一个地址后标记， 保持获取页面间隔
	"""
	items = mysql.select_all('mgenre', 'flag=1')
	# item = mysql.select('mgenre', 'flag=1')
	for item in items:
		url = item['addr']

		data = {}
		data['title'] = item['title']
		data['addr'] = url
		data['flag'] = 1
		data['m_id'] = item['id']


		h = request.get_html(url)

		soup = bs(h, 'lxml')
		page_info = soup.find('p', class_='rpage')
		# print(page.text, len(page.text))
		a = page_info.text.split(' ')
		page = a[2].split('/')[1]
		print(page)
		for i in range(1, int(page)+1):
			data['addr'] = url + '/%s'%(i)
			# query = tuple(data.values())
			data_tup = (data['title'], data['addr'], data['flag'], data['m_id'])
			sql = '''insert into %s (title, addr, flag, mgenre_id) values %s'''%('migenre', data_tup)
			if i == int(page):

				mysql.insert(sql)
				print('last one:[%s]'%data['addr'])
				mysql.update('mgenre', 'flag=0 where addr="%s"'%(url))

			else:
				mysql.insert(sql)
				print('insert: [%s]'%data['addr'])

		time.sleep(3)


def check_url(table, query):
	flag = mysql.select(table, query)
	if not flag:
		return False
	else:
		return True


def current_progress():
	"""
	查看进度
	"""
	a_num = mysql.select_sql('select count(*) as num from migenre')
	s_num = mysql.select_sql('select count(*) as num from migenre where flag=0')
	print('进度： %s/%s'%(s_num['num'], a_num['num']))


def get_info_url():
	"""
	获取地址表地址，填充数据到详情地址表中
	要点：
		检查地址是否存在，获取完标记 保持获取速度
		关联表数据插入检查
	"""
	pool_flag = True
	while pool_flag:

		item = mysql.select('migenre', 'flag=1')
		current_progress()
		print('当前正在分析[%s].'%(item['addr']))
		time.sleep(randint(8,11))
		# time.sleep(0.5)
		if item:
			url = item['addr']
			data = {}
			data['title'] = item['title']
			data['addr'] = url
			data['flag'] = 1
			data['m_id'] = item['mgenre_id'] 
			# print(data)

			h = request.get_html(url)

			soup = bs(h, 'lxml')
			div_info = soup.find('div', class_='ss-3 clear')
			a_list = div_info.find_all('a')
			for li in range(len(a_list)):
				if li == (len(a_list)-1):
					data['addr'] = dns[:-1]+a_list[li]['href']
					# flag = check_url('midata', 'addr="%s"'%(data['addr']))
					flag = mysql.select('midata', 'addr="%s"'%(data['addr']))
					if not flag:
						data_tup = (data['title'], data['addr'], data['flag'], data['m_id'])
						sql = '''insert into %s (title, addr, flag, mgenre_id) values %s'''%('midata', data_tup)
						# print(sql)
						# mysql.insert(sql)
						print('最后一条: [%s]'%(data['addr']))
						mysql.update('migenre', 'flag=0 where id=%s'%(item['id']))
						print('添加数据，因为是最后一条，更新数据地址。')
					else:
						mysql.update('migenre', 'flag=0 where id=%s'%(item['id']))
						print('该数据已存在。因为是最后一条，更新地址数据')
				else:
					data['addr'] = dns[:-1]+a_list[li]['href']
					flag = mysql.select('midata', 'addr="%s"'%(data['addr']))
					if not flag:
						data_tup = (data['title'], data['addr'], data['flag'], data['m_id'])
						sql = '''insert into %s (title, addr, flag, mgenre_id) values %s'''%('midata', data_tup)
						# print(sql)
						mysql.insert(sql)
						print('记录条目: [%s]'%data['addr'])
					else:
						print('改数据已记录。')
		else:
			print('表数据记录完毕，退出。')
			pool_flag = False


def get_info(offset):
	"""
	获取详情地址表中的地址，填充数据到信息表，同时填充关联表
	要点：
		数据查询 获取完标记 保持获取速度
	"""

	item = mysql.select('midata', 'flag=1 limit %s,1'%(offset))
	if item:
		url = item['addr']
		print('当前地址：[%s]'%url)
		print(time.strftime('%H:%M:%S'))
		# time.sleep(randint(6,10))
		time.sleep(0.5)
		data = {}

		# data['m_id'] = item['mgenre_id'] 
		# print(data)	
		mt_dict = {
			'剧情':1, '短片':2, '喜剧':3, '记录':4, '动作':5, '惊怵':6, '爱情':7, '犯罪':8, '恐怖':9, 
			'家庭':10, '冒险':11, '动画':12, '科幻':13, '奇幻':14, '音乐':15, '神秘':16, '音乐剧':17, 
			'战争':18, '西部':19, '传记':20, '运动':21, '历史':22, '真人秀':23, '游戏节目':24, '脱口秀':25, '黑色':26, '新闻':27
			}
		h = request.get_html(url)

		soup = bs(h, 'lxml')
		div_info = soup.find('div', class_='fk-3')
		# print(div_info)
		# data['title'] = item['title']
		data['title'] = div_info.find('div', class_='hdd').h3.text
		data['sorce'] = div_info.find('div', class_='hdd').i.text

		info_list = div_info.find_all('li')
		for i in range(len(info_list)):
			con = '%s -%s\n'%(i, info_list[i])
		data['name'] = info_list[0].a.text
		# data['name'] = info_list[1].a.text
		four_data = info_list[3].i.text
		if '主演' in four_data:
			data['actor'] = '/'.join([i.text for i in info_list[3].find_all('a')])
			if '时长' in info_list[4].text:
				# print('有主演有时长')
				data['ptime'] = (info_list[4].text.split('：'))[1].replace('语言', '').replace('&nbsp', '')
				data['language'] = '' if not info_list[4].a else info_list[4].a.text
				data['pyear'] = info_list[5].find('a')['title']
				mtype = [i.text for i in info_list[5].find_all('a')]
				data['country'] = '' if not info_list[6].a else info_list[6].a.text
			else:
				# print('有主演无时长')
				data['ptime'] = ''
				data['language'] = ''
				data['pyear'] = info_list[4].find('a')['title']
				mtype = [i.text for i in info_list[4].find_all('a')]
				data['country'] = '' if not info_list[5].a else info_list[5].a.text
		elif '时长' in four_data:
			# print('无主演有时长')
			data['actor'] = ''
			data['ptime'] = (info_list[3].text.split('：'))[1].replace('语言', '').replace('&nbsp', '')
			data['language'] = '' if not info_list[3].a else info_list[3].a.text
			data['pyear'] = info_list[4].find('a')['title']
			mtype = [i.text for i in info_list[4].find_all('a')]
			data['country'] = '' if not info_list[5].a else info_list[5].a.text

		else:
			# print('无主演无时长')
			data['actor'] = ''
			data['ptime'] = ''
			data['language'] = ''
			data['pyear'] = info_list[3].find('a')['title']
			mtype = [i.text for i in info_list[3].find_all('a')]
			data['country'] = '' if not info_list[4].a else info_list[4].a.text
		
		data['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
		data['img'] = soup.find('div', class_='fk-2').img['src']
		activator_info =  '' if not info_list[2].a else info_list[2].a.text
		if activator_info:
			data['activator'] =  '' if '未知' in activator_info else info_list[2].a['title']
		else:
			data['activator'] = ''
		# time.sleep(3)
		data['summary'] = (escape_string(soup.find('div', class_='fk-4 clear').find('div', class_='bdd clear').text) 
			if soup.find('div', class_='fk-4 clear').find('div', class_='bdd clear') else '')
		# print(data)
		# print(data.values())
		data_tup = (data['title'], data['sorce'], data['name'], data['actor'], data['ptime'], data['language'], 
			data['pyear'], data['country'], data['create_time'], data['img'], data['activator'], data['summary'])
		sql = '''insert into %s (title, sorce, name, actor, ptime, language, pyear, country, create_time, img, activator, summary) 
				values %s'''%('minformation', data_tup)
		# print('sql1: %s'%sql)
		sql2 = '''update %s set flag=0 where id=%s'''%('midata', item['id'])
		# print('sql2: %s'%sql2)
		mysql.begin(sql, sql2)
		print('[%s]已记录。'%item['addr'])
		# return 
		for m in mtype:
			if m in mt_dict:
				mi_id = mysql.select_sql('select id from minformation order by id desc limit 1')
				mg_id = mt_dict[m]
				values = (mi_id['id'], mg_id)
				# values = (1,mg_id)
				sql = '''insert into %s (minformation_id, mgenre_id) values %s'''%('minformation_mtype',values)
				# print('igsql: %s'%sql)
				query = 'minformation_id=%s and mgenre_id=%s'%(mi_id['id'],mg_id)
				f = mysql.select('minformation_mtype', query)
				if f:
					print('该条数据已记录')
					continue
				else:
					mysql.insert(sql)
					print('[%s]已记录到关联数据库。'%(values,))
			else:
				print('[%s]字段不在当前分类中。'%m)
				continue
		# print(mtype)
	else:
		print('没有值，试试偏移为0')


def main():
	# save_html(base_url)
	# get_html()
	# get_info_url()
	while True:
		get_info(0)
	# 设置偏移值
	# offset = 0
	# get_info(offset)


if __name__ == '__main__':
	main()
