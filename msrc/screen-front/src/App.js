import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginForm from './LoginForm';
import MainPage from './MainPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<LoginForm />} />
        <Route path="/main" element={<MainPage />} />
      </Routes>
    </Router>
  );
}

export default App;