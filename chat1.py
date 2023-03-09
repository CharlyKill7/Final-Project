import openai
import requests
import json
from ps import popenai
import zmq

context = zmq.Context()
socket_rec = context.socket(zmq.SUB)
socket_rec.connect("tcp://127.0.0.1:5555")
socket_rec.setsockopt_string(zmq.SUBSCRIBE, "")

socket_sen = context.socket(zmq.PUB)
socket_sen.bind("tcp://127.0.0.1:5556")

openai.api_key = popenai
model_engine = "text-davinci-003"

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
print("Bot: Caminaré sobre las cenizas de este bootcamp. ¿Qué necesitas?")
while True:
    message = socket_rec.recv_string() #input("User: ") 
    if 'luna' or 'tierra' not in message.lower():
        chat_log.append({"speaker": "user", "text": message})
        # Check for specific instructions
        if "como te llamas" in message.lower():
            chat_log.append({"speaker": "bot", "text": "Soy Bot."})
        elif "di tu frase" in message.lower():
            chat_log.append({"speaker": "bot", "text": "Del parqué... al parque."})

        response = send_message(message, chat_log)
        chat_log.append({"speaker": "bot", "text": response})
        socket_sen.send_string(response)
        print("Bot:", response)

    # Save chatlog to file
    with open("chatlog.json", "w") as f:
        json.dump(chat_log, f)

