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

  const exportToPDF = async () => {
    if (!results || !results.responses || results.responses.length === 0) {
      alert('No results to export');
      return;
    }

    try {
      // Dynamically import jsPDF
      const { jsPDF } = await import('jspdf');
      
      const doc = new jsPDF();
      
      // Add title
      doc.setFontSize(20);
      doc.setFont('helvetica', 'bold');
      doc.text('AI Comparison Results', 20, 20);
      
      // Add prompt
      doc.setFontSize(12);
      doc.setFont('helvetica', 'normal');
      const promptLines = doc.splitTextToSize(results.prompt, 180);
      doc.text('Prompt:', 20, 40);
      doc.setFont('helvetica', 'italic');
      promptLines.forEach((line: string, index: number) => {
        doc.text(line, 25, 50 + (index * 6));
      });
      
      // Add responses
      let yPosition = 80;
      results.responses.forEach((response, index) => {
        if (yPosition > 250) {
          doc.addPage();
          yPosition = 20;
        }
        
        doc.setFont('helvetica', 'bold');
        doc.text(`${response.provider.toUpperCase()} Response:`, 20, yPosition);
        doc.setFont('helvetica', 'normal');
        
        const responseLines = doc.splitTextToSize(response.response, 160);
        responseLines.forEach((line: string, lineIndex: number) => {
          doc.text(line, 25, yPosition + 10 + (lineIndex * 5));
        });
        
        if (response.tokens_used) {
          doc.text(`Tokens: ${response.tokens_used}`, 25, yPosition + 10 + (responseLines.length * 5));
        }
        
        if (response.error) {
          doc.text(`Error: ${response.error}`, 25, yPosition + 10 + (responseLines.length * 5));
        }
        
        yPosition += 15 + (responseLines.length * 5) + 10;
      });
      
      // Add timestamp
      doc.setFontSize(10);
      doc.text(`Generated: ${new Date(results.timestamp).toLocaleString()}`, 20, yPosition + 10);
      
      // Save the PDF
      doc.save('ai-comparison-results.pdf');
    } catch (error) {
      console.error('Error generating PDF:', error);
      alert('Failed to generate PDF. Please try again.');
    }
  };

  const exportToMarkdown = () => {
    if (!results || !results.responses || results.responses.length === 0) {
      alert('No results to export');
      return;
    }

    let markdown = `# AI Comparison Results\n\n`;
    
    // Add prompt
    markdown += `## Prompt\n${results.prompt}\n\n`;
    
    // Add responses
    results.responses.forEach((response, index) => {
      markdown += `## ${response.provider.toUpperCase()} Response\n\n`;
      markdown += `${response.response}\n\n`;
      
      if (response.tokens_used) {
        markdown += `*Tokens used: ${response.tokens_used}*\n\n`;
      }
      
      if (response.error) {
        markdown += `*Error: ${response.error}*\n\n`;
      }
      
      markdown += `---\n\n`;
    });
    
    // Add timestamp
    markdown += `*Generated: ${new Date(results.timestamp).toLocaleString()}*\n`;
    
    // Create and download markdown file
    const blob = new Blob([markdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'ai-comparison-results.md';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
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
        <div className="export-buttons">
          <button 
            className="export-button pdf-button"
            onClick={exportToPDF}
            title="Download comparison results as PDF"
          >
            📄 Download PDF
          </button>
          <button 
            className="export-button markdown-button"
            onClick={exportToMarkdown}
            title="Download comparison results as Markdown"
          >
            📝 Download Markdown
          </button>
        </div>
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
