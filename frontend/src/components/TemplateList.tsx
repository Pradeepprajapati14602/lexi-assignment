'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { FileText, Tag, Calendar, Eye, Trash2, Loader2 } from 'lucide-react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface Template {
  id: string;
  title: string;
  file_description?: string;
  doc_type?: string;
  jurisdiction?: string;
  similarity_tags?: string[];
  created_at: string;
  variables: Array<{
    id: number;
    key: string;
    label: string;
    required: boolean;
  }>;
}

export default function TemplateList() {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedTemplate, setSelectedTemplate] = useState<Template | null>(null);
  const [showDetails, setShowDetails] = useState(false);

  useEffect(() => {
    fetchTemplates();
  }, []);

  const fetchTemplates = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_URL}/api/templates/`);
      setTemplates(response.data);
    } catch (error) {
      console.error('Error fetching templates:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (templateId: string) => {
    if (!confirm('Are you sure you want to delete this template?')) return;

    try {
      await axios.delete(`${API_URL}/api/templates/${templateId}`);
      setTemplates(templates.filter((t) => t.id !== templateId));
    } catch (error) {
      console.error('Error deleting template:', error);
      alert('Error deleting template');
    }
  };

  const handleViewDetails = (template: Template) => {
    setSelectedTemplate(template);
    setShowDetails(true);
  };

  const exportTemplate = async (templateId: string) => {
    try {
      const response = await axios.get(
        `${API_URL}/api/templates/${templateId}/export`
      );
      
      const blob = new Blob([response.data.markdown], { type: 'text/markdown' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `template_${templateId}.md`;
      a.click();
    } catch (error) {
      console.error('Error exporting template:', error);
      alert('Error exporting template');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-8 h-8 animate-spin text-primary-500" />
      </div>
    );
  }

  if (templates.length === 0) {
    return (
      <div className="text-center py-12">
        <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          No templates yet
        </h3>
        <p className="text-gray-600">
          Upload a document to create your first template
        </p>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Templates</h2>
        <p className="text-gray-600 mt-1">
          {templates.length} template{templates.length !== 1 ? 's' : ''} available
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {templates.map((template) => (
          <div
            key={template.id}
            className="border rounded-lg p-4 hover:shadow-md transition"
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex-1">
                <h3 className="font-semibold text-gray-900 mb-1">
                  {template.title}
                </h3>
                <p className="text-sm text-gray-600 line-clamp-2">
                  {template.file_description || 'No description'}
                </p>
              </div>
            </div>

            {template.similarity_tags && template.similarity_tags.length > 0 && (
              <div className="flex flex-wrap gap-1 mb-3">
                {template.similarity_tags.slice(0, 3).map((tag, index) => (
                  <span
                    key={index}
                    className="inline-flex items-center space-x-1 bg-blue-50 text-blue-700 text-xs px-2 py-1 rounded"
                  >
                    <Tag className="w-3 h-3" />
                    <span>{tag}</span>
                  </span>
                ))}
              </div>
            )}

            <div className="flex items-center justify-between text-sm text-gray-500 mb-3">
              <span>{template.variables.length} variables</span>
              <span className="flex items-center space-x-1">
                <Calendar className="w-3 h-3" />
                <span>{new Date(template.created_at).toLocaleDateString()}</span>
              </span>
            </div>

            <div className="flex space-x-2">
              <button
                onClick={() => handleViewDetails(template)}
                className="flex-1 flex items-center justify-center space-x-1 bg-primary-50 text-primary-700 px-3 py-2 rounded hover:bg-primary-100 transition text-sm"
              >
                <Eye className="w-4 h-4" />
                <span>View</span>
              </button>
              
              <button
                onClick={() => exportTemplate(template.id)}
                className="flex items-center justify-center space-x-1 bg-gray-50 text-gray-700 px-3 py-2 rounded hover:bg-gray-100 transition text-sm"
              >
                <FileText className="w-4 h-4" />
              </button>
              
              <button
                onClick={() => handleDelete(template.id)}
                className="flex items-center justify-center space-x-1 bg-red-50 text-red-700 px-3 py-2 rounded hover:bg-red-100 transition text-sm"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Details Modal */}
      {showDetails && selectedTemplate && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto m-4">
            <div className="flex items-center justify-between p-6 border-b">
              <h2 className="text-2xl font-bold text-gray-900">
                {selectedTemplate.title}
              </h2>
              <button
                onClick={() => setShowDetails(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                ✕
              </button>
            </div>

            <div className="p-6 space-y-6">
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Details</h3>
                <div className="bg-gray-50 rounded-lg p-4 space-y-2 text-sm">
                  <p><span className="font-medium">ID:</span> {selectedTemplate.id}</p>
                  <p><span className="font-medium">Type:</span> {selectedTemplate.doc_type || 'N/A'}</p>
                  <p><span className="font-medium">Jurisdiction:</span> {selectedTemplate.jurisdiction || 'N/A'}</p>
                  <p><span className="font-medium">Created:</span> {new Date(selectedTemplate.created_at).toLocaleString()}</p>
                </div>
              </div>

              <div>
                <h3 className="font-semibold text-gray-900 mb-2">
                  Variables ({selectedTemplate.variables.length})
                </h3>
                <div className="space-y-2 max-h-96 overflow-y-auto">
                  {selectedTemplate.variables.map((variable) => (
                    <div
                      key={variable.id}
                      className="border rounded-lg p-3 flex items-center justify-between"
                    >
                      <div>
                        <p className="font-medium text-gray-900">{variable.label}</p>
                        <p className="text-sm text-gray-500">{variable.key}</p>
                      </div>
                      {variable.required && (
                        <span className="text-xs bg-red-100 text-red-700 px-2 py-1 rounded">
                          Required
                        </span>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="border-t p-4 text-center text-xs text-gray-500">
              UOIONHHC - Template Details
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
