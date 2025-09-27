export interface Article {
    id: string;
    title: string;
    content: string;
    author: string;
    publishedAt: string;
    tags?: string[];
    summary?: string;
}

export interface SearchResponse {
    articles: Article[];
    total: number;
    page: number;
    limit: number;
}

export interface SearchParams {
    query: string;
    page?: number;
    limit?: number;
    author?: string;
    tags?: string[];
}
