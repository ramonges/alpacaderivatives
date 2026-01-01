'use client'

import { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { supabase } from '@/lib/supabase'

interface IVEvolutionProps {
  expirationDate: string
}

interface IVData {
  time_to_maturity: number
  implied_volatility: number
  strike_price: number
  option_type: string
  recorded_at: string
}

export default function IVEvolution({ expirationDate }: IVEvolutionProps) {
  const [ivData, setIvData] = useState<any[]>([])
  const [selectedStrike, setSelectedStrike] = useState<number | null>(null)
  const [availableStrikes, setAvailableStrikes] = useState<number[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (expirationDate) {
      fetchIVEvolutionData()
    }
  }, [expirationDate, selectedStrike])

  const fetchIVEvolutionData = async () => {
    setLoading(true)
    try {
      let query = supabase
        .from('iv_evolution')
        .select('time_to_maturity, implied_volatility, strike_price, option_type, recorded_at')
        .eq('expiration_date', expirationDate)
        .not('implied_volatility', 'is', null)
        .not('time_to_maturity', 'is', null)
        .order('recorded_at', { ascending: true })

      if (selectedStrike) {
        query = query.eq('strike_price', selectedStrike)
      }

      const { data, error } = await query

      if (error) throw error

      // Get unique strikes for the dropdown
      const strikes = Array.from(
        new Set(data.map((item: IVData) => item.strike_price))
      ).sort((a, b) => a - b) as number[]

      setAvailableStrikes(strikes)

      // Group by strike and option type, then sort by time to maturity
      const grouped: { [key: string]: any[] } = {}
      data.forEach((item: IVData) => {
        const key = `${item.strike_price}_${item.option_type}`
        if (!grouped[key]) {
          grouped[key] = []
        }
        grouped[key].push({
          timeToMaturity: item.time_to_maturity * 365, // Convert to days
          iv: item.implied_volatility * 100, // Convert to percentage
          strike: item.strike_price,
          option_type: item.option_type,
        })
      })

      // Sort each group by time to maturity
      Object.keys(grouped).forEach((key) => {
        grouped[key].sort((a, b) => a.timeToMaturity - b.timeToMaturity)
      })

      // Flatten and format for chart
      const chartData: any[] = []
      Object.values(grouped).forEach((group) => {
        chartData.push(...group)
      })

      setIvData(chartData)

      // Auto-select first strike if none selected
      if (!selectedStrike && strikes.length > 0) {
        setSelectedStrike(strikes[Math.floor(strikes.length / 2)]) // Select middle strike
      }
    } catch (error: any) {
      console.error('Error fetching IV evolution data:', error)
      if (error?.code === 'PGRST116' || error?.message?.includes('404') || error?.message?.includes('NOT_FOUND')) {
        console.error('Table does not exist. Please run the SQL schema in Supabase.')
      }
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="h-64 flex items-center justify-center">Loading...</div>
  }

  if (ivData.length === 0) {
    return (
      <div className="h-64 flex items-center justify-center text-gray-400">
        No IV evolution data available for this expiration date
      </div>
    )
  }

  // Filter data by selected strike
  const filteredData = selectedStrike
    ? ivData.filter((item) => item.strike === selectedStrike)
    : ivData

  const calls = filteredData.filter((item) => item.option_type === 'call')
  const puts = filteredData.filter((item) => item.option_type === 'put')

  return (
    <div>
      <div className="mb-4">
        <label htmlFor="strike-select" className="block text-sm font-medium mb-2">
          Select Strike Price (optional):
        </label>
        <select
          id="strike-select"
          value={selectedStrike || ''}
          onChange={(e) => setSelectedStrike(e.target.value ? Number(e.target.value) : null)}
          className="bg-gray-700 text-white px-4 py-2 rounded-lg border border-gray-600 focus:border-blue-500 focus:outline-none"
        >
          <option value="">All Strikes</option>
          {availableStrikes.map((strike) => (
            <option key={strike} value={strike}>
              ${strike}
            </option>
          ))}
        </select>
      </div>

      <ResponsiveContainer width="100%" height={500}>
        <LineChart>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis
            dataKey="timeToMaturity"
            type="number"
            scale="linear"
            domain={['dataMin', 'dataMax']}
            stroke="#9CA3AF"
            label={{ value: 'Days to Maturity', position: 'insideBottom', offset: -5 }}
          />
          <YAxis
            stroke="#9CA3AF"
            label={{ value: 'Implied Volatility (%)', angle: -90, position: 'insideLeft' }}
          />
          <Tooltip
            contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151' }}
            formatter={(value: number) => [`${value.toFixed(2)}%`, 'IV']}
            labelFormatter={(label) => `Days to Maturity: ${label.toFixed(1)}`}
          />
          <Legend />
          {calls.length > 0 && (
            <Line
              type="monotone"
              data={calls}
              dataKey="iv"
              name="Calls"
              stroke="#3B82F6"
              strokeWidth={2}
              dot={{ r: 3 }}
              connectNulls
            />
          )}
          {puts.length > 0 && (
            <Line
              type="monotone"
              data={puts}
              dataKey="iv"
              name="Puts"
              stroke="#EF4444"
              strokeWidth={2}
              dot={{ r: 3 }}
              connectNulls
            />
          )}
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

