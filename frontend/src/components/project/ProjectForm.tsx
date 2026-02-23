// src/components/project/ProjectForm.tsx
'use client';

import { useState } from 'react';
import { ProjectRequest, ProjectType } from '@/types/project.types';
import { motion } from 'framer-motion';
import Swal from 'sweetalert2';
import { validateProjectRequest } from '@/utils/validators';

interface ProjectFormProps {
  onSubmit: (data: ProjectRequest) => Promise<void>;
  isLoading: boolean;
}

export default function ProjectForm({ onSubmit, isLoading }: ProjectFormProps) {
  const [formData, setFormData] = useState<ProjectRequest>({
    name: '',
    requirements: '',
    project_type: ProjectType.WEB_APP,
    budget_range: '',
    timeline: '',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    
    // Clear error for this field
    if (errors[name]) {
      setErrors((prev) => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validate form
    const validation = validateProjectRequest(formData);
    if (!validation.isValid) {
      setErrors(validation.errors);
      
      Swal.fire({
        icon: 'warning',
        title: 'Validation Error',
        text: 'Please fix the errors in the form',
        confirmButtonColor: '#f59e0b',
      });
      return;
    }

    try {
      await onSubmit(formData);
    } catch (error) {
      console.error('Form submission error:', error);
    }
  };

  const handleCancel = () => {
    Swal.fire({
      title: 'Cancel Analysis?',
      text: "You'll lose all entered data",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#ef4444',
      cancelButtonColor: '#6b7280',
      confirmButtonText: 'Yes, cancel',
    }).then((result) => {
      if (result.isConfirmed) {
        setFormData({
          name: '',
          requirements: '',
          project_type: ProjectType.WEB_APP,
          budget_range: '',
          timeline: '',
        });
        setErrors({});
      }
    });
  };

  return (
    <motion.form
      onSubmit={handleSubmit}
      className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100"
      initial={{ scale: 0.95 }}
      animate={{ scale: 1 }}
      transition={{ duration: 0.3 }}
    >
      <div className="space-y-6">
        {/* Project Name */}
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
            Project Name <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            disabled={isLoading}
            className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all
              ${errors.name ? 'border-red-500' : 'border-gray-300'}
              ${isLoading ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'}`}
            placeholder="e.g., E-commerce Platform"
            maxLength={100}
          />
          {errors.name && (
            <p className="mt-1 text-sm text-red-600">{errors.name}</p>
          )}
        </div>

        {/* Project Type */}
        <div>
          <label htmlFor="project_type" className="block text-sm font-medium text-gray-700 mb-2">
            Project Type <span className="text-red-500">*</span>
          </label>
          <select
            id="project_type"
            name="project_type"
            value={formData.project_type}
            onChange={handleChange}
            disabled={isLoading}
            className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all
              ${errors.project_type ? 'border-red-500' : 'border-gray-300'}
              ${isLoading ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'}`}
          >
            <option value={ProjectType.WEB_APP}>Web Application</option>
            <option value={ProjectType.MOBILE_APP}>Mobile App</option>
            <option value={ProjectType.API}>API / Backend Service</option>
            <option value={ProjectType.ML_SERVICE}>ML / AI Service</option>
            <option value={ProjectType.ECOMMERCE}>E-commerce Platform</option>
          </select>
        </div>

        {/* Requirements */}
        <div>
          <label htmlFor="requirements" className="block text-sm font-medium text-gray-700 mb-2">
            Project Requirements <span className="text-red-500">*</span>
          </label>
          <textarea
            id="requirements"
            name="requirements"
            value={formData.requirements}
            onChange={handleChange}
            disabled={isLoading}
            rows={8}
            className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all
              ${errors.requirements ? 'border-red-500' : 'border-gray-300'}
              ${isLoading ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'}`}
            placeholder="Describe your project in detail...&#10;&#10;Example:&#10;Build an e-commerce platform with user authentication, product catalog, shopping cart, payment integration (Stripe), order management, admin dashboard. Tech preferences: FastAPI, React, PostgreSQL."
            maxLength={10000}
          />
          <div className="flex justify-between mt-1">
            {errors.requirements ? (
              <p className="text-sm text-red-600">{errors.requirements}</p>
            ) : (
              <p className="text-sm text-gray-500">
                {formData.requirements.length}/10000 characters
              </p>
            )}
            <p className="text-sm text-gray-500">
              Min. 10 characters
            </p>
          </div>
        </div>

        {/* Budget & Timeline */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="budget_range" className="block text-sm font-medium text-gray-700 mb-2">
              Budget Range (Optional)
            </label>
            <input
              type="text"
              id="budget_range"
              name="budget_range"
              value={formData.budget_range}
              onChange={handleChange}
              disabled={isLoading}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
              placeholder="e.g., $50,000 - $100,000"
              maxLength={50}
            />
          </div>

          <div>
            <label htmlFor="timeline" className="block text-sm font-medium text-gray-700 mb-2">
              Timeline (Optional)
            </label>
            <input
              type="text"
              id="timeline"
              name="timeline"
              value={formData.timeline}
              onChange={handleChange}
              disabled={isLoading}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
              placeholder="e.g., 3 months"
              maxLength={50}
            />
          </div>
        </div>

        {/* Submit Button */}
        <div className="flex space-x-4 pt-4">
          <button
            type="submit"
            disabled={isLoading}
            className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-6 rounded-lg font-medium hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Analyzing...
              </span>
            ) : (
              'Analyze Project →'
            )}
          </button>
          
          <button
            type="button"
            onClick={handleCancel}
            disabled={isLoading}
            className="px-6 py-3 border border-gray-300 rounded-lg font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Clear
          </button>
        </div>
      </div>

      {/* Security Note */}
      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <p className="text-sm text-blue-700 flex items-center">
          <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
          </svg>
          Your data is encrypted and never stored permanently. API keys are kept secure.
        </p>
      </div>
    </motion.form>
  );
}