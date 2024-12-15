import Head from 'next/head';
import React, { useState } from 'react';
import axios from 'axios';
import Header from '../components/header'; 
const Home: React.FC = () => {
  const [prompt, setPrompt] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [textPrompt, setTextPrompt] = useState(''); // Added state for the text prompt

  const handleTextInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setTextPrompt(e.target.value);
  };

  const handlePromptSubmit = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/generate', {
        text_prompt: textPrompt,
      });
      console.log('Response:', response.data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <>
      <Head>
        <title>Microsite generator</title>
      </Head>
      <Header />  {/* Add the Header component here */}
      <main className="text-center mt-20 space-y-4">
        <h1 className="text-6xl">Microsite Generator</h1>

        <input
          type="text"
          value={textPrompt}
          onChange={handleTextInputChange}
          placeholder="Enter your text prompt"
          className="border border-gray-300 p-2 rounded"
        />

        <button
          onClick={handlePromptSubmit}
          className="ml-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Generate a Microsite
        </button>
      </main>
    </>
  );
};

export default Home;
