#!/usr/bin/env python3
"""
Flask API for Slot Machine Leaderboard
Connects to Aiven PostgreSQL database
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__, static_folder='.')
CORS(app)

# Database connection parameters
DB_CONFIG = {
    'host': 'pg-3c241857-maxvak12-867e.i.aivencloud.com',
    'port': 13837,
    'database': 'defaultdb',
    'user': 'avnadmin',
    'password': 'AVNS_PS0cT7HmCXugiWhxY8M',
    'sslmode': 'require'
}

def get_db_connection():
    """Create a database connection"""
    return psycopg2.connect(**DB_CONFIG)

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'slot-machine.html')

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get top 5 players from leaderboard"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT 
                player_name,
                win_amount,
                bet_amount,
                multiplier,
                winning_symbols,
                created_at
            FROM slot_leaderboard 
            ORDER BY win_amount DESC 
            LIMIT 5;
        """)
        
        results = cur.fetchall()
        cur.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'data': [dict(row) for row in results]
        })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/leaderboard', methods=['POST'])
def add_to_leaderboard():
    """Add a new winning entry to the leaderboard"""
    try:
        data = request.get_json()
        
        required_fields = ['player_name', 'win_amount', 'bet_amount', 'multiplier', 'winning_symbols']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400
        
        player_name = data['player_name'].strip()
        win_amount = int(data['win_amount'])
        bet_amount = int(data['bet_amount'])
        multiplier = float(data['multiplier'])
        winning_symbols = data['winning_symbols'].strip()
        
        if not player_name or len(player_name) > 50:
            return jsonify({
                'success': False,
                'message': 'Player name must be 1-50 characters'
            }), 400
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            INSERT INTO slot_leaderboard 
                (player_name, win_amount, bet_amount, multiplier, winning_symbols) 
            VALUES (%s, %s, %s, %s, %s) 
            RETURNING id, player_name, win_amount, winning_symbols, created_at;
        """, (player_name, win_amount, bet_amount, multiplier, winning_symbols))
        
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Added to leaderboard!',
            'data': dict(result)
        }), 201
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/player-rank/<player_name>', methods=['GET'])
def get_player_rank(player_name):
    """Get a player's best win and rank"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            WITH ranked_wins AS (
                SELECT 
                    player_name,
                    win_amount,
                    winning_symbols,
                    RANK() OVER (ORDER BY win_amount DESC) as rank
                FROM slot_leaderboard
            )
            SELECT * FROM ranked_wins 
            WHERE LOWER(player_name) = LOWER(%s)
            ORDER BY win_amount DESC
            LIMIT 1;
        """, (player_name,))
        
        result = cur.fetchone()
        cur.close()
        conn.close()
        
        if result:
            return jsonify({
                'success': True,
                'data': dict(result)
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Player not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Check database connection"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM slot_leaderboard;")
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Database connection successful',
            'total_entries': count
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Visit http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
