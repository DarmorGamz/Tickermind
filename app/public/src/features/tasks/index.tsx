import { useEffect, useState } from 'react'
import { Header } from '@/components/layout/header'
import { Main } from '@/components/layout/main'
import { ThemeSwitch } from '@/components/theme-switch'
import { stockColumns } from './components/columns-stock'
import { Stock } from './data/schema'
import { DataTable } from './components/data-table'
import { TasksDialogs } from './components/tasks-dialogs'
import TasksProvider from './context/tasks-context'

export default function Tasks() {
  const [data, setData] = useState<Stock[]>([])
  const [loading, setLoading] = useState(true)
 
  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch('/api?Cmd=Tickers.GetList')
        const raw = await res.json()
        // Assuming: [ { ticker: 'AAPL', Close: 200 }, { ticker: 'MSFT', Close: 300 }, ... ]
        const parsed = raw.data.map((item: any) => ({
          ticker: item.ticker,
          Close: item.Close,
          Sentiment_Label: item.Sentiment_Label,
        }))
        setData(parsed)
      } catch (err) {
        console.error('Failed to fetch stocks:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])


  return (
    <TasksProvider>
      <Header fixed>
        <div className='ml-auto flex items-center space-x-4'>
          <ThemeSwitch />
        </div>
      </Header>

      <Main>
        <div className='mb-2 flex flex-wrap items-center justify-between space-y-2 gap-x-4'>
          <div>
            <h2 className='text-2xl font-bold tracking-tight'>Stocks</h2>
            <p className='text-muted-foreground'>
              Here&apos;s the latest stock close prices!
            </p>
          </div>
        </div>
        <div className='-mx-4 flex-1 overflow-auto px-4 py-1 lg:flex-row lg:space-y-0 lg:space-x-12'>
          {loading ? (
            <p className='text-muted-foreground'>Loading data...</p>
          ) : (
            <DataTable data={data} columns={stockColumns} />
          )}
        </div>
      </Main>

      <TasksDialogs />
    </TasksProvider>
  )
}
