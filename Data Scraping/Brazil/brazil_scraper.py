# Install selenium: https://selenium-python.readthedocs.io/installation.html#introduction

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time


data_website = 'https://datasus.saude.gov.br/acesso-a-informacao/doencas-e-agravos-de-notificacao-de-2007-em-diante-sinan/'

dengue_2014_site = 'http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sinannet/cnv/denguebbr.def'

driver = webdriver.Chrome()
driver.get(dengue_2014_site)

#Set settings
line = driver.find_element(By.ID, "L")
column = driver.find_element(By.ID, "C")
years = driver.find_element(By.ID, "A")

# check format to be in Colunas separadas por ";"
line = driver.find_element(By.ID, "F").click()

#Show data
driver.find_element(By.CLASS_NAME, "mostra").click()

time.sleep(10)

driver.close()
