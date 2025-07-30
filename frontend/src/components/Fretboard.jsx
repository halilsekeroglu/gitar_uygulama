import React, { useState, useEffect } from 'react';
import { Volume2, VolumeX } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import mockData from '../mock/mockData';

const Fretboard = () => {
  const [selectedNotes, setSelectedNotes] = useState([]);
  const [soundEnabled, setSoundEnabled] = useState(true);
  const [recognizedChords, setRecognizedChords] = useState([]);

  // Guitar strings in standard tuning (from low E to high E)
  const strings = [
    { name: 'E', baseNote: 4, octave: 2 }, // Low E
    { name: 'A', baseNote: 9, octave: 2 }, // A
    { name: 'D', baseNote: 2, octave: 3 }, // D
    { name: 'G', baseNote: 7, octave: 3 }, // G
    { name: 'B', baseNote: 11, octave: 3 }, // B
    { name: 'E', baseNote: 4, octave: 4 } // High E
  ];

  const noteNames = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
  const frets = Array.from({ length: 25 }, (_, i) => i); // 0-24 frets

  const getNoteAtFret = (stringIndex, fret) => {
    const string = strings[stringIndex];
    const noteIndex = (string.baseNote + fret) % 12;
    return noteNames[noteIndex];
  };

  const handleFretClick = (stringIndex, fret) => {
    const note = getNoteAtFret(stringIndex, fret);
    const noteId = `${stringIndex}-${fret}`;
    
    // Play sound if enabled (mock)
    if (soundEnabled) {
      console.log(`Playing note: ${note}`);
      // Mock MIDI sound - will be replaced with actual implementation
    }

    setSelectedNotes(prev => {
      const isSelected = prev.some(n => n.id === noteId);
      if (isSelected) {
        return prev.filter(n => n.id !== noteId);
      } else {
        return [...prev, { id: noteId, note, string: stringIndex, fret }];
      }
    });
  };

  const isNoteSelected = (stringIndex, fret) => {
    return selectedNotes.some(n => n.id === `${stringIndex}-${fret}`);
  };

  const clearSelection = () => {
    setSelectedNotes([]);
    setRecognizedChords([]);
  };

  // Chord recognition with mock data
  useEffect(() => {
    if (selectedNotes.length >= 2) {
      const notesList = selectedNotes.map(n => n.note);
      const chords = mockData.recognizeChords(notesList);
      setRecognizedChords(chords);
    } else {
      setRecognizedChords([]);
    }
  }, [selectedNotes]);

  const getFretMarkers = (fret) => {
    const markerFrets = [3, 5, 7, 9, 15, 17, 19, 21];
    const doubleMarkerFrets = [12, 24];
    
    if (doubleMarkerFrets.includes(fret)) {
      return 'double-marker';
    } else if (markerFrets.includes(fret)) {
      return 'single-marker';
    }
    return '';
  };

  return (
    <div className="w-full max-w-7xl mx-auto p-4 bg-gradient-to-b from-amber-50 to-amber-100 min-h-screen">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-amber-900 mb-2">🎸 Gitar Fretboard Akor Tanıma</h1>
        <p className="text-amber-700">Perdeler üzerine tıklayarak akor oluşturun</p>
      </div>

      {/* Controls */}
      <div className="flex justify-between items-center mb-6">
        <Button
          onClick={() => setSoundEnabled(!soundEnabled)}
          variant="outline"
          className="flex items-center gap-2 bg-amber-800 text-white hover:bg-amber-700"
        >
          {soundEnabled ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
          Ses {soundEnabled ? 'Açık' : 'Kapalı'}
        </Button>

        <Button 
          onClick={clearSelection}
          variant="outline"
          className="bg-red-600 text-white hover:bg-red-700"
          disabled={selectedNotes.length === 0}
        >
          Temizle
        </Button>
      </div>

      {/* Fretboard */}
      <Card className="p-6 bg-gradient-to-r from-amber-900 via-amber-800 to-amber-900 shadow-2xl border-amber-600">
        <div className="relative">
          {/* Fret numbers */}
          <div className="flex mb-4">
            <div className="w-16"></div> {/* String names column */}
            {frets.map(fret => (
              <div key={fret} className="flex-1 text-center text-xs text-amber-200 font-semibold min-w-[40px]">
                {fret}
              </div>
            ))}
          </div>

          {/* Strings and frets */}
          <div className="space-y-3">
            {strings.map((string, stringIndex) => (
              <div key={stringIndex} className="flex items-center relative">
                {/* String name */}
                <div className="w-16 text-right pr-4 font-bold text-amber-100 text-lg">
                  {string.name}
                </div>

                {/* String line and frets */}
                <div className="flex-1 relative flex">
                  {/* String line */}
                  <div 
                    className="absolute top-1/2 left-0 right-0 transform -translate-y-1/2 bg-gradient-to-r from-gray-400 to-gray-300"
                    style={{ height: `${6 - stringIndex}px` }}
                  ></div>

                  {/* Frets */}
                  {frets.map(fret => (
                    <div key={fret} className="flex-1 relative min-w-[40px] h-10">
                      {/* Fret markers */}
                      {stringIndex === 2 && ( // Show markers on middle string
                        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
                          {getFretMarkers(fret) === 'double-marker' && (
                            <div className="flex flex-col space-y-1">
                              <div className="w-2 h-2 bg-amber-200 rounded-full opacity-60"></div>
                              <div className="w-2 h-2 bg-amber-200 rounded-full opacity-60"></div>
                            </div>
                          )}
                          {getFretMarkers(fret) === 'single-marker' && (
                            <div className="w-3 h-3 bg-amber-200 rounded-full opacity-60"></div>
                          )}
                        </div>
                      )}

                      {/* Fret wire */}
                      {fret > 0 && (
                        <div className="absolute left-0 top-0 bottom-0 w-0.5 bg-gray-600"></div>
                      )}

                      {/* Clickable area */}
                      <button
                        onClick={() => handleFretClick(stringIndex, fret)}
                        className={`absolute inset-0 rounded-full m-1 transition-all duration-200 hover:scale-110 ${
                          isNoteSelected(stringIndex, fret)
                            ? 'bg-yellow-400 shadow-lg shadow-yellow-400/50 border-2 border-yellow-300'
                            : 'hover:bg-amber-600/30'
                        }`}
                        title={`${string.name} - Perde ${fret} - ${getNoteAtFret(stringIndex, fret)}`}
                      >
                        {isNoteSelected(stringIndex, fret) && (
                          <span className="absolute inset-0 flex items-center justify-center text-xs font-bold text-amber-900">
                            {getNoteAtFret(stringIndex, fret)}
                          </span>
                        )}
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </Card>

      {/* Selected Notes and Chord Recognition */}
      <div className="grid md:grid-cols-2 gap-6 mt-6">
        {/* Selected Notes */}
        <Card className="p-6 bg-white shadow-lg border-amber-200">
          <h3 className="text-xl font-bold text-amber-900 mb-4">Seçilen Notalar</h3>
          {selectedNotes.length === 0 ? (
            <p className="text-gray-500 italic">Henüz nota seçilmedi</p>
          ) : (
            <div className="space-y-2">
              <div className="flex flex-wrap gap-2">
                {[...new Set(selectedNotes.map(n => n.note))].map(note => (
                  <span key={note} className="px-3 py-1 bg-amber-100 text-amber-800 rounded-full font-semibold">
                    {note}
                  </span>
                ))}
              </div>
              <p className="text-sm text-gray-600 mt-2">
                Toplam {selectedNotes.length} perde seçildi
              </p>
            </div>
          )}
        </Card>

        {/* Chord Recognition */}
        <Card className="p-6 bg-white shadow-lg border-amber-200">
          <h3 className="text-xl font-bold text-amber-900 mb-4">Tanınan Akorlar</h3>
          {recognizedChords.length === 0 ? (
            <p className="text-gray-500 italic">
              {selectedNotes.length < 2 ? 'En az 2 nota seçin' : 'Akor analiz ediliyor...'}
            </p>
          ) : (
            <div className="space-y-3">
              {recognizedChords.map((chord, index) => (
                <div key={index} className="border border-amber-200 rounded-lg p-3">
                  <div className="flex justify-between items-start">
                    <div>
                      <h4 className="font-bold text-lg text-amber-800">{chord.name}</h4>
                      <p className="text-sm text-gray-600">{chord.type}</p>
                    </div>
                    <div className="bg-amber-100 px-2 py-1 rounded text-xs font-semibold text-amber-700">
                      %{chord.confidence} eşleşme
                    </div>
                  </div>
                  <div className="mt-2">
                    <p className="text-xs text-gray-500">Yapı: {chord.structure}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};

export default Fretboard;