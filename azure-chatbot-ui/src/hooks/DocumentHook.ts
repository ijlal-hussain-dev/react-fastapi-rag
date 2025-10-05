import type { SearchResult } from "../types/searchResult";
import config from "../config";
import { useQuery } from "@tanstack/react-query";
import axios, { AxiosError } from "axios";

// Fetch keyword search results
const useKeywordSearch = (query: string, enabled = true) => {
  return useQuery<SearchResult[], AxiosError>({
    queryKey: ["search", query],
    queryFn: () =>
      axios
        .get(`${config.baseApiUrl}/search/keyword`, {
          params: { query, top: 10 }, // pass query dynamically
        })
        .then((res) => res.data),
    enabled: enabled && query.length > 0, // only run if query is not empty
  });
};

// Fetch semantic search results
const useSemanticSearch = (query: string, enabled = true) => {
  return useQuery<SearchResult[], AxiosError>({
    queryKey: ["semantic-search", query],
    queryFn: () =>
      axios
        .get(`${config.baseApiUrl}/search/semantic`, { params: { query } })
        .then((res) => res.data),
    enabled: enabled && query.length > 0,
  });
};

// Fetch suggestions (returns string list)
const useSuggestSearch = (query: string, top = 5, enabled = true) => {
  return useQuery<string[], AxiosError>({
    queryKey: ["suggest", query],
    queryFn: () =>
      axios
        .get(`${config.baseApiUrl}/search/suggest`, { params: { query, top } })
        .then((res) => res.data),
    enabled: enabled && query.length > 0,
  });
};

export { useKeywordSearch, useSemanticSearch, useSuggestSearch };
