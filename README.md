# AI Web Scraper

AI Web Scraper is a powerful tool that combines web scraping capabilities with AI-powered content parsing. It uses Streamlit for the user interface, Selenium for web scraping, and Ollama LLM for intelligent content extraction.

## Features

- Web scraping with Selenium and BeautifulSoup
- Captcha solving integration
- AI-powered content parsing using Ollama LLM
- User-friendly interface with Streamlit

## Prerequisites

- Python 3.7+
- [Ollama](https://ollama.ai/) installed and running
- Access to a Scraping Browser remote WebDriver

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-web-scraper.git
   cd ai-web-scraper
   ```

2. Create a virtual environment:
   ```
   python -m venv ai
   source ai/bin/activate  # On Windows, use `ai\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root and add the following:
   ```
   SBR_WEBDRIVER=<Your Scraping Browser WebDriver URL>
   ```

## Usage

1. Ensure Ollama is running with the `llama3.2` model loaded.

2. Start the Streamlit app:
   ```
   bash run_streamlit_app.sh
   ```
   Or run directly with:
   ```
   streamlit run main.py
   ```

3. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

4. Enter a website URL in the input field and click "Scrape Website".

5. Once the content is scraped, you can view the DOM content in the expandable section.

6. Enter a description of what you want to parse from the content and click "Parse Content".

7. The AI will extract the requested information and display it on the page.

## Project Structure

- `main.py`: The main Streamlit application
- `scrape.py`: Contains functions for web scraping and content cleaning
- `parse.py`: Handles the AI-powered content parsing using Ollama
- `requirements.txt`: List of Python dependencies
- `run_streamlit_app.sh`: Shell script to run the Streamlit app

## Troubleshooting

- If you encounter issues with the Scraping Browser, ensure the `SBR_WEBDRIVER` environment variable is correctly set.
- Make sure Ollama is running and the `llama3.2` model is available.
- Check the console output for any error messages or debugging information.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
