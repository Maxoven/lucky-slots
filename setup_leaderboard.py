#!/usr/bin/env python3
"""
Database setup script for Slot Machine Leaderboard
This script creates the leaderboard table in Aiven PostgreSQL
"""

import psycopg2
from psycopg2 import sql

# Database connection parameters
DB_CONFIG = {
    'host': 'pg-3c241857-maxvak12-867e.i.aivencloud.com',
    'port': 13837,
    'database': 'defaultdb',
    'user': 'avnadmin',
    'password': 'AVNS_PS0cT7HmCXugiWhxY8M',
    'sslmode': 'require'
}

def setup_leaderboard_table():
    """Create the leaderboard table"""
    try:
        # Connect to the database
        print("Connecting to database...")
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Create the leaderboard table
        print("Creating leaderboard table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS slot_leaderboard (
                id SERIAL PRIMARY KEY,
                player_name VARCHAR(50) NOT NULL,
                win_amount INTEGER NOT NULL,
                bet_amount INTEGER NOT NULL,
                multiplier DECIMAL(5,1) NOT NULL,
                winning_symbols VARCHAR(20) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create index for faster queries
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_win_amount 
            ON slot_leaderboard(win_amount DESC);
        """)
        
        # Check if table already has data
        cur.execute("SELECT COUNT(*) FROM slot_leaderboard;")
        count = cur.fetchone()[0]
        
        if count == 0:
            print("Adding sample leaderboard data...")
            sample_data = [
                ('Alice', 1500, 100, 50.0, '💎💎💎'),
                ('Bob', 1300, 100, 20.0, '🍀🍀🍀'),
                ('Charlie', 120, 100, 15.0, '🎰🎰🎰'),
                ('Diana', 110, 100, 10.0, '🍇🍇🍇'),
                ('Eve', 100, 100, 8.0, '🍊🍊🍊')
            ]
            
            cur.executemany(
                """INSERT INTO slot_leaderboard 
                   (player_name, win_amount, bet_amount, multiplier, winning_symbols) 
                   VALUES (%s, %s, %s, %s, %s);""",
                sample_data
            )
            print(f"Added {len(sample_data)} sample entries")
        else:
            print(f"Table already contains {count} records")
        
        # Commit changes
        conn.commit()
        
        # Display current leaderboard
        cur.execute("""
            SELECT player_name, win_amount, winning_symbols, created_at 
            FROM slot_leaderboard 
            ORDER BY win_amount DESC 
            LIMIT 10;
        """)
        print("\nCurrent Top 10 Leaderboard:")
        print("-" * 60)
        for idx, row in enumerate(cur.fetchall(), 1):
            print(f"{idx}. {row[0]} - {row[1]} UE ({row[2]}) - {row[3]}")
        
        cur.close()
        conn.close()
        print("\nLeaderboard table setup complete!")
        
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    setup_leaderboard_table()
