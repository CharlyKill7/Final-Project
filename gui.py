import PySimpleGUI as sg
import zmq
import tkinter as tk

sg.LOOK_AND_FEEL_TABLE['Moon'] = {'BACKGROUND': '#263A7A',
                                            'TEXT': '#FFD700',
                                            'INPUT': '#263A7A',
                                            'TEXT_INPUT': '#FFD700',
                                            'SCROLL': '#263A7A',
                                            'BUTTON': ('#C0C0C0', '#263A7A'),
                                            'PROGRESS': ('#263A7A', '#263A7A'),
                                            'BORDER': 0, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0}

sg.theme('Moon')
sg.set_options(font=('Avenir', 11, 'bold'))

context = zmq.Context()
socket_rec = context.socket(zmq.SUB)
socket_rec.connect("tcp://127.0.0.1:7788")
socket_rec.setsockopt_string(zmq.SUBSCRIBE, "")

print('GUI Ready')

while True:
    try:
        message = socket_rec.recv_string(flags=zmq.NOBLOCK)
        layout = [#[sg.Text('Respuesta', font='Any 15')],
                  [sg.Multiline(size=(80, 20), key='-OUTPUT-')],
                  [sg.Button('Cerrar'), sg.Button('Copiar')]]

        root = tk.Tk()
        root.withdraw()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window = sg.Window('LUNA', 
                           layout, 
                           size=(400, 300), 
                           location=(screen_width - 415, screen_height - 395), 
                           grab_anywhere=True, 
                           resizable=True,
                           background_color='#263A7A', 
                           titlebar_font='bold', 
                           #titlebar_icon=r"img\moon.ico", 
                           finalize=True)
        window.TKroot.attributes("-topmost", True)
        
        while True:
            event, values = window.read(timeout=10)
            if event == sg.WIN_CLOSED or event == 'Cerrar':
                window.close()
                break
            if message:
                window['-OUTPUT-'].print(message)
                message = None
            if event == 'Copiar':
                sg.clipboard_set(window['-OUTPUT-'].get())

    except zmq.Again:
        pass


