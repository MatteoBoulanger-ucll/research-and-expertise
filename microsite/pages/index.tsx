import Head from 'next/head';
import React, { useState } from "react";
import axios from "axios";

const Home: React.FC = () => {
  const [prompt, setPrompt] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const handlePromptSubmit = async () => {
    try {
      return await axios.post("http://127.0.0.1:8000/generate", {
        prompt: prompt,    
        }
      );
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <>
      <Head>
        <title>Microsite generator</title>
      </Head>
      <main className="flex flex-col items-center justify-center h-screen bg-[rgb(243,223,191)]">
        <h1 className="text-black text-3xl font-mono">Microsite Generator</h1>
        
        <div className="text-center mt-8">
          <p className="font-mono text-xl">
            With this application you are able to generate a basic website based on a picture and a prompt.
          </p>
        </div>

        <div className="flex flex-col items-center space-y-4 mt-8">
          <input
            type="text"
            placeholder="Enter your prompt here"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            className="px-4 py-2 border rounded w-80"
          />
          <button
            onClick={handlePromptSubmit}
            className="px-4 py-2 bg-customButton text-black rounded font-mono"
          >
            Generate a Microsite
          </button>
        </div>
      </main>
    </>
  );
};

export default Home;

function setOutput(output: any) {
  throw new Error("Function not implemented.");
}
