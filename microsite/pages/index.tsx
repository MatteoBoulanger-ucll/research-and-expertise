import Head from 'next/head';
import React, { useState } from "react";
import axios from "axios";

const Home: React.FC = () => {
  const [prompt, setPrompt] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [textPrompt, setTextPrompt] = useState(""); // Added state for the text prompt

  // Handle the text input change
  const handleTextInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setTextPrompt(e.target.value);
  };

  const handlePromptSubmit = async () => {
    try {
      // Send the text prompt along with the file (if any) to the backend
      const response = await axios.post("http://127.0.0.1:8000/generate", {
        text_prompt: textPrompt,  // Send the text prompt here
      });
      console.log("Response:", response.data);
      // Handle the response as needed (e.g., set an output state or show an image preview)
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <>
      <Head>
        <title>Microsite generator</title>
      </Head>
      <main className="text-center mt-20 space-y-4">
        <h1 className="text-6xl">Microsite Generator</h1>
        
        {/* Input for the text prompt */}
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
