#!/usr/bin/env python3
"""
Simplest possible script to call Claude 3.7 Sonnet via OpenRouter.
"""
import os
from dotenv import load_dotenv
from openrouter import OpenRouterClient

# Load API key from .env file
load_dotenv()

# Create OpenRouter client
client = OpenRouterClient()

# Get user prompt
prompt = input("Enter your prompt for Claude 3.7 Sonnet: ")

# Call Claude 3.7 Sonnet
response = client.client.chat.completions.create(
    model="anthropic/claude-3-7-sonnet",
    messages=[{"role": "user", "content": prompt}]
)

# Print the response
print("\n--- Claude 3.7 Sonnet Response ---\n")
print(response.choices[0].message.content)
print("\n---------------------------------\n") 