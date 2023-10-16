# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 08:16:09 2022

@author: Amir
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from waiting import wait


fp = webdriver.FirefoxProfile('./profile')
driver = webdriver.Firefox(firefox_profile=fp)


# driver = webdriver.Chrome('./chromedriver.exe'  )   
driver.get("https://web.telegram.org/")

print(driver.title)


def go_to_channel(chanel_name):
    
    # if(is_channel_right(chanel_name)):
    #     return True
    
    try:
        ########
        a1 = driver.find_elements(By.CSS_SELECTOR, "div.ListItem.Chat.chat-item-clickable.no-selection.has-ripple")
        a2 = driver.find_elements(By.CSS_SELECTOR, "a.chatlist-chat.rp")
        if(len(a1) > len(a2)):
            a = a1
            inside_selector = 'div.title h3'
            down_page = "button.Button.src-components-middle-ScrollDownButton-module__button.default.secondary.round i"
        else:
            a = a2
            inside_selector = 'span.user-title.tgico span.peer-title'
            down_page = "button.btn-circle.btn-corner.z-depth-1.bubbles-corner-button.bubbles-go-down.tgico-arrow_down.rp"

        my_channel = ''
        for i in a:
            tmp = i.find_element(By.CSS_SELECTOR, inside_selector)
            if(tmp.text == chanel_name):
                my_channel = i
        
        if(my_channel != ''):
            my_channel.click()
            sleep(0.5)

            try:
                down_page1  = driver.find_element(By.CSS_SELECTOR, down_page)
                down_page1.click()
            except :
                pass
            sleep(0.5)
            return True
        else:
            return False
    
    except :
        return False
    
    
def get_last_massage():
    try:
        mass1  = driver.find_elements(By.CSS_SELECTOR, "p.text-content.with-meta")
        mass2  = driver.find_elements(By.CSS_SELECTOR, "div.bubbles-group div.message")
        if(len(mass1) > len(mass2)):
            mass = mass1
        else:
            mass = mass2
        
        return mass[-1].text
    except :
        return False


def is_channel_right(chanel_name):
    selected_channel1 = driver.find_elements(By.CSS_SELECTOR, "div.MiddleHeader div.ChatInfo div.info div.title h3")
    selected_channel2 = driver.find_elements(By.CSS_SELECTOR, "div.chat-info-container div.user-title  span.peer-title")
    if(len(selected_channel1) > len(selected_channel2)):
        selected_channel = selected_channel1
    else:
        selected_channel = selected_channel2

    try:
        if((selected_channel[-1].text == chanel_name)):
            return True
        else:
            return False
    except :
        return False
        

def is_new_massage(chanel_name):
    global last_massage
    
    if(not is_channel_right(chanel_name)):
        while not go_to_channel(chanel_name):
            print("###########  ERROR : Unable to find channel  ###########")
            print("################  Channel not selected  ################")
            
    
    
    mass  = get_last_massage()
    if(last_massage != mass):
        
        last_massage = mass
        return True;
    else:
        return False
    


def waiting_function(chanel_name):
    
    while (not go_to_channel(chanel_name)):
        print("waiting until login")
        sleep(10)
        
        
    while (True):
        wait(lambda: is_new_massage(chanel_name), timeout_seconds=60, waiting_for="something to be ready")
        print('**************\n'+ last_massage +'\n**************' )
       

if __name__ == '__main__':
    
    chanel_name = 'Testchannel'
    last_massage = get_last_massage()
    waiting_function(chanel_name)










