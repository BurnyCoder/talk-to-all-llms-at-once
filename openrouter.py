import os
from dotenv import load_dotenv
from openai import OpenAI


class OpenRouterClient:
    """A client for interacting with the OpenRouter API."""
    
    def __init__(self, site_url=None, site_name=None):
        """
        Initialize the OpenRouter client.
        
        Args:
            site_url (str, optional): Site URL for rankings on openrouter.ai
            site_name (str, optional): Site title for rankings on openrouter.ai
        """
        # Load environment variables from .env file
        load_dotenv()
        
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ.get("OPENROUTER_API_KEY"),
        )
        
        # self.extra_headers = {
        #     "HTTP-Referer": site_url or "<YOUR_SITE_URL>",
        #     "X-Title": site_name or "<YOUR_SITE_NAME>",
        # }
    
    def generate_completion(self, messages, model="openai/gpt-4o"):
        """
        Generate a completion using the OpenRouter API.
        
        Args:
            messages (list): List of message dictionaries
            model (str, optional): Model to use for completion
            
        Returns:
            str: The generated completion text
        """
        completion = self.client.chat.completions.create(
            #extra_headers=self.extra_headers,
            model=model,
            messages=messages
        )
        
        return completion
    
    def generate_answer(self, messages, model="openai/gpt-4o"):
        """
        Generate a completion using the OpenRouter API.
        
        Args:
            messages (list): List of message dictionaries
            model (str, optional): Model to use for completion
            
        Returns:
            str: The generated completion text
        """
        completion = self.client.chat.completions.create(
            #extra_headers=self.extra_headers,
            model=model,
            messages=messages
        )
        
        return completion.choices[0].message.content


# Example usage
if __name__ == "__main__":
    router = OpenRouterClient()
    response = router.generate_answer([
        {
            "role": "user",
            "content": "What is the meaning of life?"
        }
    ])
    
    print(response)