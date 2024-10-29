

import Head from 'next/head';
import React, { useState } from "react";
const Home: React.FC = () => {

  const [prompt, setPrompt] = useState("");

  const handlePromptSubmit = () => {
      console.log("User Prompt:", prompt);
  };


    return (
        <>
            <Head>
                <title>CarRentFolio</title>
            </Head>
            <main className='text-center mt-20 space-y-4 '>
                <h1 className='text-6xl'>Microsite generator</h1>
                <p>Give a prompt to generate a site</p>
                <div className='space-y-4'>
                    <input 
                        type="text" 
                        value={prompt} 
                        onChange={(e) => setPrompt(e.target.value)} 
                        placeholder="Enter your prompt here..." 
                        className="border rounded p-2 w-80"
                    />
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