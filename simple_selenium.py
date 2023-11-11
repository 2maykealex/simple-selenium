#coding=utf-8
from sys import exc_info
from pathlib import Path
from os import path, walk
from decouple import config
from selenium import webdriver
from json import dump, dumps, load
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (NoSuchElementException,
                                        ElementNotVisibleException,
                                        ElementNotSelectableException)

class Simple_Selenium (object):

    def __init__(self, browser='chrome', personal_download_path= ''):
        '''DEFAULT BROWSER=CHROME AND headless=False'''
        self.Keys = Keys
        self.By = By
        self.driver = None
        self.browser = browser
        self.personal_download_path = personal_download_path
        self.download_path = path.expanduser('~') + '\\Downloads'
        self.chromedriver_path = path.expanduser('~') + '\\.wdm\\drivers\\chromedriver\\win32'
        self.check_webdriver()

    def select_options(self, element_name):
        '''GET OPTIONS FROM A SELECT ELEMENT'''
        return (Select(element_name)).options

    def go_to_url(self, url):
        self.driver.get(url)
        self.change_background_color()

    def switch_to_windows(self, window_number=-1):
        self.driver.switch_to.window(self.driver.window_handles[window_number])

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

    def change_background_color(self):
        try:
            if (config('BG_COLOR')):
                js_code = "document.body.style.backgroundColor = '{}';".format(config('BG_COLOR'))
                self.driver.execute_script(js_code)
        except:
            pass

    def check_webdriver(self):
        ''' - COMPARE WEBDRIVER AND BROWSER VERSIONS - DOWNLOAD THE LATEST WEBDRIVER IF IT DOESN'T MATCH
            - CHECK .ENV FILE THE BROWSER CONFIGURATIONS '''

        def set_download_folder():
            '''- THE DEFAULT DOWNLOAD FOLDER WILL ONLY BE CHANGED TO THE ROOT OF THE SCRIPT IF THE "DOWNLOAD_FOLDER" VARIABLE IS SET TO "TRUE".
               - THE DEFAULT DOWNLOAD FOLDER WILL ONLY BE CHANGED TO ANY OTHER LOCATION IF THE "CHANGE_DOWNLOAD_FOLDER" VARIABLE CONTAINS THE ADDRESS OF THE DESIRED NEW FOLDER.'''

            self.download_path = str('{}\\downloads'.format(path.dirname(path.abspath(__name__)))) #at the root of the project
            try:
                if (config('CHANGE_DOWNLOAD_FOLDER')): #path to the other folder configured in the .env file.
                    self.download_path = config('CHANGE_DOWNLOAD_FOLDER')
            except:
                pass

            if (self.personal_download_path):
                self.download_path = '{}\\{}'.format(self.download_path , self.personal_download_path)

            render_image = 0
            try:
                if (config('NOT_RENDER_IMAGE')):
                    render_image = 2
            except:
                pass

            Path(self.download_path).mkdir(parents=True, exist_ok=True)
            settings = {"recentDestinations": [{"id": "Save as PDF",
                                                "origin": "local",
                                                "account": ""}],
                        "selectedDestinationId": "Save as PDF", "version": 2}
            prefs = {"download.default_directory": "{}".format(self.download_path),
                    'printing.print_preview_sticky_settings.appState': dumps(settings),
                    'savefile.default_directory': "{}".format(self.download_path),
                    "enabled": False,
                    "name": "Chrome PDF Viewer",
                    "credentials_enable_service": False,
                    "profile.password_manager_enabled": False,
                    "profile.cookies": 2,
                    "profile.geolocation": 2,
                    "profile.managed_default_content_settings.images": render_image}
            return prefs

        if (self.browser == 'chrome'):
            chrome_arguments_env = config('CHROME_ARGUMENTS').split(';') #.env file
            chrome_experimental_option_env = config('CHROME_EXPERIMENTAL_OPTION').split(';') #.env file
            options = webdriver.ChromeOptions()

            try:
                if (config('HEADLESS')):
                    options.add_argument('--headless')
            except:
                pass

            for option in chrome_arguments_env:
                if (option == ''): continue
                options.add_argument(option)

            for option in chrome_experimental_option_env:
                if (option == ''): continue

                option = option.replace(' ', '')
                if ('{' in option):
                    value = {}
                    k = option.replace('}', '').split(':{')[0]
                    values = option.replace('}', '').split(':{')[-1].split(',')
                    for v in values:
                        parameters = v.split(':')
                        if (parameters[0].isnumeric()):
                            try:
                                parameters[0] = int(parameters[0])
                            except:
                                parameters[0] = float(parameters[0])

                        if ('True' in parameters[1] or 'False' in parameters[1]):
                            parameters[1] = True if parameters[1] == 'True' else False
                        else:
                            parameters[1] = '{}'.format(parameters[1])

                        value.update({parameters[0]: parameters[1]})

                else:
                    option = option.split(':')
                    k = option[0]
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

                    options.add_experimental_option(k, value)
            try:
                if (config('DOWNLOAD_FOLDER')):
                    options.add_experimental_option("prefs", set_download_folder())
            except:
                pass

            try:
                if (config('BROWSER_POSITION_X') and config('BROWSER_POSITION_Y')):
                    self.driver.set_window_position(config('BROWSER_POSITION_X'), config('BROWSER_POSITION_Y'))
            except:
                pass
            try:
                if (config('WIND_MAX')):
                    self.driver.maximize_window()
            except:
                pass
            try:
                if (config('WIND_MIN')):
                    self.driver.maximize_window()
            except:
                pass

            return self.initialize_chrome_driver(options)

    def initialize_chrome_driver(self, options):

        def remove_oldest_version():
            if (len(versions) >= 5):
                versions.pop()

        def check_versions():
            chrome_version = self.driver.capabilities['browserVersion']
            remove_oldest_version()
            data['chromedriver_versions_last_used'] = chrome_version
            if (chrome_version not in versions):
                versions.append(chrome_version)
                sorted_versions = sorted(versions, reverse=True)
                data['chromedriver_versions'] = sorted_versions
            with open(json_path, 'w') as file:
                dump(data, file, indent=2)

        versions = []
        script_dir = path.dirname(path.abspath(__file__))
        json_path = path.join(script_dir, 'chrome_driver_versions.json')

        if (not path.exists(json_path)): # if JSON file not exists
            data = {"chromedriver_versions": []}
            with open(json_path, 'w') as file:
                dump(data, file, indent=2)
        try:
            with open(json_path, 'r') as file: # open JSON
                data = load(file)

            versions = data['chromedriver_versions']
            last_used_version = None
            try:
                last_used_version = data['chromedriver_versions_last_used']
                if (last_used_version in versions):
                    versions.remove(last_used_version)
            except:
                pass
            versions = sorted(data['chromedriver_versions'], reverse=True)
            if (last_used_version):
                versions.insert(0, last_used_version)
        except:
            versions.append('')
            pass

        match_version = False
        for version in versions:
            try:
                if (not(version)): service = Service(ChromeDriverManager().install())
                service = Service(ChromeDriverManager(version=version).install())
                self.driver = webdriver.Chrome(service=service, options=options)
                match_version = True
                check_versions()
                break
            except Exception as err:
                exception_type, exception_object, exception_traceback = exc_info()
                line_number = exception_traceback.tb_lineno
                try:
                    _error_ = err.msg
                except:
                    try:
                        _error_ = '|'.join(err.args)
                    except:
                        _error_ = err
                # print('\n <<< HOUVE UM ERRO INESPERADO EM -> {} NA LINHA {} DO simple_selenium>>>'.format(_error_, line_number))

            if (versions.index(version) == (len(versions)-1)): # if is the last version in test
                if (not(match_version)):
                    nome_arquivo = 'chromedriver.exe'
                    for pasta_raiz, sub_pastas, arquivos in walk(self.chromedriver_path):
                        sub_pastas.reverse()
                        if nome_arquivo in arquivos:
                            try:
                                executable_path = path.join(pasta_raiz, nome_arquivo)
                                if path.exists(executable_path):
                                    service = Service(executable_path=executable_path)
                                else:
                                    executable_path=None
                                    cdm_service = ChromeDriverManager(version=version).install()
                                    service = Service(cdm_service, executable_path=executable_path)
                                self.driver = webdriver.Chrome(service=service, options=options)
                                match_version = True
                                break
                            except Exception as err:
                                exception_type, exception_object, exception_traceback = exc_info()
                                line_number = exception_traceback.tb_lineno
                                print('\n <<< HOUVE UM ERRO INESPERADO EM -> {} NA LINHA {} DO simple_selenium>>>'.format(_error_, line_number))

        if (not(match_version)):
            print('NÃO FOI ENCONTRADA UMA VERSÃO VÁLIDA')
            return False

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