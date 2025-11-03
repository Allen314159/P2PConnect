import tkinter as tk
import os
import bencodepy
import hashlib
import urllib.parse
import re
import signal
from threading import Thread
from tkinter import *
import sys
import socket
import customtkinter as ctk
from tkinter import messagebox
from PEER_BE import WIDTH, HEIGHT, subFileSize, PEER_BE
from tkinter import filedialog

class SlidePanel(ctk.CTkFrame):
  def __init__(self,parent,start_pos,end_pos):
      super().__init__(master=parent)
      
      self.start_pos=start_pos
      self.end_pos=end_pos
      self.width = abs(start_pos-end_pos)
      
      self.pos = start_pos
      self.in_start_pos = True
      
      self.place(relx=self.start_pos,rely=0,relwidth=self.width,relheight=0.65)
      
  def animate(self):
      if self.in_start_pos:
          self.animate_forward()
      else:
          self.animate_backward()
  def animate_forward(self):
      if self.pos > self.end_pos:
          self.pos -= 0.008
          self.place(relx=self.pos,rely=0,relwidth=self.width,relheight=0.65)
          self.after(10,self.animate_forward)
      else:
          self.in_start_pos = False
  def animate_backward(self):
      if self.pos < self.start_pos:
          self.pos += 0.008
          self.place(relx=self.pos,rely=0,relwidth=self.width,relheight= 0.65)
          self.after(10,self.animate_backward)
      else:
          self.in_start_pos = True

