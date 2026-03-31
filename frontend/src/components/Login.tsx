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
  const [isGuestMode, setIsGuestMode] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (isGuestMode) {
      // Guest mode login
      onLogin('guest', 'guest');
    } else if (username.trim() && password.trim()) {
      // Regular login
      onLogin(username.trim(), password.trim());
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSubmit(e as any);
    }
  };

  const toggleGuestMode = () => {
    setIsGuestMode(!isGuestMode);
    setUsername('');
    setPassword('');
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>AnythingLibrary</h1>
          <p>Multi-AI Comparison Platform</p>
          <button 
            className="guest-mode-toggle"
            onClick={toggleGuestMode}
            type="button"
          >
            {isGuestMode ? '👤 Use Account' : '🎭 Guest Mode'}
          </button>
        </div>
        
        <form onSubmit={handleSubmit} className="login-form">
          {isGuestMode ? (
            <div className="guest-mode-info">
              <h3>Guest Mode</h3>
              <p>Click "Continue as Guest" to use the app without creating an account</p>
              <button type="submit" className="guest-continue-button" disabled={loading}>
                {loading ? 'Continuing...' : 'Continue as Guest'}
              </button>
            </div>
          ) : (
            <>
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
            </>
          )}
          
          {error && (
            <div className="error-message">
              <p>{error}</p>
            </div>
          )}
          
          {!isGuestMode && (
            <button
              type="submit"
              disabled={loading || !username.trim() || !password.trim()}
              className="login-button"
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
          )}
        </form>
        
        <div className="login-footer">
          <p>✨ Demo Mode: Any username (2+ chars) and password (3+ chars) will work</p>
          <p>🎭 Guest Mode: Click "Continue as Guest" for instant access</p>
        </div>
      </div>
    </div>
  );
};

export default Login;
