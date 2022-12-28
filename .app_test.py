from simple_selenium import Simple_Selenium
ss = Simple_Selenium()
ss.driver.get('https://www.google.com')

#TEST 1
# search_input = ss.fbc('gLFyf', all=False)
# search_input.send_keys('GOOGLE')

#TEST 2
search_input = ss.wait4element('gLFyf', 'class')
if search_input:
    search_input.send_keys('GOOGLE')
    search_input = ss.wait4element('sbct', 'class')
    if search_input:
        print(search_input.text)

print('\nfinished')