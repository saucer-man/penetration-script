#coding=utf-8

import time
from selenium import webdriver
import sys

def login_test(browser, username, password):
    browser.get('http://10.40.80.173/pad/login')
    browser.implicitly_wait(10)

    # 填充username
    user_elem = browser.find_element_by_id("username")
    user_elem.send_keys(username)
    # 填充password
    pass_elem = browser.find_element_by_id("password")
    pass_elem.send_keys(password)

    # 点击登录
    button_elem = browser.find_element_by_class_name("antd-pro-pages-user-login-pad-loginFormButton")
    button_elem.click()
    time.sleep(1)
    if "用户名密码错误" not in browser.page_source:
        return True
    else:
        return False



if __name__ == '__main__':
    browser = webdriver.Chrome()
    username_list = ["admin123","root", "admin"]
    password_list = ["password", "123456", "12345678"]
    for username in username_list:
        for password in password_list:
            if(login_test(browser, username, password)):
                print(f"username:{username}, password:{password}")
                browser.quit()
                sys.exit()
    browser.quit()