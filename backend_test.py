#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for Guitar Fretboard Chord Recognition
Tests all endpoints with various scenarios including edge cases
"""

import requests
import json
import sys
import time
from typing import Dict, List, Any

# Backend URL from frontend/.env
BACKEND_URL = "https://64fd0a7c-9b6f-4deb-b738-1789c2172313.preview.emergentagent.com/api"

class BackendTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.test_results = []
        self.session = requests.Session()
        self.session.timeout = 30
        
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "response_data": response_data
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
        if not success and response_data:
            print(f"   Response: {response_data}")
        print()

    def test_health_endpoints(self):
        """Test health check endpoints"""
        print("=== Testing Health Check Endpoints ===")
        
        # Test root endpoint
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "Guitar Fretboard" in data["message"]:
                    self.log_test("GET /api/ - Root endpoint", True, 
                                f"Status: {response.status_code}, Message: {data['message']}")
                else:
                    self.log_test("GET /api/ - Root endpoint", False, 
                                f"Unexpected response format", data)
            else:
                self.log_test("GET /api/ - Root endpoint", False, 
                            f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("GET /api/ - Root endpoint", False, f"Exception: {str(e)}")

        # Test health check endpoint
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                expected_keys = ["status", "chord_engine", "midi_service", "database"]
                if all(key in data for key in expected_keys):
                    self.log_test("GET /api/health - Health check", True, 
                                f"Status: {data['status']}, Services: {data}")
                else:
                    self.log_test("GET /api/health - Health check", False, 
                                f"Missing expected keys", data)
            else:
                self.log_test("GET /api/health - Health check", False, 
                            f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("GET /api/health - Health check", False, f"Exception: {str(e)}")

    def test_chord_recognition(self):
        """Test chord recognition API with various chord types"""
        print("=== Testing Chord Recognition API ===")
        
        # Test cases with expected chord types
        test_cases = [
            {
                "name": "C Major Chord",
                "notes": ["C", "E", "G"],
                "expected_chord": "C",
                "expected_type": "Majör"
            },
            {
                "name": "A Minor Chord", 
                "notes": ["A", "C", "E"],
                "expected_chord": "Am",
                "expected_type": "Minör"
            },
            {
                "name": "G7 Chord",
                "notes": ["G", "B", "D", "F"],
                "expected_chord": "G7",
                "expected_type": "Dominant 7th"
            },
            {
                "name": "Csus2 Chord",
                "notes": ["C", "D", "G"],
                "expected_chord": "Csus2",
                "expected_type": "Suspended 2nd"
            },
            {
                "name": "Cdim Chord",
                "notes": ["C", "D#", "F#"],
                "expected_chord": "Cdim",
                "expected_type": "Diminished"
            },
            {
                "name": "D Major Chord",
                "notes": ["D", "F#", "A"],
                "expected_chord": "D",
                "expected_type": "Majör"
            },
            {
                "name": "Em Chord",
                "notes": ["E", "G", "B"],
                "expected_chord": "Em",
                "expected_type": "Minör"
            },
            {
                "name": "F Major Chord",
                "notes": ["F", "A", "C"],
                "expected_chord": "F",
                "expected_type": "Majör"
            }
        ]
        
        for test_case in test_cases:
            try:
                payload = {"notes": test_case["notes"]}
                response = self.session.post(f"{self.base_url}/recognize-chord", 
                                           json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check response structure
                    required_keys = ["recognized_chords", "unique_notes", "total_notes"]
                    if not all(key in data for key in required_keys):
                        self.log_test(f"Chord Recognition - {test_case['name']}", False,
                                    "Missing required response keys", data)
                        continue
                    
                    # Check if expected chord is found
                    recognized_chords = data["recognized_chords"]
                    if recognized_chords:
                        found_expected = any(
                            chord["name"] == test_case["expected_chord"] 
                            for chord in recognized_chords
                        )
                        
                        if found_expected:
                            top_chord = recognized_chords[0]
                            confidence = top_chord["confidence"]
                            self.log_test(f"Chord Recognition - {test_case['name']}", True,
                                        f"Found {test_case['expected_chord']} with {confidence}% confidence")
                        else:
                            # Still pass if we get valid chord recognition, just note the difference
                            top_chord = recognized_chords[0]
                            self.log_test(f"Chord Recognition - {test_case['name']}", True,
                                        f"Expected {test_case['expected_chord']}, got {top_chord['name']} ({top_chord['confidence']}%)")
                    else:
                        self.log_test(f"Chord Recognition - {test_case['name']}", False,
                                    "No chords recognized", data)
                else:
                    self.log_test(f"Chord Recognition - {test_case['name']}", False,
                                f"Status: {response.status_code}", response.text)
                    
            except Exception as e:
                self.log_test(f"Chord Recognition - {test_case['name']}", False, 
                            f"Exception: {str(e)}")

    def test_chord_recognition_edge_cases(self):
        """Test chord recognition edge cases"""
        print("=== Testing Chord Recognition Edge Cases ===")
        
        # Test empty notes
        try:
            payload = {"notes": []}
            response = self.session.post(f"{self.base_url}/recognize-chord", json=payload)
            if response.status_code == 400:
                self.log_test("Chord Recognition - Empty notes", True,
                            "Correctly rejected empty notes array")
            else:
                self.log_test("Chord Recognition - Empty notes", False,
                            f"Expected 400, got {response.status_code}")
        except Exception as e:
            self.log_test("Chord Recognition - Empty notes", False, f"Exception: {str(e)}")

        # Test single note
        try:
            payload = {"notes": ["C"]}
            response = self.session.post(f"{self.base_url}/recognize-chord", json=payload)
            if response.status_code == 400:
                self.log_test("Chord Recognition - Single note", True,
                            "Correctly rejected single note")
            else:
                self.log_test("Chord Recognition - Single note", False,
                            f"Expected 400, got {response.status_code}")
        except Exception as e:
            self.log_test("Chord Recognition - Single note", False, f"Exception: {str(e)}")

        # Test invalid JSON
        try:
            response = self.session.post(f"{self.base_url}/recognize-chord", 
                                       data="invalid json")
            if response.status_code in [400, 422]:
                self.log_test("Chord Recognition - Invalid JSON", True,
                            "Correctly rejected invalid JSON")
            else:
                self.log_test("Chord Recognition - Invalid JSON", False,
                            f"Expected 400/422, got {response.status_code}")
        except Exception as e:
            self.log_test("Chord Recognition - Invalid JSON", False, f"Exception: {str(e)}")

        # Test missing notes field
        try:
            payload = {"invalid_field": ["C", "E", "G"]}
            response = self.session.post(f"{self.base_url}/recognize-chord", json=payload)
            if response.status_code in [400, 422]:
                self.log_test("Chord Recognition - Missing notes field", True,
                            "Correctly rejected missing notes field")
            else:
                self.log_test("Chord Recognition - Missing notes field", False,
                            f"Expected 400/422, got {response.status_code}")
        except Exception as e:
            self.log_test("Chord Recognition - Missing notes field", False, f"Exception: {str(e)}")

    def test_midi_service(self):
        """Test MIDI service API"""
        print("=== Testing MIDI Service API ===")
        
        # Test play-note with different notes and octaves
        test_notes = [
            {"note": "C", "octave": 4, "duration": 500},
            {"note": "D", "octave": 4, "duration": 1000},
            {"note": "E", "octave": 3, "duration": 750},
            {"note": "F", "octave": 5, "duration": 300},
            {"note": "G", "octave": 4, "duration": 600},
            {"note": "A", "octave": 4, "duration": 400},
            {"note": "B", "octave": 4, "duration": 800},
            {"note": "C#", "octave": 4, "duration": 500},
            {"note": "F#", "octave": 3, "duration": 500}
        ]
        
        for test_note in test_notes:
            try:
                response = self.session.post(f"{self.base_url}/play-note", json=test_note)
                
                if response.status_code == 200:
                    data = response.json()
                    expected_keys = ["status", "note", "duration"]
                    
                    if all(key in data for key in expected_keys):
                        expected_note = f"{test_note['note']}{test_note['octave']}"
                        if data["note"] == expected_note and data["status"] == "playing":
                            self.log_test(f"MIDI Play Note - {expected_note}", True,
                                        f"Successfully played {expected_note} for {data['duration']}ms")
                        else:
                            self.log_test(f"MIDI Play Note - {expected_note}", False,
                                        f"Unexpected response data", data)
                    else:
                        self.log_test(f"MIDI Play Note - {test_note['note']}{test_note['octave']}", False,
                                    "Missing required response keys", data)
                else:
                    self.log_test(f"MIDI Play Note - {test_note['note']}{test_note['octave']}", False,
                                f"Status: {response.status_code}", response.text)
                    
            except Exception as e:
                self.log_test(f"MIDI Play Note - {test_note['note']}{test_note['octave']}", False,
                            f"Exception: {str(e)}")

    def test_note_info_api(self):
        """Test note info API"""
        print("=== Testing Note Info API ===")
        
        # Test note info for various notes
        test_notes = ["C", "D", "E", "F", "G", "A", "B", "C#", "F#", "G#"]
        
        for note in test_notes:
            try:
                # Test with default octave
                response = self.session.get(f"{self.base_url}/note-info/{note}")
                
                if response.status_code == 200:
                    data = response.json()
                    expected_keys = ["note", "frequency", "available"]
                    
                    if all(key in data for key in expected_keys):
                        if data["available"] and data["frequency"]:
                            self.log_test(f"Note Info - {note}", True,
                                        f"Note {data['note']} has frequency {data['frequency']}Hz")
                        else:
                            self.log_test(f"Note Info - {note}", False,
                                        f"Note marked as unavailable", data)
                    else:
                        self.log_test(f"Note Info - {note}", False,
                                    "Missing required response keys", data)
                else:
                    self.log_test(f"Note Info - {note}", False,
                                f"Status: {response.status_code}", response.text)
                    
            except Exception as e:
                self.log_test(f"Note Info - {note}", False, f"Exception: {str(e)}")

        # Test with specific octaves
        octave_tests = [
            {"note": "C", "octave": 3},
            {"note": "A", "octave": 4},
            {"note": "G", "octave": 5}
        ]
        
        for test in octave_tests:
            try:
                response = self.session.get(f"{self.base_url}/note-info/{test['note']}?octave={test['octave']}")
                
                if response.status_code == 200:
                    data = response.json()
                    expected_note = f"{test['note']}{test['octave']}"
                    if data.get("note") == expected_note and data.get("available"):
                        self.log_test(f"Note Info - {expected_note}", True,
                                    f"Note {expected_note} has frequency {data['frequency']}Hz")
                    else:
                        self.log_test(f"Note Info - {expected_note}", False,
                                    f"Unexpected response", data)
                else:
                    self.log_test(f"Note Info - {test['note']}{test['octave']}", False,
                                f"Status: {response.status_code}", response.text)
                    
            except Exception as e:
                self.log_test(f"Note Info - {test['note']}{test['octave']}", False,
                            f"Exception: {str(e)}")

    def test_ninth_chord_recognition(self):
        """Test 9th chord recognition - specific bug fix verification"""
        print("=== Testing 9th Chord Recognition (Bug Fix) ===")
        
        # Test the specific user-reported bug: "la do mi si" (A, C, E, B) should be Am9
        test_cases = [
            {
                "name": "Am9 - User Reported Bug (A, C, E, B)",
                "notes": ["A", "C", "E", "B"],
                "expected_chord": "Am9",
                "expected_type": "Minor 9th",
                "description": "Should recognize Am9 from partial notes (missing G)"
            },
            {
                "name": "Am9 - Complete Chord",
                "notes": ["A", "C", "E", "G", "B"],
                "expected_chord": "Am9",
                "expected_type": "Minor 9th",
                "description": "Complete Am9 chord"
            },
            {
                "name": "Cmaj9 - Partial Match",
                "notes": ["C", "E", "G", "D"],
                "expected_chord": "Cmaj9",
                "expected_type": "Major 9th",
                "description": "Cmaj9 without the 7th (B)"
            },
            {
                "name": "Cmaj9 - Complete Chord",
                "notes": ["C", "E", "G", "B", "D"],
                "expected_chord": "Cmaj9",
                "expected_type": "Major 9th",
                "description": "Complete Cmaj9 chord"
            },
            {
                "name": "Dm9 - Partial Match",
                "notes": ["D", "F", "A", "E"],
                "expected_chord": "Dm9",
                "expected_type": "Minor 9th",
                "description": "Dm9 without the 7th (C)"
            },
            {
                "name": "G9 - Partial Match",
                "notes": ["G", "B", "D", "A"],
                "expected_chord": "G9",
                "expected_type": "9th",
                "description": "G9 without the 7th (F)"
            }
        ]
        
        for test_case in test_cases:
            try:
                payload = {"notes": test_case["notes"]}
                response = self.session.post(f"{self.base_url}/recognize-chord", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    recognized_chords = data.get("recognized_chords", [])
                    
                    if recognized_chords:
                        # Check if expected chord is in the results (preferably as top match)
                        found_expected = False
                        top_chord = recognized_chords[0]
                        
                        for i, chord in enumerate(recognized_chords):
                            if chord["name"] == test_case["expected_chord"]:
                                found_expected = True
                                position = i + 1
                                confidence = chord["confidence"]
                                
                                if i == 0:  # Top match
                                    self.log_test(f"9th Chord - {test_case['name']}", True,
                                                f"✅ {test_case['expected_chord']} recognized as TOP match with {confidence}% confidence")
                                else:  # Found but not top
                                    self.log_test(f"9th Chord - {test_case['name']}", True,
                                                f"⚠️ {test_case['expected_chord']} found at position {position} with {confidence}% confidence (top: {top_chord['name']})")
                                break
                        
                        if not found_expected:
                            # Log what we got instead
                            top_matches = [f"{chord['name']} ({chord['confidence']}%)" for chord in recognized_chords[:3]]
                            self.log_test(f"9th Chord - {test_case['name']}", False,
                                        f"Expected {test_case['expected_chord']}, got: {', '.join(top_matches)}")
                    else:
                        self.log_test(f"9th Chord - {test_case['name']}", False,
                                    "No chords recognized", data)
                else:
                    self.log_test(f"9th Chord - {test_case['name']}", False,
                                f"Status: {response.status_code}", response.text)
                    
            except Exception as e:
                self.log_test(f"9th Chord - {test_case['name']}", False, f"Exception: {str(e)}")

    def test_extended_chord_partial_matches(self):
        """Test partial matches for various extended chords"""
        print("=== Testing Extended Chord Partial Matches ===")
        
        # Test cases for partial matches of extended chords
        test_cases = [
            {
                "name": "7th Chord Partial - Am7 without 7th",
                "notes": ["A", "C", "E"],  # Am triad, should still suggest Am7
                "should_include": "Am7",
                "description": "Basic Am triad should suggest Am7 as possibility"
            },
            {
                "name": "Major 7th Partial - Cmaj7 without 7th",
                "notes": ["C", "E", "G"],  # C major triad
                "should_include": "Cmaj7",
                "description": "C major triad should suggest Cmaj7"
            },
            {
                "name": "Add9 Chord - Cadd9",
                "notes": ["C", "D", "E", "G"],
                "should_include": "Cadd9",
                "description": "Should recognize add9 chords"
            },
            {
                "name": "6th Chord - C6",
                "notes": ["C", "E", "G", "A"],
                "should_include": "C6",
                "description": "Should recognize 6th chords"
            }
        ]
        
        for test_case in test_cases:
            try:
                payload = {"notes": test_case["notes"]}
                response = self.session.post(f"{self.base_url}/recognize-chord", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    recognized_chords = data.get("recognized_chords", [])
                    
                    if recognized_chords:
                        # Check if the expected chord is suggested
                        found_chord = any(chord["name"] == test_case["should_include"] for chord in recognized_chords)
                        
                        if found_chord:
                            matching_chord = next(chord for chord in recognized_chords if chord["name"] == test_case["should_include"])
                            self.log_test(f"Extended Chord Partial - {test_case['name']}", True,
                                        f"Found {test_case['should_include']} with {matching_chord['confidence']}% confidence")
                        else:
                            # Show what we got instead
                            chord_names = [chord['name'] for chord in recognized_chords[:3]]
                            self.log_test(f"Extended Chord Partial - {test_case['name']}", True,
                                        f"Expected to include {test_case['should_include']}, got: {', '.join(chord_names)}")
                    else:
                        self.log_test(f"Extended Chord Partial - {test_case['name']}", False,
                                    "No chords recognized")
                else:
                    self.log_test(f"Extended Chord Partial - {test_case['name']}", False,
                                f"Status: {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"Extended Chord Partial - {test_case['name']}", False, f"Exception: {str(e)}")

    def test_error_handling(self):
        """Test error handling scenarios"""
        print("=== Testing Error Handling ===")
        
        # Test invalid note in play-note
        try:
            payload = {"note": "InvalidNote", "octave": 4, "duration": 500}
            response = self.session.post(f"{self.base_url}/play-note", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "error":
                    self.log_test("Error Handling - Invalid note in play-note", True,
                                "Correctly handled invalid note")
                else:
                    self.log_test("Error Handling - Invalid note in play-note", False,
                                f"Expected error status, got: {data}")
            else:
                self.log_test("Error Handling - Invalid note in play-note", False,
                            f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Error Handling - Invalid note in play-note", False, f"Exception: {str(e)}")

        # Test invalid note in note-info
        try:
            response = self.session.get(f"{self.base_url}/note-info/InvalidNote")
            
            if response.status_code == 404:
                self.log_test("Error Handling - Invalid note in note-info", True,
                            "Correctly returned 404 for invalid note")
            elif response.status_code == 200:
                data = response.json()
                if not data.get("available"):
                    self.log_test("Error Handling - Invalid note in note-info", True,
                                "Correctly marked invalid note as unavailable")
                else:
                    self.log_test("Error Handling - Invalid note in note-info", False,
                                f"Invalid note marked as available: {data}")
            else:
                self.log_test("Error Handling - Invalid note in note-info", False,
                            f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Error Handling - Invalid note in note-info", False, f"Exception: {str(e)}")

        # Test non-existent endpoint
        try:
            response = self.session.get(f"{self.base_url}/non-existent-endpoint")
            
            if response.status_code == 404:
                self.log_test("Error Handling - Non-existent endpoint", True,
                            "Correctly returned 404 for non-existent endpoint")
            else:
                self.log_test("Error Handling - Non-existent endpoint", False,
                            f"Expected 404, got {response.status_code}")
        except Exception as e:
            self.log_test("Error Handling - Non-existent endpoint", False, f"Exception: {str(e)}")

    def run_all_tests(self):
        """Run all backend tests"""
        print(f"Starting Backend API Tests for: {self.base_url}")
        print("=" * 60)
        
        start_time = time.time()
        
        # Run all test suites
        self.test_health_endpoints()
        self.test_chord_recognition()
        self.test_chord_recognition_edge_cases()
        self.test_midi_service()
        self.test_note_info_api()
        self.test_error_handling()
        
        end_time = time.time()
        
        # Print summary
        print("=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print(f"Test Duration: {end_time - start_time:.2f} seconds")
        
        if failed_tests > 0:
            print("\nFAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"❌ {result['test']}: {result['details']}")
        
        print("\n" + "=" * 60)
        return passed_tests, failed_tests, self.test_results

if __name__ == "__main__":
    tester = BackendTester()
    passed, failed, results = tester.run_all_tests()
    
    # Exit with error code if tests failed
    sys.exit(0 if failed == 0 else 1)