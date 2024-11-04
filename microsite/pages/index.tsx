import Head from 'next/head';
import React, { useState } from "react";

const Home: React.FC = () => {
  const [prompt, setPrompt] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const handlePromptSubmit = () => {
    console.log("User Prompt:", prompt);
    if (file) {
      console.log("User Uploaded File:", file);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const uploadedFile = e.target.files?.[0];
    if (uploadedFile) {
      setFile(uploadedFile);
      setPreviewUrl(URL.createObjectURL(uploadedFile)); // Generate a preview URL
    }
  };

  return (
    <>
      <Head>
        <title>CarRentFolio</title>
      </Head>
      <main className='text-center mt-20 space-y-4 '>
        <h1 className='text-6xl'>Microsite Generator</h1>
        <p>Give a prompt to generate a site</p>
        <div className='space-y-4'>
          <input 
            type="text" 
            value={prompt} 
            onChange={(e) => setPrompt(e.target.value)} 
            placeholder="Enter your prompt here..." 
            className="border rounded p-2 w-80"
          />
          <input 
            type="file" 
            onChange={handleFileChange} 
            className="block mt-4"
          />
          
          {previewUrl && (
            <div className="mt-4">
              <p>Image Preview:</p>
              <img src={previewUrl} alt="Image preview" className="w-40 h-40 object-cover rounded-md mx-auto" />
            </div>
          )}

          <button 
            onClick={handlePromptSubmit} 
            className="ml-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Generate
          </button>
        </div>
      </main>
    </>
  );
};

export default Home;
