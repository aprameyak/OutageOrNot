import axios, { AxiosError } from 'axios';
import type { PredictionRequest, PredictionResponse, ApiError } from '../types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 seconds
});

export const getPrediction = async (request: PredictionRequest): Promise<PredictionResponse> => {
  try {
    const response = await apiClient.post<PredictionResponse>('/predict', request);
    return response.data;
  } catch (error) {
    if (error instanceof AxiosError) {
      const apiError: ApiError = error.response?.data || {
        error: 'Network Error',
        message: 'Failed to connect to the server',
      };
      throw apiError;
    }
    throw {
      error: 'Unknown Error',
      message: 'An unexpected error occurred',
    };
  }
};

export const checkHealth = async (): Promise<boolean> => {
  try {
    const response = await apiClient.get('/health');
    return response.status === 200;
  } catch {
    return false;
  }
}; 