import time
import threading
from statistics import fmean as mean
from random import randrange, uniform
from pynput.mouse import Button, Controller, Listener
from win32api import GetSystemMetrics
from pynput.keyboard import Listener, KeyCode, Key, Controller as keyController
import time
import logging                                                                

logging.basicConfig(filename='logger.log', filemode='w', level=logging.DEBUG)
logging.debug('debug')
logging.info('info')
logging.warning('warning')
logging.error('error')
logging.critical('critical')

delay_anterior = None
delay = 0.01
clients_horizontais = 3
clients_verticais = 2
button = Button.left
button2 = Button.right
start_stop_key = KeyCode(char='z')
reset_key = KeyCode(char='r')
add_key = KeyCode(char='1')
add_key_with_shift = KeyCode(char='2')
quit_key = KeyCode(char='q')
click_positions = [] 

class MyTask:
    def __init__(self, mouse_position, shift_pressed, delay):
        global delay_anterior
        self.mouse_position = mouse_position
        self.shift_pressed = shift_pressed
        if(delay_anterior == None):
            self.delay = 0
        else:
            self.delay = delay - delay_anterior
        delay_anterior = int(round(time.time_ns()))

    def imprime(self):
        print(self.mouse_position + self.shift_pressed)


class ClickMouse(threading.Thread):
    def __init__(self, delay, button,button2):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.button2 = button2
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False
        keyboard.release(Key.shift)

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                for item in click_positions:
                    time.sleep(item.delay/1000000000 + uniform(0.0, 0.1))
                    randomize_position = (item.mouse_position[0] + randrange(2),item.mouse_position[1] + randrange(2))
                    mouse.position = (randomize_position)
                    if(item.shift_pressed == False):
                        keyboard.release(Key.shift)
                    else:
                        keyboard.press(Key.shift)

                    time.sleep(0.1)
                    mouse.click(self.button)
                    time.sleep(0.1)
                time.sleep(0.01)
             
                
                
            #mouse.position = (initial[0]+(GetSystemMetrics(0)/clients_horizontais*x),initial[1]+(GetSystemMetrics(1)/clients_verticais*y))
            #initial = mouse.position

            #for y in range(clients_verticais):
            #    for x in range(clients_horizontais):
            #        if(y == 0):
            #            mouse.position = (initial[0]+(GetSystemMetrics(0)/clients_horizontais*x),initial[1]+(GetSystemMetrics(1)/clients_verticais*y))
            #        else:
            #            if(initial[1] > GetSystemMetrics(1)/2):
            #                mouse.position = (initial[0]+(GetSystemMetrics(0)/clients_horizontais*x),initial[1])
            #            else:
            #                mouse.position = (initial[0]+(GetSystemMetrics(0)/clients_horizontais*x),initial[1]+(GetSystemMetrics(1)/clients_verticais*y)-20)
            #        time.sleep(self.delay)
            #        mouse.click(self.button)
            #        time.sleep(self.delay)
            #mouse.position = initial

    def aperta_botao_direito(self):
        print(mouse.position)

keyboard = keyController()
mouse = Controller()
click_thread = ClickMouse(delay, button,button2)
click_thread.start()

def on_press(key):
    global click_positions
    global delay_anterior
    if key == start_stop_key:
        if click_thread.running:
            keyboard.release(Key.shift)
            click_thread.stop_clicking()
        else:
            click_thread.start_clicking()
        
    elif key == add_key:
        obj = MyTask(mouse.position,False,int(round(time.time_ns())))
        click_positions.append(obj)
        mouse.click(button)
    elif key == add_key_with_shift:
        keyboard.press(Key.shift)
        time.sleep(0.1)
        obj = MyTask(mouse.position,True,int(round(time.time_ns())))
        click_positions.append(obj)
        mouse.click(button)
        time.sleep(0.1)
        keyboard.release(Key.shift)
    elif key == reset_key:
        click_positions = []
        delay_anterior = None
    elif key == quit_key:
        keyboard.release(Key.shift)
        click_thread.exit()
        listener.stop()

with Listener(on_release=on_press) as listener:
    listener.join()

#def on_click(x, y, button, pressed):
#     global teste
#     if pressed:
#         if(teste == False):
#             teste = True
#             click_thread.aperta_botao_esquerdo()
#             teste = False

# def on_scroll(x, y, dx, dy):
#     print('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))

# with Listener(on_click=on_click, on_scroll=on_scroll) as listener:
#     listener.join()