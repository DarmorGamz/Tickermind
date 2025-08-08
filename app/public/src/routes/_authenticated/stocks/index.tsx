import { createFileRoute } from '@tanstack/react-router'
import Tasks from '@/features/stocks'

export const Route = createFileRoute('/_authenticated/stocks/')({
  component: Tasks,
})
