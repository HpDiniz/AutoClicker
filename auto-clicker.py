import time
import threading
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
clients_horizontais = 2
button = Button.left
button2 = Button.right
click_key = KeyCode(char='z')
quit_key = KeyCode(char='q')
keyboard = keyController()
mouse = Controller()

def on_press(key):
    global delay_anterior
    if key == click_key:
        initial = mouse.position
        for x in range(clients_horizontais):
            mouse.position = (initial[0]+(GetSystemMetrics(0)/clients_horizontais*x),initial[1])
            time.sleep(0.01)
            mouse.click(button)
            time.sleep(0.01)
        mouse.position = initial

with Listener(on_release=on_press) as listener:
    listener.join()
