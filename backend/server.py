from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from models import (
    ChordRecognitionRequest, ChordRecognitionResponse, 
    PlayNoteRequest, PlayNoteResponse
)
from chord_recognition import ChordRecognitionEngine
from midi_service import MIDIService

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initialize services
chord_engine = ChordRecognitionEngine()
midi_service = MIDIService()

# Create the main app without a prefix
app = FastAPI(title="Guitar Fretboard Chord Recognition API")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Health check endpoint
@api_router.get("/")
async def root():
    return {"message": "Guitar Fretboard Chord Recognition API is running"}

@api_router.post("/recognize-chord", response_model=ChordRecognitionResponse)
async def recognize_chord(request: ChordRecognitionRequest):
    """
    Recognize chords from the given notes
    """
    try:
        if not request.notes or len(request.notes) < 2:
            raise HTTPException(status_code=400, detail="At least 2 notes are required for chord recognition")
        
        # Get unique notes
        unique_notes = list(dict.fromkeys(request.notes))
        
        # Recognize chords using the chord engine
        recognized_chords = chord_engine.recognize_chords(request.notes)
        
        return ChordRecognitionResponse(
            recognized_chords=recognized_chords,
            unique_notes=unique_notes,
            total_notes=len(request.notes)
        )
        
    except Exception as e:
        logging.error(f"Error in chord recognition: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@api_router.post("/play-note", response_model=PlayNoteResponse)
async def play_note(request: PlayNoteRequest):
    """
    Play a MIDI note (simulation)
    """
    try:
        response = await midi_service.play_note(request)
        return response
        
    except Exception as e:
        logging.error(f"Error playing note: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error playing note: {str(e)}")

@api_router.get("/note-info/{note}")
async def get_note_info(note: str, octave: int = 4):
    """
    Get information about a specific note
    """
    try:
        info = midi_service.get_note_info(note, octave)
        if not info['available']:
            raise HTTPException(status_code=404, detail=f"Note {note}{octave} not found")
        return info
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error getting note info: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting note info: {str(e)}")

@api_router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "chord_engine": "initialized",
        "midi_service": "initialized",
        "database": "connected" if client else "disconnected"
    }

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("Guitar Fretboard Chord Recognition API started")
    logger.info(f"Chord database loaded with {len(chord_engine.chord_database)} chords")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
    logger.info("Database connection closed")