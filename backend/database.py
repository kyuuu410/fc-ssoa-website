import csv
import os
import uuid
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional
import json

# Data directory path
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DB_PATH = os.path.join(DATA_DIR, "fc_ssoa.db")

# In-memory storage (players only, others use SQLite)
players_db: Dict[str, dict] = {}
team_stats_data: dict = {}  # 팀 전체 전적

# SQLite connection
def get_db_connection():
    """Get SQLite database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_sqlite_db():
    """Initialize SQLite database tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create matches table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id TEXT PRIMARY KEY,
            match_date TEXT NOT NULL,
            opponent TEXT NOT NULL,
            location TEXT,
            status TEXT DEFAULT 'scheduled',
            fc_ssoa_score INTEGER,
            opponent_score INTEGER,
            notes TEXT,
            goal_scorers TEXT,
            assist_providers TEXT,
            created_at TEXT NOT NULL
        )
    ''')
    
    # Create announcements table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS announcements (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def get_csv_path(filename: str) -> str:
    return os.path.join(DATA_DIR, filename)

def load_players_from_csv():
    """Load players from stats_all.csv"""
    global players_db
    players_db.clear()
    
    csv_path = get_csv_path("stats_all.csv")
    if not os.path.exists(csv_path):
        print(f"Warning: {csv_path} not found")
        return
    
    position_map = {
        "GK": "goalkeeper",
        "DF": "defender", 
        "MF": "midfielder",
        "FW": "forward"
    }
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('이름', '').strip()
            if not name:
                continue
                
            position_code = row.get('포지션', '').strip()
            jersey_str = row.get('등번호', '').strip()
            goals_str = row.get('골', '0').strip()
            assists_str = row.get('어시', '0').strip()
            
            player_id = name  # Use name as ID for simplicity
            
            players_db[player_id] = {
                "id": player_id,
                "name": name,
                "position": position_map.get(position_code, "midfielder"),
                "jersey_number": int(jersey_str) if jersey_str.isdigit() else None,
                "phone": None,
                "email": None,
                "join_date": "2024-01-01",
                "goals": int(goals_str) if goals_str.isdigit() else 0,
                "assists": int(assists_str) if assists_str.isdigit() else 0,
                "matches_played": 37  # From team_stats.csv
            }

def save_players_to_csv():
    """Save players data back to CSV"""
    csv_path = get_csv_path("stats_all.csv")
    
    position_reverse_map = {
        "goalkeeper": "GK",
        "defender": "DF",
        "midfielder": "MF", 
        "forward": "FW"
    }
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['포지션', '등번호', '이름', '골', '어시', '공격포인트']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for player in players_db.values():
            goals = player.get('goals', 0)
            assists = player.get('assists', 0)
            writer.writerow({
                '포지션': position_reverse_map.get(player.get('position'), 'MF'),
                '등번호': player.get('jersey_number', ''),
                '이름': player.get('name', ''),
                '골': goals,
                '어시': assists,
                '공격포인트': goals + assists
            })

def load_team_stats_from_csv():
    """Load team stats from team_stats.csv"""
    global team_stats_data
    
    csv_path = get_csv_path("team_stats.csv")
    if not os.path.exists(csv_path):
        print(f"Warning: {csv_path} not found")
        return
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            team_stats_data = {
                "total_matches": int(row.get('전적', 0)),
                "wins": int(row.get('승리', 0)),
                "draws": int(row.get('무승부', 0)),
                "losses": int(row.get('패배', 0)),
                "goals_scored": int(row.get('득점', 0)),
                "goals_conceded": int(row.get('실점', 0))
            }
            break  # 첫 번째 행만 읽음

def get_team_stats() -> dict:
    """Get team stats"""
    return team_stats_data

def init_db():
    """Initialize database from CSV files and SQLite"""
    init_sqlite_db()
    load_players_from_csv()
    load_team_stats_from_csv()
    
    # Add sample announcements if database is empty
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM announcements")
    count = cursor.fetchone()[0]
    
    if count == 0:
        sample_announcements = [
            {
                "id": str(uuid.uuid4()),
                "title": "FC쏘아에 오신 것을 환영합니다!",
                "content": "우리 팀 웹사이트에 오신 것을 환영합니다. 경기 일정과 팀 소식을 확인하세요!",
                "author": "팀 매니저",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": str(uuid.uuid4()),
                "title": "이번 주 토요일 훈련",
                "content": "이번 주 토요일 오전 7시 훈련이 있습니다. 15분 일찍 도착해주세요.",
                "author": "코치",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
        ]
        
        for announcement in sample_announcements:
            cursor.execute('''
                INSERT INTO announcements (id, title, content, author, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                announcement["id"],
                announcement["title"],
                announcement["content"],
                announcement["author"],
                announcement["created_at"],
                announcement["updated_at"]
            ))
        
        conn.commit()
    conn.close()

# Player functions
def get_players() -> List[dict]:
    return list(players_db.values())

def get_player(player_id: str) -> Optional[dict]:
    return players_db.get(player_id)

def create_player(player_data: dict) -> dict:
    player_id = player_data.get('name', str(uuid.uuid4()))
    player = {
        "id": player_id,
        "goals": 0,
        "assists": 0,
        "matches_played": 0,
        **player_data
    }
    players_db[player_id] = player
    save_players_to_csv()
    return player

def update_player(player_id: str, player_data: dict) -> Optional[dict]:
    if player_id not in players_db:
        return None
    
    player = players_db[player_id]
    for key, value in player_data.items():
        if value is not None:
            player[key] = value
    
    players_db[player_id] = player
    save_players_to_csv()
    return player

