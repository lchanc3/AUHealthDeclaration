import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

'''設定區域開始'''
#import os
#os.environ['WDM_LOG_LEVEL'] = '0' #關閉webdriver_manager在cmd內的log，不建議使用
'''視瀏覽器更改設定區域開始'''
#參見 https://github.com/SergeyPirogov/webdriver_manager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

browser_options = Options()
browser_options.add_argument('--headless') #firefox 無頭模式

browser = webdriver.Firefox(service=Service(GeckoDriverManager().install()),options=browser_options) 
'''視瀏覽器更改設定區域結束'''

StudentID = "學號"
Password = "密碼"
Email = "電郵"
Phone = "電話"

codeVer = 'v.1.3.15'
wait = WebDriverWait(browser, 5) #等待幾秒 推薦5-10秒
browser.set_page_load_timeout(100)
'''設定區域結束'''

def login():
    browser.find_element(By.ID, "username").send_keys(StudentID)
    browser.find_element(By.ID, "password").send_keys(Password)
    browser.find_element(By.ID, "password").send_keys(Keys.ENTER)
    print("登入中...")

def check_ver():
    
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-outline-primary"))).click() #"同意"
    browser.get("https://pacific.asia.edu.tw/HealthDeclaration#/") #回到表單
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "text-secondary"))).text #獲取版本
    ver = browser.find_element(By.CLASS_NAME, "text-secondary").text

    if ver == codeVer:
        print("版本檢查：正確")
    else:
        print("版本檢查：不符，可能會產生意外的狀況。建議更新版本")

def write():
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "btn.btn-sm.btn-info.mt-2"))) #check_written
        print("你已經填寫過表格了！",browser.find_element(By.CLASS_NAME, "text-right.text-success").text) #print_when
    except:
        print("填寫中...")
        wait.until(EC.element_to_be_clickable((By.ID, "cell"))).send_keys(Phone) #Phone
        wait.until(EC.element_to_be_clickable((By.ID, "mail"))).clear()
        wait.until(EC.element_to_be_clickable((By.ID, "mail"))).send_keys(Email) #mail
        wait.until(EC.element_to_be_clickable((By.ID, "Q1Option7"))).click() #narmal
        wait.until(EC.element_to_be_clickable((By.ID, "Q2Option5"))).click() #@Taiwan
        wait.until(EC.element_to_be_clickable((By.ID, "Q30"))).click() #unHomeIsolation
        wait.until(EC.element_to_be_clickable((By.ID, "read"))).click() #read
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn.btn-primary"))).click() #submit
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn.btn-outline-success.mr-3"))).click() #check
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn.btn-outline-primary.float-right"))).click() #close

def main():
    browser.get("https://pacific.asia.edu.tw/HealthDeclaration#/Login")
    try:
        login()
    except:
        print(browser.switchTo().alert().getText())
        print("登入失敗，請檢查帳號和密碼是否正確")
    check_ver()
    write()

main()
print("所有工作皆已完成，瀏覽器將於5秒後關閉")
time.sleep(5)
browser.quit()