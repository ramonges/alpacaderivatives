'use client'

import { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { supabase } from '@/lib/supabase'

interface SmileCurveProps {
  expirationDate: string
}

interface OptionData {
  strike_price: number
  implied_volatility: number
  option_type: string
}

export default function SmileCurve({ expirationDate }: SmileCurveProps) {
  const [callData, setCallData] = useState<any[]>([])
  const [putData, setPutData] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (expirationDate) {
      fetchSmileCurveData()
    }
  }, [expirationDate])

  const fetchSmileCurveData = async () => {
    setLoading(true)
    try {
      const { data, error } = await supabase
        .from('options_data')
        .select('strike_price, implied_volatility, option_type')
        .eq('expiration_date', expirationDate)
        .not('implied_volatility', 'is', null)
        .order('strike_price', { ascending: true })

      if (error) throw error

      const calls = data
        .filter((item: OptionData) => item.option_type === 'call')
        .map((item: OptionData) => ({
          strike: item.strike_price,
          iv: item.implied_volatility * 100, // Convert to percentage
        }))
        .filter((item) => item.iv > 0)

      const puts = data
        .filter((item: OptionData) => item.option_type === 'put')
        .map((item: OptionData) => ({
          strike: item.strike_price,
          iv: item.implied_volatility * 100,
        }))
        .filter((item) => item.iv > 0)

      setCallData(calls)
      setPutData(puts)
    } catch (error: any) {
      console.error('Error fetching smile curve data:', error)
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

  if (callData.length === 0 && putData.length === 0) {
    return (
      <div className="h-64 flex items-center justify-center text-gray-400">
        No data available for this expiration date
      </div>
    )
  }

  // Combine data for domain calculation
  const allData = [...callData, ...putData]
  const minStrike = allData.length > 0 ? Math.min(...allData.map(d => d.strike)) : 0
  const maxStrike = allData.length > 0 ? Math.max(...allData.map(d => d.strike)) : 1000

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart>
        <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
        <XAxis
          dataKey="strike"
          type="number"
          scale="linear"
          domain={[minStrike * 0.95, maxStrike * 1.05]}
          stroke="#9CA3AF"
          label={{ value: 'Strike Price', position: 'insideBottom', offset: -5 }}
        />
        <YAxis
          stroke="#9CA3AF"
          label={{ value: 'Implied Volatility (%)', angle: -90, position: 'insideLeft' }}
        />
        <Tooltip
          contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151' }}
          formatter={(value: number) => [`${value.toFixed(2)}%`, 'IV']}
          labelFormatter={(label) => `Strike: $${label}`}
        />
        <Legend />
        {callData.length > 0 && (
          <Line
            type="monotone"
            dataKey="iv"
            data={callData}
            name="Calls"
            stroke="#3B82F6"
            strokeWidth={2}
            dot={{ r: 3 }}
            connectNulls
          />
        )}
        {putData.length > 0 && (
          <Line
            type="monotone"
            dataKey="iv"
            data={putData}
            name="Puts"
            stroke="#EF4444"
            strokeWidth={2}
            dot={{ r: 3 }}
            connectNulls
          />
        )}
      </LineChart>
    </ResponsiveContainer>
  )
}

