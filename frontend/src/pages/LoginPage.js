import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import authService from '../services/authService';

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh',
    backgroundColor: '#f0f2f5',
    fontFamily: 'Arial, sans-serif'
  },
  formContainer: {
    backgroundColor: 'white',
    padding: '40px',
    borderRadius: '8px',
    boxShadow: '0 4px 8px rgba(0,0,0,0.1)',
    width: '100%',
    maxWidth: '400px',
    textAlign: 'center'
  },
  h2: {
    marginBottom: '20px',
    color: '#333'
  },
  formGroup: {
    marginBottom: '15px',
    textAlign: 'left'
  },
  label: {
    display: 'block',
    marginBottom: '5px',
    fontWeight: 'bold',
    color: '#555'
  },
  input: {
    width: 'calc(100% - 22px)', // Restamos padding y borde
    padding: '10px',
    border: '1px solid #ddd',
    borderRadius: '4px',
    fontSize: '16px',
    transition: 'border-color 0.3s ease-in-out, box-shadow 0.3s ease-in-out',
    '&:focus': {
      borderColor: '#007bff',
      boxShadow: '0 0 0 0.2rem rgba(0,123,255,.25)',
      outline: 'none'
    }
  },
  button: {
    width: '100%',
    padding: '10px',
    border: 'none',
    borderRadius: '4px',
    backgroundColor: '#007bff',
    color: 'white',
    fontSize: '18px',
    cursor: 'pointer',
    marginTop: '20px',
    transition: 'background-color 0.3s ease-in-out',
    '&:hover': {
      backgroundColor: '#0056b3'
    }
  },
  error: {
    color: 'red',
    marginTop: '10px',
    marginBottom: '10px'
  },
  link: {
    marginTop: '20px',
    color: '#007bff',
    textDecoration: 'none',
    '&:hover': {
      textDecoration: 'underline'
    }
  }
};

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await authService.login(username, password);
      navigate('/contacts');
      window.location.reload(); // Forzamos recarga para que el App.js re-evalúe la autenticación
    } catch (err) {
      const errorMessage = err.response?.data?.message || 'Failed to login. Please check your credentials.';
      setError(errorMessage);
      console.error(err);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.formContainer}>
        <h2 style={styles.h2}>Login</h2>
        <form onSubmit={handleSubmit}>
          <div style={styles.formGroup}>
            <label style={styles.label}>Username</label>
            <input 
              type="text" 
              value={username} 
              onChange={(e) => setUsername(e.target.value)} 
              required 
              style={styles.input}
            />
          </div>
          <div style={styles.formGroup}>
            <label style={styles.label}>Password</label>
            <input 
              type="password" 
              value={password} 
              onChange={(e) => setPassword(e.target.value)} 
              required 
              style={styles.input}
            />
          </div>
          {error && <p style={styles.error}>{error}</p>}
          <button type="submit" style={styles.button}>Login</button>
        </form>
        <p style={styles.link}>
          Don't have an account? <Link to="/register" style={styles.link}>Register</Link>
        </p>
      </div>
    </div>
  );
}

export default LoginPage;