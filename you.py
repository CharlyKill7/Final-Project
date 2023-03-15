from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
#import logging
import zmq
import warnings
warnings.filterwarnings('ignore')

# Se comenta esto para que no guarde log, porque suele haberlos y es pesado. Activar en caso de necesidad
#logging.basicConfig(filename='log_youtube.txt', level=logging.DEBUG)

options=Options()

options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--remote-allow-origins=*");
options.add_argument(r"user-data-dir=C:\Users\elmat\anaconda3\envs\luna\Lib\site-packages\selenium2\cookies")
#options.add_argument('--headless')                 #Habilitar si no queremos ver la ventana
options.add_experimental_option("detach", True)    #Esta opción corrige el error de cierre repentino
options.add_argument('--start-minimized')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_extension('driver/adblock.crx') 
#options.add_argument('--disable-extensions')
options.add_argument('--disable-infobars')

context = zmq.Context()
socket_rec = context.socket(zmq.SUB)
socket_rec.connect("tcp://127.0.0.1:7777")
socket_rec.setsockopt_string(zmq.SUBSCRIBE, "");

PATH = ChromeDriverManager().install() 

print('Youtube Ready')

# Variable global para mantener el estado del navegador
driver2 = None

while True:

    try:
        mensa = socket_rec.recv_string(flags=zmq.NOBLOCK)

        if mensa.split()[0].lower() != 'youtube':
            continue

        if driver2 is None:
            # Si no hay una sesión de Selenium abierta
            service2 = Service(PATH)
            driver2 = webdriver.Chrome(service=service2, options=options)
            driver2.get('https://www.google.com/')

        elif driver2 is not None:
            driver2.quit()
            service2 = Service(PATH)
            driver2 = webdriver.Chrome(service=service2, options=options)
            driver2.get('https://www.google.com/')

        wait2 = WebDriverWait(driver2, 30)  

        buscador = wait2.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')))
        buscador.click()
        buscador.send_keys(mensa)
        buscador.send_keys(Keys.ENTER)

        time.sleep(0.4)

        buscar = driver2.find_element(By.XPATH,'//*[@id="tsf"]/div[1]/div[1]/div[2]/div/div[2]/input')
        buscar.click()
        buscar.send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, 
                        Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.ENTER)

    except Exception as e:
        #logging.error(f"Ocurrió un error: {e}")
        time.sleep(0.1)
        continue

