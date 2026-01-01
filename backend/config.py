import os
from dotenv import load_dotenv

load_dotenv()

# Alpaca API Configuration
ALPACA_API_KEY = os.getenv('ALPACA_API_KEY', 'sacZc0e60Tffp4vbJcgvG62FpV0rrDXbGFEupQbn')
ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY', '')
ALPACA_BASE_URL = os.getenv('ALPACA_BASE_URL', 'https://paper-api.alpaca.markets')

# Supabase Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://bbxcukvhekihomnevirr.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJieGN1a3ZoZWtpaG9tbmV2aXJyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjcyODA2MjAsImV4cCI6MjA4Mjg1NjYyMH0.k-xiLQIaMw_11Unr1EtfhZS55Pa66u7-apArBTOyDoQ')

# Trading Configuration
SYMBOL = 'SPY'  # S&P 500 ETF

