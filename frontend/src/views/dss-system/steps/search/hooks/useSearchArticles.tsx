import { useQuery } from '@tanstack/react-query'
import { searchArticles } from '../../../../../services/api.ts'
import type { SearchParams } from '../../../../../types/article.ts';

export function useSearchArticles(params: SearchParams) {
  return useQuery({
    queryKey: ["searchArticles", params],
    queryFn: () => searchArticles(params),
    enabled: !!(params.query?.trim() || (params.dsl && Object.keys(params.dsl).length > 0)),
  });
}