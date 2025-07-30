# Gitar Fretboard Akor Tanıma - Backend Contracts

## API Endpoints

### 1. Chord Recognition API
**Endpoint:** `POST /api/recognize-chord`
**Purpose:** Seçilen notalardan akor tanıma
**Request:**
```json
{
  "notes": ["C", "E", "G"],
  "selected_positions": [
    {"string": 0, "fret": 3, "note": "C"},
    {"string": 1, "fret": 2, "note": "E"}, 
    {"string": 2, "fret": 0, "note": "G"}
  ]
}
```

**Response:**
```json
{
  "recognized_chords": [
    {
      "name": "C Major",
      "type": "Majör Akor", 
      "structure": "Root + Major 3rd + Perfect 5th",
      "confidence": 100,
      "notes": ["C", "E", "G"],
      "is_exact_match": true
    }
  ],
  "unique_notes": ["C", "E", "G"]
}
```

### 2. MIDI Sound API
**Endpoint:** `POST /api/play-note`
**Purpose:** MIDI nota sesi çalma
**Request:**
```json
{
  "note": "C",
  "octave": 4,
  "duration": 500
}
```

**Response:**
```json
{
  "status": "playing",
  "note": "C4",
  "duration": 500
}
```

### 3. Chord Database API
**Endpoint:** `GET /api/chords`
**Purpose:** Tüm akor veritabanını getir (opsiyonel)

## Database Models

### ChordModel
```python
class ChordModel(BaseModel):
    name: str
    notes: List[str]
    chord_type: str
    structure: str
    category: str  # "major", "minor", "seventh", "suspended", etc.
```

### NotePosition
```python
class NotePosition(BaseModel):
    string: int
    fret: int  
    note: str
```

## Mock Data Replacement

### Frontend Mock Data (mock/mockData.js):
- `recognizeChords()` fonksiyonu -> `/api/recognize-chord` API call
- Console.log MIDI sounds -> `/api/play-note` API call

### Current Mock Implementation:
```javascript
// Bu kod:
const chords = mockData.recognizeChords(notesList);

// Şuna dönüşecek:
const response = await axios.post(`${API}/recognize-chord`, {
  notes: notesList,
  selected_positions: selectedNotes
});
const chords = response.data.recognized_chords;
```

## Backend Implementation Plan

1. **Chord Recognition Algorithm:**
   - Major, minor, 7th chords (basic)
   - sus, add, dim, aug chords (advanced)
   - Note normalization (flats to sharps)
   - Confidence calculation
   - Alternative chord suggestions

2. **MIDI Sound System:**
   - Note to frequency mapping
   - Mock/simulation response for now
   - Future: WebAudio API integration

3. **Database:**
   - MongoDB collection: "chords"
   - Seed with comprehensive chord database
   - Efficient chord matching queries

4. **Frontend Integration:**
   - Replace mock calls with axios API calls
   - Handle loading states
   - Error handling for API failures
   - Maintain UI responsiveness

## Success Criteria

- [ ] Chord recognition API working with complex chords
- [ ] Frontend successfully integrated with backend APIs
- [ ] Mock data completely removed from frontend
- [ ] MIDI sound system prepared (simulation)
- [ ] All existing frontend functionality preserved
- [ ] Better accuracy than mock system (targeting >90% for exact matches)