import json
import signal
import sys
import time
from tkinter import *
import tkinter as tk
import customtkinter as ctk
import threading
import pickle
import socket
from threading import Thread
from pymongo import MongoClient

WIDTH = 850
HEIGHT = 650
subFileSize = 512*1024 # 512KB

#---------------------------------SERVER_FE----------------------------------------------
class SERVER_FE(ctk.CTk):
    def __init__(self, serverHost, serverPort):
        super().__init__()
        
        self.peerCount = 0

        self.serverHost = serverHost
        self.serverPort = serverPort
        
        # Initial frame of several page
        self.frameMainPage= ctk.CTkFrame(self,width=WIDTH,height=HEIGHT)
        self.frameListFiles= ctk.CTkFrame(self,width=WIDTH,height=HEIGHT)
        self.frameListPeers = ctk.CTkFrame(self, width=WIDTH, height=HEIGHT)
        #--------------------------------------------------------------------------
        
        # initial the text and animation
        self.outputStatus = ctk.CTkTextbox(self.frameMainPage)
        self.outputListPeer = ctk.CTkTextbox(self.frameListPeers)
        self.outputFile = ctk.CTkTextbox(self.frameListFiles)
        #-----------------------------------------------------------------------------
        
        self.title("Tracker Of File Sharing Application")
        self.resizable(False,False) 
        self.geometry("850x650")
        
        self.current_frame = self.main_page()
        self.current_frame.pack()

    def switch_frame(self, frame):
      self.current_frame.pack_forget()
      self.current_frame = frame()
      self.current_frame.pack(padx = 0)       
        
    def main_page(self):  
        self.outputStatus.place(relx=0.5,rely=0.55,anchor=tk.CENTER,relwidth=0.6,relheight=0.4)
        self.outputStatus.configure(state=DISABLED)
        
        frame_label = ctk.CTkLabel(self.frameMainPage, text="Peers Action", font = ("Arial", 15))
        frame_label.place(relx=0.5,rely=0.80,anchor=tk.CENTER)

        # main page server
        frame_label = ctk.CTkLabel(self.frameMainPage, text="WELCOME ADMIN", font = ("Arial", 35,"bold"))
        frame_label.place(relx=0.5,rely=0.1,anchor=tk.CENTER)
        
        frame_label = ctk.CTkLabel(self.frameMainPage, text="INFORMATION OF TRACKER", font = ("Arial",20, "bold"))
        frame_label.place(relx=0.5,rely=0.2,anchor=tk.CENTER)
        
        frame_label = ctk.CTkLabel(self.frameMainPage, text="Server Host: "+ self.serverHost, font = ("Arial", 15))
        frame_label.place(relx=0.5,rely=0.28,anchor=tk.CENTER)
        
        frame_label = ctk.CTkLabel(self.frameMainPage, text="Server Port: "+ str(self.serverPort), font = ("Arial", 15))
        frame_label.place(relx=0.5,rely=0.32,anchor=tk.CENTER)

        # display inforpeer
        
        btn_view_user = ctk.CTkButton(self.frameMainPage, text="LIST PEERS", font=("Arial", 20, "bold"),
                                      command=lambda: self.switch_frame(self.list_peers_page))
        btn_view_user.place(relx=0.3, rely=0.9, anchor=ctk.CENTER)

        btn_show_peer = ctk.CTkButton(self.frameMainPage, text="FILES ON SYSTEM", font=("Arial", 20, "bold"),
                                      command=lambda: self.switch_frame(self.list_files))
        btn_show_peer.place(relx=0.7, rely=0.9, anchor=ctk.CENTER)
        
        return self.frameMainPage
    
    def list_peers_page(self):
        self.outputListPeer.place(relx=0.5, rely=0.55, anchor=ctk.CENTER, relwidth=0.6, relheight=0.4)
        self.outputListPeer.configure(state=DISABLED)

        frame_label = ctk.CTkLabel(self.frameListPeers, text="LIST OF PEERS", font = ("Arial", 40, "bold"))
        frame_label.place(relx = 0.5, rely = 0.1, anchor = ctk.CENTER)

        frame_label = ctk.CTkLabel(self.frameListPeers, text="INFORMATION OF TRACKER", font = ("Arial", 20, "bold"))
        frame_label.place(relx = 0.5, rely = 0.2, anchor = ctk.CENTER)

        frame_label = ctk.CTkLabel(self.frameListPeers, text="Server Host: " + self.serverHost, font = ("Arial", 15))
        frame_label.place(relx = 0.5, rely = 0.28, anchor = ctk.CENTER)

        frame_label = ctk.CTkLabel(self.frameListPeers, text="Server Port: " + str(self.serverPort), font = ("Arial", 15))
        frame_label.place(relx = 0.5, rely = 0.32, anchor = ctk.CENTER)

        # Button to go back to the main page
        btn_BACK = ctk.CTkButton(self.frameListPeers, text="BACK", font=("Arial", 20, "bold"),
                                 command=lambda: self.switch_frame(self.main_page))
        btn_BACK.place(relx=0.5, rely=0.9, anchor=ctk.CENTER)

        return self.frameListPeers
    
    def showPeers(self, state, informPeer):
      if state == "on":
        self.outputListPeer.configure(state = NORMAL)
        self.peerCount += 1
        self.outputListPeer.insert(ctk.END, f"{self.peerCount}.  PeerHost: {informPeer[0]}, PeerPort: {informPeer[1]}." +"\n\n" )
        self.outputListPeer.see(ctk.END)
        self.outputListPeer.configure(state=DISABLED)
      else:
        self.outputListPeer.configure(state=NORMAL)
        # Lấy toàn bộ nội dung của widget
        peer_list = self.outputListPeer.get("1.0", ctk.END)  # Lấy từ dòng đầu tiên tới cuối
        lines = peer_list.split("\n")  # Chia các dòng thành danh sách
        for i, line in enumerate(lines):
          if f"PeerHost: {informPeer[0]}, PeerPort: {informPeer[1]}" in line:
              start_index = f"{i + 1}.0"  # Dòng bắt đầu
              end_index = f"{i + 2}.0"  # Dòng kết thúc (dòng tiếp theo)
              self.outputListPeer.delete(start_index, end_index)  # Xóa dòng đó
              break
        self.peerCount -= 1
        self.outputListPeer.see(ctk.END)
        self.outputListPeer.configure(state = DISABLED)
    
    def list_files(self):  
        self.outputFile.place(relx = 0.5, rely = 0.55, anchor = tk.CENTER, relwidth = 0.6, relheight = 0.4)
        self.outputFile.configure(state=DISABLED)

        # main page server
        frame_label = ctk.CTkLabel(self.frameListFiles, text="LIST OF FILES ON THE SYSTEM", font =( "Arial", 40,"bold"))
        frame_label.place(relx = 0.5, rely = 0.1, anchor = tk.CENTER)
        
        frame_label = ctk.CTkLabel(self.frameListFiles, text="INFORMATION OF TRACKER", font = ("Arial",20, "bold"))
        frame_label.place(relx = 0.5, rely = 0.2, anchor = tk.CENTER)
        
        frame_label = ctk.CTkLabel(self.frameListFiles, text="Server Host: "+ self.serverHost, font = ("Arial", 16))
        frame_label.place(relx = 0.5, rely = 0.28, anchor = tk.CENTER)
        
        frame_label = ctk.CTkLabel(self.frameListFiles, text="Server Port: "+ str(self.serverPort), font = ("Arial", 16))
        frame_label.place(relx = 0.5, rely = 0.32, anchor = tk.CENTER)

        #display inforpeer
        
        btn_BACK= ctk.CTkButton(self.frameListFiles, text= "BACK", font= ("Arial", 20, "bold"),
                                command = lambda:self.switch_frame(self.main_page))
        btn_BACK.place(relx = 0.5, rely =0.9, anchor = tk.CENTER)

        return self.frameListFiles
      
    def showListFile(self):
        self.outputFile.configure(state = NORMAL)
        counter = 1
        self.outputFile.delete(1.0, ctk.END)
        for file in SERVER_BE_object.listFileShared:
            self.outputFile.insert(ctk.END, f"{counter}. fileName: \"{file}\"." + "\n")
            self.outputFile.insert(ctk.END, "\n")
            counter += 1

        self.outputFile.see(ctk.END)
        self.outputFile.configure(state = DISABLED)

    def showStatus(self, typeOfStatement, peerHost, peerPort, fileName):
        self.outputStatus.configure(state = NORMAL)
        if typeOfStatement == "Download":
            self.outputStatus.insert(ctk.END, f"PeerHost: {peerHost}, PeerPort: {peerPort} download file \"{fileName}\""+ "\n\n")
        else:
            if typeOfStatement == "Sharing":
                self.outputStatus.insert(ctk.END, f"PeerHost: {peerHost}, PeerPort: {peerPort} upload file \"{fileName}\""+ "\n\n")
            else:
                if typeOfStatement == "Join to LAN":
                    self.outputStatus.insert(ctk.END, f"PeerHost: {peerHost}, PeerPort: {peerPort} joined to network"+ "\n\n")
                elif typeOfStatement == "Close the App":
                    self.outputStatus.insert(ctk.END, f"PeerHost: {peerHost}, PeerPort: {peerPort} Closed the App"+ "\n\n")
        self.outputStatus.see(ctk.END)
        self.outputStatus.configure(state= DISABLED)


        
