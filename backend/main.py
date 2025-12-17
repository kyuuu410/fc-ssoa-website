from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import players, matches, announcements, team
from database import init_db

app = FastAPI(
    title="FC Ssoa API",
    description="Backend API for FC Ssoa early morning soccer team",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Include routers
app.include_router(team.router, prefix="/api/team", tags=["Team"])
app.include_router(players.router, prefix="/api/players", tags=["Players"])
app.include_router(matches.router, prefix="/api/matches", tags=["Matches"])
app.include_router(announcements.router, prefix="/api/announcements", tags=["Announcements"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to FC Ssoa API",
        "team": "FC쏘아",
        "version": "1.0.0"
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/gallery")
async def get_gallery():
    """Get gallery images"""
    return {
        "images": [
            {
                "id": "1",
                "url": "https://images.unsplash.com/photo-1579952363873-27f3bade9f55",
                "title": "Team Training",
                "description": "Early morning training session",
                "date": "2024-12-01"
            },
            {
                "id": "2",
                "url": "https://images.unsplash.com/photo-1606925797300-0b35e9d1794e",
                "title": "Match Day",
                "description": "Victory against FC Thunder",
                "date": "2024-11-28"
            },
            {
                "id": "3",
                "url": "https://images.unsplash.com/photo-1560272564-c83b66b1ad12",
                "title": "Team Photo",
                "description": "FC Ssoa team photo 2024",
                "date": "2024-11-15"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
