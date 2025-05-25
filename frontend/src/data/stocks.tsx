import { Stock } from '../types';

export const stockData: Stock[] = [
  {
    symbol: 'AAPL',
    name: 'Apple Inc.',
    price: 145.30,
    changePercent: 2.15,
    volume: 12500000,
    marketCap: 2400000000000,
    peRatio: 28.4
  },
  {
    symbol: 'GOOGL',
    name: 'Alphabet Inc.',
    price: 2750.10,
    changePercent: -1.25,
    volume: 8700000,
    marketCap: 1800000000000,
    peRatio: 32.1
  },
  {
    symbol: 'MSFT',
    name: 'Microsoft Corp.',
    price: 305.45,
    changePercent: 0.95,
    volume: 10200000,
    marketCap: 2300000000000,
    peRatio: 35.7
  },
  {
    symbol: 'AMZN',
    name: 'Amazon.com Inc.',
    price: 3122.90,
    changePercent: -0.78,
    volume: 9500000,
    marketCap: 1600000000000,
    peRatio: 41.2
  },
  {
    symbol: 'META',
    name: 'Meta Platforms Inc.',
    price: 321.65,
    changePercent: 1.42,
    volume: 7800000,
    marketCap: 850000000000,
    peRatio: 25.8
  },
  {
    symbol: 'TSLA',
    name: 'Tesla Inc.',
    price: 734.20,
    changePercent: 3.28,
    volume: 15600000,
    marketCap: 780000000000,
    peRatio: 58.3
  },
  {
    symbol: 'NFLX',
    name: 'Netflix Inc.',
    price: 625.80,
    changePercent: -2.10,
    volume: 5400000,
    marketCap: 275000000000,
    peRatio: 43.5
  },
  {
    symbol: 'NVDA',
    name: 'NVIDIA Corp.',
    price: 215.75,
    changePercent: 4.32,
    volume: 18900000,
    marketCap: 540000000000,
    peRatio: 63.8
  }
];

export const columns: ColumnConfig[] = [
  { id: 'symbol', label: 'Symbol', optional: false },
  { id: 'price', label: 'Price', optional: false },
  { id: 'changePercent', label: 'Change %', optional: false },
  { id: 'volume', label: 'Volume', optional: true },
  { id: 'marketCap', label: 'Market Cap', optional: true },
  { id: 'peRatio', label: 'P/E Ratio', optional: true }
];