import Head from 'next/head';
import React, { useState } from 'react';
import axios from 'axios';
import Header from '../components/header';

const Home: React.FC = () => {
  const [textPrompt, setTextPrompt] = useState('');
  const [message, setMessage] = useState(''); // State to display the message
  const [loading, setLoading] = useState(false); // State to show a loading spinner

  const handleTextInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setTextPrompt(e.target.value);
  };

  const handlePromptSubmit = async () => {
    if (!textPrompt.trim()) {
      setMessage('Please enter a valid text prompt.');
      return;
    }

    setLoading(true); // Start loading
    setMessage(''); // Clear any previous messages

    try {
      const response = await axios.post('http://127.0.0.1:8000/generate', {
        text_prompt: textPrompt,
      });

      console.log('Response:', response.data);

      // Show success message
      setMessage(
        'The site has been successfully generated. You can find the output in the "output/Research" folder where ComfyUI is running.'
      );
    } catch (error) {
      console.error('Error:', error);

      // Show error message
      setMessage('An error occurred while generating the site. Please try again.');
    } finally {
      setLoading(false); // Stop loading
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

        <button
          onClick={handlePromptSubmit}
          className="ml-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          disabled={loading} // Disable the button while loading
        >
          {loading ? 'Generating...' : 'Generate a Microsite'}
        </button>

        {/* Display the success or error message */}
        {message && (
          <div className={`mt-4 p-4 rounded ${loading ? 'text-gray-500' : 'text-green-600'}`}>
            {message}
          </div>
        )}
      </main>
    </>
  );
};

export default Home;
