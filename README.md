# AI Scraper

AI Scraper is a powerful tool that combines web scraping capabilities with AI-powered content parsing. It features a Streamlit interface, async web crawling, and intelligent content extraction powered by Ollama LLM.

## Features

- Simple and Advanced scraping modes
- Asynchronous web crawling with aiohttp
- AI-powered content extraction using Ollama LLM
- Captcha solving integration with Scraping Browser
- Configurable extraction strategies
- User-friendly interface with animated components
- Content chunking for efficient processing

## Prerequisites

- Python 3.7+
- [Ollama](https://ollama.ai/) installed and running with `llama3.1` model
- Access to a Scraping Browser remote WebDriver
- Required Python packages (see Installation)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/newtglobalgit/ai-scraper.git
   cd ai-scraper
   ```

2. Create a virtual environment:
   ```bash
   python -m venv ai
   source ai/bin/activate  # On Windows, use `ai\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root and add:
   ```
   SBR_WEBDRIVER=<Your Scraping Browser WebDriver URL>
   ```

## Usage

1. Ensure Ollama is running with the `llama3.1` model loaded.

2. Start the Streamlit app:
   ```bash
   streamlit run main.py
   ```

3. Using the application:
   - Choose between Simple and Advanced scraping modes
   - Enter a website URL to scrape
   - In Advanced mode, provide specific extraction instructions
   - View the scraped content in the expandable section
   - Provide parsing instructions for AI-powered content extraction
   - Review the parsed results

## Project Structure

- `main.py`: Streamlit application with UI components and main workflow
- `scrape.py`: Handles web scraping, async crawling, and content processing
  - `AsyncWebCrawler`: Asynchronous web crawling implementation
  - `ScrapingResult`: Data class for crawling results
  - Content processing utilities (cleaning, chunking)
- `extraction_strategy.py`: Defines extraction strategy interface and LLM implementation
  - `ExtractionStrategy`: Abstract base class for extraction strategies
  - `LLMExtractionStrategy`: Ollama-based extraction implementation
- `parse.py`: Manages AI-powered content parsing using Ollama LLM

## Key Components

### Extraction Strategy

The system uses a flexible extraction strategy pattern:
```python
class ExtractionStrategy(ABC):
    @abstractmethod
    async def extract(self, content):
        pass
```

### Async Web Crawler

Asynchronous web crawling with context management:
```python
async with AsyncWebCrawler(verbose=True) as crawler:
    result = await crawler.arun(url, extraction_strategy)
```

### Content Processing

- DOM content extraction and cleaning
- Content chunking for efficient processing
- Captcha solving integration
- Custom parsing with LLM

## Troubleshooting

- Verify the `SBR_WEBDRIVER` environment variable is correctly set
- Ensure Ollama is running and the `llama3.1` model is available
- Check console output for error messages and debugging information
- For captcha-related issues, verify Scraping Browser configuration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
