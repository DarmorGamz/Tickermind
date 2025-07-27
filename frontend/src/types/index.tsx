export interface Stock {
  symbol: string;
  name: string;
  price: number;
  changePercent: number;
  volume?: number;
  marketCap?: number;
  peRatio?: number;
}

export type Column = 'symbol' | 'price' | 'changePercent' | 'volume' | 'marketCap' | 'peRatio';

export interface ColumnConfig {
  id: Column;
  label: string;
  optional: boolean;
}

export interface User {
  id: string;
  email: string;
  name: string;
  token?: string;
}