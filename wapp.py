from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import zmq
import tqdm
import warnings
warnings.filterwarnings('ignore')
import logging

from functions import procesar_mensaje2

logging.basicConfig(filename='log.txt', level=logging.DEBUG)

options=Options()

# quita la bandera de ser robot
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--remote-allow-origins=*");
options.add_argument(r"user-data-dir=C:\Users\elmat\anaconda3\envs\final\Lib\site-packages\selenium")
options.add_experimental_option("detach", True)    #Esta opción corrige el error de cierre repentino

context = zmq.Context()
socket_rec = context.socket(zmq.SUB)
socket_rec.connect("tcp://127.0.0.1:7777")
socket_rec.setsockopt_string(zmq.SUBSCRIBE, "");

while True:

    try:
        message = socket_rec.recv_string()
        mode, text, name = procesar_mensaje2(message)

        if mode != 'whatsapp':
            continue

        print(f"Modo: {mode}")
        print(f"Texto: {text}")
        print(f"Nombre: {name}")

        PATH = ChromeDriverManager().install()
        driver=webdriver.Chrome(PATH, options=options)
        driver.get('https://web.whatsapp.com/')

        wait = WebDriverWait(driver, 30)  # Wait for up to 10 seconds

        busca = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]/p')))
        busca.click()
        busca.click()
        busca.send_keys(name)

        busca.click()
        busca.send_keys('')
        time.sleep(1)
        busca.send_keys(Keys.TAB, Keys.TAB)
        time.sleep(0.5)
        busca.send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB)

        txt = driver.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
        txt.send_keys(text)
        time.sleep(1)

        ent = driver.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button')
        ent.click()
        time.sleep(1.5)

        driver.quit() 

        continue

    except Exception as e:
        logging.error(f"Ocurrió un error: {e}")
        time.sleep(1)
        continue
    












