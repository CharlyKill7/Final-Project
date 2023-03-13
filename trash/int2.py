import PySimpleGUI as sg
import zmq
import tkinter as tk

sg.theme('DarkBlue3')

context = zmq.Context()
socket_rec = context.socket(zmq.SUB)
socket_rec.connect("tcp://127.0.0.1:7777")
socket_rec.setsockopt_string(zmq.SUBSCRIBE, "")

while True:
    try:
        message = socket_rec.recv_string(flags=zmq.NOBLOCK)
        layout = [[sg.Text('Output del socket sub:', font='Any 15')],
                  [sg.Output(size=(80, 20))],
                  [sg.Button('Cerrar')]]

        root = tk.Tk()
        root.withdraw()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window = sg.Window('Socket Sub Output', layout, size=(400, 300), location=(screen_width - 400, screen_height - 300))

        while True:
            event, values = window.read(timeout=10)
            if event == sg.WIN_CLOSED or event == 'Cerrar':
                window.close()
                break
            # Si se recibe otro mensaje mientras la ventana está abierta, se muestra en la ventana
            try:
                message = socket_rec.recv_string(flags=zmq.NOBLOCK)
                print('-----------')
                print(message)
                print('-----------')
            except zmq.Again:
                pass
    except zmq.Again:
        pass

socket_rec.close()
context.term()