#---------------------------FINISH SERVER_FE------------------------------------------------


#---------------------------------SERVER_BE-------------------------------------------------
class fileShared:
  def __init__(self, fileName, filePath, peerHost, peerPort, size):
    self.fileName = fileName
    self.numberOfPeer = 1
    self.size = size
    self.informPeerLocal = [[filePath, peerHost, peerPort]]
    
class SERVER_BE:
  
  def __init__(self, serverHost, serverPort):
    self.listPeer = []
    self.listFileExist = []
    self.listFileShared = set()
    
    self.serverHost = serverHost
    self.serverPort = serverPort

    self.serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    self.stopFlag = threading.Event()
    self.running = True
    self.connections = []


  def seekListOfPeers(self,serverhost,serverport):
    #---------------------------------
    print()
  
  def implementDownload(self, conn):  
    #Receive the info_hash want to down
    info_hash = str(conn.recv(4096), "utf-8")
    conn.send(bytes("SUCCESS", "utf-8"))  # confirm
    #----------------------------------------------------------------------------------
    
    #Receive serverHost and serverPort
    serverhost = str(conn.recv(4096), "utf-8")
    conn.send(bytes("SUCCESS", "utf-8"))
    serverport = int(str(conn.recv(4096), "utf-8"))
    conn.send(bytes("SUCCESS", "utf-8"))
    #----------------------------------------------------------------------------------
    
    conn.recv(4096) #kepp contact

    #implement find list of peers
    documents = client_db.find(
      {
        "info_hash":info_hash,
        "state": { "$ne": "off" }
      },
      {
        "ip_address":1,
        "ip_port":1,
        "_id":0
      }
    )
    list_peer = list(documents)

    json_data = json.dumps(list_peer)
    
    # Gửi dữ liệu qua socket
    conn.sendall(json_data.encode('utf-8'))
    conn.recv(4096) #success
    #----------------------------------------------------------------------------------------------
    
  def updateState(self, state, PeerHost, PeerPort):
     client_db.update_one({"ip_address": PeerHost, "ip_port": PeerPort},{"$set": {"state": state}})

  def implementListenPeer(self):
    self.serverSocket.bind((self.serverHost, self.serverPort))
    self.serverSocket.listen(10)
  
    while self.running:
      try:
        conn, addr = self.serverSocket.accept()
        #stopFlag= threading.Event()
        self.stopFlag.clear()
        condition = Thread(target = self.threadListenPeer, args=[conn])
        condition.start()
      except OSError:
        break
      except Exception as e:
        print(f"Error: {e}")
      time.sleep(0.1)

  def stop(self):
    self.running = False
    self.serverSocket.close()
    for conn in self.connections:
      conn.close()
    self.connections.clear()
    
  def implementSharing(self, filePath, peerHost, peerPort, size):
    #get fileName from filePath
    iterator = -1
    while True:
      if filePath[iterator] == "\\":
        break
      else:
        iterator -= 1
    fileName = filePath[(iterator+ 1): ]
    #-----------------------------------------------------------------
    
    #Add inform to listFileShared
    flagFileExist = False
    for fileSharedObject in self.listFileShared:   # fileShared is the object
      if fileSharedObject.fileName == fileName:
        for informPeerLocal in fileSharedObject.informPeerLocal:  # informPeerLocal is the list
          if informPeerLocal[1] == peerHost and informPeerLocal[2] == peerPort:  # path equal or not
            flagFileExist = True
            break
        if flagFileExist == True:
          break
        else:
          flagFileExist = True
          fileSharedObject.numberOfPeer += 1
          fileSharedObject.informPeerLocal.append([filePath, peerHost, peerPort])
          SERVER_FE_object.showListFile()
          break
            
    if flagFileExist == False:
      fileShareObject = fileShared(fileName, filePath, peerHost, peerPort, size)
      self.listFileShared.append(fileShareObject)
      self.listFileExist.append(fileName)
      SERVER_FE_object.showListFile()
    #------------------------------------------------------------------------------
    
    SERVER_FE_object.showStatus("Upload", peerHost, peerPort, fileName)

  def threadListenPeer(self, conn):
    try:
      while not self.stopFlag.is_set():
        #Receive the type of request
        typeOfRequest = str(conn.recv(4096), "utf-8")
        conn.send(bytes("SUCCESS", "utf-8"))  # confirm
        #-------------------------------------------------------------
        
        #Classify the type request
        if typeOfRequest == "Join to LAN":
          #Receive inform of peer
          peerInform= pickle.loads(conn.recv(4096))
          conn.send(bytes("SUCCESS", "utf-8"))  # confirm
          #------------------------------------------------------------
          
          #--------------------Check peer in database--------------------
          existing_peer = client_db.find_one({"ip_address": peerInform[0], "ip_port": peerInform[1]})
          if existing_peer:
            self.updateState("on", peerInform[0], peerInform[1])
            print("Peer already exists. Updated state to 'on'.")
          else:
            client_db.insert_one({
                "ip_address": peerInform[0],
                "ip_port": peerInform[1],
                "state": "on"
            })
            print("New peer added with state 'on'.")
          #---------------------------------------------------------------

          #Add inform of peer to list
          self.listPeer.append(peerInform)
          #---------------------------------------------------------------
          SERVER_FE_object.showPeers("on", peerInform)
          conn.recv(4096)  # new insert
          
          #Send the list of peers
          conn.sendall(pickle.dumps(self.listPeer))
          conn.recv(4096)  # success
          #---------------------------------------------------------------
          
          conn.send(bytes("SUCCESS", "utf-8"))
          
          SERVER_FE_object.showStatus(typeOfRequest, peerInform[0], peerInform[1], "")

        elif typeOfRequest == "Cancel":
            self.stopFlag.set()  

        elif typeOfRequest== "Upload":
              # upload filePath
              filePath = str(conn.recv(4096), "utf-8")
              conn.send(bytes("SUCCESS", "utf-8"))  # confirm
              #----------------------------------------------------------------

              #Receive peerHost and peerPort
              peerHost= str(conn.recv(4096), "utf-8")
              conn.send(bytes("SUCCESS", "utf-8"))  # confirm
              peerPort= int(str(conn.recv(4096), "utf-8"))
              conn.send(bytes("SUCCESS", "utf-8"))  # confirm
              #----------------------------------------------------------------
              
              #Receive size of file
              size= int(str(conn.recv(4096), "utf-8"))
              conn.send(bytes("SUCCESS", "utf-8"))  # confirm
              #----------------------------------------------------------------
              
              #add inform File to listFileShared
              self.implementSharing(filePath, peerHost, peerPort, size)
              #----------------------------------------------------------------
              
              SERVER_FE_object.showStatus(typeOfRequest, peerInform[0], peerInform[1], "")
           
        elif typeOfRequest == "Sharing":
               #Receive inform of peer
               peerInform = pickle.loads(conn.recv(4096))
               conn.send(bytes("SUCCESS", "utf-8"))  # confirm
               #------------------------------------------------------------

               #Receive upload filePath
               info_hash = str(conn.recv(4096), "utf-8")
               conn.send(bytes("SUCCESS", "utf-8"))  # confirm
               #---------------------------------------------------------------

               #Receive peerHost and peerPort
               peerHost = str(conn.recv(4096), "utf-8")
               conn.send(bytes("SUCCESS", "utf-8"))  # confirm
               peerPort = int(str(conn.recv(4096), "utf-8"))
               conn.send(bytes("SUCCESS", "utf-8"))  # confirm
               #---------------------------------------------------------------

               #Receive fileName
               fileName = str(conn.recv(4096), "utf-8")
               conn.send(bytes("SUCCESS", "utf-8"))  # confirm
               self.listFileShared.add(fileName)
               SERVER_FE_object.showListFile()
               #---------------------------------------------------------------
                
               #Receive magnet text
               magnet_text = str(conn.recv(4096), "utf-8")
               conn.send(bytes("SUCCESS", "utf-8"))  # confirm
               #---------------------------------------------------------------
              
               SERVER_FE_object.showStatus(typeOfRequest, peerInform[0], peerInform[1], fileName)

               # Update or add info_hash to database
               client_db.update_one(
                 {"ip_address": peerHost, "ip_port": peerPort},
                 {"$addToSet": {"info_hash": info_hash,"files": {"fileName": fileName, "magnet_text":magnet_text}}}
               )

        elif typeOfRequest == "Download":
                  #Receive inform of peer
                  peerInform = pickle.loads(conn.recv(4096))
                  conn.send(bytes("SUCCESS", "utf-8"))  # confirm
                  #------------------------------------------------------------

                  #Receive fileName
                  fileName = str(conn.recv(4096), "utf-8")
                  conn.send(bytes("SUCCESS", "utf-8"))  # confirm
                  #---------------------------------------------------------------

                  self.implementDownload(conn)
                  SERVER_FE_object.showStatus(typeOfRequest, peerInform[0], peerInform[1], fileName) 

        elif typeOfRequest == "fileExist":
                      conn.recv(4096)
                      conn.sendall(pickle.dumps(self.listFileExist))
                      conn.recv(4096)
                      conn.send(bytes("SUCCESS", "utf-8"))      

        elif typeOfRequest == "Close the App":
                        peerInform= pickle.loads(conn.recv(4096))
                        conn.send(bytes("SUCCESS", "utf-8"))
                        self.updateState("off", peerInform[0], peerInform[1])
                        SERVER_FE_object.showPeers("off",peerInform)
                        SERVER_FE_object.showStatus(typeOfRequest, peerInform[0], peerInform[1], "")
                        conn.send(bytes("SUCCESS", "utf-8"))
    except Exception as e:
      print(f"Error occurred: {e}")
    finally:
      conn.close()                                         
            
