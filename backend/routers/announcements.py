from fastapi import APIRouter, HTTPException, Query
from typing import List
from models import Announcement, AnnouncementCreate, AnnouncementUpdate
from database import (
    get_announcements,
    get_announcement,
    create_announcement,
    update_announcement,
    delete_announcement
)

router = APIRouter()

@router.get("", response_model=List[Announcement])
async def list_announcements(
    limit: int = Query(20, ge=1, le=100, description="Limit number of results")
):
    """Get all announcements"""
    announcements = get_announcements()
    return announcements[:limit]

@router.get("/{announcement_id}", response_model=Announcement)
async def get_announcement_by_id(announcement_id: str):
    """Get a specific announcement by ID"""
    announcement = get_announcement(announcement_id)
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return announcement

@router.post("", response_model=Announcement, status_code=201)
async def create_new_announcement(announcement: AnnouncementCreate):
    """Create a new announcement"""
    announcement_data = announcement.model_dump()
    new_announcement = create_announcement(announcement_data)
    return new_announcement

@router.put("/{announcement_id}", response_model=Announcement)
async def update_announcement_by_id(announcement_id: str, announcement_update: AnnouncementUpdate):
    """Update an announcement"""
    announcement = get_announcement(announcement_id)
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    update_data = announcement_update.model_dump(exclude_unset=True)
    updated_announcement = update_announcement(announcement_id, update_data)

    if not updated_announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    return updated_announcement

@router.delete("/{announcement_id}", status_code=204)
async def delete_announcement_by_id(announcement_id: str):
    """Delete an announcement"""
    success = delete_announcement(announcement_id)
    if not success:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return None

@router.get("/latest/list", response_model=List[Announcement])
async def get_latest_announcements(limit: int = Query(5, ge=1, le=20)):
    """Get latest announcements"""
    announcements = get_announcements()
    return announcements[:limit]
