'use client';

import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { X, Upload, Loader2, FileText, CheckCircle } from 'lucide-react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface UploadDialogProps {
  onClose: () => void;
}

interface ExtractedVariable {
  key: string;
  label: string;
  description?: string;
  example?: string;
  required: boolean;
}

export default function UploadDialog({ onClose }: UploadDialogProps) {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [extracting, setExtracting] = useState(false);
  const [documentId, setDocumentId] = useState<string | null>(null);
  const [extractedData, setExtractedData] = useState<any>(null);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
    maxFiles: 1,
  });

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const uploadResponse = await axios.post(
        `${API_URL}/api/documents/upload`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      const docId = uploadResponse.data.document_id;
      setDocumentId(docId);
      setUploading(false);
      setExtracting(true);

      // Extract template
      const extractResponse = await axios.post(
        `${API_URL}/api/documents/extract-template/${docId}`
      );

      setExtractedData(extractResponse.data);
      setExtracting(false);
    } catch (error) {
      console.error('Error uploading document:', error);
      alert('Error uploading document. Please try again.');
      setUploading(false);
      setExtracting(false);
    }
  };

  const handleSaveTemplate = async () => {
    if (!extractedData) return;

    setSaving(true);

    try {
      await axios.post(`${API_URL}/api/templates/`, extractedData.template);
      setSaved(true);
      
      setTimeout(() => {
        onClose();
        window.location.reload(); // Refresh to show new template
      }, 2000);
    } catch (error) {
      console.error('Error saving template:', error);
      alert('Error saving template. Please try again.');
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto m-4">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b">
          <h2 className="text-2xl font-bold text-gray-900">Upload Document</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          {!file && (
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition ${
                isDragActive
                  ? 'border-primary-500 bg-primary-50'
                  : 'border-gray-300 hover:border-primary-400'
              }`}
            >
              <input {...getInputProps()} />
              <Upload className="w-12 h-12 mx-auto mb-4 text-gray-400" />
              <p className="text-lg font-medium text-gray-700 mb-2">
                {isDragActive ? 'Drop the file here' : 'Drag & drop a document'}
              </p>
              <p className="text-sm text-gray-500">
                or click to select (PDF, DOCX only, max 10MB)
              </p>
            </div>
          )}

          {file && !extractedData && (
            <div className="space-y-4">
              <div className="flex items-center space-x-3 p-4 bg-gray-50 rounded-lg">
                <FileText className="w-8 h-8 text-primary-500" />
                <div className="flex-1">
                  <p className="font-medium text-gray-900">{file.name}</p>
                  <p className="text-sm text-gray-500">
                    {(file.size / 1024).toFixed(2)} KB
                  </p>
                </div>
                {!uploading && !extracting && (
                  <button
                    onClick={() => setFile(null)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    <X className="w-5 h-5" />
                  </button>
                )}
              </div>

              {uploading && (
                <div className="flex items-center justify-center space-x-2 py-8">
                  <Loader2 className="w-6 h-6 animate-spin text-primary-500" />
                  <span className="text-gray-600">Uploading document...</span>
                </div>
              )}

              {extracting && (
                <div className="flex items-center justify-center space-x-2 py-8">
                  <Loader2 className="w-6 h-6 animate-spin text-primary-500" />
                  <span className="text-gray-600">Extracting variables with AI...</span>
                </div>
              )}

              {!uploading && !extracting && (
                <button
                  onClick={handleUpload}
                  className="w-full bg-primary-500 text-white px-6 py-3 rounded-lg hover:bg-primary-600 transition font-medium"
                >
                  Process Document
                </button>
              )}
            </div>
          )}

          {extractedData && !saved && (
            <div className="space-y-6">
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-5 h-5 text-green-600" />
                  <span className="font-medium text-green-900">
                    Template extracted successfully!
                  </span>
                </div>
                <p className="text-sm text-green-700 mt-1">
                  Found {extractedData.template.variables.length} variables
                </p>
              </div>

              <div>
                <h3 className="text-lg font-semibold mb-2">Template Details</h3>
                <div className="bg-gray-50 rounded-lg p-4 space-y-2">
                  <p><span className="font-medium">Title:</span> {extractedData.template.title}</p>
                  <p><span className="font-medium">Tags:</span> {extractedData.template.similarity_tags?.join(', ') || 'None'}</p>
                </div>
              </div>

              <div>
                <h3 className="text-lg font-semibold mb-3">Detected Variables</h3>
                <div className="space-y-2 max-h-96 overflow-y-auto">
                  {extractedData.template.variables.map((variable: ExtractedVariable, index: number) => (
                    <div key={index} className="border rounded-lg p-3 hover:bg-gray-50">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <p className="font-medium text-gray-900">{variable.label}</p>
                          <p className="text-sm text-gray-600 mt-1">{variable.description}</p>
                          {variable.example && (
                            <p className="text-xs text-gray-500 mt-1">
                              Example: {variable.example}
                            </p>
                          )}
                        </div>
                        {variable.required && (
                          <span className="text-xs bg-red-100 text-red-700 px-2 py-1 rounded">
                            Required
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="flex space-x-3">
                <button
                  onClick={handleSaveTemplate}
                  disabled={saving}
                  className="flex-1 bg-primary-500 text-white px-6 py-3 rounded-lg hover:bg-primary-600 transition font-medium disabled:opacity-50"
                >
                  {saving ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin inline mr-2" />
                      Saving...
                    </>
                  ) : (
                    'Save Template'
                  )}
                </button>
                
                <button
                  onClick={onClose}
                  className="px-6 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition font-medium"
                >
                  Cancel
                </button>
              </div>
            </div>
          )}

          {saved && (
            <div className="py-12 text-center">
              <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Template Saved Successfully!
              </h3>
              <p className="text-gray-600">
                You can now use this template for drafting documents.
              </p>
            </div>
          )}
        </div>

        {/* Footer - UOIONHHC */}
        <div className="border-t p-4 text-center text-xs text-gray-500">
          AI-powered template extraction using Gemini
        </div>
      </div>
    </div>
  );
}
