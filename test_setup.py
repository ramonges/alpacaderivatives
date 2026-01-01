"""
Test script to verify the setup is working correctly
"""
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.config import ALPACA_API_KEY, ALPACA_SECRET_KEY, SUPABASE_URL, SUPABASE_KEY
from backend.database import get_supabase_client
from backend.alpaca_client import AlpacaOptionsClient

def test_supabase_connection():
    """Test Supabase connection"""
    print("Testing Supabase connection...")
    try:
        supabase = get_supabase_client()
        # Try a simple query
        result = supabase.table('options_data').select('id').limit(1).execute()
        print("✓ Supabase connection successful")
        return True
    except Exception as e:
        print(f"✗ Supabase connection failed: {str(e)}")
        print("  Make sure you've run the SQL schema in Supabase")
        return False

def test_alpaca_connection():
    """Test Alpaca API connection"""
    print("\nTesting Alpaca API connection...")
    try:
        if not ALPACA_SECRET_KEY or ALPACA_SECRET_KEY == 'your_secret_key_here':
            print("✗ Alpaca secret key not configured in .env file")
            return False
        
        client = AlpacaOptionsClient()
        # Try to get underlying price
        price = client.get_underlying_price()
        if price:
            print(f"✓ Alpaca connection successful (SPY price: ${price:.2f})")
            return True
        else:
            print("✗ Could not fetch underlying price")
            return False
    except Exception as e:
        print(f"✗ Alpaca connection failed: {str(e)}")
        print("  Check your API credentials in .env file")
        return False

def test_options_fetch():
    """Test fetching options data"""
    print("\nTesting options data fetch...")
    try:
        client = AlpacaOptionsClient()
        contracts = client.get_option_contracts()
        if contracts:
            print(f"✓ Successfully fetched {len(contracts)} option contracts")
            if len(contracts) > 0:
                print(f"  Sample contract: {contracts[0]}")
            return True
        else:
            print("✗ No option contracts found")
            print("  This might be normal if market is closed or no options available")
            return False
    except Exception as e:
        print(f"✗ Options fetch failed: {str(e)}")
        return False
    except Exception:
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Alpaca Options Dashboard - Setup Test")
    print("=" * 50)
    
    supabase_ok = test_supabase_connection()
    alpaca_ok = test_alpaca_connection()
    options_ok = test_options_fetch()
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    print(f"  Supabase: {'✓' if supabase_ok else '✗'}")
    print(f"  Alpaca: {'✓' if alpaca_ok else '✗'}")
    print(f"  Options Fetch: {'✓' if options_ok else '✗'}")
    print("=" * 50)
    
    if supabase_ok and alpaca_ok:
        print("\n✓ Setup looks good! You can now run the collector:")
        print("  python backend/collector.py")
    else:
        print("\n✗ Please fix the issues above before running the collector")

