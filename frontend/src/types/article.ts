export interface Article {
    name: string;
    abstract: string;
    url: string;
}

export interface SearchResponse {
    list_docs: Article[];
}

export interface SearchParams {
    query: string;
}
