from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class NotePosition(BaseModel):
    string: int
    fret: int
    note: str

class ChordRecognitionRequest(BaseModel):
    notes: List[str]
    selected_positions: Optional[List[NotePosition]] = []

class RecognizedChord(BaseModel):
    name: str
    type: str
    structure: str
    confidence: int
    notes: List[str]
    is_exact_match: bool
    category: str = ""

class ChordRecognitionResponse(BaseModel):
    recognized_chords: List[RecognizedChord]
    unique_notes: List[str]
    total_notes: int

class PlayNoteRequest(BaseModel):
    note: str
    octave: Optional[int] = 4
    duration: Optional[int] = 500

class PlayNoteResponse(BaseModel):
    status: str
    note: str
    duration: int

class ChordModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    notes: List[str]
    chord_type: str
    structure: str
    category: str
    created_at: datetime = Field(default_factory=datetime.utcnow)