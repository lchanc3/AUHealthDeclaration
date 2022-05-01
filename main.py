import time
from selenium import webdriver
from settings import (StudentID,Password,Email,Phone)
from selenium.webdriver.common.by import By #看起來更酷的選擇器
from selenium.webdriver.common.keys import Keys #用來發送一些酷酷的東西
from selenium.webdriver.support.ui import WebDriverWait #我們太快了，要等一下其他人的腳步
from selenium.webdriver.support import expected_conditions as EC #例外出現時的救星

'''
設定區域
'''
from webdriver_manager.firefox import GeckoDriverManager #現在不用再挑版本安裝了，讚吧？
from selenium.webdriver.firefox.service import Service #瀏覽器不同這邊還是要改 :P
browser = webdriver.Firefox(service=Service(GeckoDriverManager().install())) #參見 https://github.com/SergeyPirogov/webdriver_manager
codeVer = 'v.1.3.14'
#個人資料
StudentID = "學號"
Password = "密碼"
Email = "電郵"
Phone = "電話"


#def login():
browser.set_page_load_timeout(100)
browser.get("https://pacific.asia.edu.tw/HealthDeclaration#/Login")
browser.find_element(By.ID, "username").send_keys(StudentID) #id.send_keys(passkey[0])
browser.find_element(By.ID, "password").send_keys(Password) #password.send_keys(passkey[1])
browser.find_element(By.ID, "password").send_keys(Keys.ENTER) #password.submit() 
print("登入成功！")

wait = WebDriverWait(browser, 10)
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-outline-primary"))).click() #WebDriverWait(browser, 20)
#---#
browser.get("https://pacific.asia.edu.tw/HealthDeclaration#/") #回到表單
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "text-secondary"))).text #獲取版本
ver = browser.find_element(By.CLASS_NAME, "text-secondary").text

if ver == codeVer:
    print("版本檢查：正確")
else:
    print("版本檢查：不符，可能會產生意外的狀況。建議更新版本")

try:
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ml-3.btn-info")))
    print("你已經填寫過表格了！",browser.find_element(By.CLASS_NAME, "text-right.text-success").text)
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

print("所有工作皆已完成，瀏覽器將於5秒後關閉")
time.sleep(5)
browser.quit()
