#coding=utf-8
from decouple import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException

class Simple_Selenium (object):

    def __init__(self, browser='chrome'):
        '''DEFAULT BROWSER=CHROME AND headless=False'''
        self.Keys = Keys
        self.driver = None
        self.browser = browser
        self.check_webdriver()

    def check_webdriver(self):
        ''' - COMPARE WEBDRIVER AND BROWSER VERSIONS - DOWNLOAD THE LATEST WEBDRIVER IF IT DOESN'T MATCH
            - CHECK .ENV FILE THE BROWSER CONFIGURATIONS '''

        if (self.browser == 'chrome'):
            chrome_arguments_env = config('CHROME_ARGUMENTS').split(';') #.env file
            chrome_experimental_option_env = config('CHROME_EXPERIMENTAL_OPTION').split(';') #.env file

            options = webdriver.ChromeOptions()

            if (config('HEADLESS')):
                options.add_argument('--headless')

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

    def select_options(self, element_name):
        '''GET OPTIONS FROM A SELECT ELEMENT'''
        return (Select(element_name)).options

    def fbc (self, class_name, all=True):
        '''FBC -> FIND ELEMENT BY CLASS_NAME (Default: all=True -> all elements)'''
        if (all):
            return self.driver.find_elements(By.CLASS_NAME, class_name)
        else:
            return self.driver.find_element(By.CLASS_NAME, class_name)

    def fbcs (self, css_selector, all=False):
        '''FBCS -> FIND ELEMENT BY CSS_SELECTOR (Default: all=False -> only one element - first)'''
        if (all):
            return self.driver.find_elements(By.CSS_SELECTOR, css_selector)
        else:
            return self.driver.find_element(By.CSS_SELECTOR, css_selector)

    def fbi (self, id, all=False):
        '''FBI -> FIND ELEMENT BY ID (Default: all=False -> only one element - first)'''
        if (all):
            return self.driver.find_elements(By.ID, id)
        else:
            return self.driver.find_element(By.ID, id)

    def fbl (self, link_text):
        '''FBL -> FIND ELEMENT BY LINK_TEXT (only one element)'''
        return self.driver.find_element(By.LINK_TEXT, link_text)

    def fbp (self, partial_link_text):
        '''FBP -> find element BY PARTIAL_LINK_TEXT (only one element)'''
        return self.driver.find_element(By.PARTIAL_LINK_TEXT, partial_link_text)

    def fbt (self, tag, all=True):
        '''FBT -> FIND ELEMENT BY TAG_NAME (Default: all=True -> all elements)'''
        if (all):
            return self.driver.find_elements(By.TAG_NAME, tag)
        else:
            return self.driver.find_element(By.TAG_NAME, tag)

    def fbx (self, xpath):
        '''FBX -> FIND ELEMENT BY XPATH (only one element)'''
        return self.driver.find_element(By.XPATH, xpath)

    def wait4element(self, element_name, type='xpath', action='click', poll=5, timeOut=20):
        '''FLUENTWAIT -> FUNCTION WORKS WITH TIMEOUT AND PRE-DEFINED ATTEMPTS
        - Default type=xpath
        - Default action='click'
        - RETURN ONLY ONE (FIRST) ELEMENT
        '''
        try:
            if not(element_name): return False

            if action == 'click':
                if type == 'xpath':
                    element = WebDriverWait(self.driver, timeOut, poll_frequency=poll, ignored_exceptions=[
                                        NoSuchElementException,
                                        ElementNotVisibleException,
                                        ElementNotSelectableException]).until(
                                        EC.element_to_be_clickable((By.XPATH, element_name)))

                elif type == 'id':
                    element = WebDriverWait(self.driver, timeOut, poll_frequency=poll, ignored_exceptions=[
                                        NoSuchElementException,
                                        ElementNotVisibleException,
                                        ElementNotSelectableException]).until(
                                        EC.element_to_be_clickable((By.ID, element_name)))

                elif type == 'class':
                    element = WebDriverWait(self.driver, timeOut, poll_frequency=poll, ignored_exceptions=[
                                        NoSuchElementException,
                                        ElementNotVisibleException,
                                        ElementNotSelectableException]).until(
                                        EC.element_to_be_clickable((By.CLASS_NAME, element_name)))

            elif action == 'show':
                if type == 'xpath':
                    element = WebDriverWait(self.driver, timeOut, poll_frequency=poll, ignored_exceptions=[
                                        NoSuchElementException,
                                        ElementNotVisibleException,
                                        ElementNotSelectableException]).until(
                                        EC.presence_of_element_located((By.XPATH, element_name)))

                elif type == 'id':
                    element = WebDriverWait(self.driver, timeOut, poll_frequency=poll, ignored_exceptions=[
                                        NoSuchElementException,
                                        ElementNotVisibleException,
                                        ElementNotSelectableException]).until(
                                        EC.presence_of_element_located((By.ID, element_name)))

                elif type == 'class':
                    element = WebDriverWait(self.driver, timeOut, poll_frequency=poll, ignored_exceptions=[
                                        NoSuchElementException,
                                        ElementNotVisibleException,
                                        ElementNotSelectableException]).until(
                                        EC.presence_of_element_located((By.CLASS_NAME, element_name)))

            return element

        except:
            return False