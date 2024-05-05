import React, { useState, useRef } from 'react';
import axios from 'axios';
import logo from './logo.svg';
import './App.css';
import imagenHombre from './imagenes_hombre/hombre1.jpg';
import imagenMujer from './imagenes_mujer/mujer1.jpg';

function App() {
  const [previewUrl, setPreviewUrl] = useState('');
  const fileInputRefSingle = useRef(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setPreviewUrl(URL.createObjectURL(file));
      sendImageToBackend(file);
    }
  };

  const sendImageToBackend = async (image) => {
    const formData = new FormData();
    formData.append('image', image);

    try {
      const response = await axios.post('http://localhost:8000/upload_images', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      console.log(response.data);
    } catch (error) {
      console.error('Error al enviar la imagen al servidor:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo-small" alt="logo" />
        <div className="header-line"></div>
      </header>
      <div className="file-input-area">
        <div className="column">
          <img src={imagenHombre} alt="Hombre" style={{ maxWidth: '100%', maxHeight: '100%' }} />
        </div>
        <div className="column column-middle">
          <div className="file-drop-area-square" onDragOver={(e) => e.preventDefault()} onDrop={(e) => {
            e.preventDefault();
            handleFileChange({ target: { files: e.dataTransfer.files } });
          }} onClick={() => fileInputRefSingle.current && fileInputRefSingle.current.click()}>
            {!previewUrl && "Arrastra aquí una imagen o haz clic para seleccionar"}
            <input type="file" ref={fileInputRefSingle} onChange={handleFileChange} style={{ display: 'none' }} />
            {previewUrl && <img src={previewUrl} alt="Vista previa" />}
          </div>
          <button className="button-similar" onClick={() => sendImageToBackend}>Get similar images</button>
        </div>
        <div className="column">
          <img src={imagenMujer} alt="Mujer" style={{ maxWidth: '100%', maxHeight: '100%' }} />
        </div>
      </div>
    </div>
  );
}

export default App;