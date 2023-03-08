import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://10.0.0.109:5555")
socket.setsockopt_string(zmq.SUBSCRIBE, "")


while True:
    print('a')
    message = socket.recv_string() # Esperar un mensaje
    print("Mensaje recibido: {}".format(message)) # Procesar el mensaje recibido


