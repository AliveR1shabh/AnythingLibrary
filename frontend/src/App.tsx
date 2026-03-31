import React, { useState, useEffect } from 'react';
import './App.css';
import SearchBar from './components/SearchBar';
import ResultColumns from './components/ResultColumns';
import Login from './components/Login';
import LandingPage from './components/LandingPage';
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
      {showLanding ? (
        <LandingPage onGetStarted={handleGetStarted} />
      ) : !isAuthenticated ? (
        <Login 
          onLogin={handleLogin} 
          loading={loginLoading} 
          error={loginError} 
        />
      ) : (
        <>
          <header className="App-header">
            <div className="header-content">
              <div className="header-left">
                <div className="app-title-section">
                  <div className="app-logo">
                    <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <rect width="40" height="40" rx="8" fill="url(#gradient1)"/>
                      <path d="M10 20L15 15L20 20L25 15L30 20L25 25L20 20L15 25L10 20Z" fill="white"/>
                      <defs>
                        <linearGradient id="gradient1" x1="0" y1="0" x2="40" y2="40" gradientUnits="userSpaceOnUse">
                          <stop stopColor="#667eea"/>
                          <stop offset="1" stopColor="#764ba2"/>
                        </linearGradient>
                      </defs>
                    </svg>
                  </div>
                  <div className="app-title">
                    <h1>AnythingLibrary</h1>
                    <p>Compare multiple AI responses side by side</p>
                  </div>
                </div>
              </div>
              <div className="header-right">
                <span className="welcome-text">Welcome, {user?.username}</span>
                <button onClick={handleLogout} className="logout-button">
                  Logout
                </button>
              </div>
            </div>
          </header>
          
          <main>
            <SearchBar 
              onSearch={handleSearch} 
              loading={loading} 
              availableProviders={availableProviders}
            />
            
            {error && (
              <div className="error-message">
                <p>Error: {error}</p>
              </div>
            )}
            
            {results && (
              <ResultColumns results={results} />
            )}
          </main>
          
          <footer className="App-footer">
            <p>&copy; 2026 AnythingLibrary. Compare AI responses with ease. Made by Rishabh Gupta.</p>
          </footer>
        </>
      )}
    </div>
  );
};

export default App;
