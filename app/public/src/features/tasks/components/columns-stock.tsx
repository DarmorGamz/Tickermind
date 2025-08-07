import { ColumnDef } from '@tanstack/react-table'
import { Stock } from '../data/schema'

export const stockColumns: ColumnDef<Stock>[] = [
  {
    accessorKey: 'ticker',
    header: 'Ticker',
    cell: ({ row }) => (
      <div className='font-medium'>{row.original.ticker}</div>
    ),
  },
  {
    accessorKey: 'Close',
    header: 'Close Price',
    cell: ({ row }) => (
      <div>${row.original.Close.toFixed(2)}</div>
    ),
  },
]
