from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from userinfo import username1,password1
from time import sleep
from insertdatabase import insert_user
options = Options()
options.headless = True

#in the string/Quotation marks enter the path to where you downloaded the chromedriver.
browser = webdriver.Chrome("/usr/local/bin/chromedriver")


#navigates you to the page.
browser.get('https://student.amizone.net/')

#find the username field and enter the email example@yahoo.com.
username = browser.find_elements_by_css_selector("input[name=_UserName]")
username[0].send_keys(username1)
user=[username1,password1]
insert_user(user)
#find the password field and enter the password password.
password = browser.find_elements_by_css_selector("input[name=_Password]")
password[0].send_keys(password1)

#find the login button and click it.
loginButton = browser.find_elements_by_css_selector("button[type=submit]")
loginButton[0].click()
sleep(3)
#browser.find_element_by_xpath('//*[@id="myModal"]/div/div/div[1]/button').click()
sleep(1)
user=browser.find_element_by_xpath('/html/body/div[2]/div/div[3]/ul/li[5]/a/span[2]').text
userimg=browser.find_element_by_xpath('/html/body/div[2]/div/div[3]/ul/li[5]/a/span[1]/img').get_attribute("src")
print(user.split("\n"))
print(userimg)


attendance = browser.find_element_by_xpath('/html/body/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div/div/div/div[6]/div[2]/div/div/div/div[2]')
browser.execute_script("arguments[0].style.maxHeight='900px'", attendance)
sleep(1)
eles=attendance.find_elements_by_tag_name("span")
for e in eles:
    print(e.text)

lecture_schedule = browser.find_element_by_xpath('/html/body/div[3]/div[1]/div[2]/div[1]/div/div[2]/div/div/div/div[6]/div[1]/div/div/div/div[2]')
browser.execute_script("arguments[0].style.maxHeight='900px'", lecture_schedule)

print(lecture_schedule.text)