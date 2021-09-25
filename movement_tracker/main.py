
import opencv.MotionModule as m    
import websocket
import time
try:
    import thread
except ImportError:
    import _thread as thread
import cv2
import numpy as np
import time

import sys
from datetime import datetime
from threading import *
from EventManager import *
#server的HOST
HOST = 'ws://127.0.0.1:12345'

#與server約定好的protocol server端也要設定
SUBPROTOCOLS = ['echo-protocol']
#收到server傳來的message的callback

eventName='findPeople'
def onMessage(ws, msg):
    print("收到了從server傳來的message：" + msg)
def onError(ws, error):
    print(error)
def onClose(ws):
    print("### closed ###")
#與server建立連線後的callback
def onOpen(ws):
    print('onOpen')
    eventManager = EventManager()
    def eventSend(event):
        ws.send(event.dict[eventName])
    eventManager.AddEventListener(eventName,eventSend )
    eventManager.Start()
    detection=m.MotionDetection(eventManager,eventName)
    def run(*args):
        detection.start()
    thread.start_new_thread(run, ())
def start():
    #建立websocket
    #ws = websocket.WebSocketApp(HOST, subprotocols = SUBPROTOCOLS, on_open = onOpen, on_message = onMessage)   
    ws = websocket.WebSocketApp(HOST,on_message = onMessage,on_error = onError,on_close = onClose)
    ws.on_open = onOpen 
    ws.run_forever()

if __name__ == '__main__':
    start()