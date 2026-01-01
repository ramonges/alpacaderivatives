# Fixing 404 NOT_FOUND Error

## What the Error Means

The `404: NOT_FOUND` error from Supabase means the database tables don't exist yet. This happens when:
1. The SQL schema hasn't been run in Supabase
2. Tables were created with different names
3. There's a connection issue

## Quick Fix

### Step 1: Create the Tables in Supabase

1. **Go to your Supabase Dashboard**
   - Visit: https://bbxcukvhekihomnevirr.supabase.co
   - Or: https://supabase.com/dashboard

2. **Open SQL Editor**
   - Click "SQL Editor" in the left sidebar
   - Click "New query"

3. **Run the Schema**
   - Open the file `supabase_schema.sql` from this project
   - Copy ALL the SQL code
   - Paste it into the SQL Editor
   - Click "Run" (or press Cmd/Ctrl + Enter)

4. **Verify Tables Created**
   - Go to "Table Editor" in the left sidebar
   - You should see 3 tables:
     - `options_data`
     - `greeks_data`
     - `iv_evolution`

### Step 2: Verify Connection

Check your Supabase credentials in:
- **Frontend**: `frontend/.env.local` (should already be configured)
- **Backend**: `.env` file (should already be configured)

### Step 3: Test the Connection

After creating tables, refresh your frontend or run:
```bash
python test_setup.py
```

## Common Issues

### Issue: "Table does not exist"
**Solution**: Run the SQL schema in Supabase SQL Editor

### Issue: "Permission denied"
**Solution**: The RLS policies in the schema allow public access. If you still get errors, check:
- Supabase project is active
- API keys are correct
- Row Level Security policies are created

### Issue: "Invalid API key"
**Solution**: Verify your Supabase anon key in:
- Frontend: `frontend/.env.local`
- The key should start with: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

## Step-by-Step: Creating Tables

1. **Copy the SQL**:
   ```bash
   cat supabase_schema.sql
   ```

2. **Paste in Supabase**:
   - Go to Supabase Dashboard → SQL Editor
   - Paste the entire SQL
   - Click "Run"

3. **Verify**:
   - Check Table Editor
   - You should see 3 tables with columns

## After Fixing

Once tables are created:
1. ✅ Frontend will stop showing 404 errors
2. ✅ You can run the data collector
3. ✅ Dashboard will display data

## Still Having Issues?

1. Check browser console for exact error message
2. Verify Supabase project is active (not paused)
3. Check Supabase logs in the dashboard
4. Ensure you're using the correct project URL and key

