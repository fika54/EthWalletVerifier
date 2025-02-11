# backend/utils/config.py

import os

# >>> FILL HERE: Real or mock Flare FDC endpoint
FLARE_FDC_URL = os.getenv("FLARE_FDC_URL", "https://fakeflare.io/fdc/check-wallet")

# >>> FILL HERE: Your OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-YourKeyGoesHere")

# >>> FILL HERE (Optional): Any other config variables you need
# e.g., SECRET_KEY = os.getenv("SECRET_KEY", "some-secret")
