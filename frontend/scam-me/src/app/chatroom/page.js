// app/page.jsx
'use client';

import { useState } from 'react';
import { getSocket } from '../socket';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronLeft, ChevronRight, Plus, MessageSquare, Send } from 'lucide-react';
import clsx from 'clsx';

const Home = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activeChat, setActiveChat] = useState(1); // Default to first chat
  const [chats, setChats] = useState([
    { id: 1, name: 'Community 1' },
    { id: 2, name: 'Community 2' },
    { id: 3, name: 'Community 3' },
  ]);
  const [messages, setMessages] = useState([
    { id: 1, text: "Hey there!", chatId: 1, timestamp: new Date().toISOString(), sender: "System" },
    { id: 2, text: "Welcome to the chat!", chatId: 1, timestamp: new Date().toISOString(), sender: "System" },
  ]);
  const [newMessage, setNewMessage] = useState('');

  const handleSendMessage = () => {
    const socket = getSocket();

    socket.on("connect", () => {
      console.log("Connected to server:", socket.id);
    });

    if (newMessage.trim() && activeChat) {
      const message = {
        id: Date.now(),
        text: newMessage,
        chatId: activeChat,
        timestamp: new Date().toISOString(),
        sender: 'You',
      };

       // Emit message to server
       socket.emit('chat message', {
          newMessage,
          sender: 'You' // NEED TO REPLACE WITH USERNAME STATE
      });

      setMessages([...messages, message]);
      setNewMessage('');
    }
  };

  const addNewChat = () => {
    const newChatId = chats.length > 0 ? Math.max(...chats.map(c => c.id)) + 1 : 1;
    const newChat = {
      id: newChatId,
      name: `Chat ${newChatId}`,
    };
    setChats([...chats, newChat]);
    setActiveChat(newChatId);
    // Add welcome message to new chat
    setMessages([...messages, {
      id: Date.now() + 1,
      text: `Welcome to ${newChat.name}!`,
      chatId: newChatId,
      timestamp: new Date().toISOString(),
      sender: "System"
    }]);
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-gradient-to-br from-cyan-100 to-blue-100">
      {/* Sidebar - now with all content */}
      <motion.div
        className="flex flex-col h-full bg-white/30 backdrop-blur-md"
        animate={{
          width: sidebarOpen ? 240 : 80,
        }}
        initial={false}
        transition={{ type: 'spring', stiffness: 300, damping: 30 }}
        style={{
          borderRight: '1px solid rgba(255, 255, 255, 0.5)',
          boxShadow: '0 0 15px rgba(0, 150, 255, 0.2)',
        }}
      >
        <div className="p-4 flex justify-between items-center border-b border-white/30">
          {sidebarOpen && (
            <motion.h2
              className="text-xl font-bold text-cyan-800"
              initial={{ opacity: 0 }}
              animate={{ opacity: sidebarOpen ? 1 : 0 }}
              transition={{ duration: 0.2 }}
            >
              Communities
            </motion.h2>
          )}
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 rounded-full hover:bg-white/30 transition-colors text-cyan-700"
            style={{
              backdropFilter: 'blur(5px)',
              boxShadow: '0 0 5px rgba(0, 150, 255, 0.3)',
            }}
          >
            {sidebarOpen ? <ChevronLeft /> : <ChevronRight />}
          </button>
        </div>

        <div className="p-2 flex-1 overflow-y-auto">
          {chats.map(chat => (
            <motion.div
              key={chat.id}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setActiveChat(chat.id)}
              className={clsx(
                "p-3 rounded-xl cursor-pointer mb-2 flex items-center gap-2 transition-all",
                activeChat === chat.id
                  ? 'bg-gradient-to-r from-cyan-400/30 to-blue-400/30 border border-white/30 shadow-lg'
                  : 'hover:bg-white/30 border border-transparent hover:border-white/30'
              )}
              style={{
                backdropFilter: 'blur(5px)',
              }}
            >
              <div className="bg-cyan-500 p-2 rounded-lg text-white">
                <MessageSquare size={16} />
              </div>
              <AnimatePresence>
                {sidebarOpen && (
                  <motion.span
                    className="text-cyan-800 font-medium"
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -10 }}
                    transition={{ duration: 0.2 }}
                  >
                    {chat.name}
                  </motion.span>
                )}
              </AnimatePresence>
            </motion.div>
          ))}
        </div>

        <div className="p-3 border-t border-white/30">
          <button
            onClick={addNewChat}
            className="w-full p-2 rounded-xl flex items-center justify-center gap-2 hover:bg-white/30 transition-colors text-cyan-700 font-medium"
            style={{
              backdropFilter: 'blur(5px)',
              boxShadow: '0 0 5px rgba(0, 150, 255, 0.3)',
            }}
          >
            <div className="bg-cyan-500 p-1 rounded-lg text-white">
              <Plus size={16} />
            </div>
            {sidebarOpen && (
              <motion.span
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
              >
                New Chat
              </motion.span>
            )}
          </button>
        </div>
      </motion.div>

      {/* Main chat area */}
      <div className="flex-1 flex flex-col h-full p-4 overflow-hidden">
        {activeChat ? (
          <>
            {/* Chat header */}
            <div
              className="p-4 rounded-xl bg-white/30 backdrop-blur-md mb-4 flex-shrink-0"
              style={{
                border: '1px solid rgba(255, 255, 255, 0.5)',
                boxShadow: '0 0 15px rgba(0, 150, 255, 0.2)',
              }}
            >
              <h2 className="text-xl font-semibold text-cyan-800">
                {chats.find(c => c.id === activeChat)?.name || 'Chat'}
              </h2>
            </div>

            {/* Messages container - scrollable area */}
            <div
              className="flex-1 overflow-y-auto p-4 rounded-xl bg-white/30 backdrop-blur-md mb-4"
              style={{
                border: '1px solid rgba(255, 255, 255, 0.5)',
                boxShadow: '0 0 15px rgba(0, 150, 255, 0.2)',
              }}
            >
              <div className="flex flex-col">
                {messages
                  .filter(m => m.chatId === activeChat)
                  .map(message => (
                    <motion.div
                      key={message.id}
                      className={clsx(
                        "mb-4",
                        message.sender === 'You' ? 'self-end' : 'self-start'
                      )}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                    >
                      <div
                        className={clsx(
                          "p-3 rounded-xl inline-block max-w-xs shadow-md",
                          message.sender === 'You'
                            ? 'bg-gradient-to-r from-cyan-400 to-blue-400 text-white'
                            : message.sender === 'System'
                            ? 'bg-purple-400/30 text-cyan-800'
                            : 'bg-white/80 text-cyan-800'
                        )}
                        style={{
                          border: '1px solid rgba(255, 255, 255, 0.5)',
                        }}
                      >
                        {message.text}
                      </div>
                      <div
                        className={clsx(
                          "text-xs mt-1",
                          message.sender === 'You'
                            ? 'text-right text-cyan-700'
                            : 'text-left text-cyan-700/80'
                        )}
                      >
                        {message.sender} • {new Date(message.timestamp).toLocaleTimeString()}
                      </div>
                    </motion.div>
                  ))}
              </div>
            </div>

            {/* Input area */}
            <div className="flex gap-2 flex-shrink-0">
              <input
                type="text"
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                placeholder="Type a message..."
                className="flex-1 p-3 rounded-xl bg-white/50 backdrop-blur-md border border-white/30 focus:outline-none focus:ring-2 focus:ring-cyan-400 text-cyan-800 placeholder-cyan-600/70 shadow-sm"
                style={{
                  boxShadow: '0 0 10px rgba(0, 150, 255, 0.1) inset',
                }}
              />
              <button
                onClick={handleSendMessage}
                className="bg-gradient-to-r from-cyan-400 to-blue-400 text-white p-3 rounded-xl hover:from-cyan-500 hover:to-blue-500 transition-all shadow-lg flex items-center justify-center"
                style={{
                  border: '1px solid rgba(255, 255, 255, 0.5)',
                }}
              >
                <Send size={20} />
              </button>
            </div>
          </>
        ) : (
          <motion.div
            className="flex-1 flex items-center justify-center rounded-xl bg-white/30 backdrop-blur-md"
            style={{
              border: '1px solid rgba(255, 255, 255, 0.5)',
              boxShadow: '0 0 15px rgba(0, 150, 255, 0.2)',
            }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <div className="text-cyan-700/80 text-center p-6">
              <div className="text-4xl mb-4">💬</div>
              <h3 className="text-xl font-medium mb-2">Welcome to the chat</h3>
              <p>Select a chat from the sidebar or create a new one</p>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
}

export default Home;