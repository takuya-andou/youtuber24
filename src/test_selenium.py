from selenium import webdriver
import time
from conversation import postConv
import os

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


youtubeURL = "https://youtu.be/2glBKDEfaBo"

# ChromeDriverのパスを引数に指定しChromeを起動
# driver = webdriver.Chrome(os.path.expanduser(
#     "/home/youtuber24/src/chromedriver"))

driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub',
                          desired_capabilities=DesiredCapabilities.CHROME)

driver.get(youtubeURL)

# iframeが出てくるまで待つ
# より良い書き方があるはず
time.sleep(5)
element = driver.find_element_by_id("chatframe").get_attribute("src")
print(element)


driver.get(element)
# Googleの検索テキストボックスの要素をID名から取得

element = driver.find_element_by_id("chat")

# print(element.text)
authorname = element.find_elements_by_id("author-name")
message = element.find_elements_by_id("message")
for (i, comment) in enumerate(authorname):
    print(comment.text + ' : ' + message[i].text)

maxcomment_index = 0
beforeauthor = ""
beformessage = ""

while(1):
    time.sleep(1)
    authorname = element.find_elements_by_id("author-name")
    message = element.find_elements_by_id("message")
    if len(authorname) != 0:
        authorname = authorname[-1:][0].text
        message = message[-1:][0].text

        if ((authorname != beforeauthor) or (message != beformessage)) & (message != '') & (authorname != ''):
            print(authorname + ' : ' + message)
            print("あんどう" + ' : ' + postConv(message))
            print(" ")

        beforeauthor = authorname
        beformessage = message
    else:
        pass
