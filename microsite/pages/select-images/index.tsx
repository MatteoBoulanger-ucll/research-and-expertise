import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Header from '@/components/header';

const SelectImages: React.FC = () => {
  const [imagesData, setImagesData] = useState<Record<string, string[]>>({});
  const [selected, setSelected] = useState<Record<string, string>>({});

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/images')
      .then(response => setImagesData(response.data))
      .catch(error => console.error(error));
  }, []);

  const handleSelectImage = (folder: string, imageName: string) => {
    setSelected(prev => ({ ...prev, [folder]: imageName }));
  };

  const handleFinalize = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/finalize', selected, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      alert('Final microsite generated. Check output folder!');
      console.log(response.data);
    } catch (error) {
      console.error(error);
      alert('Error finalizing images');
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '20px' }}>
      {/* Full-width Header */}
      <div style={{ width: '100%' }}>
        <Header />
      </div>

      {/* Centered Content */}
      <div style={{ width: '100%', maxWidth: '1200px', marginTop: '20px' }}>
        <h1 style={{ textAlign: 'center' }}>Select Your Images</h1>

        {/* Image Selection */}
        {Object.entries(imagesData).map(([folder, files]) => (
          <div key={folder} style={{ marginBottom: '20px', textAlign: 'center' }}>
            <h2 style={{ textTransform: 'capitalize' }}>{folder}</h2>
            <div style={{ display: 'flex', justifyContent: 'center', flexWrap: 'wrap', gap: '10px' }}>
              {files.map(file => {
                const isSelected = selected[folder] === file;
                return (
                  <div 
                    key={file}
                    style={{ 
                      border: isSelected ? '3px solid blue' : '1px solid #ccc',
                      padding: '5px',
                      cursor: 'pointer',
                      borderRadius: '5px',
                      transition: 'border 0.3s ease'
                    }}
                    onClick={() => handleSelectImage(folder, file)}
                  >
                    <img
                      src={`http://127.0.0.1:8000/images/${folder}/${file}`}
                      alt={file}
                      style={{ 
                        width: '100px', 
                        height: '100px', 
                        objectFit: 'cover', 
                        display: 'block',
                        borderRadius: '5px'
                      }}
                    />
                    <div style={{ textAlign: 'center', fontSize: '12px' }}>{file}</div>
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      {/* Finalize Button */}
      <button 
        onClick={handleFinalize} 
        style={{
          padding: '10px 20px',
          fontSize: '16px',
          backgroundColor: '#007BFF',
          color: '#fff',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
          marginTop: '20px',
          transition: 'background-color 0.3s ease'
        }}
        onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#0056b3'}
        onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#007BFF'}
      >
        Finalize
      </button>
    </div>
  );
};

export default SelectImages;
