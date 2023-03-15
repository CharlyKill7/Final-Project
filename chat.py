import openai
import requests
import json
import zmq
import time
import logging
import warnings
warnings.filterwarnings('ignore')

from ps import popenai
from functions import procesar_chat

logging.basicConfig(filename='log_chat.txt', level=logging.DEBUG)

context = zmq.Context()
socket_rec = context.socket(zmq.SUB)
socket_rec.connect("tcp://127.0.0.1:7777")
socket_rec.setsockopt_string(zmq.SUBSCRIBE, "");

socket_sen = context.socket(zmq.PUB)
socket_sen.bind("tcp://127.0.0.1:7788")

openai.api_key = popenai
model_engine = "text-davinci-003"

print('Chat Ready')

def send_message(message, chat_log=None):
    # If chat_log is not None, it should be a list of chat messages that have already been sent
    # to the chatbot, in the format [{"speaker": "user", "text": "hello"}, {"speaker": "bot", "text": "hi"}]
    if chat_log is None:
        chat_log = []
        
    # Set the API endpoint and parameters
    endpoint = "https://api.openai.com/v1/engines/" + model_engine + "/completions"
    prompt = ""
    for chat in chat_log:
        prompt += chat["speaker"] + ": " + chat["text"] + "\n"
    prompt += "User: " + message + "\nBot:"

    # Set the authentication header
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}",
    }

    # Send the API request
    data = {
        "prompt": prompt,
        "max_tokens": 1024,
        "temperature": 0.7,
        "n": 1,
        "stop": "Bot:",
    }
    response = requests.post(endpoint, headers=headers, json=data)

    # Extract the response text
    response_text = response.json()["choices"][0]["text"]
    return response_text.strip()

# Chat loop
chat_log = []
print("Luna: ¿Qué necesitas?")
while True:
    try:
        message = socket_rec.recv_string() #input("User: ") 
        if 'consulta' in message:
                mode, text = procesar_chat(message)
                print(mode)
                print(text)
                chat_log.append({"speaker": "user", "text": text})
                # Check for specific instructions
                if "como te llamas" in text.lower():
                    chat_log.append({"speaker": "luna", "text": "Soy Luna."})
                elif "di tu frase" in text.lower():
                    chat_log.append({"speaker": "luna", "text": "Del parqué... al parque."})

                response = send_message(text, chat_log)
                chat_log.append({"speaker": "luna", "text": response})
                socket_sen.send_string(response)
                print("Luna:", response)

        # Save chatlog to file
        with open("chatlog.json", "w") as f:
            json.dump(chat_log, f)

    except Exception as e:
        logging.error(f"Ocurrió un error: {e}")
        time.sleep(0.5)
        continue
    