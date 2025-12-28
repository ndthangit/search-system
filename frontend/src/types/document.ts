export interface ElasticDocument {
    id: string,
    url: string,
    title: string,
    summary: string,
    contents: string,
    date: string,
    authors: string[],
    category: string,
    tags: string[]
}