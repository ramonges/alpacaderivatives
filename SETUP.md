# Setup Guide

## Step-by-Step Setup Instructions

### 1. Supabase Database Setup

1. **Go to Supabase Dashboard**
   - Visit: https://bbxcukvhekihomnevirr.supabase.co
   - Or go to https://supabase.com/dashboard and select your project

2. **Create Database Tables**
   - Navigate to **SQL Editor** in the left sidebar
   - Open the file `supabase_schema.sql` from this project
   - Copy and paste the entire SQL into the SQL Editor
   - Click **Run** to execute

3. **Verify Tables Created**
   - Go to **Table Editor** in the left sidebar
   - You should see three tables:
     - `options_data`
     - `greeks_data`
     - `iv_evolution`

### 2. Backend Setup

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**
   ```bash
   # Create .env file
   cp .env.example .env
   ```

3. **Edit `.env` file**
   - Add your Alpaca API secret key (you have the API key, but need the secret)
   - The Supabase credentials are already configured

4. **Test the Setup**
   ```bash
   python test_setup.py
   ```

5. **Run Data Collector**
   ```bash
   # One-time collection
   python backend/collector.py
   
   # For continuous collection, edit backend/collector.py
   # and uncomment the last line:
   # collector.run_continuous(interval_minutes=15)
   ```

### 3. Frontend Setup

1. **Navigate to Frontend Directory**
   ```bash
   cd frontend
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Start Development Server**
   ```bash
   npm run dev
   ```

4. **Open Browser**
   - Visit: http://localhost:3000
   - You should see the dashboard

## Troubleshooting

### "No data available" in dashboard

- Make sure you've run the data collector at least once
- Check that data exists in Supabase tables
- Verify the expiration date selector has dates available

### Alpaca API Errors

- Verify your API key and secret are correct
- Check that you have options data access in your Alpaca account
- Ensure you're using the correct base URL (paper vs live)

### Supabase Connection Errors

- Verify the Supabase URL and anon key are correct
- Check that tables were created successfully
- Ensure Row Level Security policies allow read access

### Python Import Errors

- Make sure you're in the project root directory
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check that Python path includes the project directory

## Next Steps

1. **Set up Continuous Data Collection**
   - Use a cron job or cloud scheduler
   - Or deploy the collector as a background service

2. **Customize Visualizations**
   - Edit components in `frontend/components/`
   - Adjust chart styles and colors

3. **Add More Features**
   - Real-time updates using Supabase Realtime
   - Additional Greeks visualizations
   - Historical data analysis

