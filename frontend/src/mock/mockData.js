// Mock data for chord recognition
const mockChordDatabase = [
  // Major chords
  { name: 'C Major', notes: ['C', 'E', 'G'], type: 'Majör Akor', structure: 'Root + Major 3rd + Perfect 5th' },
  { name: 'D Major', notes: ['D', 'F#', 'A'], type: 'Majör Akor', structure: 'Root + Major 3rd + Perfect 5th' },
  { name: 'E Major', notes: ['E', 'G#', 'B'], type: 'Majör Akor', structure: 'Root + Major 3rd + Perfect 5th' },
  { name: 'F Major', notes: ['F', 'A', 'C'], type: 'Majör Akor', structure: 'Root + Major 3rd + Perfect 5th' },
  { name: 'G Major', notes: ['G', 'B', 'D'], type: 'Majör Akor', structure: 'Root + Major 3rd + Perfect 5th' },
  { name: 'A Major', notes: ['A', 'C#', 'E'], type: 'Majör Akor', structure: 'Root + Major 3rd + Perfect 5th' },
  { name: 'B Major', notes: ['B', 'D#', 'F#'], type: 'Majör Akor', structure: 'Root + Major 3rd + Perfect 5th' },

  // Minor chords
  { name: 'A Minor', notes: ['A', 'C', 'E'], type: 'Minör Akor', structure: 'Root + Minor 3rd + Perfect 5th' },
  { name: 'D Minor', notes: ['D', 'F', 'A'], type: 'Minör Akor', structure: 'Root + Minor 3rd + Perfect 5th' },
  { name: 'E Minor', notes: ['E', 'G', 'B'], type: 'Minör Akor', structure: 'Root + Minor 3rd + Perfect 5th' },
  { name: 'F Minor', notes: ['F', 'G#', 'C'], type: 'Minör Akor', structure: 'Root + Minor 3rd + Perfect 5th' },
  { name: 'G Minor', notes: ['G', 'A#', 'D'], type: 'Minör Akor', structure: 'Root + Minor 3rd + Perfect 5th' },
  { name: 'B Minor', notes: ['B', 'D', 'F#'], type: 'Minör Akor', structure: 'Root + Minor 3rd + Perfect 5th' },
  { name: 'C Minor', notes: ['C', 'D#', 'G'], type: 'Minör Akor', structure: 'Root + Minor 3rd + Perfect 5th' },

  // 7th chords
  { name: 'C7', notes: ['C', 'E', 'G', 'A#'], type: 'Dominant 7th', structure: 'Root + Major 3rd + Perfect 5th + Minor 7th' },
  { name: 'D7', notes: ['D', 'F#', 'A', 'C'], type: 'Dominant 7th', structure: 'Root + Major 3rd + Perfect 5th + Minor 7th' },
  { name: 'E7', notes: ['E', 'G#', 'B', 'D'], type: 'Dominant 7th', structure: 'Root + Major 3rd + Perfect 5th + Minor 7th' },
  { name: 'G7', notes: ['G', 'B', 'D', 'F'], type: 'Dominant 7th', structure: 'Root + Major 3rd + Perfect 5th + Minor 7th' },
  { name: 'A7', notes: ['A', 'C#', 'E', 'G'], type: 'Dominant 7th', structure: 'Root + Major 3rd + Perfect 5th + Minor 7th' },

  // Major 7th chords
  { name: 'Cmaj7', notes: ['C', 'E', 'G', 'B'], type: 'Major 7th', structure: 'Root + Major 3rd + Perfect 5th + Major 7th' },
  { name: 'Dmaj7', notes: ['D', 'F#', 'A', 'C#'], type: 'Major 7th', structure: 'Root + Major 3rd + Perfect 5th + Major 7th' },
  { name: 'Gmaj7', notes: ['G', 'B', 'D', 'F#'], type: 'Major 7th', structure: 'Root + Major 3rd + Perfect 5th + Major 7th' },

  // Minor 7th chords
  { name: 'Am7', notes: ['A', 'C', 'E', 'G'], type: 'Minor 7th', structure: 'Root + Minor 3rd + Perfect 5th + Minor 7th' },
  { name: 'Dm7', notes: ['D', 'F', 'A', 'C'], type: 'Minor 7th', structure: 'Root + Minor 3rd + Perfect 5th + Minor 7th' },
  { name: 'Em7', notes: ['E', 'G', 'B', 'D'], type: 'Minor 7th', structure: 'Root + Minor 3rd + Perfect 5th + Minor 7th' },

  // Suspended chords
  { name: 'Csus2', notes: ['C', 'D', 'G'], type: 'Suspended 2nd', structure: 'Root + 2nd + Perfect 5th' },
  { name: 'Csus4', notes: ['C', 'F', 'G'], type: 'Suspended 4th', structure: 'Root + Perfect 4th + Perfect 5th' },
  { name: 'Dsus2', notes: ['D', 'E', 'A'], type: 'Suspended 2nd', structure: 'Root + 2nd + Perfect 5th' },
  { name: 'Dsus4', notes: ['D', 'G', 'A'], type: 'Suspended 4th', structure: 'Root + Perfect 4th + Perfect 5th' },

  // Add chords
  { name: 'Cadd9', notes: ['C', 'D', 'E', 'G'], type: 'Add 9th', structure: 'Root + Major 3rd + Perfect 5th + 9th' },
  { name: 'Gadd9', notes: ['G', 'A', 'B', 'D'], type: 'Add 9th', structure: 'Root + Major 3rd + Perfect 5th + 9th' },

  // Diminished chords
  { name: 'Cdim', notes: ['C', 'D#', 'F#'], type: 'Diminished', structure: 'Root + Minor 3rd + Diminished 5th' },
  { name: 'Ddim', notes: ['D', 'F', 'G#'], type: 'Diminished', structure: 'Root + Minor 3rd + Diminished 5th' },

  // Augmented chords
  { name: 'Caug', notes: ['C', 'E', 'G#'], type: 'Augmented', structure: 'Root + Major 3rd + Augmented 5th' },
  { name: 'Gaug', notes: ['G', 'B', 'D#'], type: 'Augmented', structure: 'Root + Major 3rd + Augmented 5th' },

  // 6th chords
  { name: 'C6', notes: ['C', 'E', 'G', 'A'], type: 'Major 6th', structure: 'Root + Major 3rd + Perfect 5th + Major 6th' },
  { name: 'Am6', notes: ['A', 'C', 'E', 'F#'], type: 'Minor 6th', structure: 'Root + Minor 3rd + Perfect 5th + Major 6th' },
];

