from selenium import webdriver
from getpass import getpass
from bs4 import BeautifulSoup
import requests
import time
import os
import glob
import shutil

username=input("Enter Your College Id")
password=input("Enter Your Password")
section = input("Enter Your Class Section")

print("DOWNLOADING......")

subjects=set()
temp=0
ext=['.pdf','.doc']

#making assignment folder
ass_path = os.path.join(os.getcwd(), 'assignments\\')
try:
    os.mkdir(ass_path)
    print("Making Assignment Folder")
except:
	print ("Assignment folder already exist updating assignments ....")

#driver setup
executable_path = os.getcwd()+"\\chromedriver.exe"
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : ass_path,"safebrowsing.enabled":False}
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(executable_path=executable_path,chrome_options=chromeOptions)

#opening portal
driver.get("http://52.220.116.248/")
driver.find_element_by_name('email').send_keys(username)#entering user name to portal
driver.find_element_by_id('password').send_keys(password)#entering password name to portal
driver.find_element_by_tag_name('button').click()
driver.find_element_by_xpath('//*[@id="sidebar-menu"]/ul/li[4]/a/span').click()#moving to assignment forlder

time.sleep(1)
table=driver.find_elements_by_tag_name('tr')
for i in table:
    #table heading left
    if temp==0:
        temp+=1
        continue

    # print(i.get_attribute('outerHTML'))
    soup = BeautifulSoup(i.get_attribute('outerHTML'), 'html.parser')
    table_data=soup.find_all('td')
    if table_data[7].text!=section:
        continue
    subjects.add(table_data[3].text)

    #making internal subjects directory
    subject_path = os.path.join(ass_path, table_data[3].text)
    try:
	    os.mkdir(subject_path)
    except:
	    pass
    
    i.find_element_by_tag_name('a').click()#download
    time.sleep(1)
    os.chdir(ass_path)
    for i in ext:
        temp_assignment=glob.glob('*'+i)
        if len(temp_assignment)==1:
            break
    source=ass_path+temp_assignment[0]
    destination=ass_path+table_data[3].text

    #if assignment already exist
    try:
	    shutil.move(source,destination)
    except:
        # print(source)
        os.remove(source)
        print ("Assignment are up to date......")
        break
	
print("Download completed... Now all assignments are up to date")
driver.close()