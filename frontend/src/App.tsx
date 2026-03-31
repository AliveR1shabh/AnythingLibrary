import React, { useState, useEffect } from 'react';
import './App.css';
import SearchBar from './components/SearchBar';
import ResultColumns from './components/ResultColumns';
import Login from './components/Login';
import LandingPage from './components/LandingPage';
import DarkModeToggle from './components/DarkModeToggle';
import { ComparisonResult } from './types';

interface User {
  username: string;
  login_time: string;
}

const App: React.FC = () => {
  const [results, setResults] = useState<ComparisonResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [availableProviders, setAvailableProviders] = useState<string[]>([]);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<User | null>(null);
  const [loginLoading, setLoginLoading] = useState(false);
  const [loginError, setLoginError] = useState<string | null>(null);
  const [showLanding, setShowLanding] = useState(true);

  // Check for existing session on mount
  useEffect(() => {
    const savedUser = localStorage.getItem('anythinglibrary_user');
    if (savedUser) {
      try {
        const userData = JSON.parse(savedUser);
        setUser(userData);
        setIsAuthenticated(true);
        fetchAvailableProviders();
      } catch (e) {
        localStorage.removeItem('anythinglibrary_user');
      }
    }
  }, []);

  useEffect(() => {
    if (isAuthenticated) {
      fetchAvailableProviders();
    }
  }, [isAuthenticated]);

  const fetchAvailableProviders = async () => {
    try {
      const response = await fetch('http://localhost:8001/providers');
      if (response.ok) {
        const data = await response.json();
        setAvailableProviders(data.providers);
        console.log('Available providers:', data.providers);
      } else {
        console.error('Failed to fetch providers');
      }
    } catch (err) {
      console.error('Error fetching providers:', err);
    }
  };

  const handleLogin = async (username: string, password: string) => {
    setLoginLoading(true);
    setLoginError(null);
    
    try {
      const response = await fetch('http://localhost:8001/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        const data = await response.json();
        setUser(data.user);
        setIsAuthenticated(true);
        localStorage.setItem('anythinglibrary_user', JSON.stringify(data.user));
        console.log('Login successful:', data.user);
      } else {
        const errorData = await response.json();
        setLoginError(errorData.error || 'Login failed');
      }
    } catch (err) {
      setLoginError('Network error. Please try again.');
      console.error('Login error:', err);
    } finally {
      setLoginLoading(false);
    }
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setUser(null);
    setResults(null);
    setError(null);
    setAvailableProviders([]);
    localStorage.removeItem('anythinglibrary_user');
    console.log('User logged out');
  };

  const handleSearch = async (prompt: string, providers: string[], simplify: boolean = false) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:8001/compare', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt,
          providers,
          max_tokens: 1500,
          temperature: 0.7,
          simplify
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: ComparisonResult = await response.json();
      setResults(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleGetStarted = () => {
    setShowLanding(false);
  };

  return (
    <div className="App">
      <DarkModeToggle />
      {showLanding ? (
        <LandingPage onGetStarted={handleGetStarted} />
      ) : !isAuthenticated ? (
        <Login onLogin={handleLogin} loading={loginLoading} error={loginError} />
      ) : (
        <div className="app-container">
          <div className="App-header">
            <div className="header-left">
              <div className="app-title-section">
                <div className="app-logo">
                  <svg width="40" height="40" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect width="32" height="32" rx="8" fill="url(#gradient1)"/>
                    <path d="M8 12L16 8L24 12L16 16L8 12Z" fill="white" opacity="0.9"/>
                    <path d="M8 20L16 16L24 20L16 24L8 20Z" fill="white" opacity="0.8"/>
                    <path d="M8 16L16 12L24 16L16 20L8 16Z" fill="white" opacity="0.7"/>
                    <text x="16" y="20" fontFamily="Arial, sans-serif" fontSize="8" fontWeight="bold" fill="white" textAnchor="middle">AL</text>
                    <defs>
                      <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style={{stopColor: '#667eea', stopOpacity: 1}} />
                        <stop offset="100%" style={{stopColor: '#764ba2', stopOpacity: 1}} />
                      </linearGradient>
                    </defs>
                  </svg>
                </div>
                <div className="app-title">
                  <h1>AnythingLibrary</h1>
                  <p>Compare Multiple AI Responses Side by Side</p>
                </div>
              </div>
              <div className="header-right">
                <div className="user-info">
                  <span className="welcome-text">
                    Welcome, {user?.username === 'guest' ? 'Guest User' : user?.username}!
                  </span>
                  <button className="logout-button" onClick={handleLogout}>
                    Logout
                  </button>
                </div>
              </div>
            </div>

            <SearchBar 
              onSearch={handleSearch} 
              availableProviders={availableProviders}
              loading={loading}
            />
            
            {loading && (
              <div className="loading">
                <div className="loading-spinner"></div>
              </div>
            )}
            
            {error && (
              <div className="error-message">
                ⚠️ {error}
              </div>
            )}
            
            {results && <ResultColumns results={results} />}
          </div>
        </div>
      )}
      
      <div className="App-footer">
        <p> 2024 AnythingLibrary. Powered by Multiple AI Providers.</p>
      </div>
    </div>
  );
};

export default App;
