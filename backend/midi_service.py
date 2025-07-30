from models import PlayNoteRequest, PlayNoteResponse
from typing import Dict
import asyncio
import logging

logger = logging.getLogger(__name__)

class MIDIService:
    def __init__(self):
        self.note_frequencies = self._initialize_note_frequencies()

    def _initialize_note_frequencies(self) -> Dict[str, float]:
        """Initialize note frequencies for MIDI simulation"""
        # A4 = 440Hz as reference
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        frequencies = {}
        
        # Calculate frequencies for different octaves
        for octave in range(0, 8):
            for i, note in enumerate(notes):
                # Calculate frequency using equal temperament formula
                # f = 440 * 2^((n-69)/12) where n is MIDI note number
                midi_number = octave * 12 + i
                frequency = 440.0 * (2 ** ((midi_number - 69) / 12))
                frequencies[f"{note}{octave}"] = round(frequency, 2)
        
        return frequencies

    async def play_note(self, request: PlayNoteRequest) -> PlayNoteResponse:
        """
        Simulate playing a MIDI note
        In a real implementation, this would interface with a MIDI library
        """
        note_key = f"{request.note}{request.octave}"
        
        if note_key not in self.note_frequencies:
            logger.warning(f"Note {note_key} not found in frequency table")
            return PlayNoteResponse(
                status="error",
                note=note_key,
                duration=request.duration
            )

        frequency = self.note_frequencies[note_key]
        
        # Simulate note playing duration
        await asyncio.sleep(0.1)  # Simulate processing time
        
        logger.info(f"Playing note: {note_key} at {frequency}Hz for {request.duration}ms")
        
        return PlayNoteResponse(
            status="playing",
            note=note_key,
            duration=request.duration
        )

    def get_note_info(self, note: str, octave: int = 4) -> Dict:
        """Get information about a specific note"""
        note_key = f"{note}{octave}"
        frequency = self.note_frequencies.get(note_key)
        
        return {
            "note": note_key,
            "frequency": frequency,
            "available": frequency is not None
        }