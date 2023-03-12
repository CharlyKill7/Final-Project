import zmq

context = zmq.Context()
socket_rec = context.socket(zmq.SUB)
socket_rec.connect("tcp://127.0.0.1:7788")
socket_rec.setsockopt_string(zmq.SUBSCRIBE, "");

while True:

    try:
        print('-----------')
        message = socket_rec.recv_string()
        print(message)
        print('-----------')
        
    except:
        continue