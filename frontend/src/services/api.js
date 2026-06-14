import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Quiz API calls
export const quizAPI = {
  getAll: () => api.get('/quizzes'),
  getById: (id) => api.get(`/quizzes/${id}`),
  create: (data) => api.post('/quizzes', data),
  update: (id, data) => api.put(`/quizzes/${id}`, data),
  delete: (id) => api.delete(`/quizzes/${id}`),
};

// Judgment API calls
export const judgmentAPI = {
  getAll: () => api.get('/judgments'),
  getById: (id) => api.get(`/judgments/${id}`),
  create: (data) => api.post('/judgments', data),
  update: (id, data) => api.put(`/judgments/${id}`, data),
};

export default api;
