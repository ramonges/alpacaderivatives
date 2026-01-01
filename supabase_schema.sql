-- Supabase Database Schema for Alpaca Options Dashboard
-- Run this SQL in your Supabase SQL Editor

-- Options data table
CREATE TABLE IF NOT EXISTS options_data (
    id BIGSERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    option_type VARCHAR(4) NOT NULL, -- 'call' or 'put'
    strike_price DECIMAL(10, 2) NOT NULL,
    expiration_date DATE NOT NULL,
    bid_price DECIMAL(10, 4),
    ask_price DECIMAL(10, 4),
    last_price DECIMAL(10, 4),
    volume INTEGER,
    open_interest INTEGER,
    implied_volatility DECIMAL(8, 6),
    underlying_price DECIMAL(10, 2),
    time_to_maturity DECIMAL(10, 6), -- in years
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Greeks data table
CREATE TABLE IF NOT EXISTS greeks_data (
    id BIGSERIAL PRIMARY KEY,
    option_id BIGINT REFERENCES options_data(id),
    symbol VARCHAR(10) NOT NULL,
    strike_price DECIMAL(10, 2) NOT NULL,
    expiration_date DATE NOT NULL,
    option_type VARCHAR(4) NOT NULL,
    delta DECIMAL(10, 6),
    gamma DECIMAL(10, 6),
    theta DECIMAL(10, 6),
    vega DECIMAL(10, 6),
    rho DECIMAL(10, 6),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- IV evolution table
CREATE TABLE IF NOT EXISTS iv_evolution (
    id BIGSERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    strike_price DECIMAL(10, 2) NOT NULL,
    expiration_date DATE NOT NULL,
    option_type VARCHAR(4) NOT NULL,
    implied_volatility DECIMAL(8, 6),
    time_to_maturity DECIMAL(10, 6),
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_options_symbol_exp ON options_data(symbol, expiration_date);
CREATE INDEX IF NOT EXISTS idx_options_created_at ON options_data(created_at);
CREATE INDEX IF NOT EXISTS idx_greeks_option_id ON greeks_data(option_id);
CREATE INDEX IF NOT EXISTS idx_greeks_symbol_exp ON greeks_data(symbol, expiration_date);
CREATE INDEX IF NOT EXISTS idx_iv_evolution_symbol_exp ON iv_evolution(symbol, expiration_date, strike_price);
CREATE INDEX IF NOT EXISTS idx_iv_evolution_recorded_at ON iv_evolution(recorded_at);

-- Enable Row Level Security (optional, adjust policies as needed)
ALTER TABLE options_data ENABLE ROW LEVEL SECURITY;
ALTER TABLE greeks_data ENABLE ROW LEVEL SECURITY;
ALTER TABLE iv_evolution ENABLE ROW LEVEL SECURITY;

-- Create policies to allow public read access (adjust as needed for your security requirements)
CREATE POLICY "Allow public read access" ON options_data FOR SELECT USING (true);
CREATE POLICY "Allow public read access" ON greeks_data FOR SELECT USING (true);
CREATE POLICY "Allow public read access" ON iv_evolution FOR SELECT USING (true);

-- Create policies to allow insert (for the data collector)
CREATE POLICY "Allow public insert" ON options_data FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public insert" ON greeks_data FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public insert" ON iv_evolution FOR INSERT WITH CHECK (true);

