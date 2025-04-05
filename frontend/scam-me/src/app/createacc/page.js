'use client'

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showClearUsername, setShowClearUsername] = useState(false);
  const [showClearPassword, setShowClearPassword] = useState(false);

  const router = useRouter();

  useEffect(() => {
    setShowClearUsername(username.length > 0);
  }, [username]);

  useEffect(() => {
    setShowClearPassword(password.length > 0);
  }, [password]);

  const clearUsername = () => {
    setUsername('');
    document.getElementById('username').focus();
  };

  const clearPassword = () => {
    setPassword('');
    document.getElementById('password').focus();
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!username.trim() || !password.trim()) {
      alert('Please enter both username and password');
      return;
    }

    console.log('Login attempt:', { username, password });
    // Here you would add login functionality
  };

  const handleCreateAccount = () => {
    router.push('/chatroom'); 
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center"
      style={{
        backgroundImage: "url('../images/createbackground.jpg')",
        backgroundSize: 'cover',
        backgroundPosition: 'center'
      }}
    >
      <div className="w-full max-w-md p-6 bg-black/60 rounded-xl">
        <form onSubmit={handleSubmit} className="flex flex-col gap-6">
          <div className="relative">
            <label htmlFor="username" className="block text-sm font-medium text-white mb-1">
              Username
            </label>
            <div className="relative">
              <input
                id="username"
                type="text"
                placeholder="..."
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full p-3 rounded border-2 border-white text-black"
                autoComplete="off"
              />
              {showClearUsername && (
                <button
                  type="button"
                  onClick={clearUsername}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 flex items-center justify-center w-5 h-5 rounded-full bg-gray-200 text-black"
                >
                  ✕
                </button>
              )}
            </div>
          </div>

          <div className="relative">
            <label htmlFor="password" className="block text-sm font-medium text-white mb-1">
              Password
            </label>
            <div className="relative">
              <input
                id="password"
                type="password"
                placeholder="..."
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full p-3 rounded border-2 border-white text-black"
                autoComplete="off"
              />
              {showClearPassword && (
                <button
                  type="button"
                  onClick={clearPassword}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 flex items-center justify-center w-5 h-5 rounded-full bg-gray-200 text-black"
                >
                  ✕
                </button>
              )}
            </div>
          </div>

          <button
            type="submit"
            className="bg-white text-black p-3 rounded hover:bg-gray-300 transition"
          >
            Sign In
          </button>

          <div className="text-center mt-2">
            <button
              type="button"
              onClick={handleCreateAccount}
              className="text-white hover:underline cursor-pointer"
            >
              Create account
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
