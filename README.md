# AI Scraper

A modular web scraping tool designed for extracting and processing information from various sources.

## Project Structure

- `main.py`: Entry point of the application, orchestrates the scraping and parsing workflow
- `scrape.py`: Contains web scraping functionality and related utilities
- `parse.py`: Handles parsing and processing of scraped data 
- `extraction_strategy.py`: Defines different strategies for data extraction
- `requirements.txt`: Lists project dependencies
- `run_streamlit_app.sh`: Script to launch the Streamlit interface
- `.env.example`: Template for environment variables configuration

## Setup

1. Clone the repository
2. Create a virtual environment:
- python -m venv venv source venv/bin/activate # On Windows: venv\Scripts\activate
3. Install dependencies:
- pip install -r requirements.txt
4. Copy `.env.example` to `.env` and configure your settings

## Usage

### Streamlit Interface
-  streamlit run main.py

## Features

- Modular design with separate scraping and parsing components
- Multiple extraction strategies support
- Configurable through environment variables
- Web interface powered by Streamlit

## License

See [LICENSE](LICENSE) file for details.
