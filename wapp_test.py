while True:
        
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager 
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By # By es para buscar por tag, clase, id...
    import time
    import zmq
    import tqdm
    import warnings
    warnings.filterwarnings('ignore')

    from functions import procesar_mensaje

    options=Options()

    # quita la bandera de ser robot
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--remote-allow-origins=*");
    options.add_argument(r"user-data-dir=C:\Users\elmat\anaconda3\envs\final\Lib\site-packages\selenium")
    options.add_experimental_option("detach", True)     #Esta opción corrige el error de cierre repentino

    context = zmq.Context()
    socket_rec = context.socket(zmq.SUB)
    socket_rec.connect("tcp://127.0.0.1:5555")
    socket_rec.setsockopt_string(zmq.SUBSCRIBE, "whatsapp")



    message = socket_rec.recv_string()

    print(message)

    mode, text, name = procesar_mensaje(message)

    print(f"Modo: {mode}")
    print(f"Texto: {text}")
    print(f"Nombre: {name}")

    PATH = ChromeDriverManager().install() 
    driver=webdriver.Chrome(PATH, options=options)     
    driver.get('https://web.whatsapp.com/')

    time.sleep(5)

    busca = driver.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div/div[2]/div/div[2]')
    busca.click() 
    busca.send_keys(name)

    time.sleep(3)
    uno = driver.find_element(By.XPATH,'//*[@id="pane-side"]/div[1]/div/div/div[1]/div/div/div/div[2]')
    uno.click()

    txt = driver.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
    txt.send_keys(text)
    time.sleep(3)

    ent = driver.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button')
    ent.click()




