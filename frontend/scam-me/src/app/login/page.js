'use client'

import { useState } from 'react';
import { useRouter } from 'next/navigation'; // Import Next.js router to handle navigation

export default function Page() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter(); // Initialize the router for navigation

  // Sign In button functionality
  const handleSignIn = () => {
    // Placeholder for actual authentication logic
    if (username && password) {
      alert('Signed in successfully!'); // Replace with actual sign-in logic (API call, etc.)
      // You can redirect the user to a different page, e.g., a dashboard after successful login
      router.push('/chatroom'); // Example: Navigate to a dashboard page after sign-in
    } else {
      alert('Please enter both username and password');
    }
  };

  // "No account?" button functionality
  const handleNoAccount = () => {
    // Navigate to the sign-up page
    router.push('/createacc'); // Example: Redirect to the sign-up page
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center bg-cover bg-center"
      style={{ backgroundImage: "url('/images/loginbackground.jpg')" }} // Fixed image path
    >
      <div className="flex gap-20 bg-black/60 p-10 rounded-xl">
        
        {/* Left Info Box */}
        <div className="bg-white/80 p-8 rounded-xl max-w-md">
          <h1 className="text-3xl font-semibold mb-4 text-center text-black">Information</h1>
          <p className="text-gray-700">
            Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis.
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
            className="p-3 rounded border"
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="p-3 rounded border"
          />

          <div className="flex gap-2">
            {/* Sign in button with onClick handler */}
            <button
              className="bg-black p-2 rounded hover:bg-gray-200"
              onClick={handleSignIn}
            >
              Sign in
            </button>

            {/* No account button with onClick handler */}
            <button
              className="bg-black p-2 rounded hover:bg-gray-200"
              onClick={handleNoAccount}
            >
              No account?
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
