"""
Quick script to check if Supabase tables exist
"""
from backend.database import get_supabase_client

def check_tables():
    """Check if required tables exist in Supabase"""
    supabase = get_supabase_client()
    
    tables_to_check = ['options_data', 'greeks_data', 'iv_evolution']
    
    print("Checking Supabase tables...")
    print("=" * 50)
    
    for table in tables_to_check:
        try:
            # Try to query the table
            result = supabase.table(table).select('*').limit(1).execute()
            print(f"✓ Table '{table}' exists")
            if result.data:
                print(f"  - Has {len(result.data)} record(s) (showing first record)")
            else:
                print(f"  - Table is empty")
        except Exception as e:
            error_msg = str(e)
            if '404' in error_msg or 'NOT_FOUND' in error_msg or 'does not exist' in error_msg.lower():
                print(f"✗ Table '{table}' does NOT exist")
                print(f"  Error: {error_msg}")
            else:
                print(f"✗ Error checking table '{table}': {error_msg}")
        print()
    
    print("=" * 50)
    print("\nIf tables don't exist, run the SQL from 'supabase_schema.sql' in your Supabase SQL Editor")

if __name__ == "__main__":
    check_tables()

