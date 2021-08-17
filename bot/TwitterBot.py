from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from sys import argv
import os


def account_info():
    file = rf'{os.path.dirname(__file__)}/AccountInfo.txt'
    with open(file, 'r') as f:
        info = f.read().split()
        email = info[0]
        password = info[1]
    return email, password


email, password = account_info()
# tweet = 'TYPE YOUR TWEET HERE'
tweet = argv[1]

options = Options()
options.add_argument("start-maximized")
dr = rf'{os.path.dirname(__file__)}/chromedriver.exe'
driver = webdriver.Chrome(executable_path=dr, options=options)
driver.get("https://twitter.com/login")

email_xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label/div/div[2]/div/input'
acc_password_xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]/div/input'
login_button_xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div/div'

time.sleep(5)
driver.find_element_by_xpath(email_xpath).send_keys(email)
time.sleep(1)
driver.find_element_by_xpath(acc_password_xpath).send_keys(password)
time.sleep(1)
driver.find_element_by_xpath(login_button_xpath).click()

tweet_xpath = '//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a/div'
message_xpath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[3]/div/div/div/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div'
post_xpath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[3]/div/div/div/div[1]/div/div/div/div/div[2]/div[3]/div/div/div[2]/div/div/span/span'

time.sleep(10)
driver.find_element_by_xpath(tweet_xpath).click()
time.sleep(2)
driver.find_element_by_xpath(message_xpath).send_keys(tweet)
time.sleep(5)
driver.find_element_by_xpath(post_xpath).click()

profile_xpath = '//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[2]/div/div'
logout_xpath = '//*[@id="layers"]/div[2]/div/div/div[2]/div/div[2]/div/div/div/div/div/a[2]'
logout_button_xpath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div[3]/div[2]/div'

time.sleep(5)
driver.find_element_by_xpath(profile_xpath).click()
time.sleep(5)
driver.find_element_by_xpath(logout_xpath).click()
time.sleep(5)
driver.find_element_by_xpath(logout_button_xpath).click()
