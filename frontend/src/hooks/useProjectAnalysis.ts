import { useState, useCallback, useRef } from 'react';
import { ProjectRequest, ApiResponse } from '@/types/project.types';
import apiService from '@/services/api';
import Swal from 'sweetalert2';
import toast from 'react-hot-toast';

interface UseProjectAnalysisReturn {
  analyze: (data: ProjectRequest) => Promise<void>;
  loading: boolean;
  progress: number;
  response: ApiResponse | null;
  error: string | null;
  streamingText: string;
  cancelAnalysis: () => void;
  reset: () => void;
}

export const useProjectAnalysis = (): UseProjectAnalysisReturn => {
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [response, setResponse] = useState<ApiResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [streamingText, setStreamingText] = useState('');
  
  const progressInterval = useRef<NodeJS.Timeout | null>(null);
  const streamingInterval = useRef<NodeJS.Timeout | null>(null);

  // Simulate progress for better UX
  const startProgressSimulation = () => {
    setProgress(0);
    if (progressInterval.current) {
      clearInterval(progressInterval.current);
    }
    progressInterval.current = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 90) return prev;
        return prev + Math.random() * 10;
      });
    }, 1000);
  };

  // Simulate streaming text (word by word like AI)
  const startStreamingSimulation = (finalText: string) => {
    const words = finalText.split(' ');
    let index = 0;
    
    setStreamingText('');
    
    if (streamingInterval.current) {
      clearInterval(streamingInterval.current);
    }
    
    streamingInterval.current = setInterval(() => {
      if (index < words.length) {
        setStreamingText((prev) => prev + ' ' + words[index]);
        index++;
      } else {
        if (streamingInterval.current) {
          clearInterval(streamingInterval.current);
          streamingInterval.current = null;
        }
      }
    }, 50);
  };

  const analyze = useCallback(async (data: ProjectRequest) => {
    try {
      setLoading(true);
      setError(null);
      setResponse(null);
      setStreamingText('');
      
      startProgressSimulation();

      const result = await apiService.analyzeProject(data);
      
      // Clear progress interval
      if (progressInterval.current) {
        clearInterval(progressInterval.current);
        progressInterval.current = null;
      }
      setProgress(100);

      // Show success message
      toast.success('Analysis completed successfully!', {
        duration: 3000,
        position: 'top-right',
      });

      setResponse(result);

      // Start streaming simulation with summary
      const summary = `Project "${data.name}" analyzed with ${result.agents_used?.length || 0} agents. Found ${result.data?.project_planning?.features?.length || 0} features. Risk level: ${result.data?.risk_assessment?.risk_level || 'Unknown'}. Estimated timeline: ${result.data?.project_planning?.estimated_timeline_months || '?'} months.`;
      
      startStreamingSimulation(summary);

    } catch (err: any) {
      if (err.code !== 'REQUEST_CANCELLED') {
        setError(err.message || 'Analysis failed');
        
        // Show error alert
        Swal.fire({
          icon: 'error',
          title: 'Analysis Failed',
          text: err.message || 'Failed to analyze project',
          confirmButtonColor: '#ef4444',
        });
      }
    } finally {
      setLoading(false);
    }
  }, []);

  const cancelAnalysis = useCallback(() => {
    apiService.cancelRequest();
    if (progressInterval.current) {
      clearInterval(progressInterval.current);
      progressInterval.current = null;
    }
    if (streamingInterval.current) {
      clearInterval(streamingInterval.current);
      streamingInterval.current = null;
    }
    setLoading(false);
    setProgress(0);
    
    toast('Analysis cancelled', {
      icon: '⚠️',
      duration: 2000,
    });
  }, []);

  const reset = useCallback(() => {
    setResponse(null);
    setError(null);
    setProgress(0);
    setStreamingText('');
    if (streamingInterval.current) {
      clearInterval(streamingInterval.current);
      streamingInterval.current = null;
    }
  }, []);

  return {
    analyze,
    loading,
    progress,
    response,
    error,
    streamingText,
    cancelAnalysis,
    reset,
  };
};