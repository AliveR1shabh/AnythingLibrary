export interface AIResponse {
  provider: string;
  response: string;
  timestamp: string;
  tokens_used?: number;
  error?: string;
}

export interface ComparisonResult {
  prompt: string;
  responses: AIResponse[];
  timestamp: string;
}

export interface SearchProps {
  onSearch: (prompt: string, providers: string[], simplify: boolean) => void;
  loading: boolean;
}

export interface ResultColumnsProps {
  results: ComparisonResult;
}
