import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4-turbo-preview"

# Streamlit Configuration
PAGE_TITLE = "SEO Content Generator"
PAGE_ICON = "📝"

# Content Generation Settings
MAX_TOKENS = 4000
TEMPERATURE = 0.7