class PEER_FE(ctk.CTk):
  
  def __init__(self, peerHost, peerPort):
    super().__init__()
    
    self.numberOfFileUploaded= 0
    self.numberOfFileDownloaded= 0
    
    self.fileUploaded= []
    self.fileDownloaded= []
    self.fileExist= []

    self.peerHost= peerHost
    self.peerPort= peerPort

    self.nameServer= ""

    # Initial frame for each page
    self.frameInitialPage= ctk.CTkFrame(self, width=1020, height=700)
    self.frameAcountPage= ctk.CTkFrame(self, width=1020, height=700)
    self.frameConnectToServer= ctk.CTkFrame(self, width=WIDTH, height=HEIGHT)
    self.frameMainPage= ctk.CTkFrame(self, width=WIDTH, height=HEIGHT)
    self.frameExecuteUploadButton= ctk.CTkFrame(self, width=WIDTH, height=HEIGHT)
    self.frameExecuteDownloadButton= ctk.CTkFrame(self, width=WIDTH, height=HEIGHT)
    
    self.textFileExist= ctk.CTkTextbox(self.frameExecuteDownloadButton)
    
    self.animatePanelDownload = SlidePanel(self.frameExecuteDownloadButton, 1, 0.7)
    self.outputFileDownload = ctk.CTkTextbox(self.animatePanelDownload)
    
    self.animatePaneUpload = SlidePanel(self.frameExecuteUploadButton, 1, 0.7)
    self.outputFileUpload = ctk.CTkTextbox(self.animatePaneUpload)

    self.ServerHost = None
    self.ServerPort = None

    self.resizable(False, False)
    self.title("Bittorrent File Sharing")
    self.geometry("900x600")
    
    # Set close window event
    self.protocol("WM_DELETE_WINDOW", lambda: self.on_close())
  
    self.current_frame = self.initialPage()
    self.current_frame.pack()

  def on_close(self):  
    PEER_BEObject.stateClose()
    print("Closing window...")
    PEER_BEObject.stopFlag.set()  # Stop threads
    self.destroy()
    
  def switch_frame(self, frame):
    self.current_frame.pack_forget()
    self.current_frame = frame()
    self.current_frame.pack(padx = 0)   
    
  def initialPage(self):

    ctk.set_appearance_mode("light")
    
    frame_label = ctk.CTkLabel(self.frameInitialPage, text="WELCOME TO\n BITTORENT FILE SHARING", font=("Arial",40,"bold"))
    frame_label.place(relx=0.5,rely=0.4,anchor=tk.CENTER)

    button_Tracker1 = ctk.CTkButton(self.frameInitialPage, text="Tracker 1 Server", font=("Arial", 15, "bold"),
                                    command=lambda:self.executeChooseTrackerButton("Tracker1"))
    button_Tracker1.place(relx=0.4,rely=0.7,anchor=tk.CENTER)
    
    button_Tracker2 = ctk.CTkButton(self.frameInitialPage, text="Tracker 2 Server", font=("Arial", 15, "bold"),
                                        command=lambda:self.executeChooseTrackerButton("Tracker2"))
    button_Tracker2.place(relx=0.6,rely=0.7,anchor=tk.CENTER)
    
    return self.frameInitialPage
  
  def executeChooseTrackerButton(self, location):
    if location == "Tracker1":
      PEER_BEObject.serverHost = "10.229.11.50"
      PEER_BEObject.serverPort = 8080
      self.nameServer = "Tracker 1 Server"
      PEER_BEObject.implementJoinToLAN()
    elif location == "Tracker2":
      PEER_BEObject.serverHost = "10.229.11.50"
      PEER_BEObject.serverPort = 8081
      self.nameServer = "Tracker2 Server"
      PEER_BEObject.implementJoinToLAN()
    print("Connect success")
    self.switch_frame(self.mainPage)
    
  def accountPage(self):
    frame_label = ctk.CTkLabel(self.frameAcountPage, text="WELCOME TO\n BITTORENT FILE SHARING", font=("Arial",40,"bold"))
    frame_label.place(relx=0.5,rely=0.4,anchor=tk.CENTER)

    button_back = ctk.CTkButton(self.frameAcountPage, text="Back", font=("Arial", 15, "bold"),
                                    command=lambda:self.switch_frame(self.initialPage))
    button_back.place(relx=0.5,rely=0.8,anchor=tk.CENTER)    

    return self.frameAcountPage

  def mainPage(self):
      
    frame_label = ctk.CTkLabel(self.frameMainPage, text=self.nameServer, font=("Arial",40,"bold"))
    frame_label.place(relx=0.5,rely=0.2,anchor=tk.CENTER)
    
    frame_label = ctk.CTkLabel(self.frameMainPage, text="INFORMATION OF PEER", font=("Arial",20, "bold"))
    frame_label.place(relx=0.5,rely=0.4,anchor=tk.CENTER)
    
    frame_label = ctk.CTkLabel(self.frameMainPage, text="Peer Host: "+ self.peerHost, font=("Arial", 15 ))
    frame_label.place(relx=0.5,rely=0.5,anchor=tk.CENTER)
    
    frame_label = ctk.CTkLabel(self.frameMainPage, text="Peer Port: "+ str(self.peerPort), font=("Arial", 15))
    frame_label.place(relx=0.5,rely=0.55,anchor=tk.CENTER)
    
    #----------------Button UPLOAD---------------------------------------------------------
    self.btn_upload = ctk.CTkButton(self.frameMainPage, text="UPLOAD", font=("Arial", 20, "bold"),
                                    command=lambda:self.switch_frame(self.executeUploadButton))
    self.btn_upload.place(relx=0.33,rely = 0.7,anchor =tk.CENTER)
    #---------------------------------------------------------------------------------------
    
    #---------------------------Button DOWNLOAD----------------------------------------------
    self.btn_download = ctk.CTkButton(self.frameMainPage, text="DOWNLOAD", font=("Arial", 20, "bold"),
                                        command=lambda:self.switch_frame(self.executeDownloadButton))
    self.btn_download.place(relx=0.67,rely = 0.7,anchor =tk.CENTER)
    #----------------------------------------------------------------------------------------

    #----------------------------Button CHANGE THEME--------------------------------------------------------
    """self.btn_show_listpeer = ctk.CTkButton(self.frameMainPage, text="CHANGE THEME", font=("Arial", 20, "bold"),
                                            command= self.changeTheme)
    self.btn_show_listpeer.place(relx= 0.7,rely=0.7,anchor = tk.CENTER)"""
    #--------------------------------------------------------------------------------------------------
  
    return self.frameMainPage
  
  def executeUploadButton(self):

    header_upload = ctk.CTkLabel(self.frameExecuteUploadButton, text="UPLOAD FILE", font=("Arial", 40,"bold"))
    header_upload.place(relx = 0.5,rely=0.3,anchor = CENTER)
    
    self.outputFileUpload.place(relx=0.5,rely=0.55,anchor=ctk.CENTER,relwidth=0.8,relheight=0.8)
    self.outputFileUpload.configure(state=DISABLED)

    upload_label = ctk.CTkLabel(self.frameExecuteUploadButton, text="Choose the file you want to share", font=("Arial", 20,"bold"))
    upload_label.place(relx = 0.5, rely=0.43,anchor = tk.CENTER)

    upload_entry = ctk.CTkEntry(self.frameExecuteUploadButton, width=200, height= 10, placeholder_text="Enter path to file")
    upload_entry.place(relx = 0.6, rely=0.5,anchor = tk.CENTER)
    # Nút mở cửa sổ chọn file
    btn_browse = ctk.CTkButton(self.frameExecuteUploadButton, text="Browse", font=("Arial", 20,"bold"),
                               command=lambda: self.browseFile(upload_entry))
    btn_browse.place(relx=0.4, rely=0.5, anchor=tk.CENTER)
    
    btn_BACK= ctk.CTkButton(self.frameExecuteUploadButton,text="BACK", font=("Arial", 20,"bold"),
                          command =lambda: self.switch_frame(self.mainPage))
    btn_BACK.place(relx= 0.3, rely= 0.7, anchor= tk.CENTER)
    
    btn_upload = ctk.CTkButton(self.frameExecuteUploadButton, text="UPLOAD", font=("Arial", 20,"bold"),
                                command=lambda:(self.getFileUpload(upload_entry)))      
    btn_upload.place(relx = 0.7,rely=0.7,anchor = CENTER)
  

    # btn_view_repo=ctk.CTkButton(self.frameExecuteUploadButton,text="FILE UPLOADED", font=("Arial", 20,"bold"),
    #                       command =lambda:self.animatePaneUpload.animate())
    # btn_view_repo.place(relx= 0.7, rely= 0.7, anchor= tk.CENTER)
    
    # list_header=ctk.CTkLabel(self.animatePaneUpload, text = " LIST FILES ", font=("Comic Sans",30,"bold"))
    # list_header.place(relx=0.5,rely=0.1,anchor=ctk.CENTER)
    # list_header.pack()

    return self.frameExecuteUploadButton

  def browseFile(self, upload_entry):
    # Tạo cửa sổ chọn file hoặc thư mục
    file_path = tk.filedialog.askopenfilename(title="Select a File",
                                               filetypes=(("All Files", "*.*"),))
    if file_path:  # Nếu chọn file
        upload_entry.delete(0, tk.END)  # Xóa nội dung trước đó của entry
        upload_entry.insert(0, file_path)  # Chèn đường dẫn của file được chọn
    else:  # Nếu không chọn file, kiểm tra xem người dùng có chọn thư mục không
        folder_path = tk.filedialog.askdirectory(title="Select a Folder")
        if folder_path:  # Nếu chọn thư mục
            upload_entry.delete(0, tk.END)  # Xóa nội dung trước đó của entry
            upload_entry.insert(0, folder_path)  # Chèn đường dẫn của thư mục được chọn
  
  def create_torrent(self, path):
    piece_length = 524288  # 512KB cho mỗi piece
    torrent_info = {
        'info': {
            'name': os.path.basename(path),
            'piece length': piece_length,
            'pieces': b'',  # Mảng chứa hash của từng piece (để cập nhật sau)
            'length': 0,  # Tổng kích thước sẽ được cập nhật sau
            'files': []  # Chứa thông tin về các file nếu là thư mục
        },
        'announce': f"tcp://{PEER_BEObject.serverHost}:{PEER_BEObject.serverPort}",
        'creation date': int(os.path.getmtime(path)),
        'comment': 'Created by my torrent application',
        'file_path': os.path.abspath(path)  # Thêm đường dẫn tuyệt đối của thư mục gốc
    }

    # Kiểm tra xem path là file hay thư mục
    if os.path.isfile(path):
        # Nếu là file đơn lẻ, xử lý như bình thường
        file_size = os.path.getsize(path)
        if file_size == 0:
            raise ValueError("File is empty, cannot create torrent.")
        
        pieces = []
        with open(path, 'rb') as f:
            while True:
                piece = f.read(piece_length)
                if not piece:
                    break
                pieces.append(hashlib.sha1(piece).digest())

        # Tính info_hash cho file đơn
        info_hash = hashlib.sha1(b''.join(pieces)).hexdigest()

        torrent_info['info']['pieces'] = b''.join(pieces)
        torrent_info['info']['length'] = file_size
        torrent_info['info']['files'].append({
            'path': [os.path.abspath(path)],  # Lưu đường dẫn tuyệt đối của file đơn
            'length': file_size,
            'piece indices': list(range(len(pieces))),  # Lưu chỉ số của các piece
            'info_hash': info_hash  # Lưu info_hash
        })

    elif os.path.isdir(path):
        # Nếu là thư mục, duyệt qua các file trong thư mục (bao gồm cả thư mục con)
        total_length = 0
        for dirpath, _, filenames in os.walk(path):  # Sử dụng os.walk để duyệt qua tất cả thư mục
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                file_size = os.path.getsize(file_path)
                if file_size == 0:
                    raise ValueError(f"File '{filename}' is empty, cannot create torrent.")

                pieces = []
                with open(file_path, 'rb') as f:
                    while True:
                        piece = f.read(piece_length)
                        if not piece:
                            break
                        pieces.append(hashlib.sha1(piece).digest())

                # Tính info_hash cho file
                info_hash = hashlib.sha1(b''.join(pieces)).hexdigest()

                # Cập nhật thông tin cho file
                torrent_info['info']['files'].append({
                    'path': [os.path.abspath(file_path)],  # Lưu đường dẫn tuyệt đối của từng file
                    'length': file_size,
                    'piece indices': list(range(len(pieces))),  # Lưu chỉ số của các piece
                    'info_hash': info_hash  # Lưu info_hash
                })
                torrent_info['info']['pieces'] += b''.join(pieces)  # Cập nhật các piece
                total_length += file_size

        torrent_info['info']['length'] = total_length  # Cập nhật tổng kích thước

    else:
        raise ValueError("Path does not exist or is not a file or directory.")

    # Lưu file torrent vào thư mục Downloads
    program_dir = os.path.dirname(os.path.abspath(__file__))
    torrent_folder = os.path.join(program_dir, "Torrent_files")

     # Tạo thư mục nếu chưa tồn tại
    if not os.path.exists(torrent_folder):
       os.makedirs(torrent_folder)

    # Đường dẫn file torrent
    torrent_file_path = os.path.join(torrent_folder, f"{os.path.basename(path)}.torrent")

    # Ghi file torrent
    with open(torrent_file_path, 'wb') as torrent_file:
        torrent_file.write(bencodepy.encode(torrent_info))
    
    return torrent_file_path

  def create_magnet_link(self,torrent_file_path):
    # Đọc file torrent để lấy thông tin
    with open(torrent_file_path, 'rb') as torrent_file:
        torrent_info = bencodepy.decode(torrent_file.read())

    # Lấy info_hash
    info_hash = hashlib.sha1(bencodepy.encode(torrent_info[b'info'])).hexdigest()
    
    # Lấy tên file và tracker URL
    file_name = torrent_info[b'info'][b'name']
    file_size = torrent_info[b'info'][b'length']
    tracker_url = torrent_info[b'announce'].decode('utf-8')  # Chuyển đổi từ bytes sang str

    # Tạo magnet link
    magnet_link = f"magnet:?xt=urn:btih:{info_hash}&dn={urllib.parse.quote(file_name)}&tr={tracker_url}&xl={file_size}"
    
    info = [info_hash, magnet_link, file_size]
    return info

  def show_magnet_link(self, magnet_link):
    # Tạo một cửa sổ Toplevel
    top = tk.Toplevel()
    top.title("Magnet Link")
    top.geometry("400x200")  # Thiết lập kích thước cửa sổ dài hơn

    # Thêm nhãn
    label = ctk.CTkLabel(top, text="Your magnet link:",width=300, height=8)
    label.pack(pady=10)

    # Thêm Entry widget để hiển thị magnet link
    entry = ctk.CTkEntry(top, width=300, height=8)  # Thay đổi kích thước Entry
    entry.insert(0, magnet_link)  # Đưa magnet link vào Entry
    entry.pack(pady=10)

    # Hàm sao chép vào clipboard
    def copy_to_clipboard():
        entry.select_range(0, tk.END)  # Chọn toàn bộ nội dung
        entry.focus_set()  # Đặt con trỏ vào Entry
        top.clipboard_clear()  # Xóa clipboard
        top.clipboard_append(entry.get())  # Thêm nội dung vào clipboard
        messagebox.showinfo("Copied", "Magnet link copied to clipboard!")  # Thông báo cho người dùng

    # Khung để chứa nút Copy và Close
    button_frame = tk.Frame(top)
    button_frame.pack(pady=10)

    # Nút Copy
    copy_button = ctk.CTkButton(button_frame, text="Copy", command=copy_to_clipboard, width=15, height=8)
    copy_button.pack(side=tk.LEFT, padx=5)  # Nút Copy nằm bên trái

    # Nút Close
    close_button = ctk.CTkButton(button_frame, text="Close", command=top.destroy, width=15, height=8)
    close_button.pack(side=tk.LEFT, padx=5)  # Nút Close nằm bên phải

  def getFileUpload(self, upload_entry):
    filePathUpload = upload_entry.get()   # file path

    # Remove quotes if present
    if filePathUpload.startswith('"') and filePathUpload.endswith('"'):
        filePathUpload = filePathUpload[1:-1]

    # Convert backslashes to forward slashes
    filePathUpload = filePathUpload.replace('/', '\\')

    if not os.path.exists(filePathUpload):
      messagebox.showerror("Error", "File don't exist!")
      return

    torrent_file_path = self.create_torrent(filePathUpload)
    info = self.create_magnet_link(torrent_file_path)

    condition = Thread(target=PEER_BEObject.implementSharing, args=[info[0], filePathUpload, info[1]])
    condition.start()
    self.show_magnet_link(info[1])
    self.switch_frame(self.executeUploadButton)
         
  def showFileUploaded(self, fileName):
    # self.fileUploaded.append(fileName)

    self.outputFileUpload.configure(state=NORMAL)
    self.numberOfFileUploaded+= 1
    self.outputFileUpload.insert(ctk.END, f"{self.numberOfFileUploaded}.   \"{fileName}\"" +"\n\n" )

    self.outputFileUpload.see(ctk.END)
    self.outputFileUpload.configure(state=DISABLED)
  
  def showMoment(self):
    frame = ctk.CTkFrame(self,width=(WIDTH + 120),height=700)

    header_upload = ctk.CTkLabel(frame, text="WAITING A MOMENT!", font=("Arial", 40,"bold"))
    header_upload.place(relx = 0.5,rely=0.5,anchor = CENTER)
    
    return frame
      
  def executeDownloadButton(self):

    header_upload = ctk.CTkLabel(self.frameExecuteDownloadButton, text="DOWNLOAD FILE", font=("Arial", 40,"bold"))
    header_upload.place(relx = 0.5,rely=0.1,anchor = CENTER)
    
    # listOfFile = ctk.CTkLabel(self.frameExecuteDownloadButton, text="LIST OF FILES", font=("Arial", 20,"bold"))
    # listOfFile.place(relx = 0.5,rely=0.2,anchor = CENTER)
 
    self.textFileExist.place(relx=0.5,rely=0.44,anchor=ctk.CENTER,relwidth=0.3,relheight=0.4)
    self.textFileExist.configure(state=DISABLED)
    self.showFileExist()
    
    self.outputFileDownload.place(relx=0.5,rely=0.55,anchor=ctk.CENTER,relwidth=0.8,relheight=0.8)
    self.outputFileDownload.configure(state=DISABLED)

    upload_label = ctk.CTkLabel(self.frameExecuteDownloadButton, text="Enter your magnet text", font=("Arial", 20,"bold"))
    upload_label.place(relx = 0.5, rely=0.7,anchor = tk.CENTER)

    upload_entry = ctk.CTkEntry(self.frameExecuteDownloadButton, width=300, height= 10, placeholder_text="Enter magnet text")
    upload_entry.place(relx = 0.5, rely=0.75,anchor = tk.CENTER)
    
    btn_BACK= ctk.CTkButton(self.frameExecuteDownloadButton,text="BACK", font=("Arial", 20,"bold"),
                          command =lambda: self.switch_frame(self.mainPage))
    btn_BACK.place(relx= 0.3, rely= 0.85, anchor= tk.CENTER)
    
    btn_upload = ctk.CTkButton(self.frameExecuteDownloadButton, text="DOWNLOAD", font=("Arial", 20,"bold"),
                                command=lambda:(self.getFileDownload(upload_entry)))      
    btn_upload.place(relx = 0.7,rely=0.85,anchor = CENTER)

    # btn_view_repo=ctk.CTkButton(self.frameExecuteDownloadButton,text="FILE DOWNLOADED", font=("Arial", 20,"bold"),
    #                       command =lambda: self.animatePanelDownload.animate())
    # btn_view_repo.place(relx= 0.75, rely= 0.85, anchor= tk.CENTER)
    
    # list_header=ctk.CTkLabel(self.animatePanelDownload, text = " LIST FILES ", font=("Comic Sans",30,"bold")
    #                           )
    # list_header.place(relx=0.5,rely=0.1,anchor=ctk.CENTER)
    # list_header.pack()

    return self.frameExecuteDownloadButton
  
  def choose_download_location(self):
    download_dir = filedialog.askdirectory(title="Select Download Directory")
    if download_dir:
        self.download_dir = download_dir
        print(f"Download directory set to: {self.download_dir}")
    else:
        self.download_dir = None
        print("No directory selected")

  def getFileDownload(self, download_entry):
    magnet_text = str(download_entry.get())
    if magnet_text == "":
        messagebox.showerror("Error", "No files specified for download!")
    else:
        listMagnetLinks = magnet_text.split(", ")

        for magnet in listMagnetLinks:
            try:
                info_hash_match = re.search(r'xt=urn:btih:([a-fA-F0-9]+)', magnet)
                tracker_match = re.search(r'tr=tcp://([^:/]+):(\d+)', magnet)
                file_size_match = re.search(r'xl=(\d+)', magnet)
                file_name_match = re.search(r'dn=([^&]+)', magnet)

                if info_hash_match and tracker_match and file_size_match and file_name_match:
                    info_hash = info_hash_match.group(1)
                    server_host = tracker_match.group(1)
                    server_port = int(tracker_match.group(2))
                    file_size = int(file_size_match.group(1))
                    file_name = urllib.parse.unquote(file_name_match.group(1))

                    self.choose_download_location()
                    if self.download_dir:
                        condition = Thread(
                            target=PEER_BEObject.implementDownload, 
                            args=[info_hash, server_host, server_port, file_size, file_name, self.download_dir]
                        )
                        condition.start()
                    else:
                        messagebox.showerror("Error", "No download directory selected")
                else:
                    messagebox.showerror("Error", f"Invalid magnet link format: {magnet}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
                continue

        self.switch_frame(self.executeDownloadButton)

  def showFileDownloaded(self, fileName):
    self.outputFileDownload.configure(state=NORMAL)
    self.numberOfFileDownloaded+= 1
    self.outputFileDownload.insert(ctk.END, f"{self.numberOfFileDownloaded}:   \"{fileName}\"" +"\n\n" )
    self.outputFileDownload.see(ctk.END)
    self.outputFileDownload.configure(state=DISABLED)

  def showFileExist(self):
    self.fileExist = PEER_BEObject.implementReceiveListFileExist()
    self.textFileExist.configure(state=NORMAL)
    count = 1
    self.textFileExist.delete(1.0, ctk.END)
    for file in self.fileExist:
        self.textFileExist.insert(ctk.END, f"{count}:   {file}" + "\n\n")
        count += 1
    self.textFileExist.see(ctk.END)
    self.textFileExist.configure(state=DISABLED)

def signal_handler(sig, frame):
    print('You pressed Ctrl+C! Closing application...')
    PEER_BEObject.stop()  # Gọi phương thức stop của PEER_BE
    sys.exit(0)
      
if __name__ == "__main__":
    import socket

    # Get the list of IP addresses associated with the hostname
    ip_addresses = socket.gethostbyname_ex(socket.gethostname())[2]

    # Check if there are enough elements in the list
    if len(ip_addresses) > 2:
        peerHost = ip_addresses[2]
    else:
        # Handle the case where there are not enough IP addresses
        peerHost = ip_addresses[1]  # or set to a default value

    peerPort = 8000

    PEER_BEObject = PEER_BE(peerHost, peerPort)

    # Register Ctrl+C signal
    signal.signal(signal.SIGINT, signal_handler)

    condition1 = Thread(target=PEER_BEObject.listenServerOrPeers)
    condition1.daemon = True  # Set daemon flag to allow thread to exit when main program exits
    condition1.start()
    
    PEER_FEObject = PEER_FE(peerHost, peerPort)
    PEER_FEObject.mainloop()