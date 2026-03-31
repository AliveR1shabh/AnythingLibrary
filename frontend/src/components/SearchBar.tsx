import React, { useState, useEffect } from 'react';
import './SearchBar.css';
import { SearchProps } from '../types';

interface SearchBarProps {
  onSearch: (prompt: string, providers: string[], simplify: boolean) => void;
  loading: boolean;
  availableProviders: string[];
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch, loading, availableProviders }) => {
  const [prompt, setPrompt] = useState('');
  const [selectedProviders, setSelectedProviders] = useState<string[]>([]);
  const [simplify, setSimplify] = useState(false);

  const allProviders = [
    { id: 'google', name: 'Google', color: '#4285f4' },
    { id: 'groq', name: 'GROQ', color: '#00d4aa' },
    { id: 'cerebras', name: 'Cerebras', color: '#6366f1' }
  ];

  // Filter providers to only show available ones
  const providers = allProviders.filter(provider => 
    availableProviders.includes(provider.id)
  );

  // Auto-select available providers on mount
  useEffect(() => {
    if (availableProviders.length > 0 && selectedProviders.length === 0) {
      setSelectedProviders(availableProviders);
    }
  }, [availableProviders]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (prompt.trim() && selectedProviders.length > 0) {
      onSearch(prompt.trim(), selectedProviders, simplify);
    }
  };

  const toggleProvider = (providerId: string) => {
    setSelectedProviders(prev => {
      if (prev.includes(providerId)) {
        if (prev.length === 1) return prev; // Keep at least one provider
        return prev.filter(p => p !== providerId);
      }
      return [...prev, providerId];
    });
  };

  return (
    <div className="search-container">
      <form onSubmit={handleSubmit} className="search-form">
        <div className="search-input-wrapper">
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Enter your prompt here..."
            className="search-input"
            rows={3}
            disabled={loading}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && e.ctrlKey) {
                handleSubmit(e);
              }
            }}
          />
          <button
            type="button"
            onClick={handleSubmit}
            disabled={loading || !prompt.trim() || selectedProviders.length === 0}
            className="quick-search-button"
          >
            {loading ? '🔄 Searching...' : '🔍 Search'}
          </button>
        </div>
        
        <div className="simplify-toggle-wrapper">
          <label className="simplify-toggle">
            <input
              type="checkbox"
              checked={simplify}
              onChange={(e) => setSimplify(e.target.checked)}
              disabled={loading}
            />
            <span className="simplify-slider"></span>
            <span className="simplify-label">
              {simplify ? '🧒 Explain Like I\'m 10' : '👤 Standard Mode'}
            </span>
          </label>
          <p className="simplify-description">
            {simplify 
              ? 'Responses will be simplified for 10-year-olds to understand' 
              : 'Get detailed, technical responses from all AI providers'
            }
          </p>
        </div>
        
        <div className="provider-selection">
          <p className="provider-label">Select AI Providers:</p>
          {providers.length === 0 ? (
            <div className="no-providers-message">
              <p>⚠️ No AI providers available. Please check your API key configuration.</p>
            </div>
          ) : (
            <div className="provider-grid">
              {providers.map(provider => (
                <label
                  key={provider.id}
                  className={`provider-checkbox ${selectedProviders.includes(provider.id) ? 'selected' : ''}`}
                  style={{ borderColor: selectedProviders.includes(provider.id) ? provider.color : '#ccc' }}
                >
                  <input
                    type="checkbox"
                    checked={selectedProviders.includes(provider.id)}
                    onChange={() => toggleProvider(provider.id)}
                    disabled={loading}
                  />
                  <span className="provider-name" style={{ color: provider.color }}>
                    {provider.id === 'google' && (
                      <>
                        <svg width="16" height="16" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ marginRight: '6px', verticalAlign: 'middle' }}>
                          <circle cx="16" cy="16" r="16" fill="#4285f4"/>
                          <circle cx="11" cy="16" r="5" fill="none" stroke="white" strokeWidth="2"/>
                          <circle cx="21" cy="16" r="5" fill="none" stroke="white" strokeWidth="2"/>
                          <text x="16" y="20" fontFamily="Arial, sans-serif" fontSize="8" fontWeight="bold" fill="white" textAnchor="middle">G</text>
                        </svg>
                        {provider.name}
                      </>
                    )}
                    {provider.id === 'groq' && (
                      <>
                        <svg width="16" height="16" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ marginRight: '6px', verticalAlign: 'middle' }}>
                          <rect width="32" height="32" rx="8" fill="#00d4aa"/>
                          <path d="M8 12L16 8L24 12L16 16L8 12Z" fill="white"/>
                          <path d="M8 20L16 16L24 20L16 24L8 20Z" fill="white" opacity="0.8"/>
                          <path d="M8 16L16 12L24 16L16 20L8 16Z" fill="white" opacity="0.6"/>
                        </svg>
                        {provider.name}
                      </>
                    )}
                    {provider.id !== 'google' && provider.id !== 'groq' && provider.name}
                  </span>
                </label>
              ))}
            </div>
          )}
        </div>
        
        <button
          type="submit"
          disabled={loading || !prompt.trim() || selectedProviders.length === 0 || providers.length === 0}
          className="search-button"
        >
          {loading ? 'Comparing...' : 'Compare AI Responses'}
        </button>
      </form>
    </div>
  );
};

export default SearchBar;
