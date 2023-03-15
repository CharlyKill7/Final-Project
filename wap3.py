from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import zmq
from multiprocessing import Process
import logging
import warnings
warnings.filterwarnings('ignore')

from functions import procesar_mensaje2

logging.basicConfig(filename='log_wap.txt', level=logging.DEBUG)

options = Options()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--remote-allow-origins=*");
options.add_argument(r"user-data-dir=C:\Users\elmat\anaconda3\envs\final\Lib\site-packages\selenium")
#options.add_argument('--headless')                 #Habilitar si no queremos ver la ventana
options.add_experimental_option("detach", True)    #Esta opción corrige el error de cierre repentino
options.add_argument('--start-minimized')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--disable-extensions')
options.add_argument('--disable-infobars')
options.add_argument('--remote-debugging-port=9222')

def whatsapp_process():

    context = zmq.Context()
    socket_rec = context.socket(zmq.SUB)
    socket_rec.connect("tcp://127.0.0.1:7777")
    socket_rec.setsockopt_string(zmq.SUBSCRIBE, "");

    PATH = ChromeDriverManager().install() 

    print('Whatsapp Ready')

    while True:

        import os

        # verificar si el archivo de estado existe y crearlo si no existe
        if not os.path.isfile('estado.txt'):
            with open('estado.txt', 'w') as f:
                f.write('cerrada')

        # leer el estado actual del archivo
        with open('estado.txt', 'r') as f:
            estado = f.read().strip()

        # si la ventana está cerrada, abrir una nueva ventana
        if estado == 'cerrada':
            driver2 = webdriver.Chrome()
            with open('estado.txt', 'w') as f:
                f.write('abierta')
        # si la ventana está abierta, abrir una pestaña nueva
        else:
            driver2 = webdriver.Remote(command_executor="http://127.0.0.1:9517", desired_capabilities={"browserName":"chrome"})
            driver2.execute_script("window.open('');")

        try:
            message = socket_rec.recv_string(flags=zmq.NOBLOCK)
            mode, text, name = procesar_mensaje2(message)

            if mode != 'whatsapp':
                continue

            print(f"Modo: {mode}")
            print(f"Texto: {text}")
            print(f"Nombre: {name}")

            service = Service(PATH)
            driver2 = webdriver.Chrome(service=service, options=options)
            driver2.get('https://web.whatsapp.com/')

            wait = WebDriverWait(driver2, 30)  # Wait for up to 10 seconds

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

            txt = driver2.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
            txt.send_keys(text)
            time.sleep(1)

            ent = driver2.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button')
            ent.click()
            time.sleep(1.5)

            driver2.close() 

            continue

        except Exception as e:
            logging.error(f"Ocurrió un error: {e}")
            time.sleep(1)
            continue

if __name__ == '__main__':
    whatsapp_proc = Process(target=whatsapp_process)
    whatsapp_proc.start()
