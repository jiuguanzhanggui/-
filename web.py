from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import random


def web_start():
    options = webdriver.EdgeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Edge(options=options)

    return driver

def web_operate_toutiao(driver):
    driver.get('https://mp.toutiao.com/profile_v4/index')
    time.sleep(random.uniform(2,5))
    driver.find_element(By.XPATH,'//*[@id="masterRoot"]/div/div[3]/section/aside/div/div/div/div[2]/div[2]/div[2]/span/a').click()
    time.sleep(random.uniform(2,5))
    driver.find_element(By.XPATH,'//*[@id="root"]/div/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div/input').send_keys()
    time.sleep(random.uniform(2,5))