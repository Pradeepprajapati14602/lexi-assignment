'use client';

import { useState } from 'react';
import ChatInterface from '@/components/ChatInterface';
import UploadDialog from '@/components/UploadDialog';
import TemplateList from '@/components/TemplateList';
import { FileText, MessageSquare, Upload } from 'lucide-react';

export default function Home() {
  const [activeTab, setActiveTab] = useState<'chat' | 'templates'>('chat');
  const [showUpload, setShowUpload] = useState(false);

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-primary-500 p-2 rounded-lg">
                <FileText className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Lexi</h1>
                <p className="text-sm text-gray-500">Legal Document Templating</p>
              </div>
            </div>
            
            <button
              onClick={() => setShowUpload(true)}
              className="flex items-center space-x-2 bg-primary-500 text-white px-4 py-2 rounded-lg hover:bg-primary-600 transition"
            >
              <Upload className="w-4 h-4" />
              <span>Upload Document</span>
            </button>
          </div>
        </div>
      </header>

      {/* Tabs */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6">
        <div className="bg-white rounded-t-lg shadow-sm">
          <div className="flex border-b">
            <button
              onClick={() => setActiveTab('chat')}
              className={`flex items-center space-x-2 px-6 py-3 font-medium border-b-2 transition ${
                activeTab === 'chat'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              <MessageSquare className="w-4 h-4" />
              <span>Chat & Draft</span>
            </button>
            
            <button
              onClick={() => setActiveTab('templates')}
              className={`flex items-center space-x-2 px-6 py-3 font-medium border-b-2 transition ${
                activeTab === 'templates'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              <FileText className="w-4 h-4" />
              <span>Templates</span>
            </button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-8">
        <div className="bg-white rounded-b-lg shadow-lg">
          {activeTab === 'chat' ? (
            <ChatInterface />
          ) : (
            <TemplateList />
          )}
        </div>
      </div>

      {/* Upload Dialog */}
      {showUpload && (
        <UploadDialog onClose={() => setShowUpload(false)} />
      )}

      {/* Footer - UOIONHHC */}
      <footer className="text-center py-4 text-gray-500 text-sm">
        <p>Built with ❤️ for practical legal tech automation</p>
      </footer>
    </main>
  );
}
