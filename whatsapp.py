﻿# SWAMI KARUPPASWAMI THUNNAI

# ============================================================
# Simple yet Hackable! WhatsApp API [UNOFFICIAL] for Python3
# Note: The author gives permission to use it under Apache 2.0
# Special Thanks To: alecxe, For reviewing my code!
# ============================================================

import time
import datetime as dt
import json
import os
import requests
import shutil
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlencode
#import pyautogui

#pyautogui.PAUSE = 1


class WhatsApp:
    """
    This class is used to interact with your whatsapp [UNOFFICIAL API]
    """
    emoji = {}  # This dict will contain all emojies needed for chatting
    browser = webdriver.Chrome()  # we are using chrome as our webbrowser
    timeout = 10  # The timeout is set for about ten seconds

    # This constructor will load all the emojies present in the json file and it will initialize the webdriver
    def __init__(self, wait, screenshot=None):
        self.browser.get("https://web.whatsapp.com/")
        # emoji.json is a json file which contains all the emojis
        with open("emoji.json") as emojies:
            self.emoji = json.load(emojies)  # This will load the emojies present in the json file into the dict
        WebDriverWait(self.browser,wait).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.jN-F5')))
        if screenshot is not None:
            self.browser.save_screenshot(screenshot)  # This will save the screenshot to the specified file location

    # This method is used to send the message to the individual person or a group
    # will return true if the message has been sent, false else
    def send_message(self, name, message):
        message = self.emojify(message)  # this will emojify all the emoji which is present as the text in string
        search = self.browser.find_element_by_css_selector(".jN-F5")
        search.send_keys(name+Keys.ENTER)  # we will send the name to the input key box
        current_time = time.time()
        try:
            send_msg = WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]")))
            send_msg.send_keys(message+Keys.ENTER)  # send the message
            return True
        except TimeoutException:
            raise TimeoutError("Your request has been timed out! Try overriding timeout!")
        except NoSuchElementException:
            return False
        except Exception:
            return False

    # This method will count the no of participants for the group name provided
    def participants_for_group(self, group_name):
        search = self.browser.find_element_by_css_selector(".jN-F5")
        search.send_keys(group_name+Keys.ENTER)  # we will send the name to the input key box
        # some say this two try catch below can be grouped into one
        # but I have some version specific issues with chrome [Other element would receive a click]
        # in older versions. So I have handled it spereately since it clicks and throws the exception
        # it is handled safely
        try:
            click_menu = WebDriverWait(self.browser,self.timeout).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div/div/div[3]/div/header/div[2]/div[1]/div/span")))
            click_menu.click()
        except TimeoutException:
            raise TimeoutError("Your request has been timed out! Try overriding timeout!")
        except NoSuchElementException as e:
            return "None"
        except Exception as e:
            return "None"
        current_time = dt.datetime.now()
        participants_xpath = "/html/body/div/div/div/div[1]/div[3]/span/div/span/div/div/div/div[4]/div[1]/div/div/div/span"
        while True:
            try:
                participants_count = self.browser.find_element_by_xpath(participants_xpath).text
                if "participants" in participants_count:
                    return participants_count
            except Exception as e:
                pass
            new_time = dt.datetime.now()
            elapsed_time = (new_time - current_time).seconds
            if elapsed_time > self.timeout:
                return "NONE"

    # This method is used to get the main page
    def goto_main(self):
        self.browser.get("https://web.whatsapp.com/")

    # get the status message of a person
    # TimeOut is approximately set to 10 seconds
    def get_status(self, name):
        search = self.browser.find_element_by_css_selector(".jN-F5")
        search.send_keys(name+Keys.ENTER)  # we will send the name to the input key box
        try:
            group_xpath = "/html/body/div/div/div/div[3]/header/div[1]/div/span/img"
            click_menu = WebDriverWait(self.browser,self.timeout).until(EC.presence_of_element_located(
                (By.XPATH, group_xpath)))
            click_menu.click()
        except TimeoutException:
            raise TimeoutError("Your request has been timed out! Try overriding timeout!")
        except NoSuchElementException:
            return "None"
        except Exception:
            return "None"
        try:
            status_css_selector = ".drawer-section-body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > span:nth-child(1)"   # This is the css selector for status
            WebDriverWait(self.browser,self.timeout).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, status_css_selector)))
            status = self.browser.find_element_by_css_selector(status_css_selector).text
            # We will try for 100 times to get the status
            for i in range(10):
                if len(status) > 0:
                    return status
                else:
                    time.sleep(1) # we need some delay
            return "None"
        except TimeoutException:
            raise TimeoutError("Your request has been timed out! Try overriding timeout!")
        except NoSuchElementException:
            return "None"
        except Exception:
            return "None"

    # to get the last seen of the person
    def get_last_seen(self, name, timeout=10):
        search = self.browser.find_element_by_css_selector(".jN-F5")
        search.send_keys(name+Keys.ENTER)  # we will send the name to the input key box
        last_seen_css_selector = ".O90ur"
        start_time = dt.datetime.now()
        try:
            WebDriverWait(self.browser,self.timeout).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, last_seen_css_selector)))
            while True:
                last_seen = self.browser.find_element_by_css_selector(last_seen_css_selector).text
                if last_seen and "click here" not in last_seen:
                    return last_seen
                end_time = dt.datetime.now()
                elapsed_time = (end_time-start_time).seconds
                if elapsed_time > 10:
                    return "None"
        except TimeoutException:
            raise TimeoutError("Your request has been timed out! Try overriding timeout!")
        except NoSuchElementException:
            return "None"
        except Exception:
            return "None"

    # This method does not care about anything, it sends message to the currently active chat
    # you can use this method to recursively send the messages to the same person
    def send_blind_message(self, message):
        try:
            message = self.emojify(message)
            send_msg = WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]")))
            send_msg.send_keys(message+Keys.ENTER)  # send the message
            return True
        except NoSuchElementException:
            return "Unable to Locate the element"
        except Exception as e:
            print(e)
            return False

    # This method will send you the picture
    # This is a windows specific function, somebody PR for Mac and Linux
    def send_picture(self, name, picture_location, caption=None):
        search = self.browser.find_element_by_css_selector(".jN-F5")
        search.send_keys(name+Keys.ENTER)  # we will send the name to the input key box
        try:
            self.browser.find_element_by_xpath("/html/body/div/div/div/div[3]/div/header/div[3]/div/div[2]/div/span").click()
        except NoSuchElementException:
            return "Unable to Locate the element"
        pyautogui.press("down")
        pyautogui.press("enter")
        pyautogui.typewrite(picture_location)
        pyautogui.press("enter")
        try:
            if caption is not None:
                message = self.browser.find_element_by_xpath("/html/body/div/div/div/div[1]/div[2]/span/div/span/div/div/div[2]/div/span/div/div[2]/div/div[3]/div[1]/div[2]")
                message.send_keys(caption)
            self.browser.find_element_by_xpath("/html/body/div/div/div/div[1]/div[2]/span/div/span/div/div/div[2]/span[2]/div/div/span").click()
        except NoSuchElementException:
            return "Cannot Send the picture"


    # override the timeout
    def override_timeout(self, new_timeout):
        self.timeout = new_timeout

    # This method is used to emojify all the text emoji's present in the message
    def emojify(self,message):
        for emoji in self.emoji:
            message = message.replace(emoji,self.emoji[emoji])
        return message

    def get_profile_pic(self, name):
        search = self.browser.find_element_by_css_selector(".jN-F5")
        search.send_keys(name+Keys.ENTER)
        try:
            open_profile = WebDriverWait(self.browser,self.timeout).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div/div/div[3]/div/header/div[1]/div/img")))
            open_profile.click()
        except:
            print("nothing found")
        try:
            open_pic =  WebDriverWait(self.browser,self.timeout).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div/div/div[1]/div[3]/span/div/span/div/div/div/div[1]/div[1]/div/img")))
            open_pic.click()
        except:
            print("Nothing found")
        try:
            img = WebDriverWait(self.browser,self.timeout).until(EC.presence_of_element_located(
                    (By.XPATH,'//*[@id="app"]/div/span[2]/div/div/div[2]/div/div/div/div/img')))
        except:
            print("Couldn't find the URL to the image")
        img_src_url = img.get_attribute('src')
        self.browser.get(img_src_url)
        self.browser.save_screenshot(name+"_img.png")

    def create_group(self, group_name, members):
        more = self.browser.find_element_by_css_selector("#side > header > div._20NlL > div > span > div:nth-child(3) > div > span")
        more.click()
        chains = ActionChains(self.browser)
        chains.send_keys(Keys.ARROW_DOWN+Keys.ENTER)
        chains.perform()
        for member in members:
            contact_name = self.browser.find_element_by_css_selector("._16RnB")
            contact_name.send_keys(member+Keys.ENTER)
        time.sleep(3) # little delay to make the process robust
        next_step = self.browser.find_element_by_css_selector("._3hV1n > span:nth-child(1)")
        next_step.click()
        group_text = self.browser.find_element_by_css_selector(".bsmJe > div:nth-child(2)")
        group_text.send_keys(group_name+Keys.ENTER)

    # This method is used to get an invite link for a particular group
    def get_invite_link_for_group(self, groupname):
        search = self.browser.find_element_by_css_selector(".jN-F5")
        search.send_keys(groupname+Keys.ENTER)
        self.browser.find_element_by_css_selector("._2zCDG > span:nth-child(1)").click()
        try:
            time.sleep(3)
            WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#app > div > div > div.MZIyP > div._3q4NP._2yeJ5 > span > div > span > div > div > div > div:nth-child(5) > div:nth-child(3) > div._3j7s9 > div > div")))
            invite_link = self.browser.find_element_by_css_selector("#app > div > div > div.MZIyP > div._3q4NP._2yeJ5 > span > div > span > div > div > div > div:nth-child(5) > div:nth-child(3) > div._3j7s9 > div > div")
            invite_link.click()
            WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located(
                    (By.ID, "group-invite-link-anchor")))
            link = self.browser.find_element_by_id("group-invite-link-anchor")
            return link.text
        except:
            print("Cannot get the link")

    # This method is used to exit a group
    def exit_group(self, group_name):
        search = self.browser.find_element_by_css_selector(".jN-F5")
        search.send_keys(group_name+Keys.ENTER)
        self.browser.find_element_by_css_selector("._2zCDG > span:nth-child(1)").click()
        WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div._1CRb5:nth-child(6) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(1)")))
        time.sleep(3)
        _exit = self.browser.find_element_by_css_selector("div._1CRb5:nth-child(6) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(1)")
        _exit.click()
        WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div._1WZqU:nth-child(2)")))
        confirm_exit = self.browser.find_element_by_css_selector("div._1WZqU:nth-child(2)")
        confirm_exit.click()
        
    # Send Anonymous message
    def send_anon_message(self, phone, text):
        payload = urlencode({"phone": phone, "text": text, "source": "", "data": ""})
        self.browser.get("https://api.whatsapp.com/send?"+payload)
        WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#action-button")))
        send_message = self.browser.find_element_by_css_selector("#action-button")
        send_message.click()
        confirm = WebDriverWait(self.browser, self.timeout+5).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]")))
        confirm.clear()
        confirm.send_keys(text+Keys.ENTER)        

    # This method is used to quit the browser
    def quit(self):
        self.browser.quit()
