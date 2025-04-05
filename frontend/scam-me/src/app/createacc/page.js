'use client'

import { useState, useEffect } from 'react';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showClearUsername, setShowClearUsername] = useState(false);
  const [showClearPassword, setShowClearPassword] = useState(false);
  
  // Handle showing/hiding clear buttons
  useEffect(() => {
    setShowClearUsername(username.length > 0);
  }, [username]);
  
  useEffect(() => {
    setShowClearPassword(password.length > 0);
  }, [password]);
  
  // Clear input handlers
  const clearUsername = () => {
    setUsername('');
    document.getElementById('username').focus();
  };
  
  const clearPassword = () => {
    setPassword('');
    document.getElementById('password').focus();
  };
  
  // Form submission handler
  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!username.trim() || !password.trim()) {
      alert('Please enter both username and password');
      return;
    }
    
    // Here you would normally handle authentication
    console.log('Login attempt:', { username, password });
  };
  
  // Create account handler
  const handleCreateAccount = () => {
    alert('Create account functionality would go here');
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
      <div className="w-full max-w-md p-6">
        <form onSubmit={handleSubmit} className="flex flex-col gap-6">
          <div className="relative">
            <label htmlFor="username" className="block text-sm font-medium text-black mb-1">
              Username
            </label>
            <div className="relative">
              <input
                id="username"
                type="text"
                placeholder="..."
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full p-3 rounded border-2 border-black"
                autoComplete="off"
              />
              {showClearUsername && (
                <button
                  type="button"
                  onClick={clearUsername}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 flex items-center justify-center w-5 h-5 rounded-full bg-gray-200 text-black-600"
                >
                  ✕
                </button>
              )}
            </div>
          </div>
          
          <div className="relative">
            <label htmlFor="password" className="block text-sm font-medium text-black mb-1">
              Password
            </label>
            <div className="relative">
              <input
                id="password"
                type="password"
                placeholder="..."
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full p-3 rounded border-2 border-black"
                autoComplete="off"
              />
              {showClearPassword && (
                <button
                  type="button"
                  onClick={clearPassword}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 flex items-center justify-center w-5 h-5 rounded-full bg-gray-200 text-gray-600"
                >
                  ✕
                </button>
              )}
            </div>
          </div>
          
          <div className="text-center mt-2">
            <button
              type="button"
              onClick={handleCreateAccount}
              className="text-black hover:underline cursor-pointer"
            >
              Create account
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}