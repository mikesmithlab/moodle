
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from time import sleep


"""
To run this code you need to install Chrome Web Driver.
https://chromedriver.chromium.org/downloads

Go to old discussion forum and export via settings cog to .json format.
Set path and filename to file
Set web address to new discussion page.

Run code, log into Moodle and then let it run. Some steps are a bit 
slow so be patient.
Code currently only copies Subject and message. For some reason the tags are missing
but it is pretty involved to add these. json does include replies etc so you could add these.
"""



discussion_file = 'discussion.json'
discussion_page = 'https://moodle.nottingham.ac.uk/mod/forum/view.php?id=6071639'


def add_post(driver,post):
    wait = WebDriverWait(driver, 10)
    add_topic_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-primary')))
    #Add topic button
    add_topic_button.click()
    wait = WebDriverWait(driver, 10)

    subject = driver.find_element(By.ID, 'id_subject')
    down_btn = driver.find_element(By.CLASS_NAME,'atto_collapse_button')
    subject.send_keys(post['subject'])
    down_btn.click()
    
    
    html_btn = driver.find_element(By.CLASS_NAME,'atto_html_button') 
    html_btn.click()

    btn = driver.find_element(By.CLASS_NAME,'atto_fullscreen_button')
    btn.send_keys(Keys.TAB)
    box = driver.switch_to.active_element
    box.send_keys(post['message'])

    submit = driver.find_element(By.ID,"id_submitbutton")
    submit.click()
    


with open(discussion_file) as f:
    discussion = json.loads(f.read())
    
driver = webdriver.Chrome()
driver.get(discussion_page)

for post in discussion[0]:
    add_post(driver, post)



