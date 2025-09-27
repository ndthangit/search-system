import axios from 'axios';
import type { SearchResponse, SearchParams } from '../types/article';

const API_BASE_URL = 'http://localhost:8001';

const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor for logging
api.interceptors.request.use(
    (config) => {
        console.log(`Making ${config.method?.toUpperCase()} request to: ${config.url}`);
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor for error handling
api.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        console.error('API Error:', error.response?.data || error.message);
        return Promise.reject(error);
    }
);

export const searchArticles = async (params: SearchParams): Promise<SearchResponse> => {
    try {
        const response = await api.get('/api/articles/search', { params });
        return response.data;
    } catch (error) {
        console.error('Error searching articles:', error);
        throw error;
    }
};

export const getArticleById = async (id: string) => {
    try {
        const response = await api.get(`/api/articles/${id}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching article:', error);
        throw error;
    }
};

export default api;
