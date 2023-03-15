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

logging.basicConfig(filename='log_youtube.txt', level=logging.DEBUG)

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

def youtube_process():

    context = zmq.Context()
    socket_rec = context.socket(zmq.SUB)
    socket_rec.connect("tcp://127.0.0.1:7777")
    socket_rec.setsockopt_string(zmq.SUBSCRIBE, "");

    PATH = ChromeDriverManager().install() 

    print('Youtube Ready')

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
            driver = webdriver.Chrome()
            with open('estado.txt', 'w') as f:
                f.write('abierta')
        # si la ventana está abierta, no hacer nada
        else:
            pass

        try:
            mensa = socket_rec.recv_string(flags=zmq.NOBLOCK)

            if mensa.split()[0].lower() != 'youtube':
                continue

            service = Service(PATH)
            driver = webdriver.Chrome(service=service, options=options)
            driver.get('https://www.google.com/')

            wait2 = WebDriverWait(driver, 30)  # Wait for up to 10 seconds

            buscador = wait2.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')))
            buscador.click()
            buscador.send_keys(mensa)
            buscador.send_keys(Keys.ENTER)

            time.sleep(2)

            buscar = driver.find_element(By.XPATH,'//*[@id="tsf"]/div[1]/div[1]/div[2]/div/div[2]/input')
            buscar.click()
            buscar.send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, 
                            Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.ENTER)

            vid = wait2.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="movie_player"]/div[5]/button')))
            vid.click()

            time.sleep(2)

            publi = wait2.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="skip-button:5"]/span/button')))
            if publi:
                publi.click()

            else:
                pass

            continue

        except Exception as e:
            logging.error(f"Ocurrió un error: {e}")
            time.sleep(1)
            continue

if __name__ == '__main__':
    youtube_proc = Process(target=youtube_process)
    youtube_proc.start()
