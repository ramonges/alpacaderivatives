'use client'

import { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { supabase } from '@/lib/supabase'

interface GreeksProps {
  expirationDate: string
}

interface GreeksData {
  strike_price: number
  delta: number
  gamma: number
  theta: number
  vega: number
  rho: number
  option_type: string
}

export default function Greeks({ expirationDate }: GreeksProps) {
  const [greeksData, setGreeksData] = useState<any[]>([])
  const [selectedGreek, setSelectedGreek] = useState<'delta' | 'gamma' | 'theta' | 'vega' | 'rho'>('delta')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (expirationDate) {
      fetchGreeksData()
    }
  }, [expirationDate])

  const fetchGreeksData = async () => {
    setLoading(true)
    try {
      const { data, error } = await supabase
        .from('greeks_data')
        .select('strike_price, delta, gamma, theta, vega, rho, option_type')
        .eq('expiration_date', expirationDate)
        .order('strike_price', { ascending: true })

      if (error) throw error

      const formattedData = data.map((item: GreeksData) => ({
        strike: item.strike_price,
        delta: item.delta,
        gamma: item.gamma,
        theta: item.theta,
        vega: item.vega,
        rho: item.rho,
        option_type: item.option_type,
      }))

      setGreeksData(formattedData)
    } catch (error) {
      console.error('Error fetching Greeks data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="h-64 flex items-center justify-center">Loading...</div>
  }

  if (greeksData.length === 0) {
    return (
      <div className="h-64 flex items-center justify-center text-gray-400">
        No Greeks data available for this expiration date
      </div>
    )
  }

  const greekLabels = {
    delta: 'Delta',
    gamma: 'Gamma',
    theta: 'Theta',
    vega: 'Vega',
    rho: 'Rho',
  }

  const calls = greeksData.filter((item) => item.option_type === 'call')
  const puts = greeksData.filter((item) => item.option_type === 'put')

  return (
    <div>
      <div className="mb-4 flex gap-2 flex-wrap">
        {(['delta', 'gamma', 'theta', 'vega', 'rho'] as const).map((greek) => (
          <button
            key={greek}
            onClick={() => setSelectedGreek(greek)}
            className={`px-4 py-2 rounded-lg transition-colors ${
              selectedGreek === greek
                ? 'bg-blue-600 text-white'
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
            }`}
          >
            {greekLabels[greek]}
          </button>
        ))}
      </div>

      <ResponsiveContainer width="100%" height={400}>
        <LineChart>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis
            dataKey="strike"
            type="number"
            scale="linear"
            domain={['dataMin', 'dataMax']}
            stroke="#9CA3AF"
            label={{ value: 'Strike Price', position: 'insideBottom', offset: -5 }}
          />
          <YAxis
            stroke="#9CA3AF"
            label={{ value: greekLabels[selectedGreek], angle: -90, position: 'insideLeft' }}
          />
          <Tooltip
            contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151' }}
            formatter={(value: number) => [value.toFixed(4), greekLabels[selectedGreek]]}
          />
          <Legend />
          {calls.length > 0 && (
            <Line
              type="monotone"
              data={calls}
              dataKey={selectedGreek}
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
              dataKey={selectedGreek}
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

