import { useQuery } from '@tanstack/react-query'
import {saveDocument} from '../../../../../services/api.ts'
import type {ElasticDocument} from "../../../../../types/document.ts";

export function useSaveDocument(indexName: string, document: ElasticDocument) {
    return useQuery({
        queryKey: ["saveDocument", indexName, document],
        queryFn: () => saveDocument(indexName, document),
    });
}