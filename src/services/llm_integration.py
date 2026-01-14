from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import asyncio
import openai
import anthropic
from ..config.settings import settings
from ..models.content_generation import (
    ContentGenerationRequest,
    ContentGenerationResponse,
    AudienceEnum,
    ToneEnum,
    StyleEnum,
    FormatEnum
)


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""

    @abstractmethod
    async def generate_content(self, request: ContentGenerationRequest) -> str:
        """Generate content based on the request"""
        pass


class OpenAILLMProvider(LLMProvider):
    """OpenAI implementation of LLM provider"""

    def __init__(self):
        if settings.openai_api_key:
            openai.api_key = settings.openai_api_key
        else:
            raise ValueError("OpenAI API key is required")

    async def generate_content(self, request: ContentGenerationRequest) -> str:
        """Generate content using OpenAI's API"""
        try:
            # Prepare the prompt based on the request
            prompt = self._construct_prompt(request)

            # Use async call to OpenAI API
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",  # Could be configurable
                messages=[
                    {"role": "system", "content": "You are an expert content writer who creates high-quality, original content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=settings.max_tokens,
                temperature=settings.temperature
            )

            # Extract the generated content
            content = response.choices[0].message.content.strip()
            return content

        except Exception as e:
            raise Exception(f"Error generating content with OpenAI: {str(e)}")

    def _construct_prompt(self, request: ContentGenerationRequest) -> str:
        """Construct the prompt based on the request parameters"""
        # Determine audience description
        audience_map = {
            AudienceEnum.GENERAL_PUBLIC: "a general audience",
            AudienceEnum.EXPERTS: "expert professionals",
            AudienceEnum.STUDENTS: "students",
            AudienceEnum.BUSINESS_PROFESSIONALS: "business professionals",
            AudienceEnum.ENVIRONMENTAL_ADVOCATES: "environmental advocates"
        }

        # Determine tone description
        tone_map = {
            ToneEnum.FORMAL: "formal and professional",
            ToneEnum.CASUAL: "casual and conversational",
            ToneEnum.PROFESSIONAL: "professional and business-appropriate",
            ToneEnum.INFORMATIVE: "informative and educational",
            ToneEnum.PERSUASIVE: "persuasive and compelling",
            ToneEnum.HUMOROUS: "humorous and light-hearted"
        }

        # Determine style description
        style_map = {
            StyleEnum.NARRATIVE: "narrative storytelling",
            StyleEnum.INFORMATIVE: "informative and factual",
            StyleEnum.PERSUASIVE: "persuasive and argumentative",
            StyleEnum.DESCRIPTIVE: "descriptive and vivid",
            StyleEnum.EDUCATIONAL: "educational and instructional"
        }

        # Construct the prompt
        prompt_parts = [
            f"Write content about '{request.topic}'",
            f"Target audience: {audience_map[request.audience]}",
            f"Tone: {tone_map[request.tone]}",
            f"Style: {style_map[request.style]}",
            f"Format: {request.format.value.replace('_', ' ').title()}",
            f"Target length: approximately {request.length} words"
        ]

        if request.keywords:
            prompt_parts.append(f"Include these keywords naturally: {', '.join(request.keywords)}")

        prompt = ". ".join(prompt_parts) + "."
        return prompt


class AnthropicLLMProvider(LLMProvider):
    """Anthropic implementation of LLM provider"""

    def __init__(self):
        if settings.anthropic_api_key:
            self.client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
        else:
            raise ValueError("Anthropic API key is required")

    async def generate_content(self, request: ContentGenerationRequest) -> str:
        """Generate content using Anthropic's API"""
        try:
            # Prepare the prompt based on the request
            prompt = self._construct_prompt(request)

            # Use async call to Anthropic API
            response = await self.client.messages.create(
                model="claude-3-haiku-20240307",  # Could be configurable
                max_tokens=settings.max_tokens,
                temperature=settings.temperature,
                system="You are an expert content writer who creates high-quality, original content.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract the generated content
            content = response.content[0].text.strip()
            return content

        except Exception as e:
            raise Exception(f"Error generating content with Anthropic: {str(e)}")

    def _construct_prompt(self, request: ContentGenerationRequest) -> str:
        """Construct the prompt based on the request parameters"""
        # Determine audience description
        audience_map = {
            AudienceEnum.GENERAL_PUBLIC: "a general audience",
            AudienceEnum.EXPERTS: "expert professionals",
            AudienceEnum.STUDENTS: "students",
            AudienceEnum.BUSINESS_PROFESSIONALS: "business professionals",
            AudienceEnum.ENVIRONMENTAL_ADVOCATES: "environmental advocates"
        }

        # Determine tone description
        tone_map = {
            ToneEnum.FORMAL: "formal and professional",
            ToneEnum.CASUAL: "casual and conversational",
            ToneEnum.PROFESSIONAL: "professional and business-appropriate",
            ToneEnum.INFORMATIVE: "informative and educational",
            ToneEnum.PERSUASIVE: "persuasive and compelling",
            ToneEnum.HUMOROUS: "humorous and light-hearted"
        }

        # Determine style description
        style_map = {
            StyleEnum.NARRATIVE: "narrative storytelling",
            StyleEnum.INFORMATIVE: "informative and factual",
            StyleEnum.PERSUASIVE: "persuasive and argumentative",
            StyleEnum.DESCRIPTIVE: "descriptive and vivid",
            StyleEnum.EDUCATIONAL: "educational and instructional"
        }

        # Construct the prompt
        prompt_parts = [
            f"Write content about '{request.topic}'",
            f"Target audience: {audience_map[request.audience]}",
            f"Tone: {tone_map[request.tone]}",
            f"Style: {style_map[request.style]}",
            f"Format: {request.format.value.replace('_', ' ').title()}",
            f"Target length: approximately {request.length} words"
        ]

        if request.keywords:
            prompt_parts.append(f"Include these keywords naturally: {', '.join(request.keywords)}")

        prompt = ". ".join(prompt_parts) + "."
        return prompt


def get_llm_provider() -> LLMProvider:
    """Factory function to get the appropriate LLM provider based on settings"""
    if settings.llm_provider == "openai":
        return OpenAILLMProvider()
    elif settings.llm_provider == "anthropic":
        return AnthropicLLMProvider()
    else:
        raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")