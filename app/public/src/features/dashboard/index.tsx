import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Header } from '@/components/layout/header'
import { Main } from '@/components/layout/main'
import { TopNav } from '@/components/layout/top-nav'
import { ThemeSwitch } from '@/components/theme-switch'
import { Overview } from './components/overview'
import { RecentSales } from './components/recent-sales'
import { TrendingUp, TrendingDown, Star, CalendarCheck } from "lucide-react"
import InfoCard from './components/info-card'


export default function Dashboard() {
  return (
    <>
      {/* ===== Top Heading ===== */}
      <Header>
        <TopNav links={topNav} />
        <div className='ml-auto flex items-center space-x-4'>
          <ThemeSwitch />
        </div>
      </Header>

      {/* ===== Main ===== */}
      <Main>
        <div className='mb-2 flex items-center justify-between space-y-2'>
          <h1 className='text-2xl font-bold tracking-tight'>Dashboard</h1>
        </div>
        <Tabs
          orientation='vertical'
          defaultValue='overview'
          className='space-y-4'
        >
          <div className='w-full overflow-x-auto pb-2'>
            <TabsList>
              <TabsTrigger value=''>Overview</TabsTrigger>
              <TabsTrigger value='analytics' disabled>
                N/A
              </TabsTrigger>
              <TabsTrigger value='reports' disabled>
                N/A
              </TabsTrigger>
              <TabsTrigger value='notifications' disabled>
                N/A
              </TabsTrigger>
            </TabsList>
          </div>
          <TabsContent value='overview' className='space-y-4'>
            <div className='grid gap-4 sm:grid-cols-2 lg:grid-cols-4'>
              <Card>
                <CardHeader className='flex flex-row items-center justify-between space-y-0 pb-2'>
                  <CardTitle className='text-sm font-medium flex items-center gap-1'>
                    Stock of the Day
                    <InfoCard 
                      title='Stock of the Day'                      
                      text='The stock which has the highest confidence metric'
                      size={4}
                    />
                  </CardTitle>
                  <Star
                    className='w-5 h-5 text-muted-foreground'
                  />
                </CardHeader>
                <CardContent>
                  <div className='text-2xl font-bold'>{/* */}STOCK PLACEHOLDER</div>
                  <p className='text-muted-foreground text-xs'>
                    {/* */}CONFIDENCE PLACEHOLDER% confidence in next-day value {}INCREASE/DECREASE
                  </p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className='flex flex-row items-center justify-between space-y-0 pb-2'>
                  <CardTitle className='text-sm font-medium flex items-center gap-1'>
                    Yesterday's Winner
                    <InfoCard 
                      title="Yesterday's Winner"                      
                      text='The stock which rose the highest in value the previous day'
                      size={4}
                    />
                  </CardTitle>
                  <CalendarCheck
                    className='w-5 h-5 text-muted-foreground'
                  />
                </CardHeader>
                <CardContent>
                  <div className='text-2xl font-bold'>{/* */}STOCK PLACEHOLDER</div>
                  <p className='text-muted-foreground text-xs'>
                    {/* */}CONFIDENCE PLACEHOLDER% confidence in next-day value increase
                  </p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className='flex flex-row items-center justify-between space-y-0 pb-2'>
                  <CardTitle className='text-sm font-medium flex items-center gap-1'>
                    Upward Trending
                    <InfoCard 
                      title='Upward Trending'                      
                      text='The stock which has the highest confidence to increase in value today'
                      size={4}
                    />
                  </CardTitle>
                  <TrendingUp
                    className='w-5 h-5 text-muted-foreground'
                  />
                </CardHeader>
                <CardContent>
                  <div className='text-2xl font-bold'>{/* */}STOCK PLACEHOLDER</div>
                  <p className='text-muted-foreground text-xs'>
                    {/* */}CONFIDENCE PLACEHOLDER% confidence in next-day value increase
                  </p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className='flex flex-row items-center justify-between space-y-0 pb-2'>
                  <CardTitle className='text-sm font-medium flex items-center gap-1'>
                    Downward Trending
                    <InfoCard 
                      title='Downward Trending'                      
                      text='The stock which has the highest confidence to decrease in value today'
                      size={4}
                    />
                  </CardTitle>
                  <TrendingDown
                    className='w-5 h-5 text-muted-foreground'
                  />
                </CardHeader>
                <CardContent>
                  <div className='text-2xl font-bold'>{/* */}STOCK PLACEHOLDER</div>
                  <p className='text-muted-foreground text-xs'>
                    {/* */}CONFIDENCE PLACEHOLDER% confidence in next-day value decrease
                  </p>
                </CardContent>
              </Card>
            </div>
            <div className='grid grid-cols-1 gap-4 lg:grid-cols-7'>
              <Card className='col-span-1 lg:col-span-4'>
                <CardHeader>
                  <CardTitle>Overview</CardTitle>
                </CardHeader>
                <CardContent className='pl-2'>
                  <Overview />
                </CardContent>
              </Card>
              <Card className='col-span-1 lg:col-span-3'>
                <CardHeader>
                  <CardTitle>Recent Sales</CardTitle>
                  <CardDescription>
                    You made 265 sales this month.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <RecentSales />
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </Main>
    </>
  )
}

const topNav = [
  {
    title: 'Overview',
    href: '/',
    isActive: true,
    disabled: false,
  },
]
