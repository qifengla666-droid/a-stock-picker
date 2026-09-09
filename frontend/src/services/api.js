import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    console.error('API错误:', error);
    return Promise.reject(error);
  }
);

// API 接口
export const stockApi = {
  // 获取股票列表
  getStocks: (skip = 0, limit = 100) =>
    api.get('/api/stocks', { params: { skip, limit } }),

  // 同步股票数据
  syncStocks: () => api.post('/api/stocks/sync'),

  // 执行选股扫描
  scanStocks: (params) => api.post('/api/scan', params),

  // 获取扫描历史
  getScanHistory: (skip = 0, limit = 50) =>
    api.get('/api/scan/history', { params: { skip, limit } }),

  // 分析单只股票
  analyzeStock: (code) => api.get(`/api/analysis/${code}`),

  // 健康检查
  healthCheck: () => api.get('/health'),
};

export default api;
