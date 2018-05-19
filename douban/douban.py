import requests
from bs4 import BeautifulSoup
import os

session = requests.session()
login_request = session.get('https://www.douban.com/login')
login_soup = BeautifulSoup(login_request.content, 'html.parser')
#print(login_soup)
post_data = {'source':'None', 'redir':'https://www.douban.com', 'form_email':'********', 'form_password':'********', 'login':'登录'}
captcha_div=login_soup.find('img', {'id':'captcha_image'})
if captcha_div != None:
	pic_request = requests.get(captcha_div['src'])
	with open('captcha_img', 'wb') as imgfile:
		imgfile.write(pic_request.content)
	os.system('eog captcha_img &')
	string = input('请输入验证码：')
	post_data['captcha-solution'] = string
	captcha_id = login_soup.find('input', {'name':'captcha-id'})
	post_data['captcha-id'] = captcha_id['value']

#print(post_data)


r = session.post('https://accounts.douban.com/login', data = post_data)

#print(r.text)
with open('logfile.log', 'w') as logfile:
	logfile.write(r.text)
