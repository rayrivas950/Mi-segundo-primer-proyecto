import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ContactsPage from './pages/ContactsPage';

function App() {
  const user = JSON.parse(localStorage.getItem('user'));
  const isAuthenticated = user && user.access_token;

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route 
          path="/contacts" 
          element={isAuthenticated ? <ContactsPage /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/" 
          element={<Navigate to={isAuthenticated ? "/contacts" : "/login"} />} 
        />
      </Routes>
    </Router>
  );
}

export default App;