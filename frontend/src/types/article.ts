export interface Article {
    name: string;
    abstract: string;
    url: string;
}

export interface SearchResponse {
    pageNumber: 0,
    pageSize: 0,
    totalElements: 0,
    totalPages: 0,
    took: null,
    maxScore: null,
    data: {
        index: string,
        id: string,
        score: null,
        source: Document,
    } []
}

export interface SearchParams {
  query: string;
  fields?: string[];
  indexName: string;
  dsl?: Record<string, any>;
  size?: number;
  page?: number;
}