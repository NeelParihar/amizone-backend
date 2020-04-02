from selenium import webdriver
from selenium.webdriver.common.keys import Keys


#in the string/Quotation marks enter the path to where you downloaded the chromedriver.

browser = webdriver.Chrome("/usr/local/bin/chromedriver")

#navigates you to the page.
browser.get('https://student.amizone.net/')

#find the username field and enter the email example@yahoo.com.
username = browser.find_elements_by_css_selector("input[name=_UserName]")
username[0].send_keys('A70405218073')

#find the password field and enter the password password.
password = browser.find_elements_by_css_selector("input[name=_Password]")
password[0].send_keys('5fe0b2')

#find the login button and click it.
loginButton = browser.find_elements_by_css_selector("button[type=submit]")
loginButton[0].click()