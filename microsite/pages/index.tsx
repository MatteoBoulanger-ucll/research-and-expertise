import Head from 'next/head';
import React, { useState } from "react";
import axios from "axios";

const Home: React.FC = () => {
  const [prompt, setPrompt] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const handlePromptSubmit = async () => {
    try {
      return await axios.post("http://127.0.0.1:8000/generate");
      // setOutput(response.data.output);  // Assuming you've set up `setOutput` to handle the output display
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <>
      <Head>
        <title>Microsite generator</title>
      </Head>
      <main className="flex flex-col justify-center items-center h-screen text-center space-y-4">
        <h1 className="text-white text-3xl">Microsite Generator</h1>
        <button 
          onClick={handlePromptSubmit} 
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Generate a Microsite
        </button>
        <div className="text-red-500 text-3xl">Hello, Tailwind!</div>

      </main>
    </>
  );
};

export default Home;

function setOutput(output: any) {
  throw new Error('Function not implemented.');
}
