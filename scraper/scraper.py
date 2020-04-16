from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from time import sleep
import os
# in the string/Quotation marks enter the path to where you downloaded the chromedriver.


class amizonebot:

    def login(self, usern, passw):
        GOOGLE_CHROME_PATH = os.environ['GOOGLE_CHROME_BIN']
        CHROMEDRIVER_PATH = os.environ['CHROMEDRIVER_PATH']
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.binary_location = GOOGLE_CHROME_PATH
        self.browser = webdriver.Chrome(
            executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

        # navigates you to the page.
        # self.browser = webdriver.Chrome()
        self.browser.get('https://student.amizone.net')
        sleep(1)
        # find the username field.
        username = self.browser.find_elements_by_css_selector(
            "input[name=_UserName]")
        username[0].send_keys(usern)

        # find the password field and enter the password password.
        password = self.browser.find_elements_by_css_selector(
            "input[name=_Password]")
        password[0].send_keys(passw)
        # find the login button and click it.
        loginButton = self.browser.find_elements_by_css_selector(
            "button[type=submit]")
        loginButton[0].click()
        sleep(5)

        if self.browser.find_element_by_xpath("/html/body/div[3]/div[1]/div[2]/div[1]/div[2]/div/div/div[1]/button"):
            self.browser.find_element_by_xpath(
                "/html/body/div[3]/div[1]/div[2]/div[1]/div[2]/div/div/div[1]/button").click()

        user = self.browser.find_element_by_xpath(
            '/html/body/div[2]/div/div[3]/ul/li[5]/a/span[2]').text
        userimg = self.browser.find_element_by_xpath(
            '/html/body/div[2]/div/div[3]/ul/li[5]/a/span[1]/img').get_attribute("src")
        user = user.split("\n")
        return {
            "fullname": user[0],
            "profilepic": userimg
        }

    def getSchedule(self):

        lecture_schedule = self.browser.find_element_by_xpath(
            '/html/body/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div/div/div/div[6]/div[1]/div/div/div/div[2]/div/div[2]/div')
        self.browser.execute_script(
            "arguments[0].style.maxHeight='900px'", lecture_schedule)
        # print(lecture_schedule.text.split("\n"))

        schedule = lecture_schedule.text.split("\n")
        print(schedule)
        return schedule

    def getAttendance(self):
        attendance = self.browser.find_element_by_xpath(
            '/html/body/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div/div/div/div[6]/div[2]/div/div/div/div[2]')
        self.browser.execute_script(
            "arguments[0].style.maxHeight='900px'", attendance)
        elements = attendance.text.split("\n")
        print(elements)
        return elements
