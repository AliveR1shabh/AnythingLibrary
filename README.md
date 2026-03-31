# AnythingLibrary

A responsive multi-AI comparison web app that aggregates and displays responses from multiple AI APIs side-by-side.

## Features

- **Multi-AI Comparison**: Compare responses from OpenAI, Anthropic, Google, and Cohere simultaneously
- **Responsive Design**: Mobile-first layout with 4-column grid on desktop, adaptive on smaller screens
- **Modern UI**: Clean, minimal interface with smooth transitions and animations
- **Expandable Results**: "Read More" functionality for longer responses
- **Parallel Processing**: Fast API calls with async/await for optimal performance
- **Secure Configuration**: Environment variable management for API keys
- **Scalable Architecture**: Ready for PostgreSQL/SQLite integration for user data and query history

## Tech Stack

### Backend
- **FastAPI** (Python 3.9+) - Modern, fast web framework
- **HTTPX** - Async HTTP client for parallel API calls
- **Pydantic** - Data validation and settings management
- **SQLAlchemy** - Database ORM (optional)
- **Python-dotenv** - Environment variable management

### Frontend
- **React 18** - Modern UI framework with TypeScript
- **CSS3** - Responsive design with Flexbox/Grid
- **Axios** - HTTP client for API communication
- **HTML5** - Semantic markup

## Quick Start

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy environment variables:
```bash
cp .env.example .env
```

5. Add your API keys to `.env`:
```env
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
```

6. Start the backend server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The app will be available at `http://localhost:3000`

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /providers` - List available AI providers
- `POST /compare` - Compare AI responses

### Compare Endpoint

**Request:**
```json
{
  "prompt": "Your question here",
  "providers": ["openai", "anthropic", "google", "cohere"],
  "max_tokens": 500,
  "temperature": 0.7
}
```

**Response:**
```json
{
  "prompt": "Your question here",
  "responses": [
    {
      "provider": "openai",
      "response": "AI response here",
      "timestamp": "2024-01-01T12:00:00",
      "tokens_used": 150,
      "error": null
    }
  ],
  "timestamp": "2024-01-01T12:00:00"
}
```

## Project Structure

```
AnythingLibrary/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── .env.example        # Environment variables template
├── frontend/
│   ├── public/
│   │   └── index.html      # HTML template
│   ├── src/
│   │   ├── components/
│   │   │   ├── SearchBar.tsx
│   │   │   ├── SearchBar.css
│   │   │   ├── ResultColumns.tsx
│   │   │   └── ResultColumns.css
│   │   ├── App.tsx         # Main application component
│   │   ├── App.css
│   │   ├── index.tsx       # Application entry point
│   │   ├── index.css       # Global styles
│   │   └── types.ts        # TypeScript type definitions
│   ├── package.json        # Node.js dependencies
│   └── tsconfig.json       # TypeScript configuration
└── README.md               # This file
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY` - OpenAI API key
- `ANTHROPIC_API_KEY` - Anthropic API key
- `GOOGLE_API_KEY` - Google AI API key
- `COHERE_API_KEY` - Cohere API key
- `DATABASE_URL` - Database connection string (optional)
- `DEBUG` - Debug mode (default: True)
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)

## Features in Detail

### Responsive Design
- **Desktop**: 4-column grid layout
- **Tablet**: 2-column grid layout
- **Mobile**: Single column layout
- Smooth transitions and hover effects
- Mobile-first approach with progressive enhancement

### AI Provider Integration
- **OpenAI**: GPT-3.5-turbo model
- **Anthropic**: Claude-3-haiku model
- **Google**: Gemini Pro model
- **Cohere**: Command model

### Security
- API keys stored in environment variables
- CORS configuration for frontend access
- Input validation and sanitization
- Error handling for API failures

## Future Enhancements

- User authentication and profiles
- Query history and favorites
- Advanced filtering and sorting
- Export results to various formats
- Custom model parameters
- Batch comparison mode
- Real-time collaboration
- Analytics and usage tracking

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please open an issue on the GitHub repository.
