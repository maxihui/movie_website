import requests
from random import randint

def get_agent():
	"""
	获取浏览器头
	"""
	agent = [
		'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
		'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
		'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
	]
	header = {}
	header['User-Agent'] = agent[randint(0, len(agent)-1)]
	return header

def get_html(url):
	try:
		r = requests.get(url, headers=get_agent())
		r.raise_for_status
		r.encoding = 'utf8'
		return r.text
	except Exception as e:
		print(e)
		print('-'*10)
		return False