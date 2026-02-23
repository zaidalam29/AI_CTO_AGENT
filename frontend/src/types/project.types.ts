// src/types/project.types.ts
export interface ProjectRequest {
  name: string;
  requirements: string;
  project_type: ProjectType;
  budget_range?: string;
  timeline?: string;
}

export enum ProjectType {
  WEB_APP = "web_app",
  MOBILE_APP = "mobile_app",
  API = "api",
  ML_SERVICE = "ml_service",
  ECOMMERCE = "ecommerce"
}

export interface Feature {
  name: string;
  description: string;
  priority: 'high' | 'medium' | 'low';
  estimated_hours?: number;
}

export interface TechStack {
  frontend: string[];
  backend: string[];
  database: string[];
  devops: string[];
  third_party: string[];
}

export interface Sprint {
  number: number;
  name: string;
  duration_weeks: number;
  features: string[];
  deliverables: string[];
}

export interface Risk {
  category: string;
  description: string;
  probability: number;
  impact: string;
  mitigation: string;
}

export interface Architecture {
  high_level_design: any;
  database_schema: any;
  api_design: any;
  components: any[];
  scaling_plan: any;
}

export interface DevOpsPlan {
  ci_cd_pipeline: string[];
  infrastructure: Record<string, any>;
  deployment_strategy: string;
  monitoring_tools: string[];
  backup_strategy: string;
  disaster_recovery: string;
}

export interface ProjectPlan {
  features: Feature[];
  tech_stack: TechStack;
  sprints: Sprint[];
  architecture: Architecture;
  risks: Risk[];
  estimated_timeline_months: number;
  estimated_cost_range: string;
}

export interface AgentStatus {
  planner: 'success' | 'error' | 'pending';
  architect: 'success' | 'error' | 'pending';
  risk: 'success' | 'error' | 'pending';
  sprint: 'success' | 'error' | 'pending';
  devops: 'success' | 'error' | 'pending';
}

export interface ApiResponse {
  success: boolean;
  message: string;
  data?: ProjectPlan & {
    project_planning: any;
    system_architecture: any;
    risk_assessment: any;
    sprint_planning: any;
    devops_plan: any;
    agent_status: AgentStatus;
  };
  error?: {
    code: string;
    message: string;
    details?: any;
  };
  request_id: string;
  processing_time?: string;
  agents_used?: string[];
}

export interface MetricsResponse {
  success: boolean;
  data: {
    total_requests: number;
    successful_requests: number;
    failed_requests: number;
    success_rate: string;
    average_processing_time: string;
    requests_by_endpoint: Record<string, number>;
    requests_by_agent: Record<string, number>;
    uptime: string;
    uptime_formatted: string;
  };
}