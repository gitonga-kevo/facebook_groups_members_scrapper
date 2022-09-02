import logging
from pickle import FALSE
from tempfile import tempdir
import threading
from operator import index
import time
from xml.dom.minidom import Element
from xml.etree.ElementTree import Comment
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import random
from bs4 import BeautifulSoup
print('Enter group link:')
link = input()
print('Enter Data File Name:')
x = input()
filename = ""
if x == "":
    filename = "data.txt"
else:
    filename = x + ".txt"
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get(link)
# create action chain object
action = ActionChains(driver)
time.sleep(5)
def login():
    email = driver.find_element(By.ID, "email")
    password = driver.find_element(By.ID,"pass")
    email.send_keys("jameswngondu@outlook.com")
    password.send_keys("pass@321")
    password.submit()
login()
def get_data():
    time.sleep(5)
    element = driver.find_elements(By.XPATH, "//div[@class='om3e55n1 g4tp4svg bdao358l alzwoclg cqf1kptm jez8cy9q gvxzyvdx q6feio67 k0kqjr44']")
    div = element[0]
    return div.text
def number_of_members():
    time.sleep(10)
    soup = get_data()
    data = soup[11:len(soup)]
    offset =data.find("\n") + 11
    x = soup[11:offset].replace(" ", "")
    x = x.replace(",", "")
    return int(x)
def scroll():
    try:
        counter = 0
        number_of_scrolls = number_of_members()/10
        while counter< number_of_scrolls:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            counter = counter + 1
            time.sleep(5)
    finally:
       return get_data()
def sort_data():
    names, description = [],[]
    unsorted_data = scroll()
    offset = unsorted_data.find("This list includes people who've joined the group, as well as people who are previewing the group. Anyone who's been invited and approved can preview the content in the group.")
    if offset>0:
        unsorted_data = unsorted_data[offset+175:]
    unsorted_data = unsorted_data.replace("Add Friend","")#remove "add friend"  
    unsorted_data = unsorted_data.replace("New to the group","")#remove "add friend" 
    unsorted_data = unsorted_data.replace("This list includes people who've joined the group, as well as people who are previewing the group. Anyone who's been invited and approved can preview the content in the group.","")#remove "add friend"   
    rows=  unsorted_data.find("Joined")
    while rows > 0:
        temp_name = unsorted_data[:rows]
        names.append(temp_name)
        unsorted_data = unsorted_data[rows:]#remove the name from the data
        offset = unsorted_data.find("\n")#find the end of "joined" line
        unsorted_data = unsorted_data[offset:]#remove the "joined" following the names
        joined_position = unsorted_data.find("Joined")#search for the descriptions
        cut_len = 0#the number of characters to cut from "unsorted_data"
        if joined_position>=0:#if execution has not reached the end of the data
            soup = unsorted_data[:joined_position]#section holding the description
            offset = soup.find("\n")
            temp_description = []
            while offset>=0:
                temp_description.append(soup[:offset])
                soup = soup[offset+1:]
                offset = soup.find("\n")
            temp_description.pop(len(temp_description)-1)#we must remove the last element because it is the name of the next user
            temp_description_str = ""
            if temp_description == []:
                temp_description_str = "NULL"
            else:#If the "temp_description" is not empty, turn it into a string
                for x in temp_description:
                    if x == "": x = " "
                    temp_description_str = temp_description_str + x
                    cut_len = len(temp_description_str)
            description.append(temp_description_str)
        else:#will run when the data pool is done
            description.append("NULL")
        unsorted_data = unsorted_data[cut_len:]
        rows =  unsorted_data.find("Joined")
    return names,description
def write_data(list_names, filename = "data.txt"):
    # Python program to explain os.mkdir() method
    
    # importing os module
    import os
    
    # Directory
    directory = "Clients_DM_Lists"
    
    # Parent Directory path
    parent_dir = "facebook_scrapper"
    
    # Path
    path = os.path.join(os.getcwd(), directory)
    
    # Create the directory
    # 'GeeksForGeeks' in
    # '/home / User / Documents'
    if os.path.isdir(path) == False:
        os.mkdir(path)
    path = path + "/"+filename
    f = open(path, "at")
    for x in list_names:
        try:   
            x = x.replace("\n","")
            x = x + "\n"
            f.write(x)       
        except Exception as error:
            print(error)
    f.close()


names, description = sort_data()
write_data(names,filename)
