from selenium import webdriver
import time
from conversation import postConv
import os
import subprocess
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

youtubeURL = "https://www.youtube.com/watch?v=hogehogehoge"

# Start ChromeDriver
driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',
                          desired_capabilities=DesiredCapabilities.CHROME)
driver.get(youtubeURL)

# waiting for iframe
# ToDo : There should be better way to write, so rewrite later
time.sleep(5)
element = driver.find_element_by_id("chatframe").get_attribute("src")
# print(element)

driver.get(element)
element = driver.find_element_by_id("chat")
# print(element.text)

authorname = element.find_elements_by_id("author-name")
message = element.find_elements_by_id("message")
for (i, comment) in enumerate(authorname):
    print(comment.text + ' : ' + message[i].text)

maxcomment_index = 0
beforeauthor = ""
beformessage = ""

try:
    while(1):
        time.sleep(0.3)
        authorname = element.find_elements_by_id("author-name")
        message = element.find_elements_by_id("message")
        if len(authorname) != 0:
            authorname = authorname[-1:][0].text
            message = message[-1:][0].text

            if ((authorname != beforeauthor) or (message != beformessage)) & (message != '') & (authorname != ''):
                print(authorname + ' : ' + message)
                reply_message = postConv(message)
                print("あんどう" + ' : ' + reply_message)
                subprocess.call('say ' + '"' + reply_message + '"', shell=True)
                print(" ")

            beforeauthor = authorname
            beformessage = message
        else:
            pass
except KeyboardInterrupt:
    driver.close()
    driver.quit()
    raise e
except Exception as e:
    driver.close()
    driver.quit()
    raise e
