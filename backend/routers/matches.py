from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from models import Match, MatchCreate, MatchUpdate, MatchStatus
from database import (
    get_matches,
    get_match,
    create_match,
    update_match,
    delete_match,
    complete_match,
    get_players
)

router = APIRouter()

class GoalAssist(BaseModel):
    player_name: str
    count: int = 1

class MatchCompleteRequest(BaseModel):
    fc_ssoa_score: int
    opponent_score: int
    goals: Optional[List[GoalAssist]] = []
    assists: Optional[List[GoalAssist]] = []

@router.get("", response_model=List[Match])
async def list_matches(
    status: Optional[MatchStatus] = Query(None, description="Filter by match status"),
    limit: Optional[int] = Query(None, ge=1, le=100, description="Limit number of results")
):
    """Get all matches with optional filtering"""
    matches = get_matches()

    if status:
        matches = [m for m in matches if m.get("status") == status]

    if limit:
        matches = matches[:limit]

    return matches

@router.get("/players-for-stats")
async def get_players_for_stats():
    """Get list of players for goal/assist selection"""
    players = get_players()
    return [{"name": p["name"], "position": p["position"], "jersey_number": p.get("jersey_number")} for p in players]

@router.get("/{match_id}", response_model=Match)
async def get_match_by_id(match_id: str):
    """Get a specific match by ID"""
    match = get_match(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match

@router.post("", response_model=Match, status_code=201)
async def create_new_match(match: MatchCreate):
    """Create a new match"""
    match_data = match.model_dump()
    new_match = create_match(match_data)
    return new_match

@router.put("/{match_id}", response_model=Match)
async def update_match_by_id(match_id: str, match_update: MatchUpdate):
    """Update a match"""
    match = get_match(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    update_data = match_update.model_dump(exclude_unset=True)
    updated_match = update_match(match_id, update_data)

    if not updated_match:
        raise HTTPException(status_code=404, detail="Match not found")

    return updated_match

@router.post("/{match_id}/complete", response_model=Match)
async def complete_match_with_stats(match_id: str, request: MatchCompleteRequest):
    """Complete a match and update player stats with goals and assists"""
    match = get_match(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    if match.get("status") == "completed":
        raise HTTPException(status_code=400, detail="Match is already completed")
    
    goal_scorers = [g.model_dump() for g in request.goals] if request.goals else []
    assist_providers = [a.model_dump() for a in request.assists] if request.assists else []
    
    updated_match = complete_match(
        match_id,
        request.fc_ssoa_score,
        request.opponent_score,
        goal_scorers,
        assist_providers
    )
    
    if not updated_match:
        raise HTTPException(status_code=500, detail="Failed to complete match")
    
    return updated_match

@router.delete("/{match_id}", status_code=204)
async def delete_match_by_id(match_id: str):
    """Delete a match"""
    success = delete_match(match_id)
    if not success:
        raise HTTPException(status_code=404, detail="Match not found")
    return None

@router.get("/upcoming/list", response_model=List[Match])
async def get_upcoming_matches(limit: int = Query(5, ge=1, le=50)):
    """Get upcoming matches"""
    matches = get_matches()
    upcoming = [m for m in matches if m.get("status") == "scheduled"]
    return upcoming[:limit]

@router.get("/completed/list", response_model=List[Match])
async def get_completed_matches(limit: int = Query(10, ge=1, le=100)):
    """Get completed matches"""
    matches = get_matches()
    completed = [m for m in matches if m.get("status") == "completed"]
    return completed[:limit]

