
# 🌀 A Hybrid P2P File Sharing Application

**Simple torrent-like peer-to-peer (P2P) file sharing application** built using **Python, React, and Node.js**.  
It implements a **Hybrid P2P Network model** with a **central tracker server** to coordinate peers, allowing users to **upload, search, and download files** directly from each other.

---

## 🚀 Features

- **Hybrid P2P Network**: Combines the benefits of client-server and pure P2P architectures.
- **Tracker Server**: Manages active peers and shared files.
- **Peer Nodes**: Act as both clients and servers for file sharing.
- **File Upload & Download**: Supports file registration, searching, and piece-based transfer via TCP.
- **Magnet Links**: Each uploaded file is associated with a unique magnet text for easy sharing.
- **Multi-threaded Transfers**: Download and upload multiple files or chunks simultaneously.
- **Web Interface**: A user-friendly website built with ReactJS for searching magnet links.
- **MongoDB Cloud Storage**: Centralized database for file and peer metadata.

---

## 🧩 System Architecture

### Components:
1. **Tracker Server** – Central node maintaining peer and file information.  
2. **Peer Node** – User client capable of uploading and downloading files.  
3. **Web Server (React + Node.js)** – Interface for searching magnet links.  
4. **MongoDB Cloud** – Stores file metadata, peer info, and logs.

### Protocols Used:
- **TCP/IP** – Reliable data transmission.
- **Custom Tracker & File Transfer Protocols** – Implemented in Python.

---

## ⚙️ Technologies

| Component | Technology |
|------------|-------------|
| Backend | Python (socket, threading, json) |
| Frontend | ReactJS |
| Web Backend | Node.js |
| Database | MongoDB Cloud |
| Network | TCP/IP |

---

## 🧠 How It Works

1. **Tracker Server** starts and waits for peer connections.  
2. **Peers** connect to the tracker and register shared files.  
3. Tracker maintains a list of peers and available files.  
4. **Clients** can:
   - Upload a file → generate a **magnet link**.
   - Search for a magnet link → get a list of peers that have the file.
   - Download pieces of the file directly from peers.
5. File transfer occurs over **TCP**, ensuring data integrity.

---

## 🖥️ Installation & Usage

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/SimpleTorrent.git
cd SimpleTorrent
````

### 2️⃣ Run the Tracker Server

```bash
cd tracker
python Tracker.py
```

### 3️⃣ Run the Peer Client

```bash
cd peer
python PEER_FE.py
```

> Ensure the `serverHost` and `serverPort` values in `PEER_FE.py` match your Tracker settings.

### 4️⃣ Run the Web Interface

```bash
cd web
npm install
npm start
```

Then open your browser at:
👉 **[http://localhost:3000](http://localhost:3000)**

---

## 🧪 Testing

* Verified on **Windows** and **macOS**.
* Supports **multiple concurrent trackers** to prevent overload.
* Handles **simultaneous peer connections** and real-time updates.

---


## 🧱 Future Improvements

* Improve UI/UX for peer and tracker dashboards.
* Implement UDP-based tracker communication.
* Add file verification using hash checksums.
* Support encrypted data transfers.

---

## 👥 Team

| Name                 | Role                       |
| -------------------- |--------------------------  |
| **Lâm Mỹ Trang**     | Backend, Report            |
| **Nguyễn Nhật Khoa** | Backend, Report            |
| **Nguyễn Hữu Khánh** | UI Design, Testing, Report |

---

## 📜 License

This project is for **educational purposes only**.
Developed as part of the **Computer Networks** course at **Ho Chi Minh City University of Technology (HCMUT)**.

---

