import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Header from '@/components/header';

const Editor: React.FC = () => {
  // images, texts (existing)
  const [imagesData, setImagesData] = useState<Record<string, string[]>>({});
  const [textData, setTextData] = useState<Record<string, string[]>>({});
  const [selectedImages, setSelectedImages] = useState<Record<string, string>>({});
  const [selectedTexts, setSelectedTexts] = useState<Record<string, string>>({});
  const [openFileContent, setOpenFileContent] = useState<Record<string, Record<string, string>>>({});

  // For the hex sets from Hex_0001.txt
  const [hexSchemes, setHexSchemes] = useState<string[][]>([]);
  const [hexIndex, setHexIndex] = useState(0);

  useEffect(() => {
    // 1) Load images
    axios.get('http://127.0.0.1:8000/images')
      .then(response => setImagesData(response.data))
      .catch(error => console.error(error));

    // 2) Load text files
    axios.get('http://127.0.0.1:8000/text-files')
      .then(response => setTextData(response.data))
      .catch(error => console.error(error));

    // 3) Load hex schemes
    axios.get('http://127.0.0.1:8000/hex-schemes')
      .then(response => {
        setHexSchemes(response.data); 
        setHexIndex(0); // Start at first scheme
      })
      .catch(error => console.error(error));
  }, []);

  // Move to previous scheme
  const handlePrevHex = () => {
    setHexIndex(prev => {
      if (!hexSchemes.length) return 0;
      let newIndex = prev - 1;
      if (newIndex < 0) {
        newIndex = hexSchemes.length - 1;
      }
      return newIndex;
    });
  };

  // Move to next scheme
  const handleNextHex = () => {
    if (!hexSchemes.length) return;
    setHexIndex(prev => (prev + 1) % hexSchemes.length);
  };

  // The currently selected block of hex codes
  const currentHexBlock: string[] = hexSchemes[hexIndex] || [];

  // IMAGE
  const handleSelectImage = (folder: string, fileName: string) => {
    setSelectedImages(prev => ({ ...prev, [folder]: fileName }));
  };

  // TEXT
  const handleSelectText = (prefix: string, fileName: string) => {
    setSelectedTexts(prev => ({ ...prev, [prefix]: fileName }));
  };

  // TEXT "View" toggle
  const handleViewContent = async (prefix: string, fileName: string) => {
    const currentContent = openFileContent[prefix]?.[fileName];
    if (currentContent) {
      // Hide
      setOpenFileContent(prev => ({
        ...prev,
        [prefix]: {
          ...prev[prefix],
          [fileName]: ''
        }
      }));
    } else {
      // Fetch from server
      try {
        const resp = await axios.get('http://127.0.0.1:8000/text-content', {
          params: { file_name: fileName }
        });
        const text = resp.data.content;
        setOpenFileContent(prev => ({
          ...prev,
          [prefix]: {
            ...(prev[prefix] || {}),
            [fileName]: text
          }
        }));
      } catch (error) {
        console.error(error);
        alert(`Failed to load text for ${fileName}`);
      }
    }
  };

  // Finalize picks => send to /finalize
  const handleFinalize = async () => {
    const payload = {
      images: selectedImages,
      texts: selectedTexts,
      selected_hex: currentHexBlock  // the array of lines user is currently on
    };

    try {
      const response = await axios.post('http://127.0.0.1:8000/finalize', payload, {
        headers: { 'Content-Type': 'application/json' }
      });
      alert('Final microsite generated. Check output folder!');
      console.log(response.data);
    } catch (error) {
      console.error(error);
      alert('Error finalizing picks');
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="mx-auto w-[60%] py-8 flex flex-col">
        <h1 className="text-3xl font-bold text-center mb-8">Editor</h1>

        {/* --- HEX SELECTION --- */}
        <section className="mb-10">
          <h2 className="font-semibold text-lg mb-2 text-center">Choose a HEX Scheme (from Hex_0001.txt)</h2>
          <div className="flex flex-wrap gap-4 justify-center">
            {/* Prev */}
            <button
              className="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300"
              onClick={handlePrevHex}
              disabled={hexSchemes.length === 0}
            >
              Prev
            </button>

            {/* Display current hex lines */}
            <div className="border p-4 rounded shadow flex flex-col items-center">
              {currentHexBlock.length ? (
                <>
                  <p className="mb-2 font-semibold text-lg">Scheme #{hexIndex + 1}</p>
                  <div className="grid grid-cols-2 gap-2">
                    {currentHexBlock.map((hexValue, idx) => (
                      <div key={idx} className="flex flex-col items-center">
                        <div
                          style={{
                            width: '40px',
                            height: '40px',
                            backgroundColor: hexValue,
                            border: '1px solid #ccc'
                          }}
                        />
                        <span className="text-sm mt-1">{hexValue}</span>
                      </div>
                    ))}
                  </div>
                </>
              ) : (
                <p>No hex data</p>
              )}
            </div>

            {/* Next */}
            <button
              className="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300"
              onClick={handleNextHex}
              disabled={hexSchemes.length === 0}
            >
              Next
            </button>
          </div>
        </section>

        {/* --- IMAGES --- */}
        <section className="mb-10">
          <h2 className="text-xl font-semibold mb-4 text-center">Select Images</h2>
          {Object.entries(imagesData).map(([folder, files]) => (
            <div key={folder} className="mb-6">
              <div className="font-semibold text-lg mb-2 text-center">{folder}</div>
              <div className="flex flex-wrap gap-4 justify-center">
                {files.map(file => {
                  const isSelected = selectedImages[folder] === file;
                  return (
                    <div
                      key={file}
                      onClick={() => handleSelectImage(folder, file)}
                      className={`border rounded-md p-2 cursor-pointer ${
                        isSelected ? 'border-4 border-blue-600' : 'border-gray-300'
                      }`}
                    >
                      <img
                        src={`http://127.0.0.1:8000/images/${folder}/${file}`}
                        alt={file}
                        className="w-[100px] h-[100px] object-cover"
                      />
                      <div className="text-center text-sm mt-1">{file}</div>
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </section>

        {/* --- TEXTS --- */}
        <section className="mb-10">
          <h2 className="text-xl font-semibold mb-4 text-center">Select Text Variants</h2>
          {Object.entries(textData).map(([prefix, files]) => (
            <div key={prefix} className="mb-6">
              <div className="font-semibold text-lg mb-2 text-center">{prefix}</div>
              <div className="flex flex-wrap gap-4 justify-center">
                {files.map(file => {
                  const isSelected = selectedTexts[prefix] === file;
                  const content = openFileContent[prefix]?.[file] || '';
                  const showingContent = content.trim().length > 0;

                  return (
                    <div
                      key={file}
                      className={`border rounded-md p-3 ${
                        isSelected ? 'border-4 border-blue-600' : 'border-gray-300'
                      }`}
                    >
                      <div className="flex items-center gap-4">
                        <span
                          className="cursor-pointer"
                          onClick={() => handleSelectText(prefix, file)}
                        >
                          {file}
                        </span>
                        <button
                          className="px-2 py-1 text-sm bg-gray-200 rounded hover:bg-gray-300"
                          onClick={() => handleViewContent(prefix, file)}
                        >
                          {showingContent ? 'Hide' : 'View'}
                        </button>
                      </div>
                      {showingContent && (
                        <div className="bg-gray-100 mt-2 p-2 rounded-md text-sm">
                          {content}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </section>

        <button
          onClick={handleFinalize}
          className="self-center px-6 py-2 bg-blue-600 text-white font-semibold rounded shadow-sm hover:bg-blue-700"
        >
          Finalize
        </button>
      </main>
    </div>
  );
};

export default Editor;