#----------------------FINISH SERVER_BE----------------------------------------------------           

# Handle Ctrl+C (stop application)
def signal_handler(sig, frame):
    print('You pressed Ctrl+C! Closing application...')
    SERVER_BE_object.stop()
    sys.exit(0)
        
if __name__ == '__main__':
    # Get the list of IP addresses associated with the hostname
    ip_addresses = socket.gethostbyname_ex(socket.gethostname())[2]

    # Check if there are enough elements in the list
    if len(ip_addresses) > 2:
        serverHost = ip_addresses[2]
    else:
        # Handle the case where there are not enough IP addresses
        serverHost = ip_addresses[1]  # or set to a default value

    serverPort = 8080
    print(socket.gethostbyname_ex(socket.gethostname())[2])

    # Kết nối đến MongoDB sử dụng URI
    uri = "mongodb+srv://project_MMT:mbk22351@cluster0.l5iob.mongodb.net/"
    mongo = MongoClient(uri)
    database_name = mongo['MMT']
    client_db = database_name['Client']

    client_db.create_index([("info_hash", 1)])
    
    SERVER_BE_object = SERVER_BE(serverHost, serverPort)

    signal.signal(signal.SIGINT, signal_handler)
    
    condition = Thread(target= SERVER_BE_object.implementListenPeer)
    condition.daemon = True
    condition.start()

    SERVER_FE_object = SERVER_FE(serverHost, serverPort)
    SERVER_FE_object.mainloop()