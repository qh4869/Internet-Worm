# -*- coding:utf-8 -*- 
import requests
import os
from bs4 import BeautifulSoup
import time

ONLINE = 1
OFFLINE = 0
while(1):
	request = requests.get('http://www.baidu.com').content
	soup = BeautifulSoup(request, 'html.parser')
	is_online = soup.find('html')
	if is_online == None:
		flag_online = OFFLINE
	else:
		flag_online = ONLINE
	#print(flag_online)
	if flag_online == OFFLINE:
		#id = input('学号：')
		#passwd = input('密码：')
		#if id == '':
		id = '***************'
		#if passwd == '':
		passwd = '******'
		userid = '%E5%AD%97%5C' + id
		#print(userid)
		#print(passwd)
		header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0', 'Connection':'keep-alive'}
		post_data = {'userId':userid, 'password':passwd, 'queryString':'wlanuserip%3D0bc386d9e643d188b011a0d00c9b5c40%26wlanacname%3D5fcbc245a7ffdfa4%26ssid%3D%26nasip%3D2c0716b583c8ac3cbd7567a84cfde5a8%26mac%3D53ba540bde596b811a6d5617a86fa028%26t%3Dwireless-v2%26url%3D2c0328164651e2b4f13b933ddf36628bea622dedcc302b30',\
					'service':'', 'operatorPwd':'','operatorUserId':'','validcode':''}
		requests.post('http://210.77.16.21/eportal/InterFace.do?method=login', data = post_data, headers = header)
		time.sleep(2)
		r2 = requests.get('http://www.baidu.com').content
		soup2 = BeautifulSoup(r2, 'html.parser')
		is_online = soup2.find('html')
		if is_online == None:
			flag_online = OFFLINE
		else:
			flag_online = ONLINE
		#print(flag_online)
	if flag_online == OFFLINE:
		delay = 60
	else:
		delay = 7200
	time.sleep(delay)

#print(soup)
#os.system('pause')
