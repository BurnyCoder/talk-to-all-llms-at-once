#!/usr/bin/env python3
"""
Script to fetch all available models from OpenRouter API and save to models.txt.
Uses curl subprocess for the API request.
"""
import json
import os
import subprocess
from dotenv import load_dotenv


def get_openrouter_models():
    """
    Fetch all available models from OpenRouter API using curl.
    
    Returns:
        dict: The parsed JSON response containing model information
    """
    # Load API key from environment variables
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable not found")
    
    # Build the curl command
    curl_command = [
        "curl",
        "-s",  # Silent mode
        "-X", "GET",
        "https://openrouter.ai/api/v1/models",
        "-H", f"Authorization: Bearer {api_key}",
        "-H", "Content-Type: application/json"
    ]
    
    # Execute the curl command
    try:
        result = subprocess.run(
            curl_command,
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing curl command: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        raise
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        print(f"Response: {result.stdout}")
        raise


def save_models_to_file(models_data, filename="models.txt"):
    """
    Save the models data to a text file.
    
    Args:
        models_data (dict): The models data from OpenRouter API
        filename (str, optional): The filename to save to. Defaults to "models.txt".
    """
    with open(filename, 'w') as f:
        f.write("OpenRouter Available Models:\n")
        f.write("==========================\n\n")
        
        # Extract the data array from the response
        models = models_data.get('data', [])
        
        for model in models:
            model_id = model.get('id', 'Unknown')
            context_length = model.get('context_length', 'Unknown')
            pricing = model.get('pricing', {})
            
            f.write(f"Model ID: {model_id}\n")
            f.write(f"Context Length: {context_length}\n")
            
            if pricing:
                f.write("Pricing:\n")
                for key, value in pricing.items():
                    f.write(f"  - {key}: {value}\n")
            
            f.write("\n")
            
        f.write(f"\nTotal models available: {len(models)}\n")
        f.write(f"Data retrieved from: https://openrouter.ai/api/v1/models\n")


def main():
    """Main function to fetch models and save to file."""
    try:
        print("Fetching models from OpenRouter API...")
        models_data = get_openrouter_models()
        
        print("Saving models to models.txt...")
        save_models_to_file(models_data)
        
        print("Successfully saved models information to models.txt")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main() 