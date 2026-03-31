import React, { useState } from 'react';
import './Login.css';

interface LoginProps {
  onLogin: (username: string, password: string) => void;
  loading?: boolean;
  error?: string | null;
}

const Login: React.FC<LoginProps> = ({ onLogin, loading = false, error = null }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (username.trim() && password.trim()) {
      onLogin(username.trim(), password.trim());
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSubmit(e as any);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>AnythingLibrary</h1>
          <p>Multi-AI Comparison Platform</p>
        </div>
        
        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="username">Username (min 2 characters)</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Enter your username"
              disabled={loading}
              autoComplete="username"
              required
              minLength={2}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="password">Password (min 3 characters)</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Enter your password"
              disabled={loading}
              autoComplete="current-password"
              required
              minLength={3}
            />
          </div>
          
          {error && (
            <div className="error-message">
              <p>{error}</p>
            </div>
          )}
          
          <button
            type="submit"
            disabled={loading || !username.trim() || !password.trim()}
            className="login-button"
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>
        
        <div className="login-footer">
          <p>✨ Demo Mode: Any username (2+ chars) and password (3+ chars) will work</p>
        </div>
      </div>
    </div>
  );
};

export default Login;
