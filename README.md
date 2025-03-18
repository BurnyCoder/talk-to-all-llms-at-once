# Talk to All LLMs at Once

A tool for simultaneously querying multiple leading language models through the OpenRouter API and comparing their responses side by side.

## 🌟 Features

- **Parallel Querying**: Send the same prompt to multiple top LLMs simultaneously
- **Performance Metrics**: Compare response times and token usage
- **Rich Display**: View results in a beautifully formatted console output
- **Result Persistence**: Save all responses and metrics to JSON files for later analysis
- **Clean API Integration**: Uses an OpenRouterClient wrapper for simplified API interactions

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

## 📝 Additional Features

### Available Models Listing

This project also includes a utility to list all available models from OpenRouter with detailed information:

```bash
python list_models.py
```

This will generate a `models.txt` file with comprehensive information about all available models on OpenRouter, sorted by price (from most expensive to least expensive).

## 🛠️ Customization

### Modifying the Model List

The models list is defined at the top of the `parallel_query.py` file. You can easily modify this list to include or exclude specific models:

```python
# List of models to query
MODELS = [
    "anthropic/claude-3-7-sonnet-thinking",
    "openai/o3-mini-2025-01-31-high",
    # Add or remove models as needed
]
```

Refer to the generated `models.txt` file or `models.json` for a comprehensive list of available models on OpenRouter.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [OpenRouter](https://openrouter.ai/) for providing unified access to multiple LLM APIs
- The teams at Anthropic, Google, OpenAI, Meta, xAI, Alibaba, DeepSeek, and other AI labs for developing these amazing models
