'use client';

import { ApiResponse } from '@/types/project.types';
import { motion } from 'framer-motion';
import TypingEffect from '@/components/ui/TypingEffect';
import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import Swal from 'sweetalert2';
import toast from 'react-hot-toast';

interface ProjectResultProps {
  response: ApiResponse | null;
  streamingText: string;
  onReset: () => void;
}

export default function ProjectResult({ response, streamingText, onReset }: ProjectResultProps) {
  const [activeTab, setActiveTab] = useState('overview');
  const [showRawJson, setShowRawJson] = useState(false);

  if (!response?.data) {
    return null;
  }

  const { data } = response;
  const agentStatus = data.agent_status || {};

  const handleDownload = () => {
    const jsonStr = JSON.stringify(response, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const href = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = href;
    link.download = `project-analysis-${new Date().toISOString()}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    toast.success('Report downloaded successfully!');
  };

  const handleShare = () => {
    navigator.clipboard.writeText(window.location.href);
    toast.success('Link copied to clipboard!');
  };

  const handlePrint = () => {
    window.print();
  };

  const getAgentIcon = (agent: string, status: string) => {
    const icons: Record<string, string> = {
      planner: '📋',
      architect: '🏗️',
      risk: '⚠️',
      sprint: '📅',
      devops: '🔧',
      code_review: '👨‍💻',
    };

    const statusEmoji = status === 'success' ? '✅' : status === 'error' ? '❌' : '⏳';
    
    return `${icons[agent] || '🤖'} ${statusEmoji}`;
  };

  return (
    <motion.div
      className="max-w-6xl mx-auto"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      {/* Header */}
      <div className="bg-white rounded-t-2xl p-6 border-b border-gray-200">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">
              Analysis Complete! 🎉
            </h2>
            <p className="text-gray-600 mt-1">
              Request ID: {response.request_id}
            </p>
          </div>
          <div className="flex space-x-2">
            <button
              onClick={handleDownload}
              className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
              title="Download JSON"
            >
              📥
            </button>
            <button
              onClick={handleShare}
              className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
              title="Share"
            >
              🔗
            </button>
            <button
              onClick={handlePrint}
              className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
              title="Print"
            >
              🖨️
            </button>
            <button
              onClick={onReset}
              className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
              title="New Analysis"
            >
              ✖️
            </button>
          </div>
        </div>

        {/* Streaming Text */}
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-4 rounded-lg">
          <TypingEffect
            text={streamingText}
            speed={30}
            className="text-gray-700"
          />
        </div>

        {/* Agent Status */}
        <div className="grid grid-cols-5 gap-2 mt-4">
          {Object.entries(agentStatus).map(([agent, status]) => (
            <div
              key={agent}
              className={`text-center p-2 rounded-lg ${
                status === 'success' ? 'bg-green-100' :
                status === 'error' ? 'bg-red-100' : 'bg-yellow-100'
              }`}
            >
              <div className="text-2xl">
                {getAgentIcon(agent, status)}
              </div>
              <div className="text-xs capitalize mt-1">{agent}</div>
            </div>
          ))}
        </div>

        {/* Meta Info */}
        <div className="flex items-center justify-between mt-4 text-sm text-gray-500">
          <span>Processing Time: {response.processing_time || 'N/A'}</span>
          <span>Agents Used: {response.agents_used?.join(', ') || 'N/A'}</span>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white border-b border-gray-200">
        <nav className="flex space-x-8 px-6" aria-label="Tabs">
          {['overview', 'planning', 'architecture', 'risks', 'sprints', 'devops'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`py-4 px-1 border-b-2 font-medium text-sm capitalize transition-colors ${
                activeTab === tab
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              {tab}
            </button>
          ))}
          <button
            onClick={() => setShowRawJson(!showRawJson)}
            className="py-4 px-1 border-b-2 border-transparent font-medium text-sm text-gray-500 hover:text-gray-700"
          >
            {showRawJson ? 'Hide JSON' : 'View JSON'}
          </button>
        </nav>
      </div>

      {/* Content */}
      <div className="bg-white rounded-b-2xl p-6 min-h-[400px]">
        {showRawJson ? (
          <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-auto max-h-[600px]">
            {JSON.stringify(response, null, 2)}
          </pre>
        ) : (
          <div className="prose max-w-none">
            {activeTab === 'overview' && (
              <div>
                <h3 className="text-xl font-semibold mb-4">Project Overview</h3>
                <div className="grid grid-cols-2 gap-6">
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <h4 className="font-medium mb-2">Features</h4>
                    <ul className="space-y-2">
                      {data.project_planning?.features?.map((f: any, i: number) => (
                        <li key={i} className="flex items-start">
                          <span className="text-green-500 mr-2">✓</span>
                          <div>
                            <span className="font-medium">{f.name}</span>
                            <span className={`ml-2 text-xs px-2 py-1 rounded ${
                              f.priority === 'high' ? 'bg-red-100 text-red-700' :
                              f.priority === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                              'bg-green-100 text-green-700'
                            }`}>
                              {f.priority}
                            </span>
                          </div>
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <h4 className="font-medium mb-2">Tech Stack</h4>
                    {Object.entries(data.project_planning?.tech_stack || {}).map(([key, value]) => (
                      <div key={key} className="mb-3">
                        <div className="text-sm font-medium text-gray-600 capitalize mb-1">{key}:</div>
                        <div className="flex flex-wrap gap-2">
                          {(value as string[]).map((tech, i) => (
                            <span key={i} className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-sm">
                              {tech}
                            </span>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="mt-6 grid grid-cols-2 gap-6">
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <h4 className="font-medium mb-2">Timeline</h4>
                    <p className="text-2xl font-bold text-blue-600">
                      {data.project_planning?.estimated_timeline_months} months
                    </p>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <h4 className="font-medium mb-2">Cost Estimate</h4>
                    <p className="text-2xl font-bold text-green-600">
                      {data.project_planning?.estimated_cost_range}
                    </p>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'risks' && (
              <div>
                <h3 className="text-xl font-semibold mb-4">Risk Assessment</h3>
                <div className="mb-6">
                  <div className="flex items-center justify-between mb-2">
                    <span>Risk Score</span>
                    <span className="font-bold">{data.risk_assessment?.overall_risk_score}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div 
                      className={`h-2.5 rounded-full ${
                        (data.risk_assessment?.overall_risk_score || 0) < 30 ? 'bg-green-600' :
                        (data.risk_assessment?.overall_risk_score || 0) < 60 ? 'bg-yellow-600' :
                        'bg-red-600'
                      }`}
                      style={{ width: `${data.risk_assessment?.overall_risk_score || 0}%` }}
                    ></div>
                  </div>
                  <p className="text-center mt-2 font-medium">
                    Risk Level: <span className={
                      data.risk_assessment?.risk_level === 'Low' ? 'text-green-600' :
                      data.risk_assessment?.risk_level === 'Medium' ? 'text-yellow-600' :
                      'text-red-600'
                    }>{data.risk_assessment?.risk_level}</span>
                  </p>
                </div>
                <div className="space-y-4">
                  {data.risk_assessment?.risks?.map((risk: any, i: number) => (
                    <div key={i} className="border rounded-lg p-4">
                      <div className="flex items-start justify-between">
                        <div>
                          <h4 className="font-medium">{risk.description}</h4>
                          <p className="text-sm text-gray-600 mt-1">Category: {risk.category}</p>
                        </div>
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                          risk.impact === 'high' ? 'bg-red-100 text-red-700' :
                          risk.impact === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                          'bg-green-100 text-green-700'
                        }`}>
                          {risk.impact}
                        </span>
                      </div>
                      <div className="mt-3">
                        <div className="w-full bg-gray-200 rounded-full h-1.5">
                          <div 
                            className="bg-blue-600 h-1.5 rounded-full"
                            style={{ width: `${risk.probability * 100}%` }}
                          ></div>
                        </div>
                        <p className="text-xs text-gray-500 mt-1">
                          Probability: {(risk.probability * 100).toFixed(0)}%
                        </p>
                      </div>
                      <p className="mt-3 text-sm text-gray-700">
                        <span className="font-medium">Mitigation:</span> {risk.mitigation}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'architecture' && (
              <div>
                <h3 className="text-xl font-semibold mb-4">System Architecture</h3>
                <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-auto">
                  {JSON.stringify(data.system_architecture, null, 2)}
                </pre>
              </div>
            )}

            {activeTab === 'sprints' && (
              <div>
                <h3 className="text-xl font-semibold mb-4">Sprint Planning</h3>
                <div className="space-y-6">
                  {data.sprint_planning?.sprints?.map((sprint: any, i: number) => (
                    <div key={i} className="border rounded-lg p-4">
                      <h4 className="text-lg font-medium mb-2">
                        Sprint {sprint.sprint_number}: {sprint.name}
                      </h4>
                      <p className="text-sm text-gray-600 mb-3">
                        Duration: {sprint.duration_weeks} weeks | Capacity: {sprint.capacity} points
                      </p>
                      <div className="space-y-2">
                        {sprint.user_stories?.map((story: any, j: number) => (
                          <div key={j} className="bg-gray-50 p-3 rounded">
                            <div className="flex items-start justify-between">
                              <span className="font-medium">{story.title}</span>
                              <span className="bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs">
                                {story.points} pts
                              </span>
                            </div>
                            <p className="text-sm text-gray-600 mt-1">{story.description}</p>
                          </div>
                        ))}
                      </div>
                      <div className="mt-3">
                        <h5 className="font-medium text-sm mb-1">Goals:</h5>
                        <ul className="list-disc list-inside text-sm text-gray-600">
                          {sprint.goals?.map((goal: string, j: number) => (
                            <li key={j}>{goal}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'devops' && (
              <div>
                <h3 className="text-xl font-semibold mb-4">DevOps Plan</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <h4 className="font-medium mb-3">CI/CD Pipeline</h4>
                    <ol className="list-decimal list-inside space-y-2">
                      {data.devops_plan?.ci_cd_pipeline?.map((step: string, i: number) => (
                        <li key={i} className="text-sm">{step}</li>
                      ))}
                    </ol>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <h4 className="font-medium mb-3">Monitoring Tools</h4>
                    <ul className="list-disc list-inside space-y-2">
                      {data.devops_plan?.monitoring_tools?.map((tool: string, i: number) => (
                        <li key={i} className="text-sm">{tool}</li>
                      ))}
                    </ul>
                  </div>
                </div>
                <div className="mt-6">
                  <h4 className="font-medium mb-3">Infrastructure</h4>
                  <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-auto">
                    {JSON.stringify(data.devops_plan?.infrastructure, null, 2)}
                  </pre>
                </div>
                <div className="mt-6">
                  <h4 className="font-medium mb-3">Backup & Recovery</h4>
                  <p className="text-gray-700 mb-2">
                    <span className="font-medium">Backup:</span> {data.devops_plan?.backup_strategy}
                  </p>
                  <p className="text-gray-700">
                    <span className="font-medium">Disaster Recovery:</span> {data.devops_plan?.disaster_recovery}
                  </p>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </motion.div>
  );
}