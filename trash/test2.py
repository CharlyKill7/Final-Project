import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:5555")
socket.setsockopt_string(zmq.SUBSCRIBE, "")


while True:
    print('a')
    result2 = socket.recv_string() # Esperar un mensaje
    print("Mensaje recibido: {}".format(result2)) # Procesar el mensaje recibido


