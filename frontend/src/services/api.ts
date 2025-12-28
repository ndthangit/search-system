import axios from "axios";
import type { SearchResponse, SearchParams } from "../types/article";
import { API_BASE_URL, TIME_OUT } from "./const.ts";
import type {ElasticDocument} from "../types/document.ts";

const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: TIME_OUT,
    headers: {
        "Content-Type": "application/json",
    },
});

// Request interceptor for logging
api.interceptors.request.use(
    config => {
        console.log(`Making ${config.method?.toUpperCase()} request to: ${config.url}`);
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

// Response interceptor for error handling
api.interceptors.response.use(
    response => {
        return response;
    },
    error => {
        console.error("API Error:", error.response?.data || error.message);
        return Promise.reject(error);
    }
);

export const searchArticles = async (params: SearchParams): Promise<SearchResponse> => {
    try {
        const { indexName, query, fields, page, size } = params;

        const response = await api.post(`/search-match/${indexName}`, {
            query: query,
            fields: fields,
            page: page || 1,
            size: size || 10,
        });

        return response.data;
    } catch (error) {
        console.error("Error searching documents:", error);
        throw error;
    }
};

export const saveDocument = async (indexName: string, document: ElasticDocument): Promise<string> => {
    try {
        const response = await api.post(`/save-document/${indexName}`, document);
        return response.data.result;
    } catch (error) {
        console.error("Error fetching article:", error);
        throw error;
    }
};

export default api;
