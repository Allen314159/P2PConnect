import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [peers, setPeers] = useState([]);


  useEffect(() => {
    axios.get('http://localhost:5000/api/data')
      .then(response => {
        setLoading(false);
        setPeers(response.data);
        console.log(response.data);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setError('Không thể lấy dữ liệu từ server');
        setLoading(false);
      });
  }, []);

  const [searchTerm, setSearchTerm] = useState("");

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
  };

  return (
    <div className="app-container">
      <div id="header">
        <h1>Danh sách các file đã tải lên</h1>
      </div>

      <div className="search-bar">
        <input
          type="text"
          placeholder="Tìm kiếm file..."
          value={searchTerm}
          onChange={handleSearchChange}
        />
      </div>

      {loading ? (
        <p>Đang tải dữ liệu...</p>
      ) : error ? (
        <p>{error}</p>
      ) : (
        <div className="file-container">
          <div className="list file-uploaded">
            {peers.map((peer, peerIndex) => (
                <div key={peerIndex}>
                  <h3>Node ID: {peer._id}</h3>
                  {peer.files.length > 0 ? (
                    <div className="table file-up">
                      <table>
                        <thead>
                          <tr>
                            <th>STT</th>
                            <th>File</th>
                            <th>Magnet text</th>
                          </tr>
                        </thead>
                        <tbody>
                          {peer.files
                            .filter(file =>
                              file.fileName
                                .toLowerCase()
                                .includes(searchTerm.toLowerCase())
                            )
                            .map((file, index) => (
                              <tr key={file._id}>
                                <td>{index + 1}</td>
                                <td>{file.fileName}</td>
                                <td>{file.magnet_text}</td>
                              </tr>
                            ))}
                        </tbody>
                      </table>
                    </div>
                  ) : (
                    <p>Không có file nào được tải lên</p>
                  )}
                </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
