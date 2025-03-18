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
    Save the models data to a text file, sorted by price from priciest to cheapest.
    Includes all available information for each model.
    
    Args:
        models_data (dict): The models data from OpenRouter API
        filename (str, optional): The filename to save to. Defaults to "models.txt".
    """
    with open(filename, 'w') as f:
        f.write("OpenRouter Available Models:\n")
        f.write("Sorted by Price (priciest to cheapest):\n")
        f.write("==========================\n\n")
        
        # Extract the data array from the response
        models = models_data.get('data', [])
        
        # Define a function to calculate total price for sorting
        def get_total_price(model):
            pricing = model.get('pricing', {})
            prompt_price = float(pricing.get('prompt', 0))
            completion_price = float(pricing.get('completion', 0))
            return prompt_price + completion_price
        
        # Sort models by total price (prompt + completion) in descending order
        sorted_models = sorted(models, key=get_total_price, reverse=True)
        
        for model in sorted_models:
            # Calculate total price for display
            pricing = model.get('pricing', {})
            prompt_price = float(pricing.get('prompt', 0))
            completion_price = float(pricing.get('completion', 0))
            total_price = prompt_price + completion_price
            
            # Display model ID and total price first for easier reference
            f.write(f"Model ID: {model.get('id', 'Unknown')}\n")
            f.write(f"Total Price (prompt + completion): {total_price:.10f}\n")
            
            # Now display all available fields for the model
            for key, value in model.items():
                if key == 'id':
                    # Already displayed at the top
                    continue
                
                if key == 'pricing':
                    # Pricing is displayed in a special format
                    f.write("Pricing:\n")
                    for price_key, price_value in value.items():
                        f.write(f"  - {price_key}: {price_value}\n")
                elif isinstance(value, dict):
                    # Handle nested dictionaries
                    f.write(f"{key.title()}:\n")
                    for sub_key, sub_value in value.items():
                        f.write(f"  - {sub_key}: {sub_value}\n")
                elif isinstance(value, list):
                    # Handle lists
                    f.write(f"{key.title()}:\n")
                    for item in value:
                        if isinstance(item, dict):
                            # If list contains dictionaries
                            for item_key, item_value in item.items():
                                f.write(f"  - {item_key}: {item_value}\n")
                        else:
                            f.write(f"  - {item}\n")
                else:
                    # Simple key-value pairs
                    f.write(f"{key.title()}: {value}\n")
            
            f.write("\n")
            f.write("-" * 50 + "\n\n")
            
        # Add summary information at the end
        f.write(f"Total models available: {len(models)}\n")
        f.write(f"Data retrieved from: https://openrouter.ai/api/v1/models\n")
        f.write(f"Models are sorted by total price (priciest to cheapest)\n")
        
        # Include any additional metadata from the API response
        for key, value in models_data.items():
            if key != 'data':  # Skip the models array which we've already processed
                f.write(f"\n{key.title()}: {value}\n")


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