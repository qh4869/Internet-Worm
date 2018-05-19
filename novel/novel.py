import requests
from bs4 import BeautifulSoup
import bs4

for num in range(13295176, 13295250):
     try:
          print(num)
     
          str1 = 'http://www.bixiabook.com/22_22798/'+ str(num) + '.html'

          request = requests.get(str1).content
          soup = BeautifulSoup(request, 'html.parser')
          name = soup.find('h1').get_text()
          main_field = soup.find('div', id = 'content')
          article = main_field.get_text()

          print(name)

          with open('output.txt', 'a+', encoding='utf-8') as f:
               f.write("==================================\n")
               f.write(name+'\n')
               f.write('==================================\n')
               f.write(article+'\n')
               f.write('\n')
     except AttributeError:
          continue