const normalizeNote = (note) => {
  // Convert flats to sharps for consistency
  const noteMap = {
    'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#', 'Ab': 'G#', 'Bb': 'A#'
  };
  return noteMap[note] || note;
};

const calculateChordMatch = (inputNotes, chordNotes) => {
  const normalizedInput = inputNotes.map(normalizeNote);
  const normalizedChord = chordNotes.map(normalizeNote);
  
  const matchingNotes = normalizedInput.filter(note => normalizedChord.includes(note));
  const matchPercentage = Math.round((matchingNotes.length / normalizedChord.length) * 100);
  
  // Bonus for exact match
  const exactMatch = normalizedInput.length === normalizedChord.length && matchPercentage === 100;
  
  return {
    matchingNotes: matchingNotes.length,
    percentage: exactMatch ? 100 : Math.max(matchPercentage - (normalizedInput.length - normalizedChord.length) * 10, 0),
    isExactMatch: exactMatch
  };
};

const recognizeChords = (inputNotes) => {
  if (!inputNotes || inputNotes.length < 2) return [];
  
  const uniqueNotes = [...new Set(inputNotes.map(normalizeNote))];
  const matches = [];
  
  mockChordDatabase.forEach(chord => {
    const match = calculateChordMatch(uniqueNotes, chord.notes);
    
    if (match.matchingNotes >= 2 && match.percentage >= 50) {
      matches.push({
        name: chord.name,
        type: chord.type,
        structure: chord.structure,
        confidence: match.percentage,
        isExactMatch: match.isExactMatch,
        matchingNotes: match.matchingNotes,
        totalNotes: chord.notes.length
      });
    }
  });
  
  // Sort by confidence and prioritize exact matches
  return matches
    .sort((a, b) => {
      if (a.isExactMatch && !b.isExactMatch) return -1;
      if (!a.isExactMatch && b.isExactMatch) return 1;
      return b.confidence - a.confidence;
    })
    .slice(0, 5); // Return top 5 matches
};

const mockData = {
  recognizeChords,
  chordDatabase: mockChordDatabase
};

export default mockData;