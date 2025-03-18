# Talk to All LLMs at Once

A tool for simultaneously querying multiple leading language models through the OpenRouter API and comparing their responses side by side.

## 🌟 Features

- **Parallel Querying**: Send the same prompt to multiple top LLMs simultaneously
- **Performance Metrics**: Compare response times and token usage
- **Rich Display**: View results in a beautifully formatted console output
- **Result Persistence**: Save all responses and metrics to JSON files for later analysis
- **Clean API Integration**: Uses an OpenRouterClient wrapper for simplified API interactions

## 📋 Supported Models

Currently queries these state-of-the-art models in parallel:

- **Claude 3.7 Sonnet** (Anthropic's advanced model)
- **Gemini Pro 1.5** (Google's large language model)
- **O1** (OpenAI's most advanced model)

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- An [OpenRouter API key](https://openrouter.ai/)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/talk-to-all-llms-at-once.git
   cd talk-to-all-llms-at-once
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your API key:
   - Copy the template env file:
     ```bash
     cp .env.template .env
     ```
   - Edit the `.env` file and add your OpenRouter API key:
     ```
     OPENROUTER_API_KEY=your_openrouter_api_key_here
     ```
   - Or set it as an environment variable:
     ```bash
     export OPENROUTER_API_KEY=your_openrouter_api_key_here
     ```

## 💻 Usage

Run the main script:

```bash
python parallel_query.py
```

You'll be prompted to enter your query, and then the script will:
1. Send your prompt to all models in parallel
2. Display performance metrics and responses from each model
3. Save all results to a time-stamped JSON file

## 📊 Example Output

The script provides a rich console output showing:

- Your original prompt
- A performance metrics table comparing all models
- The full response from each model with timing information
- A confirmation of where results were saved

## 🧩 How It Works

The script uses a modular approach:

1. **OpenRouterClient**: A clean wrapper around the OpenRouter API, handling authentication and request formatting
2. **ThreadPoolExecutor**: For parallel execution of API requests to different models
3. **Rich Console**: For beautiful terminal output with colors and formatting

Here's the core function that queries the models in parallel:

```python
def query_models_in_parallel(prompt):
    """
    Query multiple models in parallel and return their responses.
    """
    # Models to query
    models = [
        "anthropic/claude-3.7-sonnet",
        "google/gemini-pro-1.5",
        "openai/o1"
    ]
    
    # Create the OpenRouter client
    client = OpenRouterClient(
        site_url="https://talk-to-all-llms-at-once",
        site_name="LLM Comparison Tool"
    )
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(models)) as executor:
        # Start the query operations and mark each future with its model
        future_to_model = {
            executor.submit(query_model, model_id, prompt, client): model_id
            for model_id in models
        }
        
        results = []
        for future in concurrent.futures.as_completed(future_to_model):
            results.append(future.result())
            
    return results
```

## 📝 Additional Features

### Available Models Listing

This project also includes a utility to list all available models from OpenRouter with detailed information:

```bash
python list_models.py
```

This will generate a `models.txt` file with comprehensive information about all available models on OpenRouter, sorted by price (from most expensive to least expensive).

### OpenRouter Client Wrapper

The project includes a clean OpenRouter client wrapper (`openrouter.py`) that simplifies interactions with the API:

```python
from openrouter import OpenRouterClient

# Create client
client = OpenRouterClient()

# Generate completion
response = client.generate_completion([
    {"role": "user", "content": "What is the meaning of life?"}
])

# Get the response
print(response.choices[0].message.content)
```

## 🛠️ Customization

### Adding or Changing Models

To modify which models are queried, edit the `models` list in the `query_models_in_parallel` function:

```python
# Models to query
models = [
    "anthropic/claude-3.7-sonnet",
    "google/gemini-pro-1.5", 
    "openai/o1"
    # Add or replace models here
]
```

Refer to the generated `models.txt` file for a comprehensive list of available models on OpenRouter.

## 📊 Data Analysis

The saved JSON files can be used for:
- Comparing model performance across different types of prompts
- Analyzing response patterns and differences
- Creating visualizations of model performance
- Building datasets of comparative model responses

## 🔒 Security Notes

- Your API key should be kept confidential
- This tool accesses paid API services that may incur costs
- Be mindful of token usage when sending large prompts

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [OpenRouter](https://openrouter.ai/) for providing unified access to multiple LLM APIs
- The teams at Anthropic, Google, and OpenAI for developing these amazing models
