from fastapi import APIRouter, HTTPException
from typing import List
from models import TeamInfo, TeamStats, Player
from database import get_players, get_matches, get_team_stats as get_team_stats_from_db

router = APIRouter()

@router.get("/info", response_model=TeamInfo)
async def get_team_info():
    """Get team information"""
    players = get_players()
    stats = get_team_stats_from_db()

    return TeamInfo(
        name="FC쏘아",
        founded="2020",
        description="FC쏘아는 새벽 축구를 통해 열정, 팀워크, 그리고 축구에 대한 사랑을 나누는 조기축구팀입니다.",
        total_players=len(players),
        total_matches=stats.get("total_matches", 0),
        wins=stats.get("wins", 0),
        draws=stats.get("draws", 0),
        losses=stats.get("losses", 0)
    )

@router.get("/stats")
async def get_team_stats():
    """Get team statistics from CSV"""
    players = get_players()
    stats = get_team_stats_from_db()
    matches = get_matches()
    
    total_matches = stats.get("total_matches", 0)
    wins = stats.get("wins", 0)
    
    win_rate = (wins / total_matches * 100) if total_matches > 0 else 0.0
    upcoming_matches = len([m for m in matches if m.get("status") == "scheduled"])

    return {
        "total_players": len(players),
        "total_matches": total_matches,
        "wins": wins,
        "draws": stats.get("draws", 0),
        "losses": stats.get("losses", 0),
        "win_rate": round(win_rate, 2),
        "total_goals_scored": stats.get("goals_scored", 0),
        "total_goals_conceded": stats.get("goals_conceded", 0),
        "upcoming_matches": upcoming_matches
    }

@router.get("/members", response_model=List[Player])
async def get_team_members():
    """Get all team members"""
    players = get_players()
    return players
