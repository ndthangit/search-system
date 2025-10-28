import { useQuery } from '@tanstack/react-query'
import { searchArticles } from '../../../services/api'
import type { SearchParams } from '../../../types/article';

export function useSearchArticles(params: SearchParams) {
  return useQuery({
    queryKey: ["searchArticles", params],
    queryFn: () => searchArticles(params),
    enabled: !!(params.query?.trim() || (params.dsl && Object.keys(params.dsl).length > 0)),
  });
}