def delete_player(player_id: str) -> bool:
    if player_id in players_db:
        del players_db[player_id]
        save_players_to_csv()
        return True
    return False

def add_player_stats(player_name: str, goals: int = 0, assists: int = 0) -> Optional[dict]:
    """Add goals and assists to a player's stats"""
    if player_name not in players_db:
        return None
    
    player = players_db[player_name]
    player['goals'] = player.get('goals', 0) + goals
    player['assists'] = player.get('assists', 0) + assists
    players_db[player_name] = player
    save_players_to_csv()
    return player

# Match functions
def get_matches() -> List[dict]:
    """Get all matches from SQLite"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM matches ORDER BY match_date DESC")
    rows = cursor.fetchall()
    conn.close()
    
    matches = []
    for row in rows:
        match = dict(row)
        # Parse JSON fields
        if match.get('goal_scorers'):
            match['goal_scorers'] = json.loads(match['goal_scorers'])
        if match.get('assist_providers'):
            match['assist_providers'] = json.loads(match['assist_providers'])
        matches.append(match)
    
    return matches

def get_match(match_id: str) -> Optional[dict]:
    """Get a single match by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM matches WHERE id = ?", (match_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
    
    match = dict(row)
    # Parse JSON fields
    if match.get('goal_scorers'):
        match['goal_scorers'] = json.loads(match['goal_scorers'])
    if match.get('assist_providers'):
        match['assist_providers'] = json.loads(match['assist_providers'])
    
    return match

def create_match(match_data: dict) -> dict:
    """Create a new match"""
    match_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO matches (id, match_date, opponent, location, status, 
                           fc_ssoa_score, opponent_score, notes, goal_scorers, 
                           assist_providers, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        match_id,
        match_data.get('match_date'),
        match_data.get('opponent'),
        match_data.get('location'),
        match_data.get('status', 'scheduled'),
        match_data.get('fc_ssoa_score'),
        match_data.get('opponent_score'),
        match_data.get('notes'),
        None,  # goal_scorers
        None,  # assist_providers
        now
    ))
    
    conn.commit()
    conn.close()
    
    return get_match(match_id)

def update_match(match_id: str, match_data: dict) -> Optional[dict]:
    """Update an existing match"""
    if not get_match(match_id):
        return None
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Build dynamic update query
    update_fields = []
    values = []
    
    for key in ['match_date', 'opponent', 'location', 'status', 
                'fc_ssoa_score', 'opponent_score', 'notes']:
        if key in match_data and match_data[key] is not None:
            update_fields.append(f"{key} = ?")
            values.append(match_data[key])
    
    if update_fields:
        values.append(match_id)
        query = f"UPDATE matches SET {', '.join(update_fields)} WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()
    
    conn.close()
    return get_match(match_id)

def delete_match(match_id: str) -> bool:
    """Delete a match"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM matches WHERE id = ?", (match_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def complete_match(match_id: str, fc_ssoa_score: int, opponent_score: int, 
                   goal_scorers: List[dict] = None, assist_providers: List[dict] = None) -> Optional[dict]:
    """Complete a match and update player stats"""
    if not get_match(match_id):
        return None
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Update match status and scores
    cursor.execute('''
        UPDATE matches 
        SET status = 'completed', 
            fc_ssoa_score = ?, 
            opponent_score = ?,
            goal_scorers = ?,
            assist_providers = ?
        WHERE id = ?
    ''', (
        fc_ssoa_score,
        opponent_score,
        json.dumps(goal_scorers) if goal_scorers else None,
        json.dumps(assist_providers) if assist_providers else None,
        match_id
    ))
    
    conn.commit()
    conn.close()
    
    # Update player stats (CRITICAL: This preserves the CSV update flow)
    if goal_scorers:
        for scorer in goal_scorers:
            add_player_stats(scorer['player_name'], goals=scorer.get('count', 1))
    
    if assist_providers:
        for assister in assist_providers:
            add_player_stats(assister['player_name'], assists=assister.get('count', 1))
    
    return get_match(match_id)

# Announcement functions
def get_announcements() -> List[dict]:
    """Get all announcements from SQLite"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM announcements ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def get_announcement(announcement_id: str) -> Optional[dict]:
    """Get a single announcement by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM announcements WHERE id = ?", (announcement_id,))
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else None

def create_announcement(announcement_data: dict) -> dict:
    """Create a new announcement"""
    announcement_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO announcements (id, title, content, author, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        announcement_id,
        announcement_data.get('title'),
        announcement_data.get('content'),
        announcement_data.get('author'),
        now,
        now
    ))
    
    conn.commit()
    conn.close()
    
    return get_announcement(announcement_id)

def update_announcement(announcement_id: str, announcement_data: dict) -> Optional[dict]:
    """Update an existing announcement"""
    if not get_announcement(announcement_id):
        return None
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Build dynamic update query
    update_fields = []
    values = []
    
    for key in ['title', 'content', 'author']:
        if key in announcement_data and announcement_data[key] is not None:
            update_fields.append(f"{key} = ?")
            values.append(announcement_data[key])
    
    if update_fields:
        update_fields.append("updated_at = ?")
        values.append(datetime.now().isoformat())
        values.append(announcement_id)
        
        query = f"UPDATE announcements SET {', '.join(update_fields)} WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()
    
    conn.close()
    return get_announcement(announcement_id)

def delete_announcement(announcement_id: str) -> bool:
    """Delete an announcement"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM announcements WHERE id = ?", (announcement_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted
