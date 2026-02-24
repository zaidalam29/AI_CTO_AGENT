'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import ProjectForm from '@/components/project/ProjectForm';
import ProjectResult from '@/components/project/ProjectResult';
import LoadingAnimation from '@/components/project/LoadingAnimation';
import { useProjectAnalysis } from '@/hooks/useProjectAnalysis';
import { ProjectRequest } from '@/types/project.types';

export default function Home() {
  const {
    analyze,
    loading,
    progress,
    response,
    error,
    streamingText,
    reset,
  } = useProjectAnalysis();

  const [showResult, setShowResult] = useState(false);

  const handleSubmit = async (data: ProjectRequest) => {
    try {
      await analyze(data);
      setShowResult(true);
    } catch (error) {
      console.error('Analysis failed:', error);
    }
  };

  const handleReset = () => {
    reset();
    setShowResult(false);
  };

  {
    error && (
      <div className="alert-error mb-4">
        Error: {error}
      </div>
    )
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <span className="text-4xl">🤖</span>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  AI CTO Agent
                </h1>
                <p className="text-sm text-gray-600">
                  Your Artificial Intelligence Chief Technology Officer
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                v1.0.0
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <AnimatePresence mode="wait">
          {!showResult ? (
            <motion.div
              key="form"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.5 }}
              className="max-w-3xl mx-auto"
            >
              {/* Hero Section */}
              <div className="text-center mb-12">
                <motion.h2
                  className="text-4xl font-bold text-gray-900 mb-4"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 }}
                >
                  Transform Your Ideas Into
                  <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent block">
                    Technical Excellence
                  </span>
                </motion.h2>
                <motion.p
                  className="text-xl text-gray-600"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3 }}
                >
                  Describe your project and let our AI agents create a complete technical plan
                </motion.p>
              </div>

              {/* Stats */}
              <motion.div
                className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
              >
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
                  <div className="text-3xl mb-2">📋</div>
                  <div className="text-2xl font-bold text-gray-900">6</div>
                  <div className="text-sm text-gray-600">Specialized AI Agents</div>
                </div>
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
                  <div className="text-3xl mb-2">⚡</div>
                  <div className="text-2xl font-bold text-gray-900">2min</div>
                  <div className="text-sm text-gray-600">Average Analysis Time</div>
                </div>
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
                  <div className="text-3xl mb-2">🎯</div>
                  <div className="text-2xl font-bold text-gray-900">95%</div>
                  <div className="text-sm text-gray-600">Accuracy Rate</div>
                </div>
              </motion.div>

              {/* Form */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
              >
                <ProjectForm onSubmit={handleSubmit} isLoading={loading} />
              </motion.div>

              {/* Features */}
              <motion.div
                className="mt-16 grid grid-cols-1 md:grid-cols-2 gap-8"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.6 }}
              >
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0 w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center text-2xl">
                    📋
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">Smart Planning</h3>
                    <p className="text-gray-600">Automatically break down requirements into features and sprints</p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0 w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center text-2xl">
                    🏗️
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">Architecture Design</h3>
                    <p className="text-gray-600">Get scalable system architecture with database design</p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0 w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center text-2xl">
                    ⚠️
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">Risk Assessment</h3>
                    <p className="text-gray-600">Identify potential risks with ML-powered predictions</p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0 w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center text-2xl">
                    🔧
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">DevOps Ready</h3>
                    <p className="text-gray-600">Complete CI/CD pipeline and infrastructure plans</p>
                  </div>
                </div>
              </motion.div>
            </motion.div>
          ) : (
            <motion.div
              key="result"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.5 }}
            >
              {loading ? (
                <LoadingAnimation
                  progress={progress}
                  agents={response?.agents_used || ['planner', 'architect', 'risk', 'sprint', 'devops']}
                />
              ) : (
                <ProjectResult
                  response={response}
                  streamingText={streamingText}
                  onReset={handleReset}
                />
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-gray-600 text-sm">
            Copyright © 2024 AI CTO Agent
          </p>
        </div>
      </footer>
    </main>
  );
}