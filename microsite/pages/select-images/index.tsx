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
    // Send selected images to backend
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
    
    <div style={{ padding: '20px' }}>
        <Header></Header>
      <h1>Select Your Images</h1>
      {Object.entries(imagesData).map(([folder, files]) => (
        <div key={folder} style={{ marginBottom: '20px' }}>
          <h2>{folder}</h2>
          <div style={{ display: 'flex', gap: '10px' }}>
            {files.map(file => {
              const isSelected = selected[folder] === file;
              return (
                <div 
                  key={file} 
                  style={{ 
                    border: isSelected ? '3px solid blue' : '1px solid #ccc', 
                    padding: '5px',
                    cursor: 'pointer'
                  }}
                  onClick={() => handleSelectImage(folder, file)}
                >
                  <img
                    src={`http://127.0.0.1:8000/images/${folder}/${file}`}
                    alt={file}
                    style={{ width: '100px', display: 'block' }}
                  />
                  <div style={{ textAlign: 'center', fontSize: '12px' }}>{file}</div>
                </div>
              );
            })}
          </div>
        </div>
      ))}
      <button onClick={handleFinalize} style={{ padding: '10px 20px', fontSize: '16px' }}>
        Finalize
      </button>
    </div>
  );
};

export default SelectImages;
