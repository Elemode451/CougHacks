'use client'

import { useState } from 'react';
import { useRouter } from 'next/navigation'; // Import Next.js router to handle navigation

export default function Page() {
  const [username, setUsername] = useState('');
  const router = useRouter(); 

  const handleSignIn = () => {
    if (username) {
      alert('Signed in successfully!'); 
      router.push('/successfail'); 
    } else {
      alert('Please enter a username');
    }
  };

  const nfcLogin = () => {
    // Navigate to the NFC QR code
    router.push('/nfclogin'); // Example: Redirect to the QR code
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center bg-cover bg-center"
      style={{ backgroundImage: "url('/images/loginbackground.jpg')" }} // Fixed image path
    >
      <div className="flex gap-20 bg-black/60 p-10 rounded-xl">
        
        {/* Left Info Box */}
        <div className="bg-white/80 p-8 rounded-xl max-w-md">
          <h1 className="text-3xl font-semibold mb-4 text-center text-black">RADIUS</h1>
          <p className="text-gray-700">
            Connect locally and keep your info secure.
            {/* Your detailed information content */}
          </p>
        </div>

        {/* Right Login Form */}
        <div className="flex flex-col gap-4">
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="p-3 rounded border text-gray-200"
          />

          <div className="flex gap-2">
            {/* Sign in button with onClick handler */}
            <button
              className="bg-gray-500 p-2 rounded hover:bg-gray-200"
              onClick={handleSignIn}
            >
              Submit
            </button>

            {/* No account button with onClick handler */}
            <button
              className="bg-gray-500 p-2 rounded hover:bg-gray-200"
              onClick={nfcLogin}
            >
              Log in with NFC
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
