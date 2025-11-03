import re
import bencodepy
import hashlib
import json
import signal
import sys
import time
import socket
from threading import Thread
from tkinter import messagebox
import pickle
import threading
import os
import math
import urllib.parse

WIDTH = 900
HEIGHT = 600
subFileSize = 512 * 1024  # 512KB

class PEER_BE():
  
  def __init__(self, peerHost, peerPort):
    self.serverHost= None
    self.serverPort= None
    
    self.peerHost= peerHost
    self.peerPort= peerPort
    
    self.subFileSize= 512*1024

    self.running = True  # Biến cờ để kiểm soát vòng lặp
    self.connections = []  # Danh sách các kết nối
    self.peerSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    self.stopFlag = threading.Event()

    self.piece_size = 512 * 1024
    self.download_mapping = {}  # Mapping giữa file và các phần của nó

  def stateClose(self):
    #-------------------- socket initial-------------------
    peerConnectServerSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peerConnectServerSocket.connect((self.serverHost, self.serverPort))
    #-------------------------------------------------------

    #------------------ send and receive--------------------
    peerConnectServerSocket.send(bytes("Close the App", "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    # ----------------------------------------------------

    #-------------------Send inform of peer------------------------
    peerInform= pickle.dumps([self.peerHost, self.peerPort])
    peerConnectServerSocket.sendall(peerInform)
    peerConnectServerSocket.recv(4096) # success
    #--------------------------------------------------------------

    #---------------send cancel command to close the connection---------------------
    peerConnectServerSocket.send(bytes("Cancel", "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    #-----------------------------------------------------------------------------

    peerConnectServerSocket.close()

  def createPEER(self, new_user):
    #-------------------- socket initial-------------------
    peerConnectServerSocket= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    peerConnectServerSocket.connect((self.serverHost, self.serverPort))
    #-------------------------------------------------------

    #------------------ send and receive--------------------
    peerConnectServerSocket.send(bytes("Creation", "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    # --------------------------------------------------------

    #--------------Send new user to server----------------------   
    peerConnectServerSocket.send(json.dumps(new_user).encode("utf-8")) # chuyển từ Object sang Json rồi gửi cho TRACKER
    response = peerConnectServerSocket.recv(4096)  # success
    response_data = response.decode('utf-8') 
    #---------------------------------------------------------

    #---------------send cancel command to close the connection---------------------
    peerConnectServerSocket.send(bytes("Cancel", "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    #-----------------------------------------------------------------------------

    peerConnectServerSocket.close()
    return response_data

  def seedingFileCompleted(self, filePath):
     #-------------------- socket initial-------------------
    peerConnectServerSocket= socket.socket()
    peerConnectServerSocket.connect((self.serverHost, self.serverPort))
    #-------------------------------------------------------
    
    #------------------ send and receive--------------------
    peerConnectServerSocket.send(bytes("Upload", "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    # --------------------------------------------------------
      
    #--------------Send file Name to server----------------------   
    peerConnectServerSocket.send(bytes(filePath, "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    #---------------------------------------------------------
      
    #----------------Send peerHost and port--------------------
    peerConnectServerSocket.send(bytes(self.peerHost, "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    peerConnectServerSocket.send(bytes(str(self.peerPort), "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    #------------------------------------------------------------
    
    #-------------Send size of file--------------------------------
    sizeOfFile= os.path.getsize(filePath)
    peerConnectServerSocket.send(bytes(str(sizeOfFile), "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    #---------------------------------------------------
    
    #---------------send cancel command to close the connection---------------------
    peerConnectServerSocket.send(bytes("Cancel", "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    #-----------------------------------------------------------------------------
    
    #close the socket
    peerConnectServerSocket.close()
    #-------------------
    
  def implementSharing(self, info_hash, file_path, magnet_text):
    try:
      #-------------------- socket initial-------------------
      peerConnectServerSocket= socket.socket()
      peerConnectServerSocket.connect((self.serverHost, self.serverPort))
      #-------------------------------------------------------
      
      #------------------ send and receive--------------------
      peerConnectServerSocket.send(bytes("Sharing", "utf-8"))
      peerConnectServerSocket.recv(4096)  # success
      # --------------------------------------------------------
        
      #-------------------Send inform of peer------------------------
      peerInform= pickle.dumps([self.peerHost, self.peerPort])
      peerConnectServerSocket.sendall(peerInform)
      peerConnectServerSocket.recv(4096) # success
      #--------------------------------------------------------------

      #--------------Send file Name to server----------------------   
      peerConnectServerSocket.send(bytes(info_hash, "utf-8"))
      peerConnectServerSocket.recv(4096)  # success
      #---------------------------------------------------------
        
      #----------------Send peerHost and port--------------------
      peerConnectServerSocket.send(bytes(self.peerHost, "utf-8"))
      peerConnectServerSocket.recv(4096)  # success
      peerConnectServerSocket.send(bytes(str(self.peerPort), "utf-8"))
      peerConnectServerSocket.recv(4096)  # success
      #------------------------------------------------------------
      
      #----------------Send fileName--------------------
      fileName = os.path.basename(file_path)
      peerConnectServerSocket.send(bytes(str(fileName),"utf-8"))
      peerConnectServerSocket.recv(4096)
      #------------------------------------------------------------
      
      #----------------Send magnet text--------------------
      peerConnectServerSocket.send(bytes(str(magnet_text),"utf-8"))
      peerConnectServerSocket.recv(4096)
      #------------------------------------------------------------        
      
      #---------------send cancel command to close the connection---------------------
      peerConnectServerSocket.send(bytes("Cancel", "utf-8"))
      peerConnectServerSocket.recv(4096)  # success
      #-----------------------------------------------------------------------------
      
      #close the socket
      peerConnectServerSocket.close()
      #-------------------
      
      """#-----------------get fileName--------------------
      fileName = os.path.basename(filePath)
      #------------------------------------------------
      messagebox.showinfo("Successful", "Upload file "+ str(fileName)+ " completed!")
      PEER_FEObject.fileUploaded.append(fileName)
      PEER_FEObject.showFileUploaded(fileName)"""
    except Exception as e:
      messagebox.showerror("Error", f"Đã xảy ra lỗi: {e}")
  
  def implementReceiveListFileExist(self):
    #-------------------- socket initial-------------------
    peerConnectServerSocket= socket.socket()
    peerConnectServerSocket.connect((self.serverHost, self.serverPort))
    #-------------------------------------------------------
    
    #------------------ send and receive--------------------
    peerConnectServerSocket.send(bytes("fileExist", "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    # ----------------------------------------------------
    
    peerConnectServerSocket.send(bytes("SUCCESS", "utf-8"))
    
    #----------------Receive list file exist-----------------------
    listFileExist= pickle.loads(peerConnectServerSocket.recv(10240))
    peerConnectServerSocket.send(bytes("SUCCESS", "utf-8"))
    #---------------------------------------------------------------
    
    peerConnectServerSocket.recv(4096)
    
    #---------------send cancel command to close the connection---------------------
    peerConnectServerSocket.send(bytes("Cancel", "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    #-----------------------------------------------------------------------------
    
    #close the socket
    peerConnectServerSocket.close()
    #-------------------
    
    return listFileExist
  
  def implementJoinToLAN(self):
    #-------------------- socket initial-------------------
    peerConnectServerSocket= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    peerConnectServerSocket.connect((self.serverHost, self.serverPort))
    #-------------------------------------------------------
    
    #------------------ send and receive--------------------
    peerConnectServerSocket.send(bytes("Join to LAN", "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    # ----------------------------------------------------
    
    #-------------------Send inform of peer------------------------
    peerInform= pickle.dumps([self.peerHost, self.peerPort])
    peerConnectServerSocket.sendall(peerInform)
    peerConnectServerSocket.recv(4096) # success
    #--------------------------------------------------------------
    
    peerConnectServerSocket.send(bytes("CONFIRM", "utf-8")) # new insert
    
    #---------------Receive the list of peers-------------------------
    listPeer= pickle.loads(peerConnectServerSocket.recv(4096))
    peerConnectServerSocket.send(bytes("SUCCESS", "utf-8"))  # confirm
    #------------------------------------------------------------------
    
    peerConnectServerSocket.recv(4096)
    
    #---------------send cancel command to close the connection---------------------
    peerConnectServerSocket.send(bytes("Cancel", "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    #-----------------------------------------------------------------------------
    
    #close the socket
    peerConnectServerSocket.close()
    #-------------------
       
  def threadListenServerOrPeers(self, conn, addr):
    try:
      while not self.stopFlag.is_set():
        #----------------Receive Type of connect server or peer-----------------------------
        serverOrPeer = str(conn.recv(4096), "utf-8")
        conn.send(bytes("SUCCESS", "utf-8"))  # confirm
        #-----------------------------------------------------------------------------------

        #---------------Classify the serverOrPeer-----------------------------------------
        if serverOrPeer== "SERVER":
          #-----------------Receive FileName-------------------------------------
          filePartPath= str(conn.recv(4096), "utf-8")
          # PEER_FEObject.showFileUploaded(filePartPath)
          conn.send(bytes("SUCCESS", "utf-8"))  # confirm
          #---------------------------------------------------------------------
          
          #-------------------------Receive size of file-----------------------------
          sizeOfFile= int(str(conn.recv(4096), "utf-8"))
          conn.send(bytes("SUCCESS", "utf-8"))  # confirm
          #-------------------------------------------------------------------------

          #--------------Receive the content of file-------------------------------
          with open(filePartPath, "wb") as file:
            content= b''
            while sizeOfFile > 0:
              data= conn.recv(min(10240, sizeOfFile))
              if not data:
                break
              content+= data
              sizeOfFile-= len(data)
            file.write(content)
            file.close()
          conn.send(bytes("SUCCESS", "utf-8"))  # confirm
          #-------------------------------------------------------------------------
          
          #-----------------------Cancel command------------------------------------
          cancelCommand= str(conn.recv(4096), "utf-8")
          conn.send(bytes("SUCCESS", "utf-8"))  # confirm
          self.stopFlag.set()
          #-----------------------------------------------------------------------    
        elif serverOrPeer== "Torrent":
          file_name = str(conn.recv(4096),"utf-8")
          conn.send(bytes("SUCCESS", "utf-8")) #confirm
          # Loại bỏ phần mở rộng hiện tại và thay bằng .torrent
          file_name = file_name + ".torrent"

          #----------------------------------------------
          script_dir = os.path.dirname(os.path.abspath(__file__))  # Đường dẫn đến thư mục chứa chương trình
          torrent_folder = os.path.join(script_dir, "Torrent_files")

          # Xác định đường dẫn đầy đủ của tệp torrent
          torrent_file_path = os.path.join(torrent_folder, file_name)
          # Kiểm tra xem tệp có tồn tại không
          if not os.path.isfile(torrent_file_path):
            raise FileNotFoundError(f"The torrent file '{file_name}' was not found in '{torrent_folder}'.")
          
          # Đọc và giải mã nội dung của tệp torrent
          with open(torrent_file_path, 'rb') as torrent_file:
             torrent_data = bencodepy.decode(torrent_file.read())

          #---------------------------------------------------------------------------------------
          torrent_info = {
              'info': {
                  'name': torrent_data.get(b'info', {}).get(b'name', b'').decode('utf-8'),
                  'piece length': torrent_data.get(b'info', {}).get(b'piece length', 0),
                  'pieces': torrent_data.get(b'info', {}).get(b'pieces', b'').hex(),  # Chuyển sang chuỗi hex
                  'length': torrent_data.get(b'info', {}).get(b'length', 0),
                  'files': [
                      {
                          'path': [p.decode('utf-8') for p in file[b'path']],
                          'length': file[b'length'],
                          'piece indices': file.get(b'piece indices', []),
                          'info_hash': file.get(b'info_hash', b'').decode('utf-8')  # Giải mã thành chuỗi UTF-8
                      } for file in torrent_data.get(b'info', {}).get(b'files', [])
                  ]
              },
              'announce': torrent_data.get(b'announce', b'').decode('utf-8'),
              'creation date': torrent_data.get(b'creation date', 0),
              'comment': torrent_data.get(b'comment', b'').decode('utf-8'),
              'file_path': torrent_data.get(b'file_path', b'').decode('utf-8')
          }

          # Chuyển `torrent_info` thành JSON và gửi qua socket
          torrent_info_serialized = json.dumps(torrent_info, ensure_ascii=False)

          # Gửi dữ liệu qua socket
          conn.sendall(torrent_info_serialized.encode('utf-8'))
          conn.recv(4096) #confirm
          #---------------------------------------------------------------------------------------
        elif serverOrPeer== "PEER":
            #-------------------- recieve info_hash to peer-------------------
            file_name = str(conn.recv(4096), "utf-8")
            conn.send(bytes("SUCCESS", "utf-8"))  # confirm
            #-----------------------------------------------------------------

            #------------------recieve range of index_piece----------------------
            piece_index_start = int(str(conn.recv(4096), "utf-8"))
            conn.send(bytes("SUCCESS", "utf-8"))
            piece_index_end = int(str(conn.recv(4096), "utf-8"))
            conn.send(bytes("SUCCESS", "utf-8"))
            number_of_pieces = int(str(conn.recv(4096), "utf-8"))
            conn.send(bytes("SUCCESS", "utf-8"))
            # Giải mã JSON thành mảng
            data = conn.recv(4096)
            all_piece_indices = json.loads(data.decode()) # Giải mã JSON thành mảng
            conn.send(bytes("SUCCESS", "utf-8")) #confirm
            #-----------------------------------------------------------------

            file_name = file_name + ".torrent"
            #----------------------------------------------
            script_dir = os.path.dirname(os.path.abspath(__file__))  # Đường dẫn đến thư mục chứa chương trình
            torrent_folder = os.path.join(script_dir, "Torrent_files")

            # Xác định đường dẫn đầy đủ của tệp torrent
            torrent_file_path = os.path.join(torrent_folder, file_name)
            # Kiểm tra xem tệp có tồn tại không
            if not os.path.isfile(torrent_file_path):
              raise FileNotFoundError(f"The torrent file '{file_name}' was not found in '{torrent_folder}'.")

            #----------------------------------------------
            # Đọc và giải mã nội dung của tệp torrent
            with open(torrent_file_path, 'rb') as torrent_file:
               torrent_data = bencodepy.decode(torrent_file.read())
               # Trích xuất `torrent_info`
               torrent_info = torrent_data.get(b'info', {})
               # Lấy danh sách tệp từ `torrent_info`
               files = torrent_info.get(b'files', [])
            #-------------------------------------------------------------------
            # Tạo một từ điển để ánh xạ info_hash tới file_path
            file_map = {
                file.get(b'info_hash').decode(): os.path.join(torrent_folder, *[p.decode() for p in file[b'path']])
                for file in files if b'info_hash' in file
            }

            #----------------- Truyền file theo all_piece_indices ----------------
            for info_hash, index in all_piece_indices[piece_index_start:piece_index_end]:  # Sử dụng khoảng từ start đến end-1
               file_path = file_map.get(info_hash)

               if file_path:
                  # Tính toán kích thước của từng phần
                  start = index * subFileSize  # Tính toán vị trí bắt đầu cho phần này

                  # Kiểm tra kích thước tệp để điều chỉnh kích thước phần cuối cùng
                  file_size = os.path.getsize(file_path)  # Lấy kích thước tệp
                  end = min(start + subFileSize, file_size)  # Tính toán vị trí kết thúc cho phần này
                  try:
                     # Mở tệp và đọc phần tương ứng
                     with open(file_path, "rb") as file:
                        file.seek(start)  # Di chuyển con trỏ đến vị trí bắt đầu
                        piece_data = file.read(end - start)  # Đọc dữ liệu cho phần hiện tại

                        if not piece_data:  # Nếu không còn dữ liệu để đọc
                           break
                        
                        conn.sendall(piece_data)  # Gửi dữ liệu qua socket
                        conn.recv(4096)  # Chờ phản hồi từ peer
                        print(f"Sent piece {index} of file {file_path}")
                  except Exception as e:
                     print(f"Error sending data: {e}")
                     conn.send(bytes("ERROR", "utf-8"))  # Thông báo lỗi
               else:
                  print(f"File path not found for info_hash {info_hash}")
                  conn.send(bytes("ERROR", "utf-8"))  # Thông báo lỗi khi không tìm thấy file
            #-------------------------------------------------------------------
        elif serverOrPeer== "Cancel":
           self.stopFlag.set()
    except Exception as e:
      print(f"Error occurred: {e}")
    finally:
        # Đảm bảo luôn đóng kết nối
        conn.close()
  
  def listenServerOrPeers(self):
    self.peerSocket.bind((self.peerHost, self.peerPort))
    self.peerSocket.listen(10)
    
    while self.running:
      try:
        conn, addr= self.peerSocket.accept()
        self.connections.append(conn)  # Thêm kết nối vào danh sách
        self.stopFlag.clear()
        #self.stopFlag= threading.Event()
        condition= Thread(target= self.threadListenServerOrPeers, args= [conn, addr])
        condition.start()
      except OSError:
        break # Nếu socket đã bị đóng, thoát vòng lặp
      except Exception as e:
        print(f"Error: {e}")
      time.sleep(0.1)  # Thêm thời gian chờ để tránh CPU sử dụng 100%

  def stop(self):
        self.stateClose()
        self.running = False  # Đặt biến cờ thành False để dừng vòng lặp
        self.peerSocket.close()  # Đóng socket để ngăn chặn kết nối mới
        for conn in self.connections:  # Đóng tất cả các kết nối
            conn.close()
        self.connections.clear()  # Xóa danh sách các kết nối

  def getTorrentInfo(self,file_name, peer):
    peerconn= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
      peerconn.connect((peer['ip_address'], peer['ip_port']))
      #-------------------------------------------------------------------
      peerconn.send(bytes("Torrent", "utf-8"))
      peerconn.recv(4096)
      #--------------------------------------------------------------------

      #--------------------------------------------------------------------
      peerconn.send(bytes(file_name, "utf-8"))
      peerconn.recv(4096) #confirm
      #--------------------------------------------------------------------

      #--------------------------------------------------------------------
      data = peerconn.recv(10*1024).decode('utf-8')
      torrent_info = json.loads(data)
      peerconn.send(bytes("SUCCESS", "utf-8"))
      #--------------------------------------------------------------------

      peerconn.send(bytes("Cancel","utf-8"))
      peerconn.recv(4096)
      peerconn.close()

      return torrent_info

    except (socket.timeout, socket.error) as e:
      print(f"Network error occurred: {e}")
    
  def implementDownload(self, info_hash, serverhost, serverport, size, file_name, download_dir):
    #-------------------- socket initial-------------------
    peerConnectServerSocket= socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        peerConnectServerSocket.connect((self.serverHost, self.serverPort))
        #-------------------------------------------------------
        
        #------------------ send and receive--------------------------------
        peerConnectServerSocket.send(bytes("Download", "utf-8"))
        peerConnectServerSocket.recv(4096)  # success
        #---------------------------------------------------------------

        #-------------------Send inform of peer------------------------
        peerInform= pickle.dumps([self.peerHost, self.peerPort])
        peerConnectServerSocket.sendall(peerInform)
        peerConnectServerSocket.recv(4096) # success
        #--------------------------------------------------------------

        #----------------Send fileName------------------------------
        peerConnectServerSocket.send(bytes(str(file_name),"utf-8"))
        peerConnectServerSocket.recv(4096)
        #------------------------------------------------------------
        
        #------------------Send info_hash want to down------------------------------
        peerConnectServerSocket.send(bytes(info_hash,"utf-8"))
        peerConnectServerSocket.recv(4096)
        #-------------------------------------------------------------------
        
        #--------------------Send peerHost and peerPort----------------------
        peerConnectServerSocket.send(bytes(serverhost, "utf-8"))
        peerConnectServerSocket.recv(4096)  # success
        peerConnectServerSocket.send(bytes(str(serverport), "utf-8"))
        peerConnectServerSocket.recv(4096)  # success
        #--------------------------------------------------------------------
        
        peerConnectServerSocket.send(bytes("SUCCESS", "utf-8")) #keep contact

        # Nhận danh sách peer
        data = peerConnectServerSocket.recv(4096).decode('utf-8')
        peerConnectServerSocket.send(bytes("SUCCESS", "utf-8"))
        list_peer = json.loads(data)

        #---------------Close connection--------------------------------------
        peerConnectServerSocket.send(bytes("Cancel", "utf-8"))
        peerConnectServerSocket.recv(4096)  # success
        peerConnectServerSocket.close()
        #---------------------------------------------------------------------
        if len(list_peer) == 0:
            messagebox.showinfo("Not success","Now there are no active peer that has this file/folder!")
            return
        torrent_info = self.getTorrentInfo(file_name, list_peer[0])
        #---------------------------------------------------------------------

        number_of_pieces = 0
        for file in torrent_info["info"]["files"]:
            piece_indices = file["piece indices"]
            number_of_pieces += len(piece_indices)
        
        piece_array = {}
        
        # Lấy số lượng peer tối đa là 5
        num_peer_to_use = min(5, len(list_peer))

        # Chia đều số lượng piece cho từng peer
        pieces_per_peer = number_of_pieces // num_peer_to_use
        remainder = number_of_pieces % num_peer_to_use
        threads = []

        # Lấy danh sách tất cả các piece indices với thông tin tương ứng
        all_piece_indices = []
        for file in torrent_info["info"]["files"]:
            for index in file["piece indices"]:
                all_piece_indices.append((file["info_hash"], index))   
        
        # Khởi tạo chỉ số bắt đầu
        start = 0
        for i in range(num_peer_to_use):
            end = start + pieces_per_peer + (1 if i < remainder else 0)  # Thêm phần dư vào peer
            peer = list_peer[i]  # Chọn peer theo chỉ số
            # Tạo luồng cho từng khoảng phần tệp
            thread = threading.Thread(target=self.download_piece, args=(start, end, all_piece_indices, peer, file_name, number_of_pieces, piece_array))
            threads.append(thread)
            thread.start()
            print(f"Peer {peer}: Downloading from {start} to {end}")
            start = end  # Cập nhật chỉ số bắt đầu cho peer tiếp the
        # Chờ tất cả các luồng hoàn thành
        for thread in threads:
            thread.join()
        
        # Tạo từ điển để ánh xạ dữ liệu
        piece_map = {}
        for idx, (ih, index) in enumerate(all_piece_indices):
            if ih not in piece_map:
                piece_map[ih] = {}
            piece_map[ih][index] = piece_array[idx]  # Ánh xạ mảnh dữ liệu theo info_hash và index

        # Kiểm tra nếu là file đơn hoặc thư mục
        if "files" in torrent_info["info"] and len(torrent_info["info"]["files"]) > 1:
            # Xử lý thư mục
            # Ghép các mảnh theo thứ tự và ghi vào file cuối cùng
            download_directory = os.path.join(download_dir, file_name)
        else:
            download_directory = download_dir
        
        # Tạo thư mục con nếu chưa tồn tại
        os.makedirs(download_directory, exist_ok=True)

        for file in torrent_info["info"]["files"]:
            info_hash = file["info_hash"]
            full_path = os.path.join(*file["path"])
            relative_path = os.path.relpath(full_path, start=torrent_info["file_path"])
            file_path = os.path.join(download_directory, relative_path)

            # Tạo đường dẫn cho file hoặc thư mục
            if len(torrent_info["info"]["files"]) > 1:  # Nếu là thư mục
                file_path = os.path.join(download_directory, relative_path)  # Đường dẫn đến file trong thư mục
            else:  # Nếu là file đơn
                file_path = os.path.join(download_directory, os.path.basename(full_path))  # Chỉ lấy tên file
            
            # Tạo thư mục con nếu chưa tồn tại
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Ghi từng mảnh vào tệp theo đúng thứ tự
            with open(file_path, "wb") as final_file:
                indices = [idx for ih, idx in all_piece_indices if ih == info_hash]
                for index in indices:
                    piece_data = piece_map.get(info_hash, {}).get(index)
                    if piece_data is not None:
                        final_file.write(piece_data)  # Ghi dữ liệu vào tệp
                        print(f"Writing piece {index} to {file_path}")
                    else:
                        print(f"Error: Missing data for piece {index} of file {file_path}")

        print("DOWNLOAD SUCCESS")
        messagebox.showinfo("notification","DOWNLOAD SUCCESS!")
    except (socket.timeout, socket.error) as e:
        print(f"Network error occurred: {e}")
       
  def download_piece(self, start, end, all_piece_indices, peer, file_name, number_of_pieces, piece_array):
    try:
        #-------------------- socket initial-------------------
        peerConnectPeerSocket= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        peerConnectPeerSocket.connect((peer['ip_address'], peer['ip_port']))
        #-------------------------------------------------------
        
        #-------------------- socket connect to peer-------------------
        peerConnectPeerSocket.send(bytes("PEER", "utf-8"))
        peerConnectPeerSocket.recv(4096)
        #---------------------------------------------------------------

        #-------------------- send file_name to peer-------------------
        peerConnectPeerSocket.send(bytes(file_name, "utf-8"))
        peerConnectPeerSocket.recv(4096)  # confirm
        #--------------------------------------------------------------

        #---------------------send range of index_piece-------------------
        peerConnectPeerSocket.send(bytes(str(start), "utf-8"))
        peerConnectPeerSocket.recv(4096) #success
        
        peerConnectPeerSocket.send(bytes(str(end), "utf-8"))
        peerConnectPeerSocket.recv(4096) #success
        peerConnectPeerSocket.send(bytes(str(number_of_pieces), "utf-8"))
        peerConnectPeerSocket.recv(4096) #success
        peerConnectPeerSocket.send(json.dumps(all_piece_indices).encode())
        peerConnectPeerSocket.recv(4096) #success
        #------------------------------------------------------------------

        #----------------- Truyền file theo all_piece_indices ----------------
        start_point = 0

        for i in all_piece_indices[start:end]:  # Sử dụng khoảng từ start đến end-1
            piece_data = peerConnectPeerSocket.recv(subFileSize)
            peerConnectPeerSocket.send(bytes("SUCCESS", "utf-8"))

            if not piece_data:
                print("No data received for piece", i)
                break
            piece_array[start_point] = piece_data
            start_point += 1
            print(f"Received piece {start_point} from {peer['ip_address']}:{peer['ip_port']}")

    except ConnectionResetError as e:
        print(f"Connection error: {e}")
    except Exception as e:
        print(f"Unknown error: {e}")
    finally:
        peerConnectPeerSocket.send(bytes("Cancel", "utf-8"))
        peerConnectPeerSocket.recv(4096)
        peerConnectPeerSocket.close()
     
  def sendStatusToTracker(self, file_path, piece_number):
    # Gửi trạng thái tới tracker (cần được định nghĩa cụ thể)
    peerConnectServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peerConnectServerSocket.connect((self.serverHost, self.serverPort))
    peerConnectServerSocket.send(bytes("STATUS", "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    peerConnectServerSocket.send(bytes(file_path, "utf-8"))
    peerConnectServerSocket.send(bytes(str(piece_number), "utf-8"))
    peerConnectServerSocket.close()