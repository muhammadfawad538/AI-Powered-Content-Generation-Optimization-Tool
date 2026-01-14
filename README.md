# AI-Powered Content Generation & Optimization Tool

An AI-powered content generation and optimization tool that allows users to create high-quality, SEO-optimized content with user-defined parameters for topic, audience, tone, style, format, and length.

## Features

- **User-Controlled Content Generation**: Define topic, audience, tone, style, format, and length
- **High-Quality Content**: Generates relevant, coherent, and readable content
- **SEO Optimization**: Ethical SEO recommendations without manipulative practices
- **Quality Review**: Improves clarity, readability, engagement, and flow
- **Ethical Safeguards**: Detects plagiarism and identifies ethical risks
- **Research Assistance**: Gathers relevant data and references to support content creation

## Architecture

The tool follows a modular architecture with the following key components:

- **Models**: Data structures and validation rules
- **Services**: Business logic for content generation, validation, and LLM integration
- **API**: FastAPI endpoints for content generation and related operations
- **Utils**: Helper functions for validation and sanitization
- **Middleware**: Security and rate limiting components

## Prerequisites

- Python 3.11+
- An API key from OpenAI, Anthropic, or other supported LLM provider

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
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

4. Configure your environment:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

## Configuration

The application uses environment variables for configuration. Copy `.env.example` to `.env` and set the following:

- `OPENAI_API_KEY`: Your OpenAI API key (required if using OpenAI)
- `ANTHROPIC_API_KEY`: Your Anthropic API key (required if using Anthropic)
- `LLM_PROVIDER`: LLM provider to use (openai, anthropic)
- `DEBUG`: Enable/disable debug mode
- `RATE_LIMIT_REQUESTS`: Number of requests allowed per time window
- `CONTENT_LENGTH_LIMIT`: Maximum content length in words

## Usage

### Running the Server

```bash
# Development
uvicorn src.api.main:app --reload

# Production
uvicorn src.api.main:app --workers 4
```

### API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health check
- `POST /api/v1/content/generate` - Generate content
- `POST /api/v1/content/validate` - Validate content generation request
- `GET /api/v1/content/providers` - Get available LLM providers

### Example Request

```bash
curl -X POST http://localhost:8000/api/v1/content/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "topic": "Benefits of renewable energy",
    "audience": "general_public",
    "tone": "informative",
    "style": "educational",
    "format": "blog_post",
    "length": 800,
    "keywords": ["sustainability", "clean energy"]
  }'
```

## Development

### Project Structure

```
src/
├── models/                 # Data models and validation
│   └── content_generation.py
├── services/              # Business logic
│   ├── content_generation.py
│   ├── llm_integration.py
│   └── validation.py
├── api/                   # API endpoints
│   ├── main.py
│   ├── routes/
│   │   └── content_generation.py
│   └── middleware/
│       └── security.py
├── config/                # Configuration
│   └── settings.py
└── utils/                 # Utility functions
    ├── validators.py
    └── sanitizer.py
```

### Running Tests

```bash
# Run all tests
pytest

# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/
```

## Security

- API key authentication required for all endpoints
- Rate limiting to prevent abuse
- Input sanitization to prevent injection attacks
- Content validation to ensure quality and safety

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.