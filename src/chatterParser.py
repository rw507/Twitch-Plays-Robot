import sys
import threading
import time
from twitchChatter import *


class chatterParser(threading.Thread):
  lock = threading.Lock()
  count = 0
  commands = ["up" , "left", "right"]
  adminCommands = ["stop"]
  
  def __init__(self, threshold ):
    threading.Thread.__init__(self)
    self.threshold = threshold
    self.twitchReader = twitchChatter()
    self.reset()
    self.running = True   

  def getTwitchChatter(self):
    return self.twitchReader
  
  def stop(self):
    with self.lock:
      self.running = False
      self.twitchReader = None
  

  
  def run(self):
    while(self.running):      
      message = self.twitchReader.getMessage()
      
      isAdmin = (message[0] == "twitch_plays_robot")
 
      if(message[0].strip() == "" or self.nextCommand):
        continue
      if(isAdmin):
        self.nextCommand = message[1]
        continue
      clean = self.cleanMessage(message[1])     
      #print("Is " + clean + " a command?")
      if (clean in self.commands or (isAdmin and clean in self.adminCommands)):
  #print("yes")
        with self.lock:
          self.comCount[clean]+=1
          if(self.comCount[clean] >= self.threshold):
            self.nextCommand = clean

  
  
  def cleanMessage(self, raw):
    clean = raw.lower().replace(" ", "").strip()
    return clean
  
  def reset(self):   
    with self.lock: 
      #print("Restarting...")
      #print("Original Count: " + str(self.count))
      
      self.count = 0
      self.nextCommand = None      
      self.comCount = {}
      for c in self.commands:
        self.comCount[c] = 0
      #print("This should be 0: " + str(self.count))
  def getNextCommand(self):
    if(self.nextCommand):
      c = self.nextCommand
      self.reset()
    else:
      return None
    
    return c

  def forceNextCommand(self):
    keys = self.comCount.keys()
    count = 0
    command = None
    for k in keys:
      if(self.comCount[k] > count):
        count = self.comCount[k]
        command = k
    return command
  
if __name__ == ("__main__"):
  threshold = 2
  chatterParser = chatterParser(threshold)
  chatterParser.start()
  
  for i in range(1,100):
    time.sleep(1)
    print(str(i) + ": " + str(chatterParser.getNextCommand()))

  print("STOPPING")
  chatterParser.stop()
  print("I SHOULD HAVE STOPPED")
  
  """
  time.sleep(2) 
  chatterParser.reset()
  time.sleep(2)
  print("STOPPING!!!")
  chatterParser.stop()
  """
  
