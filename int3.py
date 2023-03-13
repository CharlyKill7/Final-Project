import PySimpleGUI as sg
import zmq
import tkinter as tk

sg.LOOK_AND_FEEL_TABLE['Moon'] = {'BACKGROUND': '#2B2D42',
                                            'TEXT': '#FFD700',
                                            'INPUT': '#2B2D42',
                                            'TEXT_INPUT': '#FFD700',
                                            'SCROLL': '#2B2D42',
                                            'BUTTON': ('#C0C0C0', '#2B2D42'),
                                            'PROGRESS': ('#2B2D42', '#2B2D42'),
                                            'BORDER': 0, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0}

# Switch to use your newly created theme
sg.theme('Moon')
sg.set_options(font=('Consolas', 12))#, 'bold'))

context = zmq.Context()
socket_rec = context.socket(zmq.SUB)
socket_rec.connect("tcp://127.0.0.1:7788")
socket_rec.setsockopt_string(zmq.SUBSCRIBE, "")

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
                           background_color='#2B2D42',
                           #titlebar_background_color='#000000', 
                           #titlebar_text_color='#C0C0C0', 
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

socket_rec.close()
context.term()
