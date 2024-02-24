# Install selenium: https://selenium-python.readthedocs.io/installation.html#introduction

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

def extract_from_disease_site(url: str):
    driver = webdriver.Chrome()
    driver.get(url)

    wait = WebDriverWait(driver, 10) # Set up wait for later

    #Window switching
    original_window = driver.current_window_handle

    #Set settings
    line = Select(driver.find_element(By.ID, "L"))
    column = Select(driver.find_element(By.ID, "C"))
    years = Select(driver.find_element(By.ID, "A"))

    #Set settings properly
    line.select_by_value("Município_de_residência")
    column.select_by_value("Semana_epidem._1º_Sintomas(s)")

    # check format to be in Colunas separadas por ";"
    line = driver.find_element(By.XPATH, "//input[@value='prn']").click()

    years_done = []

    #select each year
    for i in range(len(years.options)):
        years.select_by_index(i)   
        current_year = years.options[i].text
        years_done.append(current_year)

        #Show data
        driver.find_element(By.CLASS_NAME, "mostra").click()

        #Wait for new tab to open
        wait.until(EC.number_of_windows_to_be(2))

        #Open new tab
        for window_handle in driver.window_handles:
                if window_handle != original_window:
                    driver.switch_to.window(window_handle)
                    break

        #Extract text data  
        print("year:",current_year)
        data = driver.find_element(By.TAG_NAME, "pre").text
        #print(data)

        #switch to first tab
        driver.close()
        driver.switch_to.window(original_window)

    print(years_done)
    
    time.sleep(10)

    driver.close()



if __name__ == '__main__':
    data_website = 'https://datasus.saude.gov.br/acesso-a-informacao/doencas-e-agravos-de-notificacao-de-2007-em-diante-sinan/'

    dengue_2014_site = 'http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sinannet/cnv/denguebbr.def'

    extract_from_disease_site(dengue_2014_site)