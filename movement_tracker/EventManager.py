# -*- encoding: UTF-8 -*-
 
# 系統模組
from queue import Queue, Empty
from threading import *
 
 
class EventManager:
  def __init__(self):
    """初始化事件管理器"""
    # 事件物件列表
    self.__eventQueue = Queue()
    # 事件管理器開關
    self.__active = False
    # 事件處理執行緒
    self.__thread = Thread(target = self.__Run)
 
    # 這裡的__handlers是一個字典，用來儲存對應的事件的響應函式
    # 其中每個鍵對應的值是一個列表，列表中儲存了對該事件監聽的響應函式，一對多
    self.__handlers = {}  # {事件型別:[處理事件的方法]}
 
  def __Run(self):
    """引擎執行"""
    while self.__active == True:
      try:
        # 獲取事件的阻塞時間設為1秒
        event = self.__eventQueue.get(block = True, timeout = 1)
        self.__EventProcess(event)
      except Empty:
        pass
 
  def __EventProcess(self, event):
    """處理事件"""
    # 檢查是否存在對該事件進行監聽的處理函式
    if event.type_ in self.__handlers:
      # 若存在，則按順序將事件傳遞給處理函式執行
      for handler in self.__handlers[event.type_]:
        handler(event)
 
  def Start(self):
    """啟動"""
    # 將事件管理器設為啟動
    self.__active = True
    # 啟動事件處理執行緒
    self.__thread.start()
 
  def Stop(self):
    """停止"""
    # 將事件管理器設為停止
    self.__active = False
    # 等待事件處理執行緒退出
    self.__thread.join()
 
  def AddEventListener(self, type_, handler):
    """繫結事件和監聽器處理函式"""
    # 嘗試獲取該事件型別對應的處理函式列表，若無則建立
    try:
      handlerList = self.__handlers[type_]
    except KeyError:
      handlerList = []
 
    self.__handlers[type_] = handlerList
    # 若要註冊的處理器不在該事件的處理器列表中，則註冊該事件
    if handler not in handlerList:
      handlerList.append(handler)
 
  def RemoveEventListener(self, type_, handler):
    """移除監聽器的處理函式"""
    #讀者自己試著實現
 
  def SendEvent(self, event):
    """傳送事件，向事件佇列中存入事件"""
    self.__eventQueue.put(event)
 
"""事件物件"""
class Event:
  def __init__(self, type_=None):
    self.type_ = type_   # 事件型別
    self.dict = {}     # 字典用於儲存具體的事件資料