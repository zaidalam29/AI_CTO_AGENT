// src/components/project/LoadingAnimation.tsx
'use client';

import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';

interface LoadingAnimationProps {
  progress: number;
  agents: string[];
}

const agentMessages = {
  planner: "📋 Breaking down requirements into features...",
  architect: "🏗️ Designing system architecture...",
  risk: "⚠️ Analyzing potential risks...",
  sprint: "📅 Creating sprint plans...",
  devops: "🔧 Setting up DevOps pipeline...",
  code_review: "👨‍💻 Reviewing code quality..."
};

export default function LoadingAnimation({ progress, agents }: LoadingAnimationProps) {
  const [currentAgentIndex, setCurrentAgentIndex] = useState(0);
  const [dots, setDots] = useState('');

  // Rotate through agents
  useEffect(() => {
    if (agents.length === 0) return;
    
    const interval = setInterval(() => {
      setCurrentAgentIndex((prev) => (prev + 1) % agents.length);
    }, 2000);
    
    return () => clearInterval(interval);
  }, [agents]);

  // Animated dots
  useEffect(() => {
    const interval = setInterval(() => {
      setDots((prev) => (prev.length >= 3 ? '' : prev + '.'));
    }, 500);
    
    return () => clearInterval(interval);
  }, []);

  const currentAgent = agents[currentAgentIndex] || 'planner';
  const message = agentMessages[currentAgent as keyof typeof agentMessages] || 'Processing...';

  return (
    <div className="w-full max-w-2xl mx-auto p-8 bg-white rounded-xl shadow-lg">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          AI CTO Agents at Work
        </h2>
        <p className="text-gray-600 mt-2">
          {message} {dots}
        </p>
      </div>

      {/* Agent Icons Row */}
      <div className="flex justify-center space-x-4 mb-8">
        {agents.map((agent, index) => (
          <motion.div
            key={agent}
            className="relative"
            animate={{
              scale: index === currentAgentIndex ? 1.2 : 1,
              opacity: index === currentAgentIndex ? 1 : 0.5,
            }}
            transition={{ duration: 0.3 }}
          >
            <div className={`w-12 h-12 rounded-full flex items-center justify-center text-2xl
              ${index === currentAgentIndex 
                ? 'bg-blue-100 text-blue-600 ring-4 ring-blue-200' 
                : 'bg-gray-100 text-gray-600'}`}>
              {agent === 'planner' && '📋'}
              {agent === 'architect' && '🏗️'}
              {agent === 'risk' && '⚠️'}
              {agent === 'sprint' && '📅'}
              {agent === 'devops' && '🔧'}
              {agent === 'code_review' && '👨‍💻'}
            </div>
          </motion.div>
        ))}
      </div>

      {/* Progress Bar */}
      <div className="relative pt-1">
        <div className="flex mb-2 items-center justify-between">
          <div>
            <span className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-blue-600 bg-blue-200">
              Progress
            </span>
          </div>
          <div className="text-right">
            <span className="text-xs font-semibold inline-block text-blue-600">
              {Math.round(progress)}%
            </span>
          </div>
        </div>
        <div className="overflow-hidden h-2 mb-4 text-xs flex rounded bg-blue-200">
          <motion.div
            className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-gradient-to-r from-blue-500 to-purple-500"
            style={{ width: `${progress}%` }}
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </div>

      {/* Animated Thinking Dots */}
      <div className="flex justify-center space-x-2 mt-4">
        {[0, 1, 2].map((i) => (
          <motion.div
            key={i}
            className="w-2 h-2 bg-blue-500 rounded-full"
            animate={{
              y: [0, -10, 0],
            }}
            transition={{
              duration: 0.6,
              repeat: Infinity,
              delay: i * 0.2,
            }}
          />
        ))}
      </div>

      {/* Agent Status */}
      <div className="mt-6 grid grid-cols-3 gap-2 text-xs text-gray-600">
        {agents.map((agent, index) => (
          <div
            key={agent}
            className={`p-2 rounded text-center ${
              index < currentAgentIndex
                ? 'bg-green-100 text-green-700'
                : index === currentAgentIndex
                ? 'bg-blue-100 text-blue-700 animate-pulse'
                : 'bg-gray-100'
            }`}
          >
            {agent}
          </div>
        ))}
      </div>
    </div>
  );
}