# FOR SELENIUM CONFIGURATION (.ENV FILE): (USE IT JUST LIKE THIS):
CHROME_ARGUMENTS=--test-type;--disable-gpu;--no-sandbox;--disable-infobars;--disable-extensions;--disable-automation;--log-level=3;
CHROME_EXPERIMENTAL_OPTION=excludeSwitches:[ignore-certificate-errors,enable-automation,enable-logging];useAutomationExtension:False;

FUNCTIONS:
Simple_Selenium.fbc()  -> FIND ELEMENT BY CLASS_NAME (Default: all=True -> all elements)
Simple_Selenium.fbcs() -> FIND ELEMENT BY CSS_SELECTOR (Default: all=False -> only one element - first)
Simple_Selenium.fbi()  -> FIND ELEMENT BY ID (Default: all=False -> only one element - first)
Simple_Selenium.fbl()  -> FIND ELEMENT BY LINK_TEXT (only one element)
Simple_Selenium.fbp()  -> FIND ELEMENT BY PARTIAL_LINK_TEXT (only one element)
Simple_Selenium.fbt()  -> FIND ELEMENT BY TAG_NAME (Default: all=True -> all elements)
Simple_Selenium.fbx()  -> FIND ELEMENT BY XPATH (only one element)



