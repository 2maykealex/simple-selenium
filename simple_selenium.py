#coding=utf-8
from os import path
from sys import exc_info
from pathlib import Path
from decouple import config
from json import dump, dumps, load
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
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
        self.download_path = path.expanduser('~') + '\\Downloads'
        self.check_webdriver()

    def check_webdriver(self):
        ''' - COMPARE WEBDRIVER AND BROWSER VERSIONS - DOWNLOAD THE LATEST WEBDRIVER IF IT DOESN'T MATCH
            - CHECK .ENV FILE THE BROWSER CONFIGURATIONS '''

        def remove_oldest_version(versions_list):
            if len(versions_list) >= 5:
                versions_list.pop()

        def check_versions(json_path):
            chrome_version = self.driver.capabilities['browserVersion']
            remove_oldest_version(versions)
            if chrome_version not in versions:
                versions.append(chrome_version)
                sorted_versions = sorted(versions, reverse=True)
                data['chromedriver_versions'] = sorted_versions
                # Salva o arquivo atualizado
                with open(json_path, 'w') as file:
                    dump(data, file, indent=2)  # O indent=2 é opcional e formata o arquivo JSON de forma mais legível

        def set_download_folder():
            '''- THE DEFAULT DOWNLOAD FOLDER WILL ONLY BE CHANGED TO THE ROOT OF THE SCRIPT IF THE "DOWNLOAD_FOLDER" VARIABLE IS SET TO "TRUE".
               - THE DEFAULT DOWNLOAD FOLDER WILL ONLY BE CHANGED TO ANY OTHER LOCATION IF THE "CHANGE_DOWNLOAD_FOLDER" VARIABLE CONTAINS THE ADDRESS OF THE DESIRED NEW FOLDER.'''

            self.download_path = str('{}\\DOWNLOADS'.format(path.dirname(path.realpath(__file__)))) #at the root of the project
            try:
                if (config('CHANGE_DOWNLOAD_FOLDER')): #path to the other folder configured in the .env file.
                    self.download_path = config('CHANGE_DOWNLOAD_FOLDER')
            except:
                pass

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
                        parametros = v.split(':')
                        if (parametros[0].isnumeric()):
                            try:
                                parametros[0] = int(parametros[0])
                            except:
                                parametros[0] = float(parametros[0])

                        if ('True' in parametros[1] or 'False' in parametros[1]):
                            parametros[1] = True if (parametros[1] == 'True') else False
                        else:
                            parametros[1] = '{}'.format(parametros[1])

                        value.update({parametros[0]: parametros[1]})

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

            versions = []
            script_dir = path.dirname(path.abspath(__file__))
            json_path = path.join(script_dir, 'chrome_driver_versions.json')
            try:
                with open(json_path, 'r') as file: # Abre o arquivo JSON
                    data = load(file)
                versions = sorted(data['chromedriver_versions'], reverse=True)
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
                    check_versions(json_path)
                    break
                except Exception as err:
                    exception_type, exception_object, exception_traceback = exc_info()
                    line_number = exception_traceback.tb_lineno
                    print('\n <<< HOUVE UM ERRO INESPERADO EM -> {} NA LINHA {} DO simple_selenium>>>'.format(err, line_number))

            if (not(match_version)):
                print('NÃO FOI ENCONTRADA UMA VERSÃO VÁLIDA')
                return False

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

    def change_background_color(self):
        try:
            if (config('BG_COLOR')):
                js_code = "document.body.style.backgroundColor = '{}';".format(config('BG_COLOR'))
                self.driver.execute_script(js_code)
        except:
            pass

    def go_to_url(self, url):
        self.driver.get(url)
        self.change_background_color()