import React from 'react';
import { useDarkMode } from '../hooks/useDarkMode';
import './DarkModeToggle.css';

const DarkModeToggle: React.FC = () => {
  const { isDarkMode, toggleDarkMode } = useDarkMode();

  return (
    <button 
      className="dark-mode-toggle"
      onClick={toggleDarkMode}
      title={isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'}
    >
      {isDarkMode ? (
        <span className="mode-icon">☀️</span>
      ) : (
        <span className="mode-icon">🌙</span>
      )}
    </button>
  );
};

export default DarkModeToggle;
