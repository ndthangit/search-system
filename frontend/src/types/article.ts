export interface Article {
    name: string;
    abstract: string;
    url: string;
}

export interface SearchResponse {
    list_docs: Article[];
}

export interface SearchParams {
  query?: string;                // Text query đơn giản
  index?: string;                // Tên index (vd: articles)
  model?: "match" | "multi_match" | "bool" | "function_score" | "script_score";
  dsl?: Record<string, any>;     // Cấu trúc truy vấn nâng cao (ES Query DSL)
  rankProfile?: string;          // Tên profile xếp hạng tùy chỉnh
  size?: number;                 // Số lượng kết quả trả về
  from?: number;                 // Offset phân trang
  sort?: Array<Record<string, any>>; // Mảng sort (vd: [{ "_score": "desc" }])
}