import Head from 'next/head';
import React, { useState } from 'react';
import axios from 'axios';

const Home: React.FC = () => {
  const [textPrompt, setTextPrompt] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleTextInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setTextPrompt(e.target.value);
  };

  const handleFileSelection = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
    } else {
      setSelectedFile(null);
    }
  };

  const handlePromptSubmit = async () => {
    if (!textPrompt.trim()) {
      setMessage('Please enter a valid text prompt.');
      return;
    }

    if (!selectedFile) {
      setMessage('Please select an image file.');
      return;
    }

    setLoading(true);
    setMessage('');

    const formData = new FormData();
    formData.append('text_prompt', textPrompt);
    formData.append('image', selectedFile);

    try {
      const response = await axios.post('http://127.0.0.1:8000/generate', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log('Response:', response.data);
      setMessage('The site has been successfully generated.');
    } catch (error) {
      console.error('Error:', error);
      setMessage('An error occurred while generating the site. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>Microsite Generator</title>
      </Head>
      <main className="text-center mt-20 space-y-4">
        <h1 className="text-6xl">Microsite Generator</h1>

        <input
          type="text"
          value={textPrompt}
          onChange={handleTextInputChange}
          placeholder="Enter your text prompt"
          className="border border-gray-300 p-2 rounded"
        />

        <input
          type="file"
          accept="image/png, image/jpeg"
          onChange={handleFileSelection}
          className="border border-gray-300 p-2 rounded"
        />

        <button
          onClick={handlePromptSubmit}
          className="ml-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          disabled={loading}
        >
          {loading ? 'Generating...' : 'Generate a Microsite'}
        </button>

        {message && (
          <div className="mt-4 p-4 rounded text-green-600">
            {message}
          </div>
        )}
      </main>
    </>
  );
};

export default Home;
