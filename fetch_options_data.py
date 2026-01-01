#!/usr/bin/env python3
"""
Simple script to fetch S&P 500 options data using Alpaca REST API
"""
import os
import sys
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# Configuration
ALPACA_API_KEY = os.getenv('ALPACA_API_KEY', 'sacZc0e60Tffp4vbJcgvG62FpV0rrDXbGFEupQbn')
ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY', '')
ALPACA_BASE_URL = os.getenv('ALPACA_BASE_URL', 'https://paper-api.alpaca.markets')
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://bbxcukvhekihomnevirr.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJieGN1a3ZoZWtpaG9tbmV2aXJyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjcyODA2MjAsImV4cCI6MjA4Mjg1NjYyMH0.k-xiLQIaMw_11Unr1EtfhZS55Pa66u7-apArBTOyDoQ')

SYMBOL = 'SPY'  # S&P 500 ETF

def get_supabase_client():
    """Get Supabase client"""
    try:
        from supabase import create_client
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except ImportError:
        print("⚠️  supabase-py not installed. Installing...")
        os.system("pip install supabase -q")
        from supabase import create_client
        return create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_options_from_alpaca():
    """Fetch options data from Alpaca using REST API"""
    print(f"Fetching S&P 500 (SPY) options data from Alpaca...")
    
    headers = {
        'APCA-API-KEY-ID': ALPACA_API_KEY,
        'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY
    }
    
    # Try to get option contracts
    # Note: This is a simplified approach - you may need to adjust based on your Alpaca subscription
    try:
        # Get latest bar for underlying
        url = f"{ALPACA_BASE_URL.replace('paper-api', 'data')}/v2/stocks/{SYMBOL}/bars/latest"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            bar_data = response.json()
            underlying_price = float(bar_data['bar']['c'])  # close price
            print(f"✓ Current SPY price: ${underlying_price:.2f}")
        else:
            print(f"⚠️  Could not fetch underlying price: {response.status_code}")
            underlying_price = None
        
        # For options, we'll use the Python SDK approach if available
        # Otherwise, we'll need to use the data collector
        print("\n⚠️  Direct REST API for options requires specific endpoints.")
        print("   Using data collector approach instead...")
        return None, underlying_price
        
    except Exception as e:
        print(f"❌ Error fetching from Alpaca: {e}")
        return None, None

def store_options_data(supabase, options_data):
    """Store options data in Supabase"""
    if not options_data:
        return 0
    
    stored = 0
    for option in options_data:
        try:
            result = supabase.table('options_data').insert(option).execute()
            if result.data:
                stored += 1
        except Exception as e:
            print(f"  ⚠️  Error storing option: {e}")
    
    return stored

def main():
    """Main function"""
    print("=" * 60)
    print("S&P 500 Options Data Fetcher")
    print("=" * 60)
    print(f"Symbol: {SYMBOL}")
    print(f"Date: {datetime.now().date()}")
    print("=" * 60)
    print()
    
    if not ALPACA_SECRET_KEY or ALPACA_SECRET_KEY == '':
        print("❌ ALPACA_SECRET_KEY not set in .env file")
        print("   Please add your Alpaca secret key to .env")
        return
    
    # Get Supabase client
    try:
        supabase = get_supabase_client()
        print("✓ Connected to Supabase")
    except Exception as e:
        print(f"❌ Error connecting to Supabase: {e}")
        return
    
    # Try to fetch options
    options_data, underlying_price = fetch_options_from_alpaca()
    
    if options_data is None:
        print("\n" + "=" * 60)
        print("Using Python SDK approach...")
        print("=" * 60)
        print("\nPlease run the data collector instead:")
        print("  python run_collector.py")
        print("\nOr install/update dependencies:")
        print("  pip install 'alpaca-py>=0.18.0' 'numpy<2'")
        return
    
    # Store data
    if options_data:
        print(f"\nStoring {len(options_data)} options...")
        stored = store_options_data(supabase, options_data)
        print(f"✓ Stored {stored} options in database")

if __name__ == "__main__":
    main()

