# Data Model for AI-Powered Content Generation Tool - Phase 1

## Core Entities

### ContentGenerationRequest
**Description**: Represents a user request for content generation with all required parameters

**Fields**:
- `id` (str): Unique identifier for the request
- `topic` (str): Main subject or theme for content generation
- `audience` (str): Target audience for the content
- `tone` (str): Desired tone of the content (professional, casual, formal, etc.)
- `style` (str): Writing style preferences (narrative, informative, persuasive, etc.)
- `format` (str): Content format (blog_post, social_media, product_description, etc.)
- `length` (int): Target length in words
- `keywords` (List[str]): SEO keywords to incorporate naturally
- `created_at` (datetime): Timestamp of request creation
- `user_id` (str): Identifier for the requesting user

**Validation rules**:
- Topic is required and must be between 5-200 characters
- Audience must be specified from predefined options
- Length must be between 100-5000 words
- Keywords list must not exceed 10 items

### ContentGenerationResponse
**Description**: Represents the result of a content generation request

**Fields**:
- `id` (str): Unique identifier matching the request
- `content` (str): Generated content text
- `word_count` (int): Actual word count of generated content
- `quality_score` (float): Score representing content quality (0.0-1.0)
- `generation_time` (float): Time taken to generate content in seconds
- `status` (str): Status of the generation process (success, error, partial)
- `feedback` (str): Optional feedback about the generation process
- `timestamp` (datetime): Time of response creation

**Validation rules**:
- Content must not be empty when status is 'success'
- Quality score must be between 0.0 and 1.0
- Generation time must be positive

### UserPreferences
**Description**: Stores user preferences for content generation

**Fields**:
- `user_id` (str): Unique identifier for the user
- `default_audience` (str): Default target audience
- `default_tone` (str): Default content tone
- `default_format` (str): Default content format
- `preferred_keywords` (List[str]): Default keywords to include
- `last_updated` (datetime): Timestamp of last preference update

**Validation rules**:
- User ID is required and must be unique
- Default values must be from predefined options

## Relationships
- One `UserPreferences` entity can be associated with multiple `ContentGenerationRequest` entities
- Each `ContentGenerationRequest` has exactly one `ContentGenerationResponse`

## State Transitions
- `ContentGenerationRequest` transitions from 'created' → 'processing' → 'completed'/'failed'
- Status of `ContentGenerationResponse` is set upon completion of generation