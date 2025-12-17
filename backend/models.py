from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class PlayerPosition(str, Enum):
    GOALKEEPER = "goalkeeper"
    DEFENDER = "defender"
    MIDFIELDER = "midfielder"
    FORWARD = "forward"

class MatchStatus(str, Enum):
    SCHEDULED = "scheduled"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class PlayerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    position: PlayerPosition
    jersey_number: Optional[int] = Field(None, ge=1, le=99)
    phone: Optional[str] = None
    email: Optional[str] = None
    join_date: Optional[str] = None

class PlayerCreate(PlayerBase):
    pass

class PlayerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    position: Optional[PlayerPosition] = None
    jersey_number: Optional[int] = Field(None, ge=1, le=99)
    phone: Optional[str] = None
    email: Optional[str] = None
    join_date: Optional[str] = None

class Player(PlayerBase):
    id: str
    goals: int = 0
    assists: int = 0
    matches_played: int = 0

    class Config:
        from_attributes = True

class MatchBase(BaseModel):
    opponent: str = Field(..., min_length=1, max_length=100)
    match_date: str
    location: str = Field(..., min_length=1, max_length=200)
    home_away: str = Field(..., pattern="^(home|away)$")

class MatchCreate(MatchBase):
    pass

class MatchUpdate(BaseModel):
    opponent: Optional[str] = Field(None, min_length=1, max_length=100)
    match_date: Optional[str] = None
    location: Optional[str] = Field(None, min_length=1, max_length=200)
    home_away: Optional[str] = Field(None, pattern="^(home|away)$")
    status: Optional[MatchStatus] = None
    fc_ssoa_score: Optional[int] = Field(None, ge=0)
    opponent_score: Optional[int] = Field(None, ge=0)
    notes: Optional[str] = None

class Match(MatchBase):
    id: str
    status: MatchStatus = MatchStatus.SCHEDULED
    fc_ssoa_score: Optional[int] = None
    opponent_score: Optional[int] = None
    notes: Optional[str] = None
    created_at: str

    class Config:
        from_attributes = True

class AnnouncementBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1, max_length=100)

class AnnouncementCreate(AnnouncementBase):
    pass

class AnnouncementUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    author: Optional[str] = Field(None, min_length=1, max_length=100)

class Announcement(AnnouncementBase):
    id: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class TeamInfo(BaseModel):
    name: str = "FC쏘아"
    founded: str = "2024"
    description: str
    total_players: int = 0
    total_matches: int = 0
    wins: int = 0
    draws: int = 0
    losses: int = 0

class TeamStats(BaseModel):
    total_players: int
    total_matches: int
    wins: int
    draws: int
    losses: int
    win_rate: float
    total_goals_scored: int
    total_goals_conceded: int
    upcoming_matches: int
