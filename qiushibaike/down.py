import requests
from bs4 import BeautifulSoup
import bs4
import os
import time

def qiushibaike():

    num = 0; #序号
    
    f = open("output.txt", "w",encoding='utf-8')
    os.system("del *.jpg")   
    request = requests.get('http://www.qiushibaike.com').content
    soup = BeautifulSoup(request, 'html.parser')

    main_field = soup.find('div', id = 'content-left')
    for joke_block in main_field.children:
        if type(joke_block) == bs4.element.Tag and joke_block.name == "div":
            num = num + 1
            author = joke_block.find("h2").get_text(strip=True)
            joke_content = joke_block.find("div", class_ = "content").get_text(strip=True)
            f.write("-----------------------\n")
            f.write("{0}、".format(num) + author)
            f.write("\n")
            f.write(joke_content)
            f.write("\n")
            pic_tag = joke_block.find("div", class_ = "thumb")
            if pic_tag != None:
                pic_link = pic_tag.find("img").get("src")
                pic_request = requests.get("http:" + pic_link)
                with open("{0}.jpg".format(num), "wb") as file:
                    file.write(pic_request.content)
    f.close()

if __name__ == '__main__':
    while(1):
        qiushibaike()
        print (time.asctime( time.localtime(time.time()) ))
        time.sleep(30)
        # os.system("cls")
    # qiushibaike()
    # os.system("pause")
