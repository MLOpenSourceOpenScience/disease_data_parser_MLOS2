# Install selenium: https://selenium-python.readthedocs.io/installation.html#introduction

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import sys
import os

def extract_from_disease_site(disease_name: str, url: str, outfile_name: str, output_folder: str):

    out_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), output_folder)
    if not os.path.exists(out_dir): # If there is no directory, make it
        os.makedirs(out_dir)
    
    
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
    #in column values, first try weekly data then monthly
    column_values = ["Semana_epidem._1º_Sintomas(s)", "Mês_1º_Sintoma(s)", "Mes_da_Notific", "Mês_acidente_", "Mês_Diag/sintomas", "Mês_Diagnóstico","Mês_notificação","Mês_da_Notific","Mês_Notificação","Mes_Notificação","Mês_de_Diagnóstico"]
    for value in column_values:
        try:
            column.select_by_value(value)
        except: #if you can't find weekly data, get monthly
            pass

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

        #Save data
        output_file = os.path.join(out_dir, f'{outfile_name}{current_year}.txt')
        with open(output_file, 'a', encoding= 'utf-8') as output:
            output.write(current_year)
            output.write('\n')
            output.write(url)
            output.write('\n')
            output.write(disease_name)
            output.write('\n')
            output.write(data)

        #switch to first tab
        driver.close()
        driver.switch_to.window(original_window)

    print("Years Done:",years_done)
    
    driver.close()



if __name__ == '__main__':
    data_website = 'https://datasus.saude.gov.br/acesso-a-informacao/doencas-e-agravos-de-notificacao-de-2007-em-diante-sinan/'

    dengue_2014_site = 'http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sinannet/cnv/denguebbr.def'
    dengue_pre_2014 = 'http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sinannet/cnv/denguebr.def'

    n = len(sys.argv)

    if n != 5:
        print("Invalid number of arguments! Correct usage: brazil_scraper.py <disease-name> <data-url> <outfile-name> <output-folder>")
        quit()

    disease_name = sys.argv[1]
    data_url = sys.argv[2]
    outfile_name = sys.argv[3]
    output_folder = sys.argv[4]   

    extract_from_disease_site(disease_name, data_url, outfile_name, output_folder)