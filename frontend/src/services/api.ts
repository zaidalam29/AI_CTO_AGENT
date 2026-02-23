import axios, { AxiosInstance, AxiosError } from 'axios';
import Swal from 'sweetalert2';
import { ApiResponse, ProjectRequest } from '@/types/project.types';

class ApiService {
  private api: AxiosInstance;
  private abortController: AbortController | null = null;

  constructor() {
    this.api = axios.create({
      // Increase timeout significantly (60 seconds)
      timeout: 60000, // 60 seconds
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    });

    // Request interceptor
    this.api.interceptors.request.use(
      (config) => {
        // Add request ID
        config.headers['X-Request-ID'] = this.generateRequestId();
        
        // Add timestamp
        config.headers['X-Timestamp'] = Date.now().toString();
        
        // TEMPORARILY DISABLE AUTH TOKEN FOR TESTING
        // Comment this out to see if token is causing the issue
        // const token = localStorage.getItem('auth_token');
        // if (token) {
        //   config.headers.Authorization = `Bearer ${token}`;
        // }

        console.log('🚀 Request:', {
          method: config.method,
          url: config.url,
          data: config.data
        });

        return config;
      },
      (error) => {
        console.error('❌ Request Error:', error);
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.api.interceptors.response.use(
      (response) => {
        console.log('✅ Response:', response.status, response.data);
        return response;
      },
      (error: AxiosError) => {
        console.error('❌ Response Error:', {
          status: error.response?.status,
          statusText: error.response?.statusText,
          data: error.response?.data,
          message: error.message,
          code: error.code
        });
        return this.handleError(error);
      }
    );
  }

  private generateRequestId(): string {
    return `req_${Math.random().toString(36).substr(2, 9)}`;
  }

  private async handleError(error: AxiosError): Promise<never> {
    let message = 'An unexpected error occurred';
    let code = 'UNKNOWN_ERROR';

    if (error.code === 'ECONNABORTED') {
      message = 'Request timeout. The server is taking too long to respond.';
      code = 'TIMEOUT_ERROR';
      
      await Swal.fire({
        icon: 'warning',
        title: 'Timeout Error',
        text: message,
        confirmButtonColor: '#f59e0b',
      });
      
      return Promise.reject({ code, message, originalError: error });
    }

    if (error.response) {
      const status = error.response.status;
      const data = error.response.data as any;

      // Log the full error response
      console.error('Server error response:', data);

      switch (status) {
        case 400:
          message = data?.error?.message || data?.message || 'Bad request';
          code = 'BAD_REQUEST';
          break;
        case 401:
          message = 'Unauthorized. Please login again.';
          code = 'UNAUTHORIZED';
          break;
        case 403:
          message = 'You do not have permission to perform this action';
          code = 'FORBIDDEN';
          break;
        case 404:
          message = 'Resource not found';
          code = 'NOT_FOUND';
          break;
        case 422:
          message = data?.error?.message || data?.message || 'Validation error';
          code = 'VALIDATION_ERROR';
          break;
        case 429:
          message = 'Too many requests. Please try again later.';
          code = 'RATE_LIMIT_EXCEEDED';
          break;
        case 500:
        case 502:
        case 503:
          message = data?.error?.message || data?.message || 'Server error. Please try again later.';
          code = 'SERVER_ERROR';
          break;
        default:
          message = data?.error?.message || data?.message || `Error ${status}`;
      }

      await Swal.fire({
        icon: 'error',
        title: 'Error',
        text: message,
        confirmButtonColor: '#ef4444',
      });

    } else if (error.request) {
      message = 'Cannot connect to server. Please check your internet connection.';
      code = 'NETWORK_ERROR';
      
      await Swal.fire({
        icon: 'error',
        title: 'Connection Error',
        text: message,
        confirmButtonColor: '#ef4444',
      });
    } else {
      message = error.message || 'An error occurred';
    }

    return Promise.reject({ code, message, originalError: error });
  }

  // Cancel ongoing request
  cancelRequest() {
    if (this.abortController) {
      this.abortController.abort();
      this.abortController = null;
    }
  }

  // Project analysis
  async analyzeProject(data: ProjectRequest): Promise<ApiResponse> {
    this.cancelRequest();
    this.abortController = new AbortController();

    try {
      console.log('📤 Sending analyzeProject request:', data);
      
      // Make sure data matches exactly what backend expects
      const requestData = {
        name: data.name,
        requirements: data.requirements,
        project_type: data.project_type,
        budget_range: data.budget_range,
        timeline: data.timeline
      };

      const response = await this.api.post<ApiResponse>(
        '/api/v1/projects/analyze',
        requestData,
        { 
          signal: this.abortController.signal,
          timeout: 120000 // 2 minutes for this specific request
        }
      );
      
      console.log('📥 analyzeProject response:', response.data);
      return response.data;
    } catch (error) {
      if (axios.isCancel(error)) {
        console.log('Request cancelled');
        return Promise.reject({ code: 'REQUEST_CANCELLED', message: 'Request cancelled' });
      }
      console.error('analyzeProject error:', error);
      throw error;
    }
  }

  // Health check (fast endpoint)
  async healthCheck(): Promise<any> {
    try {
      const response = await this.api.get('/api/v1/projects/health', {
        timeout: 5000 // 5 seconds for health check
      });
      return response.data;
    } catch (error) {
      console.error('Health check error:', error);
      throw error;
    }
  }

  // Ping (fast endpoint)
  async ping(): Promise<any> {
    try {
      const response = await this.api.get('/api/v1/projects/ping', {
        timeout: 5000
      });
      return response.data;
    } catch (error) {
      console.error('Ping error:', error);
      throw error;
    }
  }
}

export default new ApiService();