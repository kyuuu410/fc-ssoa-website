import csv
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional

# Data directory path
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# In-memory storage
players_db: Dict[str, dict] = {}
matches_db: Dict[str, dict] = {}
announcements_db: Dict[str, dict] = {}
team_stats_data: dict = {}  # 팀 전체 전적

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
    """Initialize database from CSV files"""
    load_players_from_csv()
    load_team_stats_from_csv()
    
    # 경기 일정은 웹에서 직접 추가
    # matches_db는 비워둠 - 사용자가 홈페이지에서 추가

    # Sample announcements
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
        announcements_db[announcement["id"]] = announcement

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
    return sorted(matches_db.values(), key=lambda x: x["match_date"], reverse=True)

def get_match(match_id: str) -> Optional[dict]:
    return matches_db.get(match_id)

def create_match(match_data: dict) -> dict:
    match_id = str(uuid.uuid4())
    match = {
        "id": match_id,
        "status": "scheduled",
        "fc_ssoa_score": None,
        "opponent_score": None,
        "notes": None,
        "created_at": datetime.now().isoformat(),
        **match_data
    }
    matches_db[match_id] = match
    return match

def update_match(match_id: str, match_data: dict) -> Optional[dict]:
    if match_id not in matches_db:
        return None

    match = matches_db[match_id]
    for key, value in match_data.items():
        if value is not None:
            match[key] = value

    matches_db[match_id] = match
    return match

def delete_match(match_id: str) -> bool:
    if match_id in matches_db:
        del matches_db[match_id]
        return True
    return False

def complete_match(match_id: str, fc_ssoa_score: int, opponent_score: int, 
                   goal_scorers: List[dict] = None, assist_providers: List[dict] = None) -> Optional[dict]:
    """Complete a match and update player stats"""
    if match_id not in matches_db:
        return None
    
    match = matches_db[match_id]
    match['status'] = 'completed'
    match['fc_ssoa_score'] = fc_ssoa_score
    match['opponent_score'] = opponent_score
    matches_db[match_id] = match
    
    # Update player stats
    if goal_scorers:
        for scorer in goal_scorers:
            add_player_stats(scorer['player_name'], goals=scorer.get('count', 1))
    
    if assist_providers:
        for assister in assist_providers:
            add_player_stats(assister['player_name'], assists=assister.get('count', 1))
    
    return match

# Announcement functions
def get_announcements() -> List[dict]:
    return sorted(announcements_db.values(), key=lambda x: x["created_at"], reverse=True)

def get_announcement(announcement_id: str) -> Optional[dict]:
    return announcements_db.get(announcement_id)

def create_announcement(announcement_data: dict) -> dict:
    announcement_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    announcement = {
        "id": announcement_id,
        "created_at": now,
        "updated_at": now,
        **announcement_data
    }
    announcements_db[announcement_id] = announcement
    return announcement

def update_announcement(announcement_id: str, announcement_data: dict) -> Optional[dict]:
    if announcement_id not in announcements_db:
        return None

    announcement = announcements_db[announcement_id]
    for key, value in announcement_data.items():
        if value is not None:
            announcement[key] = value

    announcement["updated_at"] = datetime.now().isoformat()
    announcements_db[announcement_id] = announcement
    return announcement

def delete_announcement(announcement_id: str) -> bool:
    if announcement_id in announcements_db:
        del announcements_db[announcement_id]
        return True
    return False
