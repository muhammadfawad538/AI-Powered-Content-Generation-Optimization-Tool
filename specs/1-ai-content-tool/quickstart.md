# Quickstart Guide: AI-Powered Content Generation Tool - Phase 1

## Setup

### Prerequisites
- Python 3.11+
- pip package manager
- Virtual environment tool (venv or conda)

### Installation
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

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (or equivalent for chosen LLM provider)
- `LLM_PROVIDER`: LLM provider to use (openai, anthropic, etc.)
- `DATABASE_URL`: Database connection string (if using persistence)
- `RATE_LIMIT_REQUESTS`: Number of requests allowed per minute
- `CONTENT_LENGTH_LIMIT`: Maximum content length in words

## Running the Service

### Development
```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the development server
python -m src.api.main
```

The API will be available at `http://localhost:8000`

### Production
```bash
# Using uvicorn for production
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Usage

### Generate Content
Send a POST request to `/api/v1/content/generate`:

```bash
curl -X POST http://localhost:8000/api/v1/content/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "topic": "Benefits of renewable energy",
    "audience": "environmental advocates",
    "tone": "informative",
    "style": "educational",
    "format": "blog_post",
    "length": 800,
    "keywords": ["sustainability", "clean energy"]
  }'
```

### Response Format
```json
{
  "id": "req_1234567890",
  "content": "Generated content text...",
  "word_count": 795,
  "quality_score": 0.89,
  "generation_time": 4.2,
  "status": "success",
  "timestamp": "2026-01-13T10:30:00Z"
}
```

## Testing

### Run Unit Tests
```bash
pytest tests/unit/
```

### Run Integration Tests
```bash
pytest tests/integration/
```

### Run Contract Tests
```bash
pytest tests/contract/
```

## Docker Support
If Docker is preferred:

```bash
# Build the image
docker build -t ai-content-generator .

# Run the container
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key_here ai-content-generator
```

## Troubleshooting

### Common Issues
- **API Key Error**: Ensure your LLM provider API key is correctly set in environment variables
- **Rate Limiting**: Check if you're exceeding API rate limits
- **Content Quality**: Adjust input parameters for better results