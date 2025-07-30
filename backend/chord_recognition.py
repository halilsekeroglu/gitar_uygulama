from typing import List, Set, Dict, Tuple
from models import RecognizedChord
import re

class ChordRecognitionEngine:
    def __init__(self):
        self.chord_database = self._initialize_chord_database()
        self.note_map = self._initialize_note_map()

    def _initialize_note_map(self) -> Dict[str, str]:
        """Convert flats to sharps for consistency"""
        return {
            'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#', 
            'Ab': 'G#', 'Bb': 'A#'
        }

    def _initialize_chord_database(self) -> List[Dict]:
        """Comprehensive chord database with basic and advanced chords"""
        return [
            # Major Chords
            {'name': 'C', 'notes': ['C', 'E', 'G'], 'type': 'Majör', 'structure': 'Root + Major 3rd + Perfect 5th', 'category': 'major'},
            {'name': 'C#', 'notes': ['C#', 'F', 'G#'], 'type': 'Majör', 'structure': 'Root + Major 3rd + Perfect 5th', 'category': 'major'},
            {'name': 'D', 'notes': ['D', 'F#', 'A'], 'type': 'Majör', 'structure': 'Root + Major 3rd + Perfect 5th', 'category': 'major'},
            {'name': 'D#', 'notes': ['D#', 'G', 'A#'], 'type': 'Majör', 'structure': 'Root + Major 3rd + Perfect 5th', 'category': 'major'},
            {'name': 'E', 'notes': ['E', 'G#', 'B'], 'type': 'Majör', 'structure': 'Root + Major 3rd + Perfect 5th', 'category': 'major'},
            {'name': 'F', 'notes': ['F', 'A', 'C'], 'type': 'Majör', 'structure': 'Root + Major 3rd + Perfect 5th', 'category': 'major'},
            {'name': 'F#', 'notes': ['F#', 'A#', 'C#'], 'type': 'Majör', 'structure': 'Root + Major 3rd + Perfect 5th', 'category': 'major'},
            {'name': 'G', 'notes': ['G', 'B', 'D'], 'type': 'Majör', 'structure': 'Root + Major 3rd + Perfect 5th', 'category': 'major'},
            {'name': 'G#', 'notes': ['G#', 'C', 'D#'], 'type': 'Majör', 'structure': 'Root + Major 3rd + Perfect 5th', 'category': 'major'},
            {'name': 'A', 'notes': ['A', 'C#', 'E'], 'type': 'Majör', 'structure': 'Root + Major 3rd + Perfect 5th', 'category': 'major'},
            {'name': 'A#', 'notes': ['A#', 'D', 'F'], 'type': 'Majör', 'structure': 'Root + Major 3rd + Perfect 5th', 'category': 'major'},
            {'name': 'B', 'notes': ['B', 'D#', 'F#'], 'type': 'Majör', 'structure': 'Root + Major 3rd + Perfect 5th', 'category': 'major'},

            # Minor Chords
            {'name': 'Am', 'notes': ['A', 'C', 'E'], 'type': 'Minör', 'structure': 'Root + Minor 3rd + Perfect 5th', 'category': 'minor'},
            {'name': 'A#m', 'notes': ['A#', 'C#', 'F'], 'type': 'Minör', 'structure': 'Root + Minor 3rd + Perfect 5th', 'category': 'minor'},
            {'name': 'Bm', 'notes': ['B', 'D', 'F#'], 'type': 'Minör', 'structure': 'Root + Minor 3rd + Perfect 5th', 'category': 'minor'},
            {'name': 'Cm', 'notes': ['C', 'D#', 'G'], 'type': 'Minör', 'structure': 'Root + Minor 3rd + Perfect 5th', 'category': 'minor'},
            {'name': 'C#m', 'notes': ['C#', 'E', 'G#'], 'type': 'Minör', 'structure': 'Root + Minor 3rd + Perfect 5th', 'category': 'minor'},
            {'name': 'Dm', 'notes': ['D', 'F', 'A'], 'type': 'Minör', 'structure': 'Root + Minor 3rd + Perfect 5th', 'category': 'minor'},
            {'name': 'D#m', 'notes': ['D#', 'F#', 'A#'], 'type': 'Minör', 'structure': 'Root + Minor 3rd + Perfect 5th', 'category': 'minor'},
            {'name': 'Em', 'notes': ['E', 'G', 'B'], 'type': 'Minör', 'structure': 'Root + Minor 3rd + Perfect 5th', 'category': 'minor'},
            {'name': 'Fm', 'notes': ['F', 'G#', 'C'], 'type': 'Minör', 'structure': 'Root + Minor 3rd + Perfect 5th', 'category': 'minor'},
            {'name': 'F#m', 'notes': ['F#', 'A', 'C#'], 'type': 'Minör', 'structure': 'Root + Minor 3rd + Perfect 5th', 'category': 'minor'},
            {'name': 'Gm', 'notes': ['G', 'A#', 'D'], 'type': 'Minör', 'structure': 'Root + Minor 3rd + Perfect 5th', 'category': 'minor'},
            {'name': 'G#m', 'notes': ['G#', 'B', 'D#'], 'type': 'Minör', 'structure': 'Root + Minor 3rd + Perfect 5th', 'category': 'minor'},

            # Dominant 7th Chords
            {'name': 'C7', 'notes': ['C', 'E', 'G', 'A#'], 'type': 'Dominant 7th', 'structure': 'Root + Major 3rd + Perfect 5th + Minor 7th', 'category': 'seventh'},
            {'name': 'D7', 'notes': ['D', 'F#', 'A', 'C'], 'type': 'Dominant 7th', 'structure': 'Root + Major 3rd + Perfect 5th + Minor 7th', 'category': 'seventh'},
            {'name': 'E7', 'notes': ['E', 'G#', 'B', 'D'], 'type': 'Dominant 7th', 'structure': 'Root + Major 3rd + Perfect 5th + Minor 7th', 'category': 'seventh'},
            {'name': 'F7', 'notes': ['F', 'A', 'C', 'D#'], 'type': 'Dominant 7th', 'structure': 'Root + Major 3rd + Perfect 5th + Minor 7th', 'category': 'seventh'},
            {'name': 'G7', 'notes': ['G', 'B', 'D', 'F'], 'type': 'Dominant 7th', 'structure': 'Root + Major 3rd + Perfect 5th + Minor 7th', 'category': 'seventh'},
            {'name': 'A7', 'notes': ['A', 'C#', 'E', 'G'], 'type': 'Dominant 7th', 'structure': 'Root + Major 3rd + Perfect 5th + Minor 7th', 'category': 'seventh'},
            {'name': 'B7', 'notes': ['B', 'D#', 'F#', 'A'], 'type': 'Dominant 7th', 'structure': 'Root + Major 3rd + Perfect 5th + Minor 7th', 'category': 'seventh'},

            # Major 7th Chords
            {'name': 'Cmaj7', 'notes': ['C', 'E', 'G', 'B'], 'type': 'Major 7th', 'structure': 'Root + Major 3rd + Perfect 5th + Major 7th', 'category': 'seventh'},
            {'name': 'Dmaj7', 'notes': ['D', 'F#', 'A', 'C#'], 'type': 'Major 7th', 'structure': 'Root + Major 3rd + Perfect 5th + Major 7th', 'category': 'seventh'},
            {'name': 'Emaj7', 'notes': ['E', 'G#', 'B', 'D#'], 'type': 'Major 7th', 'structure': 'Root + Major 3rd + Perfect 5th + Major 7th', 'category': 'seventh'},
            {'name': 'Fmaj7', 'notes': ['F', 'A', 'C', 'E'], 'type': 'Major 7th', 'structure': 'Root + Major 3rd + Perfect 5th + Major 7th', 'category': 'seventh'},
            {'name': 'Gmaj7', 'notes': ['G', 'B', 'D', 'F#'], 'type': 'Major 7th', 'structure': 'Root + Major 3rd + Perfect 5th + Major 7th', 'category': 'seventh'},
            {'name': 'Amaj7', 'notes': ['A', 'C#', 'E', 'G#'], 'type': 'Major 7th', 'structure': 'Root + Major 3rd + Perfect 5th + Major 7th', 'category': 'seventh'},
            {'name': 'Bmaj7', 'notes': ['B', 'D#', 'F#', 'A#'], 'type': 'Major 7th', 'structure': 'Root + Major 3rd + Perfect 5th + Major 7th', 'category': 'seventh'},

            # Minor 7th Chords
            {'name': 'Am7', 'notes': ['A', 'C', 'E', 'G'], 'type': 'Minor 7th', 'structure': 'Root + Minor 3rd + Perfect 5th + Minor 7th', 'category': 'seventh'},
            {'name': 'Bm7', 'notes': ['B', 'D', 'F#', 'A'], 'type': 'Minor 7th', 'structure': 'Root + Minor 3rd + Perfect 5th + Minor 7th', 'category': 'seventh'},
            {'name': 'Cm7', 'notes': ['C', 'D#', 'G', 'A#'], 'type': 'Minor 7th', 'structure': 'Root + Minor 3rd + Perfect 5th + Minor 7th', 'category': 'seventh'},
            {'name': 'Dm7', 'notes': ['D', 'F', 'A', 'C'], 'type': 'Minor 7th', 'structure': 'Root + Minor 3rd + Perfect 5th + Minor 7th', 'category': 'seventh'},
            {'name': 'Em7', 'notes': ['E', 'G', 'B', 'D'], 'type': 'Minor 7th', 'structure': 'Root + Minor 3rd + Perfect 5th + Minor 7th', 'category': 'seventh'},
            {'name': 'Fm7', 'notes': ['F', 'G#', 'C', 'D#'], 'type': 'Minor 7th', 'structure': 'Root + Minor 3rd + Perfect 5th + Minor 7th', 'category': 'seventh'},
            {'name': 'Gm7', 'notes': ['G', 'A#', 'D', 'F'], 'type': 'Minor 7th', 'structure': 'Root + Minor 3rd + Perfect 5th + Minor 7th', 'category': 'seventh'},

            # Suspended Chords
            {'name': 'Csus2', 'notes': ['C', 'D', 'G'], 'type': 'Suspended 2nd', 'structure': 'Root + 2nd + Perfect 5th', 'category': 'suspended'},
            {'name': 'Csus4', 'notes': ['C', 'F', 'G'], 'type': 'Suspended 4th', 'structure': 'Root + Perfect 4th + Perfect 5th', 'category': 'suspended'},
            {'name': 'Dsus2', 'notes': ['D', 'E', 'A'], 'type': 'Suspended 2nd', 'structure': 'Root + 2nd + Perfect 5th', 'category': 'suspended'},
            {'name': 'Dsus4', 'notes': ['D', 'G', 'A'], 'type': 'Suspended 4th', 'structure': 'Root + Perfect 4th + Perfect 5th', 'category': 'suspended'},
            {'name': 'Esus2', 'notes': ['E', 'F#', 'B'], 'type': 'Suspended 2nd', 'structure': 'Root + 2nd + Perfect 5th', 'category': 'suspended'},
            {'name': 'Esus4', 'notes': ['E', 'A', 'B'], 'type': 'Suspended 4th', 'structure': 'Root + Perfect 4th + Perfect 5th', 'category': 'suspended'},
            {'name': 'Fsus2', 'notes': ['F', 'G', 'C'], 'type': 'Suspended 2nd', 'structure': 'Root + 2nd + Perfect 5th', 'category': 'suspended'},
            {'name': 'Fsus4', 'notes': ['F', 'A#', 'C'], 'type': 'Suspended 4th', 'structure': 'Root + Perfect 4th + Perfect 5th', 'category': 'suspended'},
            {'name': 'Gsus2', 'notes': ['G', 'A', 'D'], 'type': 'Suspended 2nd', 'structure': 'Root + 2nd + Perfect 5th', 'category': 'suspended'},
            {'name': 'Gsus4', 'notes': ['G', 'C', 'D'], 'type': 'Suspended 4th', 'structure': 'Root + Perfect 4th + Perfect 5th', 'category': 'suspended'},
            {'name': 'Asus2', 'notes': ['A', 'B', 'E'], 'type': 'Suspended 2nd', 'structure': 'Root + 2nd + Perfect 5th', 'category': 'suspended'},
            {'name': 'Asus4', 'notes': ['A', 'D', 'E'], 'type': 'Suspended 4th', 'structure': 'Root + Perfect 4th + Perfect 5th', 'category': 'suspended'},

            # Add Chords
            {'name': 'Cadd9', 'notes': ['C', 'D', 'E', 'G'], 'type': 'Add 9th', 'structure': 'Root + Major 3rd + Perfect 5th + 9th', 'category': 'add'},
            {'name': 'Dadd9', 'notes': ['D', 'E', 'F#', 'A'], 'type': 'Add 9th', 'structure': 'Root + Major 3rd + Perfect 5th + 9th', 'category': 'add'},
            {'name': 'Gadd9', 'notes': ['G', 'A', 'B', 'D'], 'type': 'Add 9th', 'structure': 'Root + Major 3rd + Perfect 5th + 9th', 'category': 'add'},

            # Diminished Chords
            {'name': 'Cdim', 'notes': ['C', 'D#', 'F#'], 'type': 'Diminished', 'structure': 'Root + Minor 3rd + Diminished 5th', 'category': 'diminished'},
            {'name': 'C#dim', 'notes': ['C#', 'E', 'G'], 'type': 'Diminished', 'structure': 'Root + Minor 3rd + Diminished 5th', 'category': 'diminished'},
            {'name': 'Ddim', 'notes': ['D', 'F', 'G#'], 'type': 'Diminished', 'structure': 'Root + Minor 3rd + Diminished 5th', 'category': 'diminished'},
            {'name': 'D#dim', 'notes': ['D#', 'F#', 'A'], 'type': 'Diminished', 'structure': 'Root + Minor 3rd + Diminished 5th', 'category': 'diminished'},
            {'name': 'Edim', 'notes': ['E', 'G', 'A#'], 'type': 'Diminished', 'structure': 'Root + Minor 3rd + Diminished 5th', 'category': 'diminished'},
            {'name': 'Fdim', 'notes': ['F', 'G#', 'B'], 'type': 'Diminished', 'structure': 'Root + Minor 3rd + Diminished 5th', 'category': 'diminished'},
            {'name': 'F#dim', 'notes': ['F#', 'A', 'C'], 'type': 'Diminished', 'structure': 'Root + Minor 3rd + Diminished 5th', 'category': 'diminished'},
            {'name': 'Gdim', 'notes': ['G', 'A#', 'C#'], 'type': 'Diminished', 'structure': 'Root + Minor 3rd + Diminished 5th', 'category': 'diminished'},
            {'name': 'G#dim', 'notes': ['G#', 'B', 'D'], 'type': 'Diminished', 'structure': 'Root + Minor 3rd + Diminished 5th', 'category': 'diminished'},
            {'name': 'Adim', 'notes': ['A', 'C', 'D#'], 'type': 'Diminished', 'structure': 'Root + Minor 3rd + Diminished 5th', 'category': 'diminished'},
            {'name': 'A#dim', 'notes': ['A#', 'C#', 'E'], 'type': 'Diminished', 'structure': 'Root + Minor 3rd + Diminished 5th', 'category': 'diminished'},
            {'name': 'Bdim', 'notes': ['B', 'D', 'F'], 'type': 'Diminished', 'structure': 'Root + Minor 3rd + Diminished 5th', 'category': 'diminished'},

            # Augmented Chords
            {'name': 'Caug', 'notes': ['C', 'E', 'G#'], 'type': 'Augmented', 'structure': 'Root + Major 3rd + Augmented 5th', 'category': 'augmented'},
            {'name': 'C#aug', 'notes': ['C#', 'F', 'A'], 'type': 'Augmented', 'structure': 'Root + Major 3rd + Augmented 5th', 'category': 'augmented'},
            {'name': 'Daug', 'notes': ['D', 'F#', 'A#'], 'type': 'Augmented', 'structure': 'Root + Major 3rd + Augmented 5th', 'category': 'augmented'},
            {'name': 'D#aug', 'notes': ['D#', 'G', 'B'], 'type': 'Augmented', 'structure': 'Root + Major 3rd + Augmented 5th', 'category': 'augmented'},
            {'name': 'Eaug', 'notes': ['E', 'G#', 'C'], 'type': 'Augmented', 'structure': 'Root + Major 3rd + Augmented 5th', 'category': 'augmented'},
            {'name': 'Faug', 'notes': ['F', 'A', 'C#'], 'type': 'Augmented', 'structure': 'Root + Major 3rd + Augmented 5th', 'category': 'augmented'},
            {'name': 'F#aug', 'notes': ['F#', 'A#', 'D'], 'type': 'Augmented', 'structure': 'Root + Major 3rd + Augmented 5th', 'category': 'augmented'},
            {'name': 'Gaug', 'notes': ['G', 'B', 'D#'], 'type': 'Augmented', 'structure': 'Root + Major 3rd + Augmented 5th', 'category': 'augmented'},
            {'name': 'G#aug', 'notes': ['G#', 'C', 'E'], 'type': 'Augmented', 'structure': 'Root + Major 3rd + Augmented 5th', 'category': 'augmented'},
            {'name': 'Aaug', 'notes': ['A', 'C#', 'F'], 'type': 'Augmented', 'structure': 'Root + Major 3rd + Augmented 5th', 'category': 'augmented'},
            {'name': 'A#aug', 'notes': ['A#', 'D', 'F#'], 'type': 'Augmented', 'structure': 'Root + Major 3rd + Augmented 5th', 'category': 'augmented'},
            {'name': 'Baug', 'notes': ['B', 'D#', 'G'], 'type': 'Augmented', 'structure': 'Root + Major 3rd + Augmented 5th', 'category': 'augmented'},

            # 6th Chords
            {'name': 'C6', 'notes': ['C', 'E', 'G', 'A'], 'type': 'Major 6th', 'structure': 'Root + Major 3rd + Perfect 5th + Major 6th', 'category': 'sixth'},
            {'name': 'D6', 'notes': ['D', 'F#', 'A', 'B'], 'type': 'Major 6th', 'structure': 'Root + Major 3rd + Perfect 5th + Major 6th', 'category': 'sixth'},
            {'name': 'E6', 'notes': ['E', 'G#', 'B', 'C#'], 'type': 'Major 6th', 'structure': 'Root + Major 3rd + Perfect 5th + Major 6th', 'category': 'sixth'},
            {'name': 'F6', 'notes': ['F', 'A', 'C', 'D'], 'type': 'Major 6th', 'structure': 'Root + Major 3rd + Perfect 5th + Major 6th', 'category': 'sixth'},
            {'name': 'G6', 'notes': ['G', 'B', 'D', 'E'], 'type': 'Major 6th', 'structure': 'Root + Major 3rd + Perfect 5th + Major 6th', 'category': 'sixth'},
            {'name': 'A6', 'notes': ['A', 'C#', 'E', 'F#'], 'type': 'Major 6th', 'structure': 'Root + Major 3rd + Perfect 5th + Major 6th', 'category': 'sixth'},

            # Minor 6th Chords
            {'name': 'Am6', 'notes': ['A', 'C', 'E', 'F#'], 'type': 'Minor 6th', 'structure': 'Root + Minor 3rd + Perfect 5th + Major 6th', 'category': 'sixth'},
            {'name': 'Bm6', 'notes': ['B', 'D', 'F#', 'G#'], 'type': 'Minor 6th', 'structure': 'Root + Minor 3rd + Perfect 5th + Major 6th', 'category': 'sixth'},
            {'name': 'Cm6', 'notes': ['C', 'D#', 'G', 'A'], 'type': 'Minor 6th', 'structure': 'Root + Minor 3rd + Perfect 5th + Major 6th', 'category': 'sixth'},
            {'name': 'Dm6', 'notes': ['D', 'F', 'A', 'B'], 'type': 'Minor 6th', 'structure': 'Root + Minor 3rd + Perfect 5th + Major 6th', 'category': 'sixth'},
            {'name': 'Em6', 'notes': ['E', 'G', 'B', 'C#'], 'type': 'Minor 6th', 'structure': 'Root + Minor 3rd + Perfect 5th + Major 6th', 'category': 'sixth'},
            {'name': 'Fm6', 'notes': ['F', 'G#', 'C', 'D'], 'type': 'Minor 6th', 'structure': 'Root + Minor 3rd + Perfect 5th + Major 6th', 'category': 'sixth'},

            # 9th Chords (Major)
            {'name': 'C9', 'notes': ['C', 'E', 'G', 'A#', 'D'], 'type': '9th', 'structure': 'Root + Major 3rd + Perfect 5th + Minor 7th + 9th', 'category': 'ninth'},
            {'name': 'D9', 'notes': ['D', 'F#', 'A', 'C', 'E'], 'type': '9th', 'structure': 'Root + Major 3rd + Perfect 5th + Minor 7th + 9th', 'category': 'ninth'},
            {'name': 'E9', 'notes': ['E', 'G#', 'B', 'D', 'F#'], 'type': '9th', 'structure': 'Root + Major 3rd + Perfect 5th + Minor 7th + 9th', 'category': 'ninth'},
            {'name': 'F9', 'notes': ['F', 'A', 'C', 'D#', 'G'], 'type': '9th', 'structure': 'Root + Major 3rd + Perfect 5th + Minor 7th + 9th', 'category': 'ninth'},
            {'name': 'G9', 'notes': ['G', 'B', 'D', 'F', 'A'], 'type': '9th', 'structure': 'Root + Major 3rd + Perfect 5th + Minor 7th + 9th', 'category': 'ninth'},
            {'name': 'A9', 'notes': ['A', 'C#', 'E', 'G', 'B'], 'type': '9th', 'structure': 'Root + Major 3rd + Perfect 5th + Minor 7th + 9th', 'category': 'ninth'},
            {'name': 'B9', 'notes': ['B', 'D#', 'F#', 'A', 'C#'], 'type': '9th', 'structure': 'Root + Major 3rd + Perfect 5th + Minor 7th + 9th', 'category': 'ninth'},

            # Minor 9th Chords
            {'name': 'Am9', 'notes': ['A', 'C', 'E', 'G', 'B'], 'type': 'Minor 9th', 'structure': 'Root + Minor 3rd + Perfect 5th + Minor 7th + 9th', 'category': 'ninth'},
            {'name': 'Bm9', 'notes': ['B', 'D', 'F#', 'A', 'C#'], 'type': 'Minor 9th', 'structure': 'Root + Minor 3rd + Perfect 5th + Minor 7th + 9th', 'category': 'ninth'},
            {'name': 'Cm9', 'notes': ['C', 'D#', 'G', 'A#', 'D'], 'type': 'Minor 9th', 'structure': 'Root + Minor 3rd + Perfect 5th + Minor 7th + 9th', 'category': 'ninth'},
            {'name': 'Dm9', 'notes': ['D', 'F', 'A', 'C', 'E'], 'type': 'Minor 9th', 'structure': 'Root + Minor 3rd + Perfect 5th + Minor 7th + 9th', 'category': 'ninth'},
            {'name': 'Em9', 'notes': ['E', 'G', 'B', 'D', 'F#'], 'type': 'Minor 9th', 'structure': 'Root + Minor 3rd + Perfect 5th + Minor 7th + 9th', 'category': 'ninth'},
            {'name': 'Fm9', 'notes': ['F', 'G#', 'C', 'D#', 'G'], 'type': 'Minor 9th', 'structure': 'Root + Minor 3rd + Perfect 5th + Minor 7th + 9th', 'category': 'ninth'},
            {'name': 'Gm9', 'notes': ['G', 'A#', 'D', 'F', 'A'], 'type': 'Minor 9th', 'structure': 'Root + Minor 3rd + Perfect 5th + Minor 7th + 9th', 'category': 'ninth'},

            # Major 9th Chords
            {'name': 'Cmaj9', 'notes': ['C', 'E', 'G', 'B', 'D'], 'type': 'Major 9th', 'structure': 'Root + Major 3rd + Perfect 5th + Major 7th + 9th', 'category': 'ninth'},
            {'name': 'Dmaj9', 'notes': ['D', 'F#', 'A', 'C#', 'E'], 'type': 'Major 9th', 'structure': 'Root + Major 3rd + Perfect 5th + Major 7th + 9th', 'category': 'ninth'},
            {'name': 'Emaj9', 'notes': ['E', 'G#', 'B', 'D#', 'F#'], 'type': 'Major 9th', 'structure': 'Root + Major 3rd + Perfect 5th + Major 7th + 9th', 'category': 'ninth'},
            {'name': 'Fmaj9', 'notes': ['F', 'A', 'C', 'E', 'G'], 'type': 'Major 9th', 'structure': 'Root + Major 3rd + Perfect 5th + Major 7th + 9th', 'category': 'ninth'},
            {'name': 'Gmaj9', 'notes': ['G', 'B', 'D', 'F#', 'A'], 'type': 'Major 9th', 'structure': 'Root + Major 3rd + Perfect 5th + Major 7th + 9th', 'category': 'ninth'},
            {'name': 'Amaj9', 'notes': ['A', 'C#', 'E', 'G#', 'B'], 'type': 'Major 9th', 'structure': 'Root + Major 3rd + Perfect 5th + Major 7th + 9th', 'category': 'ninth'},
            {'name': 'Bmaj9', 'notes': ['B', 'D#', 'F#', 'A#', 'C#'], 'type': 'Major 9th', 'structure': 'Root + Major 3rd + Perfect 5th + Major 7th + 9th', 'category': 'ninth'},
        ]

    def normalize_note(self, note: str) -> str:
        """Convert flats to sharps for consistency"""
        return self.note_map.get(note, note)

    def calculate_chord_match(self, input_notes: List[str], chord_notes: List[str]) -> Dict:
        """Calculate how well input notes match a chord"""
        normalized_input = [self.normalize_note(note) for note in input_notes]
        normalized_chord = [self.normalize_note(note) for note in chord_notes]
        
        # Remove duplicates while preserving order
        unique_input = list(dict.fromkeys(normalized_input))
        unique_chord = list(dict.fromkeys(normalized_chord))
        
        matching_notes = [note for note in unique_input if note in unique_chord]
        match_percentage = len(matching_notes) / len(unique_chord) * 100 if unique_chord else 0
        
        # Bonus for exact match
        exact_match = len(unique_input) == len(unique_chord) and match_percentage == 100
        
        # Penalty for extra notes
        extra_notes_penalty = max(0, (len(unique_input) - len(unique_chord)) * 15)
        final_percentage = max(0, match_percentage - extra_notes_penalty)
        
        return {
            'matching_notes': len(matching_notes),
            'percentage': 100 if exact_match else int(final_percentage),
            'is_exact_match': exact_match,
            'extra_notes': len(unique_input) - len(matching_notes)
        }

    def recognize_chords(self, input_notes: List[str]) -> List[RecognizedChord]:
        """Main chord recognition function"""
        if not input_notes or len(input_notes) < 2:
            return []
        
        unique_notes = list(dict.fromkeys([self.normalize_note(note) for note in input_notes]))
        matches = []
        
        for chord in self.chord_database:
            match = self.calculate_chord_match(unique_notes, chord['notes'])
            
            # Only include matches with significant confidence
            if match['matching_notes'] >= 2 and match['percentage'] >= 60:
                recognized_chord = RecognizedChord(
                    name=chord['name'],
                    type=chord['type'],
                    structure=chord['structure'],
                    confidence=match['percentage'],
                    notes=chord['notes'],
                    is_exact_match=match['is_exact_match'],
                    category=chord['category']
                )
                matches.append(recognized_chord)
        
        # Sort by confidence, prioritizing exact matches
        matches.sort(key=lambda x: (-int(x.is_exact_match), -x.confidence))
        
        # Return top 6 matches
        return matches[:6]