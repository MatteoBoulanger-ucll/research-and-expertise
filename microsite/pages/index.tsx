import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Home = () => {
  const [textPrompt, setTextPrompt] = useState('');
  const [message, setMessage] = useState(''); // State to display the message
  const [loading, setLoading] = useState(false); // State to show a loading spinner
  const [progress, setProgress] = useState(0); // State for progress bar percentage

  const handleTextInputChange = (e: any) => {
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
      // Post the text prompt to the FastAPI backend
      const response = await axios.post('http://127.0.0.1:8000/generate', {
        text_prompt: textPrompt,
      });

      console.log('Response:', response.data);

      // WebSocket for real-time progress
      const ws = new WebSocket('ws://127.0.0.1:8188/ws?clientId=your_client_id'); // Replace with your WebSocket client ID

      ws.onopen = () => {
        console.log('WebSocket connection opened');
      };

      ws.onmessage = (event) => {
        const message = JSON.parse(event.data);
        if (message.type === 'executing') {
          const progress = message.data.progress; // Get progress from server response
          setProgress(progress); // Update progress
          if (progress === 100) {
            ws.close(); // Close WebSocket when progress is 100%
          }
        }
      };

      ws.onclose = () => {
        console.log('WebSocket connection closed');
        setLoading(false); // Stop loading
        setMessage('The site has been successfully generated.');
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setLoading(false); // Stop loading
        setMessage('An error occurred while generating the site. Please try again.');
      };
    } catch (error) {
      console.error('Error:', error);
      setLoading(false); // Stop loading
      setMessage('An error occurred while generating the site. Please try again.');
    }
  };

  return (
    <>
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

        {/* Display the progress bar and message */}
        <div className="w-full bg-gray-300 rounded-full h-6 mt-4">
          <div
            className="bg-green-500 h-6 rounded-full"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
        <p className="mt-4 text-center" id="progress-text">
          Progress: {progress}%
        </p>

        {/* Display success or error message */}
        {message && (
          <div
            className={`mt-4 p-4 rounded ${loading ? 'text-gray-500' : 'text-green-600'
              }`}
          >
            {message}
          </div>
        )}
      </main>
    </>
  );
};

export default Home;
