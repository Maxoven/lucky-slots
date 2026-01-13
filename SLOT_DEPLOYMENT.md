# 🎰 Slot Machine with Leaderboard - Deployment Guide

Your casino slot machine now has a **LEADERBOARD** that tracks the top 5 biggest wins of all time!

## 🆕 New Features

- 🏆 **Top 5 Leaderboard** - Shows the biggest wins
- 👤 **Player Names** - Enter your name to get on the leaderboard
- 💾 **Database Storage** - All wins saved to Aiven PostgreSQL
- 🥇 **Medal Ranks** - Gold, Silver, Bronze medals for top 3
- 🔄 **Auto-refresh** - Leaderboard updates after each big win (100+ UE)

## 📋 Files You Need

- `slot-machine.html` - The updated slot machine with leaderboard UI
- `slot-app.py` - Flask backend API for leaderboard
- `setup_leaderboard.py` - Database setup script
- `slot-requirements.txt` - Python dependencies (rename to `requirements.txt`)
- `slot-Procfile` - Render configuration (rename to `Procfile`)
- `slot-runtime.txt` - Python version (rename to `runtime.txt`)

## 🚀 Deployment Steps

### Step 1: Set Up Database Table

Run this locally first to create the leaderboard table:

```bash
python setup_leaderboard.py
```

This creates:
- `slot_leaderboard` table in your Aiven database
- Sample data with 5 initial entries
- Proper indexes for fast queries

### Step 2: Prepare Files for GitHub

Rename files:
```bash
mv slot-requirements.txt requirements.txt
mv slot-Procfile Procfile
mv slot-runtime.txt runtime.txt
mv slot-app.py app.py
```

Your folder should have:
```
slot-casino/
├── app.py
├── slot-machine.html
├── requirements.txt
├── Procfile
├── runtime.txt
└── setup_leaderboard.py (optional, for local use)
```

### Step 3: Push to GitHub

1. Create a new repository on GitHub
2. Upload all files
3. Make sure `Procfile` and `runtime.txt` are included!

### Step 4: Deploy to Render

1. Go to https://render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `slot-casino` (or your choice)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: **Free**

5. Click **"Create Web Service"**
6. Wait 3-5 minutes for deployment

### Step 5: Test Your Casino!

Visit your URL: `https://your-app.onrender.com`

Test the features:
1. ✅ Enter your name and click "SAVE"
2. ✅ Spin the wheel
3. ✅ Win a big jackpot (100+ UE)
4. ✅ Check the leaderboard - your win should appear!
5. ✅ Click "REFRESH" to reload leaderboard

## 🎮 How the Leaderboard Works

### Qualifying for Leaderboard
- Only wins of **100 UE or more** are submitted
- You must have a **player name** saved
- Automatic submission after each qualifying win

### Leaderboard Display
- Shows **Top 5** biggest wins of all time
- 🥇 Gold medal for #1
- 🥈 Silver medal for #2  
- 🥉 Bronze medal for #3
- Displays: Player name, symbols, multiplier, win amount

### Database Storage
All wins are permanently stored in your Aiven PostgreSQL database:
- Player name
- Win amount
- Bet amount
- Multiplier (e.g., 50x)
- Winning symbols (e.g., 💎💎💎)
- Timestamp

## 🔧 API Endpoints

Your Flask backend provides these endpoints:

### Get Leaderboard
```
GET /api/leaderboard
```
Returns top 5 biggest wins

### Submit Win
```
POST /api/leaderboard
Body: {
  "player_name": "Alice",
  "win_amount": 5000,
  "bet_amount": 100,
  "multiplier": 50.0,
  "winning_symbols": "💎💎💎"
}
```

### Health Check
```
GET /api/health
```
Checks database connection

## 🎯 Tips for Players

1. **Save Your Name First** - Enter your name before playing to track wins
2. **Go for Big Wins** - Only wins of 100+ UE make the leaderboard
3. **High Bets = High Wins** - Bet more for bigger payouts
4. **Refresh to Update** - Click refresh button to see latest rankings
5. **Compete for #1** - Try to beat the top score!

## 🐛 Troubleshooting

### Leaderboard Not Loading?
- Check that `setup_leaderboard.py` ran successfully
- Verify Aiven database is running
- Check Render logs for errors

### Wins Not Appearing?
- Make sure you saved your player name
- Only wins of 100+ UE are submitted
- Check browser console (F12) for errors

### "Failed to load leaderboard"?
- Database connection issue
- Check Aiven firewall allows Render's IP
- Verify database credentials in `app.py`

## 📊 Database Schema

```sql
CREATE TABLE slot_leaderboard (
    id SERIAL PRIMARY KEY,
    player_name VARCHAR(50) NOT NULL,
    win_amount INTEGER NOT NULL,
    bet_amount INTEGER NOT NULL,
    multiplier DECIMAL(5,1) NOT NULL,
    winning_symbols VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🎨 Customization Ideas

### Change Minimum Win for Leaderboard
In `slot-machine.html`, find:
```javascript
if (playerName && winAmount >= 100) {
```
Change `100` to any amount.

### Show More Entries
In `slot-app.py`, change:
```python
LIMIT 5
```
To show more (e.g., `LIMIT 10`)

### Add More Stats
You could add:
- Total wins by player
- Average win amount
- Best winning streak
- Most common winning symbols

## 🔒 Security Notes

For production use, consider:
1. Add environment variables for database credentials
2. Add rate limiting to prevent spam
3. Add input validation and sanitization
4. Add HTTPS (Render provides this automatically)

## 🎉 What's Next?

Your casino is now fully functional with:
- ✅ 70% win rate
- ✅ Player names
- ✅ Leaderboard tracking
- ✅ Database storage
- ✅ Auto-refill balance
- ✅ Sound effects
- ✅ Animations

Enjoy your casino and may the odds be ever in your favor! 🍀🎰💰

---

**Note**: Make sure to run `setup_leaderboard.py` locally before deploying to create the database table!
