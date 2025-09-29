import React, { useState, useRef, useEffect } from 'react';
import { X, Send, Bot, User, Loader2 } from 'lucide-react';

const AIChatModal = ({ isOpen, onClose }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      text: "Hello! I'm RakeAssist, your AI co-pilot for Kochi Metro operations. Ask me about specific trains and days, like 'Why was Rake-03 on maintenance on day 15?'",
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      text: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:5002/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: inputMessage }),
      });

      const data = await response.json();

      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        text: data.answer || data.error || 'Sorry, I encountered an error.',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        text: 'Sorry, I\'m having trouble connecting to the AI service. Please make sure the chatbot server is running on port 5002.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4" onClick={onClose}>
      <div 
        className="bg-gradient-to-br from-gray-800 via-gray-900 to-gray-800 rounded-3xl border-2 border-blue-400/50 w-full max-w-4xl h-[80vh] shadow-2xl flex flex-col"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex justify-between items-center p-6 border-b border-gray-700/50">
          <div className="flex items-center gap-3">
            <Bot className="text-blue-400" size={32} />
            <div>
              <h2 className="text-2xl font-bold text-transparent bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text">
                RakeAssist AI
              </h2>
              <p className="text-gray-400">Your Metro Operations Co-pilot</p>
            </div>
          </div>
          <button 
            onClick={onClose} 
            className="text-gray-400 hover:text-white transition-all duration-300 p-3 hover:bg-gray-700/50 rounded-xl group"
          >
            <X size={28} className="group-hover:scale-110 transition-transform duration-300" />
          </button>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((message) => (
            <div key={message.id} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[80%] rounded-2xl p-4 ${
                message.type === 'user' 
                  ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white'
                  : 'bg-gray-700/50 text-gray-100 border border-gray-600/50'
              }`}>
                <div className="flex items-start gap-3">
                  {message.type === 'bot' && <Bot size={20} className="text-blue-400 mt-1 flex-shrink-0" />}
                  {message.type === 'user' && <User size={20} className="text-blue-100 mt-1 flex-shrink-0" />}
                  <div className="flex-1">
                    <p className="whitespace-pre-wrap">{message.text}</p>
                    <span className="text-xs opacity-70 mt-2 block">
                      {message.timestamp.toLocaleTimeString()}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-gray-700/50 border border-gray-600/50 rounded-2xl p-4">
                <div className="flex items-center gap-3">
                  <Bot size={20} className="text-blue-400" />
                  <Loader2 size={20} className="text-blue-400 animate-spin" />
                  <span className="text-gray-300">RakeAssist is thinking...</span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-6 border-t border-gray-700/50">
          <div className="flex gap-3">
            <div className="flex-1 relative">
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask about train assignments, like 'Why was Rake-03 on maintenance on day 15?'"
                className="w-full bg-gray-700/50 border border-gray-600/50 rounded-xl p-4 pr-12 text-white placeholder-gray-400 resize-none focus:outline-none focus:ring-2 focus:ring-blue-400/50 focus:border-blue-400/50 transition-all duration-300"
                rows="2"
                disabled={isLoading}
              />
            </div>
            <button
              onClick={sendMessage}
              disabled={!inputMessage.trim() || isLoading}
              className="bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 disabled:from-gray-600 disabled:to-gray-700 text-white p-4 rounded-xl transition-all duration-300 disabled:cursor-not-allowed group"
            >
              <Send size={20} className="group-hover:scale-110 transition-transform duration-300" />
            </button>
          </div>
          
          <div className="mt-3 text-xs text-gray-400">
            💡 Tip: Mention specific train IDs (like Rake-03) and days for best results
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIChatModal;