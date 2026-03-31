import React from 'react';
import './LandingPage.css';

interface LandingPageProps {
  onGetStarted: () => void;
}

const LandingPage: React.FC<LandingPageProps> = ({ onGetStarted }) => {
  return (
    <div className="landing-page">
      <div className="landing-container">
        <header className="landing-header">
          <div className="landing-logo">
            <svg width="60" height="60" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
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
          <h1 className="landing-title">AnythingLibrary</h1>
          <p className="landing-subtitle">Compare Multiple AI Responses Side by Side</p>
        </header>

        <main className="landing-main">
          <section className="hero-section">
            <h2 className="hero-title">Get the Best AI Responses</h2>
            <p className="hero-description">
              Compare answers from multiple AI providers including Google Gemini, GROQ, Cerebras, and Anthropic 
              to get comprehensive insights and make informed decisions.
            </p>
            <button className="cta-button" onClick={onGetStarted}>
              Get Started →
            </button>
          </section>

          <section className="features-section">
            <div className="features-grid">
              <div className="feature-card">
                <div className="feature-icon">🤖</div>
                <h3>Multiple AI Providers</h3>
                <p>Access responses from Google Gemini, GROQ, Cerebras, and Anthropic in one place</p>
              </div>
              <div className="feature-card">
                <div className="feature-icon">⚡</div>
                <h3>Lightning Fast</h3>
                <p>Get concise 3-5 line responses from multiple AI models instantly</p>
              </div>
              <div className="feature-card">
                <div className="feature-icon">🎯</div>
                <h3>Side-by-Side Comparison</h3>
                <p>Easily compare different AI perspectives to find the best answers</p>
              </div>
              <div className="feature-card">
                <div className="feature-icon">🔒</div>
                <h3>Secure & Private</h3>
                <p>Your data is protected with secure login and private sessions</p>
              </div>
            </div>
          </section>

          <section className="providers-section">
            <h3>Powered by Leading AI Models</h3>
            <div className="providers-showcase">
              <div className="provider-item">
                <svg width="24" height="24" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="16" cy="16" r="16" fill="#4285f4"/>
                  <circle cx="11" cy="16" r="5" fill="none" stroke="white" strokeWidth="2"/>
                  <circle cx="21" cy="16" r="5" fill="none" stroke="white" strokeWidth="2"/>
                  <text x="16" y="20" fontFamily="Arial, sans-serif" fontSize="8" fontWeight="bold" fill="white" textAnchor="middle">G</text>
                </svg>
                <span>Google Gemini</span>
              </div>
              <div className="provider-item">
                <svg width="24" height="24" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <rect width="32" height="32" rx="8" fill="#00d4aa"/>
                  <path d="M8 12L16 8L24 12L16 16L8 12Z" fill="white"/>
                  <path d="M8 20L16 16L24 20L16 24L8 20Z" fill="white" opacity="0.8"/>
                  <path d="M8 16L16 12L24 16L16 20L8 16Z" fill="white" opacity="0.6"/>
                </svg>
                <span>GROQ AI</span>
              </div>
              <div className="provider-item">
                <div className="provider-icon">🧬</div>
                <span>Cerebras</span>
              </div>
            </div>
          </section>
        </main>

        <footer className="landing-footer">
          <p>&copy; 2026 AnythingLibrary. Compare AI responses with confidence. Made by Rishabh Gupta.</p>
        </footer>
      </div>
    </div>
  );
};

export default LandingPage;
