// src/utils/validators.ts
import { ProjectRequest } from '@/types/project.types';

interface ValidationResult {
  isValid: boolean;
  errors: Record<string, string>;
}

export function validateProjectRequest(data: Partial<ProjectRequest>): ValidationResult {
  const errors: Record<string, string> = {};

  // Validate name
  if (!data.name?.trim()) {
    errors.name = 'Project name is required';
  } else if (data.name.length < 3) {
    errors.name = 'Project name must be at least 3 characters';
  } else if (data.name.length > 100) {
    errors.name = 'Project name must be less than 100 characters';
  }

  // Validate requirements
  if (!data.requirements?.trim()) {
    errors.requirements = 'Project requirements are required';
  } else if (data.requirements.length < 10) {
    errors.requirements = 'Please provide more detailed requirements (min. 10 characters)';
  } else if (data.requirements.length > 10000) {
    errors.requirements = 'Requirements too long (max. 10000 characters)';
  }

  // Validate project type
  if (!data.project_type) {
    errors.project_type = 'Project type is required';
  }

  // Validate budget range (optional)
  if (data.budget_range && data.budget_range.length > 50) {
    errors.budget_range = 'Budget range too long';
  }

  // Validate timeline (optional)
  if (data.timeline && data.timeline.length > 50) {
    errors.timeline = 'Timeline too long';
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors,
  };
}

export function sanitizeInput(input: string): string {
  // Remove potentially dangerous characters
  return input
    .replace(/[<>]/g, '') // Remove HTML tags
    .replace(/javascript:/gi, '') // Remove javascript: protocol
    .replace(/on\w+=/gi, '') // Remove event handlers
    .trim();
}