import logo from './logo.svg';
import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/Login';
import Signup from './components/SignUp'
import Home from './components/Home';
import Company from './components/Company'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login/>} />
        <Route path="/signup" element={<Signup/>} />
        <Route path="/" element={<Home/>} />
        <Route path="/companies" element={<Company/>} />

      </Routes>
    </Router>
  );
}

export default App;
