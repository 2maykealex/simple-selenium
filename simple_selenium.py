#coding=utf-8
from decouple import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

class Simple_Selenium (object):

    def __init__(self, browser='chrome'):
        self.Keys = Keys
        self.driver = None
        self.browser = browser
        self.check_webdriver()

    def check_webdriver(self):
        if (self.browser == 'chrome'):
            chrome_arguments_env = config('CHROME_ARGUMENTS').split(';') #.env file
            chrome_experimental_option_env = config('CHROME_EXPERIMENTAL_OPTION').split(';') #.env file

            options = webdriver.ChromeOptions()
            for option in chrome_arguments_env:
                if (option == ''): continue
                options.add_argument(option)

            for option in chrome_experimental_option_env:
                if (option == ''): continue
                option = option.split(':')
                if ('[' in option[-1]):
                    value = []
                    if (',' in option[-1]):
                        subOptions = option[-1].replace('[','').replace(']','').split(',')
                        for subOpt in subOptions:
                            value.append(subOpt)
                    else:
                        value.append(option[-1].replace('[','').replace(']',''))

                elif ('True' in option[-1]):
                    value = True

                elif ('False' in option[-1]):
                    value = False

                options.add_experimental_option(option[0], value)

            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)

    def select(self, element_name):
        return Select(element_name)

    def fbc (self, class_name, all=True): #find element BY CLASS_NAME
        if (all):
            return self.driver.find_elements(By.CLASS_NAME, class_name) #all
        else:
            return self.driver.find_element(By.CLASS_NAME, class_name) #only one (first)

    def fbcs (self, css_selector, all=False): #find element BY css_selector
        if (all):
            return self.driver.find_elements(By.CSS_SELECTOR, css_selector) #all
        else:
            return self.driver.find_element(By.CSS_SELECTOR, css_selector) #only one (first)

    def fbi (self, id, all=False): #find element BY ID
        if (all):
            return self.driver.find_elements(By.ID, id) #all
        else:
            return self.driver.find_element(By.ID, id) #only one

    def fbl (self, link_text): #find element BY LINK_TEXT
        return self.driver.find_element(By.LINK_TEXT, link_text) #only one

    def fbp (self, partial_link_text): #find element BY PARTIAL_LINK_TEXT
        return self.driver.find_element(By.PARTIAL_LINK_TEXT, partial_link_text) #only one

    def fbt (self, tag, all=True): #find element BY TAG_NAME
        if (all):
            return self.driver.find_elements(By.TAG_NAME, tag) #all
        else:
            return self.driver.find_element(By.TAG_NAME, tag) #only one (first)

    def fbx (self, xpath): #find element BY XPATH
        return self.driver.find_element(By.XPATH, xpath) #only one




