import { useQuery } from "@tanstack/react-query";
import type { UseQueryResult } from "@tanstack/react-query";
import { fetchHistory } from "@/lib/api";
import type { QueryHistoryItem } from "@/lib/types";

export function useHistory(limit = 50, offset = 0): UseQueryResult<QueryHistoryItem[], Error> {
  return useQuery<QueryHistoryItem[], Error>({
    queryKey: ["history", limit, offset],
    queryFn: () => fetchHistory(limit, offset),
    staleTime: 30_000, // history doesn't need to refetch aggressively
  });
}