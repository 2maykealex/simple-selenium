#coding=utf-8
from decouple import config
from selenium import webdriver
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






