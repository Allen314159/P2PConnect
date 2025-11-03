const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
app.use(cors());

// Kết nối tới MongoDB
mongoose.connect('mongodb+srv://project_MMT:mbk22351@cluster0.l5iob.mongodb.net/MMT', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => console.log('Kết nối MongoDB thành công'))
.catch((error) => console.error('Lỗi kết nối MongoDB:', error));

// Định nghĩa Schema và Model
const fileSchema = new mongoose.Schema({
  fileName: String,
  magnet_text: String,
});

const peerSchema = new mongoose.Schema({
  _id: String,
  ip_address: String,
  ip_port: Number,
  state: String,
  info_hash: [String],
  files: [fileSchema],
}, { collection: 'Client' });

const Peer = mongoose.model('Peer', peerSchema);

// API: Lấy toàn bộ dữ liệu
app.get('/api/data', async (req, res) => {
  try {
    const peerData = await Peer.find(); // Lấy toàn bộ dữ liệu từ collection
    res.json(peerData); // Trả dữ liệu dưới dạng JSON
  } catch (error) {
    console.error('Lỗi khi lấy dữ liệu từ MongoDB:', error);
    res.status(500).json({ message: 'Lỗi khi lấy dữ liệu từ MongoDB' });
  }
});

// Khởi chạy server
const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Server đang chạy tại http://localhost:${PORT}`);
});
