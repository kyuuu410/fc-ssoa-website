from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from models import Player, PlayerCreate, PlayerUpdate, PlayerPosition
from database import (
    get_players,
    get_player,
    create_player,
    update_player,
    delete_player
)

router = APIRouter()

@router.get("", response_model=List[Player])
async def list_players(
    position: Optional[PlayerPosition] = Query(None, description="Filter by position"),
    sort_by: Optional[str] = Query("name", description="Sort by field (name, goals, assists, matches_played)")
):
    """Get all players with optional filtering and sorting"""
    players = get_players()

    if position:
        players = [p for p in players if p.get("position") == position]

    # Sort players
    if sort_by == "goals":
        players = sorted(players, key=lambda x: x.get("goals", 0), reverse=True)
    elif sort_by == "assists":
        players = sorted(players, key=lambda x: x.get("assists", 0), reverse=True)
    elif sort_by == "matches_played":
        players = sorted(players, key=lambda x: x.get("matches_played", 0), reverse=True)
    else:
        players = sorted(players, key=lambda x: x.get("name", ""))

    return players

@router.get("/{player_id}", response_model=Player)
async def get_player_by_id(player_id: str):
    """Get a specific player by ID"""
    player = get_player(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@router.post("", response_model=Player, status_code=201)
async def create_new_player(player: PlayerCreate):
    """Create a new player"""
    player_data = player.model_dump()
    new_player = create_player(player_data)
    return new_player

@router.put("/{player_id}", response_model=Player)
async def update_player_by_id(player_id: str, player_update: PlayerUpdate):
    """Update a player"""
    player = get_player(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    update_data = player_update.model_dump(exclude_unset=True)
    updated_player = update_player(player_id, update_data)

    if not updated_player:
        raise HTTPException(status_code=404, detail="Player not found")

    return updated_player

@router.delete("/{player_id}", status_code=204)
async def delete_player_by_id(player_id: str):
    """Delete a player"""
    success = delete_player(player_id)
    if not success:
        raise HTTPException(status_code=404, detail="Player not found")
    return None

@router.get("/top/scorers", response_model=List[Player])
async def get_top_scorers(limit: int = Query(10, ge=1, le=50)):
    """Get top scorers"""
    players = get_players()
    sorted_players = sorted(players, key=lambda x: x.get("goals", 0), reverse=True)
    return sorted_players[:limit]

@router.get("/top/assisters", response_model=List[Player])
async def get_top_assisters(limit: int = Query(10, ge=1, le=50)):
    """Get top assist providers"""
    players = get_players()
    sorted_players = sorted(players, key=lambda x: x.get("assists", 0), reverse=True)
    return sorted_players[:limit]
