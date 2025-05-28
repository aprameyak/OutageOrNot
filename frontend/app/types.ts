export type PredictionResponse = {
  success: boolean;
  data?: string;
  error?: string;
  message?: string;
};

export type PredictionRequest = {
  state: string;
};

export type ApiError = {
  error: string;
  message: string;
};

export type LoadingState = 'idle' | 'loading' | 'success' | 'error'; 