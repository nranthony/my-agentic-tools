# API Integrations

Unified API wrappers and client libraries for various AI and productivity services.

## Integrations Included

- **OpenAI Client**: GPT, DALL-E, Whisper APIs
- **Anthropic Client**: Claude API with streaming
- **Google APIs**: Search, Translate, Drive, Sheets
- **Social Media APIs**: Twitter, LinkedIn, Reddit
- **Productivity APIs**: Notion, Airtable, Slack
- **Data APIs**: Alpha Vantage, News API, Weather

## Key Features

- Consistent interface across different APIs
- Automatic retry logic with exponential backoff
- Rate limiting and quota management  
- Response caching and optimization
- Error handling and logging
- Async/await support

## Installation

```bash
# From root directory
pip install -e .[api-integrations]

# Or install individually
cd api-integrations && pip install -e .
```

## Configuration

Set up API credentials:

```bash
# Core AI APIs
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Social Media
TWITTER_BEARER_TOKEN=your_twitter_token
LINKEDIN_CLIENT_ID=your_linkedin_id

# Productivity  
NOTION_API_KEY=your_notion_key
SLACK_BOT_TOKEN=your_slack_token

# Data Services
NEWS_API_KEY=your_news_api_key
ALPHA_VANTAGE_KEY=your_av_key
```

## Quick Start

```python
from api_integrations.openai_client import OpenAIClient
from api_integrations.notion_client import NotionClient

# AI completion
ai = OpenAIClient()
response = await ai.chat_completion([
    {"role": "user", "content": "Explain quantum computing"}
])

# Notion integration
notion = NotionClient()
page = await notion.create_page(
    parent_id="database_id",
    title="Meeting Notes",
    content="Today we discussed..."
)
```

## Unified Interface

All clients implement common patterns:

```python
from api_integrations.base import BaseAPIClient

class CustomClient(BaseAPIClient):
    def __init__(self):
        super().__init__(
            base_url="https://api.example.com",
            rate_limit=100,  # requests per minute
            timeout=30
        )
    
    async def custom_method(self, data):
        return await self.make_request("POST", "/endpoint", data)
```

## Utilities

- **Response Parser**: Extract structured data from API responses
- **Batch Processor**: Handle bulk operations efficiently  
- **Cache Manager**: Redis/SQLite caching layer
- **Webhook Handler**: Process incoming webhooks
- **Rate Limiter**: Token bucket implementation