#!/usr/bin/env python3
"""
Script to call multiple LLM models in parallel via OpenRouter API and compare their outputs.
Models are loaded from the models list provided by the user.
"""
import json
import time
import concurrent.futures
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from datetime import datetime
from openrouter import OpenRouterClient

# Initialize rich console for nicer output
console = Console()

# List of models to query
MODELS = [
    "anthropic/claude-3-7-sonnet-thinking",
    "openai/o3-mini-2025-01-31-high",
    "openai/o1-2024-12-17-high",
    "xai/grok-3-thinking",
    "alibaba/qwq-32b",
    "deepseek/deepseek-r1",
    "openai/o3-mini-2025-01-31-medium",
    "openai/gpt-4.5-preview",
    "google/gemini-2.0-flash-thinking-exp-01-21",
    "anthropic/claude-3-7-sonnet",
    "google/gemini-2.0-pro-exp-02-05",
    "google/gemini-exp-1206",
    "openai/o3-mini-2025-01-31-low",
    "alibaba/qwen2.5-max",
    "google/gemini-2.0-flash",
    "deepseek/deepseek-v3",
    "google/gemini-2.0-flash-exp",
    "anthropic/claude-3-5-sonnet-20241022",
    "xai/grok-3",
    "openai/chatgpt-4o-latest-2025-01-29",
    "openai/o1-mini-2024-09-12",
    "stepfun/step-2-16k-202411",
    "openai/gpt-4o-2024-08-06",
    "deepseek/deepseek-r1-distill-llama-70b",
    "xai/grok-2-1212",
    "google/gemini-2.0-flash-lite",
    "google/gemini-2.0-flash-lite-preview-02-05",
    "abacusai/dracarys2-72b-instruct",
    "meta/meta-llama-3.1-405b-instruct-turbo",
    "openai/gpt-4o-2024-11-20",
    "google/learnlm-1.5-pro-experimental",
    "alibaba/qwen2.5-72b-instruct-turbo",
    "meta/llama-3.3-70b-instruct-turbo",
    "google/gemma-3-27b-it"
]

def query_model(model_id, prompt, client):
    """
    Query a specific model through OpenRouter API.
    
    Args:
        model_id (str): The ID of the model to query
        prompt (str): The prompt to send to the model
        client (OpenRouterClient): The OpenRouter client instance
        
    Returns:
        dict: The response from the model with relevant metadata
    """
    messages = [{"role": "user", "content": prompt}]
    
    start_time = time.time()
    
    try:
        completion = client.generate_completion(messages, model=model_id)
        
        elapsed_time = time.time() - start_time
        
        # Extract completion text and add timing information
        return {
            "model_id": model_id,
            "model_name": completion.model,
            "response": completion.choices[0].message.content,
            "elapsed_time": elapsed_time,
            "finish_reason": completion.choices[0].finish_reason,
            "tokens": {
                "prompt": completion.usage.prompt_tokens,
                "completion": completion.usage.completion_tokens,
                "total": completion.usage.total_tokens
            }
        }
    except Exception as e:
        console.print(f"[bold red]Error querying {model_id}:[/bold red] {str(e)}")
        return {
            "model_id": model_id,
            "model_name": model_id,
            "response": f"Error: {str(e)}",
            "elapsed_time": time.time() - start_time,
            "finish_reason": "error",
            "tokens": {"prompt": 0, "completion": 0, "total": 0}
        }

def query_models_in_parallel(prompt):
    """
    Query multiple models in parallel and return their responses.
    
    Args:
        prompt (str): The prompt to send to all models
        
    Returns:
        list: A list of response dictionaries from each model
    """
    # Create the OpenRouter client
    client = OpenRouterClient(
        site_url="https://talk-to-all-llms-at-once",
        site_name="LLM Comparison Tool"
    )
    
    # Use ThreadPoolExecutor to query models in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(MODELS)) as executor:
        # Start the query operations and mark each future with its model
        future_to_model = {
            executor.submit(query_model, model_id, prompt, client): model_id
            for model_id in MODELS
        }
        
        results = []
        for future in concurrent.futures.as_completed(future_to_model):
            results.append(future.result())
            
    return results

def display_results(results, prompt):
    """
    Display the results from multiple models in a nicely formatted way.
    
    Args:
        results (list): List of response dictionaries
        prompt (str): The original prompt
    """
    # Sort results by elapsed time
    results.sort(key=lambda x: x["elapsed_time"])
    
    # Create a table to show performance metrics
    metrics_table = Table(title="Model Performance Metrics")
    metrics_table.add_column("Model", style="cyan")
    metrics_table.add_column("Response Time", style="green")
    metrics_table.add_column("Tokens (Prompt)", style="yellow")
    metrics_table.add_column("Tokens (Completion)", style="yellow")
    metrics_table.add_column("Tokens (Total)", style="yellow")
    metrics_table.add_column("Finish Reason", style="magenta")
    
    for result in results:
        metrics_table.add_row(
            result["model_name"],
            f"{result['elapsed_time']:.2f}s",
            str(result["tokens"]["prompt"]),
            str(result["tokens"]["completion"]),
            str(result["tokens"]["total"]),
            result["finish_reason"]
        )
    
    console.print("\n")
    console.print(Panel(prompt, title="Prompt", border_style="blue"))
    console.print("\n")
    console.print(metrics_table)
    console.print("\n")
    
    # Display each model's response in a panel
    for result in results:
        console.print(Panel(
            result["response"],
            title=f"{result['model_name']} ({result['elapsed_time']:.2f}s)",
            border_style="green"
        ))
        console.print("\n")
    
    # Save results to a file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"comparison_results_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump({
            "prompt": prompt,
            "timestamp": timestamp,
            "results": results
        }, f, indent=2)
    
    console.print(f"[bold green]Results saved to:[/bold green] {filename}")

def main():
    """Main function to query models and display results."""
    console.print("[bold blue]Multi-Model Comparison Tool[/bold blue]")
    console.print(f"[italic]Compare responses from {len(MODELS)} models[/italic]\n")
    
    # Get the prompt from the user
    prompt = console.input("[bold cyan]Enter your prompt:[/bold cyan]\n")
    
    if not prompt.strip():
        console.print("[bold red]Prompt cannot be empty. Exiting.[/bold red]")
        return
    
    console.print(f"\n[bold yellow]Querying {len(MODELS)} models in parallel...[/bold yellow]")
    
    try:
        results = query_models_in_parallel(prompt)
        display_results(results, prompt)
    except Exception as e:
        console.print(f"[bold red]An error occurred:[/bold red] {str(e)}")

if __name__ == "__main__":
    main() 