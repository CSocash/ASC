import time
import lxml.html
import lxml.html.clean
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_experimental_option("detach", True)
js_code = "arguments[0].scrollIntoView();"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.ascendanalytics.com/")
driver.maximize_window()

# find the 'Store' link at the top and click it
links = driver.find_elements("xpath", "//nav/a[text()[contains(., 'Store')]]")
print("We are now going to print all the links on the main page")
print(links)
print("Click the 'Store' link")
links[0].click()


# find the buttons on the 'Store' page (those with anchor tags that contain the attribute 'href') and
# for each one print out its inner HTML
print("find all the buttons with an anchor tag")
buttons = driver.find_elements("xpath", "//a[@href][contains(@class,'button')]")
print("print each button's innnerHTML")
for button in buttons:
	print(button.get_attribute("innerHTML"))

time.sleep(5)

# find the 'Market Reports' button and click it
mrButtons = driver.find_elements("xpath", "//a[text()[contains(.,'Market Reports')]]")
mrButtons[0].click()

time.sleep(3)

# on the Market Reports page to follow, grab the price of the following reports:
# CAISO Market Report Release 4.1, ERCOT Market Report Release 4.1b

ercotPrice = driver.find_element("xpath", "//div/h3[text()[contains(.,'ERCOT')]]/following-sibling::h5[text()[contains(., '$')]]")
#print(ercotPrice.get_attribute("innerHTML"))

ercotPriceText = ercotPrice.get_attribute("innerHTML")
print(ercotPriceText)

# the inner html has some characters we don't want (&nbsp;), so let's clean that up with a cleaner
# before and after: $&nbsp;15,000.00&nbsp;USD   $ 15,000.00 USD
doc = lxml.html.fromstring(ercotPriceText)
cleaner = lxml.html.clean.Cleaner(style=True)
doc = cleaner.clean_html(doc)
text = doc.text_content().replace('$','').replace('USD', '')
print(text)


pjmPrice = driver.find_element("xpath", "//div/h3[text()[contains(.,'PJM')]]/following-sibling::h5[text()[contains(., '$')]]")
#print(ercotPrice.get_attribute("innerHTML"))

pjmPriceText = pjmPrice.get_attribute("innerHTML")
print(pjmPriceText)

# the inner html has some characters we don't want (&nbsp;), so let's clean that up with a cleaner
# before and after: $&nbsp;15,000.00&nbsp;USD   $ 15,000.00 USD
doc = lxml.html.fromstring(pjmPriceText)
cleaner = lxml.html.clean.Cleaner(style=True)
doc = cleaner.clean_html(doc)
text = doc.text_content().replace('$','').replace('USD', '')
print(text)

