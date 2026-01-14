# Manual Testing API for AI-Powered Content Generation & Optimization

This FastAPI application provides manual testing endpoints for the AI-Powered Content Generation & Optimization system. It includes simplified endpoints for all major features without complex implementation, allowing for easy manual testing via Swagger UI.

## Features

- **Content Generation**: Generate content based on topic, audience, tone, style, and format
- **SEO Optimization**: Analyze content for SEO elements and provide recommendations
- **Quality Review**: Review content for clarity, readability, engagement, and flow
- **Ethics/Plagiarism Check**: Check content for ethical issues and potential plagiarism
- **Research Assistance**: Conduct research and gather relevant information
- **Export Management**: Export content to various platforms and formats
- **Analytics & Insights**: Get performance analytics and actionable insights

## Installation

1. Install the required dependencies:
   ```bash
   pip install fastapi uvicorn
   ```

## Running the API

1. Navigate to the project directory:
   ```bash
   cd E:\DEV\SEO_App
   ```

2. Run the application:
   ```bash
   python manual_test_api.py
   ```

   Or using uvicorn directly:
   ```bash
   uvicorn manual_test_api:app --host 0.0.0.0 --port 8000 --reload
   ```

3. Access the Swagger UI at: http://localhost:8000/docs

## API Endpoints

### Content Generation
- **POST** `/content/generate` - Generate content based on parameters

### SEO Optimization
- **POST** `/seo/analyze` - Analyze content for SEO elements

### Quality Review
- **POST** `/quality/review` - Review content quality

### Ethics/Plagiarism Check
- **POST** `/ethics/check` - Check content for ethical issues

### Research Assistance
- **POST** `/research/conduct` - Conduct research on a topic

### Export Management
- **POST** `/export/content` - Export content to platforms

### Analytics & Insights
- **POST** `/analytics/query` - Query analytics data
- **POST** `/insights/generate` - Generate insights and recommendations

## Testing Instructions

1. Start the API server as described above
2. Navigate to http://localhost:8000/docs in your browser
3. Test each endpoint by clicking on it and using the "Try it out" button
4. Provide sample JSON inputs as prompted
5. Observe the realistic sample responses returned

## Example Requests

### Content Generation
```json
{
  "topic": "AI in Digital Marketing",
  "audience": "professionals",
  "tone": "informative",
  "style": "professional",
  "format": "blog_post",
  "length": 800,
  "keywords": ["AI", "marketing", "automation"],
  "requirements": ["include benefits", "focus on ROI"]
}
```

### SEO Analysis
```json
{
  "content": "This is sample content for SEO analysis...",
  "target_keywords": ["SEO", "content", "optimization"]
}
```

### Quality Review
```json
{
  "content": "This is sample content to review for quality...",
  "target_audience": "marketing professionals",
  "review_aspects": ["clarity", "readability", "engagement"]
}
```

## Purpose

This API is specifically designed for manual pre-deployment testing. It returns realistic sample responses without implementing the full complex logic, making it ideal for:

- Verifying API contracts and data structures
- Testing client applications
- Demonstrating system capabilities
- Validating request/response schemas

## Note

This is NOT a production-ready API. It contains placeholder implementations that return sample data for testing purposes only.