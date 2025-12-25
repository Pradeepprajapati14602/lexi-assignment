'use client';

import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { Send, Copy, Download, Loader2 } from 'lucide-react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  type?: string;
  data?: any;
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: 'Hello! I can help you draft legal documents. Just tell me what you need, like:\n\n- "Draft a notice to insurer in India"\n- "/draft employment termination letter"\n- "Create a lease agreement"\n\nYou can also use /vars to check variable status.',
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post(`${API_URL}/api/chat/message`, {
        message: input,
        conversation_id: conversationId,
      });

      const data = response.data;
      setConversationId(data.conversation_id);

      const assistantMessage: Message = {
        role: 'assistant',
        content: data.message,
        type: data.message_type,
        data: data.data,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: '❌ Sorry, there was an error processing your request. Please try again.',
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    alert('Copied to clipboard!');
  };

  const downloadMarkdown = (text: string) => {
    const blob = new Blob([text], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'draft.md';
    a.click();
  };

  return (
    <div className="flex flex-col h-[calc(100vh-12rem)]">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-3xl rounded-lg p-4 ${
                message.role === 'user'
                  ? 'bg-primary-500 text-white'
                  : 'bg-gray-100 text-gray-900'
              }`}
            >
              <div className="markdown-body prose prose-sm max-w-none">
                <ReactMarkdown>{message.content}</ReactMarkdown>
              </div>

              {/* Draft Actions */}
              {message.type === 'draft' && message.data && (
                <div className="mt-4 flex space-x-2 pt-4 border-t border-gray-200">
                  <button
                    onClick={() => copyToClipboard(message.data.draft_md)}
                    className="flex items-center space-x-1 bg-white text-gray-700 px-3 py-1 rounded hover:bg-gray-50 text-sm"
                  >
                    <Copy className="w-3 h-3" />
                    <span>Copy</span>
                  </button>
                  
                  <button
                    onClick={() => downloadMarkdown(message.data.draft_md)}
                    className="flex items-center space-x-1 bg-white text-gray-700 px-3 py-1 rounded hover:bg-gray-50 text-sm"
                  >
                    <Download className="w-3 h-3" />
                    <span>Download MD</span>
                  </button>
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-lg p-4">
              <Loader2 className="w-5 h-5 animate-spin text-gray-500" />
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t bg-gray-50 p-4">
        <div className="max-w-4xl mx-auto flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message or use /draft, /vars..."
            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            disabled={loading}
          />
          
          <button
            onClick={handleSend}
            disabled={loading || !input.trim()}
            className="bg-primary-500 text-white px-6 py-2 rounded-lg hover:bg-primary-600 transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </button>
        </div>
        
        <p className="text-xs text-gray-500 text-center mt-2">
          Press Enter to send, Shift+Enter for new line. Created by UOIONHHC
        </p>
      </div>
    </div>
  );
}
