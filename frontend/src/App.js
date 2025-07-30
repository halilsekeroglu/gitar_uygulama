import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Fretboard from "./components/Fretboard";
import { Toaster } from "./components/ui/sonner";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Fretboard />} />
        </Routes>
        <Toaster />
      </BrowserRouter>
    </div>
  );
}

export default App;