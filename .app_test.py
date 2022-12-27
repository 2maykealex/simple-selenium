from simple_selenium import Simple_Selenium
ss = Simple_Selenium()
ss.driver.get('https://www.google.com')
search_input = ss.fbt('input', False)
search_input.send_keys('GOOGLE')
print('\nfinished')