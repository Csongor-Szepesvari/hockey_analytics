from selenium import webdriver
from selenium.webdriver.chrome.service import Service

path = r"C:\Users\csong\Documents\Coding\Blogging\hockey_analytics\chromedriver.exe"

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

driver.get("http://www.hockey-reference.com/")

driver.quit()
