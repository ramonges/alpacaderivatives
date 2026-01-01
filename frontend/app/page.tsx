'use client'

import { useState, useEffect } from 'react'
import SmileCurve from '@/components/SmileCurve'
import Greeks from '@/components/Greeks'
import IVEvolution from '@/components/IVEvolution'

export default function Home() {
  const [selectedExpiration, setSelectedExpiration] = useState<string>('')
  const [expirationDates, setExpirationDates] = useState<string[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchExpirationDates()
  }, [])

  const fetchExpirationDates = async () => {
    try {
      const { supabase } = await import('@/lib/supabase')
      const { data, error } = await supabase
        .from('options_data')
        .select('expiration_date')
        .order('expiration_date', { ascending: true })

      if (error) throw error

      const uniqueDates = Array.from(
        new Set(data.map((item: any) => item.expiration_date))
      ).sort() as string[]

      setExpirationDates(uniqueDates)
      if (uniqueDates.length > 0 && !selectedExpiration) {
        setSelectedExpiration(uniqueDates[0])
      }
      setLoading(false)
    } catch (error: any) {
      console.error('Error fetching expiration dates:', error)
      if (error?.code === 'PGRST116' || error?.message?.includes('404') || error?.message?.includes('NOT_FOUND')) {
        console.error('⚠️ Tables do not exist. Please run supabase_schema.sql in Supabase SQL Editor.')
      }
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    )
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white">
      <div className="container mx-auto px-4 py-8">
        <header className="mb-8">
          <h1 className="text-4xl font-bold mb-2">S&P 500 Options Dashboard</h1>
          <p className="text-gray-400">Real-time options analytics and visualizations</p>
        </header>

        <div className="mb-6">
          <label htmlFor="expiration" className="block text-sm font-medium mb-2">
            Select Expiration Date:
          </label>
          <select
            id="expiration"
            value={selectedExpiration}
            onChange={(e) => setSelectedExpiration(e.target.value)}
            className="bg-gray-800 text-white px-4 py-2 rounded-lg border border-gray-700 focus:border-blue-500 focus:outline-none"
          >
            {expirationDates.map((date) => (
              <option key={date} value={date}>
                {new Date(date).toLocaleDateString()}
              </option>
            ))}
          </select>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <div className="bg-gray-800 rounded-lg p-6 shadow-xl">
            <h2 className="text-2xl font-semibold mb-4">Smile Curve</h2>
            <SmileCurve expirationDate={selectedExpiration} />
          </div>

          <div className="bg-gray-800 rounded-lg p-6 shadow-xl">
            <h2 className="text-2xl font-semibold mb-4">Greeks</h2>
            <Greeks expirationDate={selectedExpiration} />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6 shadow-xl">
          <h2 className="text-2xl font-semibold mb-4">IV Evolution Over Time to Maturity</h2>
          <IVEvolution expirationDate={selectedExpiration} />
        </div>
      </div>
    </main>
  )
}

