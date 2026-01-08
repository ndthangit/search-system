export interface Article {
    id: string;
    title: string;
    summary: string;
    url: string;
    date: string;
    contents?: string;
    authors?: string[];
    category?: string;
    tags?: string[];
}

export interface ArticleSource {
    link: string;
    title_va: string;
    title_vska: string;
    summary_va: string;
    summary_vska: string;
    length: number;
    last_updated: string;
}

export interface SearchResponse {
    pageNumber: number;
    pageSize: number;
    totalElements: number;
    totalPages: number;
    took: number | null;
    maxScore: number | null;
    data: {
        index: string;
        id: string;
        score: number | null;
        source: ArticleSource;
    }[];
}

export interface SearchParams {
  query: string;
  fields?: string[];
  indexName: string;
  dsl?: Record<string, unknown>;
  size?: number;
  page?: number;
}
