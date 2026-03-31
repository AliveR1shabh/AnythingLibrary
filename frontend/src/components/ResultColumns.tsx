import React, { useState } from 'react';
import './ResultColumns.css';
import { ResultColumnsProps } from '../types';

const ResultColumns: React.FC<ResultColumnsProps> = ({ results }) => {
  const [expandedCards, setExpandedCards] = useState<Set<string>>(new Set());

  const toggleExpanded = (provider: string) => {
    setExpandedCards(prev => {
      const newSet = new Set(prev);
      if (newSet.has(provider)) {
        newSet.delete(provider);
      } else {
        newSet.add(provider);
      }
      return newSet;
    });
  };

  const getProviderColor = (provider: string): string => {
    const colors: { [key: string]: string } = {
      google: '#4285f4',
      groq: '#00d4aa',
      cerebras: '#6366f1',
      cohere: '#f97316',
      grok: '#000000'
    };
    return colors[provider] || '#666';
  };

  const getProviderIcon = (provider: string): string => {
    const icons: { [key: string]: string } = {
      google: '🔍',
      groq: '⚡',
      cerebras: '🧬',
      cohere: '🔥',
      grok: '🚀'
    };
    return icons[provider] || '🤖';
  };

  const truncateText = (text: string, maxLength: number = 500): string => {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  return (
    <div className="results-container">
      <div className="results-header">
        <h2>Comparison Results</h2>
        <p className="prompt-display">
          <strong>Prompt as Query:</strong> {results.prompt}
        </p>
      </div>
      
      <div className="results-grid">
        {results.responses.map((response) => (
          <div
            key={response.provider}
            className="result-card"
            style={{ borderTopColor: getProviderColor(response.provider) }}
          >
            <div className="result-header">
              <div className="provider-info">
                <span className="provider-icon">{getProviderIcon(response.provider)}</span>
                <h3 className="provider-name" style={{ color: getProviderColor(response.provider) }}>
                  {response.provider === 'google' && (
                    <>
                      <svg width="18" height="18" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ marginRight: '8px', verticalAlign: 'middle' }}>
                        <circle cx="16" cy="16" r="16" fill="#4285f4"/>
                        <circle cx="11" cy="16" r="5" fill="none" stroke="white" strokeWidth="2"/>
                        <circle cx="21" cy="16" r="5" fill="none" stroke="white" strokeWidth="2"/>
                        <text x="16" y="20" fontFamily="Arial, sans-serif" fontSize="8" fontWeight="bold" fill="white" textAnchor="middle">G</text>
                      </svg>
                      Google Gemini
                    </>
                  )}
                  {response.provider === 'groq' && (
                    <>
                      <svg width="18" height="18" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ marginRight: '8px', verticalAlign: 'middle' }}>
                        <rect width="32" height="32" rx="8" fill="#00d4aa"/>
                        <path d="M8 12L16 8L24 12L16 16L8 12Z" fill="white"/>
                        <path d="M8 20L16 16L24 20L16 24L8 20Z" fill="white" opacity="0.8"/>
                        <path d="M8 16L16 12L24 16L16 20L8 16Z" fill="white" opacity="0.6"/>
                      </svg>
                      GROQ AI
                    </>
                  )}
                  {response.provider !== 'google' && response.provider !== 'groq' && (
                    response.provider.charAt(0).toUpperCase() + response.provider.slice(1)
                  )}
                </h3>
              </div>
              {response.tokens_used && (
                <span className="token-count">{response.tokens_used} tokens</span>
              )}
            </div>
            
            <div className="result-content">
              {response.error ? (
                <div className="error-content">
                  <p className="error-message">⚠️ {response.error}</p>
                </div>
              ) : (
                <>
                  <div className="response-text">
                    {expandedCards.has(response.provider) 
                      ? response.response 
                      : truncateText(response.response)
                    }
                  </div>
                  
                  {response.response.length > 300 && (
                    <button
                      className="expand-button"
                      onClick={() => toggleExpanded(response.provider)}
                      style={{ color: getProviderColor(response.provider) }}
                    >
                      {expandedCards.has(response.provider) ? 'Read Less ▲' : 'Read More ▼'}
                    </button>
                  )}
                </>
              )}
            </div>
            
            <div className="result-footer">
              <span className="timestamp">
                {new Date(response.timestamp).toLocaleTimeString()}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ResultColumns;
