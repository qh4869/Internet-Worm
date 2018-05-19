import requests

data = {'userName' : '*******', 'pwd' : '********', 'sb' : 'sb'}
sy = requests.session()
ty = sy.post('http://sep.ucas.ac.cn/slogin', data = data)
ry = sy.get('http://sep.ucas.ac.cn/appStore')
print(ry.text)

