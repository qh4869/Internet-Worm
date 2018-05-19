import requests 
import json
import re
import os

PATH = '/home/share/imgfile' #图片下载路径

jar = requests.cookies.RequestsCookieJar()

f = open("cookie.txt", 'r')
for line in f.readlines():
	if line == '\n':
		continue
	line_content = line.split()
	try:
		name = line_content[5]
		path = line_content[2]
		domain = line_content[0]
		value = line_content[6]
	except IndexError:
		value = ''
	jar.set(name, value, domain = domain, path = path)

header = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0'}

s = requests.session()
print("请先将cookie保存到本地cookie.txt文件(firefox:Advanced Cookie Manager)")
g_tk = input("输入该cookie对应的加密g_tk码(去空间的请求url里面找):")
reobj_uin = re.search(r'o(.*)', jar['uin'], re.I)
uin = reobj_uin.group(1)
host_uin = input("访问空间的qq号(不输入默认当前空间):")
if host_uin == '':
	host_uin = uin
url_temp_albumlist = 'https://h5.qzone.qq.com/proxy/domain/photo.qzone.qq.com/fcgi-bin/fcg_list_album_v3?callback=shine0_Callback&t=329780074&inCharset=utf-8&outCharset=utf-8&callbackFun=shine0'
url_json_albumlist = url_temp_albumlist + '&g_tk=' + g_tk + '&uin=' + uin + '&hostUin=' + host_uin
r_albumlist = s.get(url_json_albumlist, headers = header, cookies = jar)
reobj_json_albumlist = re.search(r'\((.*?)\)', r_albumlist.text, re.I|re.S)
json_ori_albumlist = reobj_json_albumlist.group(1)
json_data_albumlist = json.loads(json_ori_albumlist)
num_count = 0#序号用于选择
for album in json_data_albumlist['data']['albumListModeSort']:
	print('name:{0}\ttotal num:{1}\tnum:{2}'.format(album['name'], album['total'], num_count))
	num_count = num_count + 1
num_select = input('输入要下载的相册序号:')
topicid = json_data_albumlist['data']['albumListModeSort'][int(num_select)]['id']
url_temp_piclist = 'https://h5.qzone.qq.com/proxy/domain/photo.qzone.qq.com/fcgi-bin/cgi_list_photo?callback=shine0_Callback&t=845267418&inCharset=utf-8&outCharset=utf-8&callbackFun=shine0'
url_temp_piclist = url_temp_piclist + '&pageStart=0' + '&pageNum=3000' #默认最多下载的额照片个数（可改）
url_json_piclist = url_temp_piclist + '&g_tk=' + g_tk + '&uin=' + uin + '&hostUin=' + host_uin + '&topicId=' + topicid
r_piclist = s.get(url_json_piclist, headers = header, cookies = jar)
reobj_json_piclist = re.search(r'\((.*)\)', r_piclist.text, re.I|re.S)
json_ori_piclist = reobj_json_piclist.group(1)
json_data_piclist = json.loads(json_ori_piclist)
url_temp_pic = 'https://h5.qzone.qq.com/proxy/domain/photo.qzone.qq.com/fcgi-bin/cgi_floatview_photo_list_v2?callback=viewer_Callback&t=309415401&cmtNum=10&inCharset=utf-8&outCharset=utf-8&callbackFun=viewer&appid=4&isFirst=1'
url_temp_pic = url_temp_pic + '&g_tk=' + g_tk + '&topicId=' + topicid + '&uin=' + uin + '&hostUin=' + host_uin
num_count = 0
os.system('rm -r ' + PATH)
os.system('mkdir ' + PATH)
for pic in json_data_piclist['data']['photoList']:
	pickey = pic['lloc']
	url_json_pic = url_temp_pic + '&picKey=' + pickey
	r_pic = s.get(url_json_pic, headers = header, cookies = jar)
	reobj_pic = re.search(r'\((.*)\)', r_pic.text, re.I|re.S)
	json_ori_pic = reobj_pic.group(1)
	json_data_pic = json.loads(json_ori_pic)
	url_pic = json_data_pic['data']['photos'][0]['url']
	try:
		r_pic = s.get(url_pic, headers = header, cookies = jar)
		with open(PATH + '/img_{0}.jpeg'.format(num_count), 'wb') as f:
		    f.write(r_pic.content)
		num_count = num_count + 1
		print('已完成:{0}'.format(num_count))
	except requests.exceptions.ConnectTimeout:
		num_count = num_count + 1
		print('请求超时:{0}'.format(num_count))
