from bs4 import BeautifulSoup
import aiohttp
import asyncio
import random

class AsyncWebCrawler:
    def __init__(self, verbose=False):
"""
Initialize the AsyncWebCrawler instance.

Args:
    verbose (bool): If True, enables verbose output for debugging. Defaults to False.

Attributes:
    headers (dict): HTTP headers to be used for the requests, including a User-Agent.
"""
        self.verbose = verbose
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    async def __aenter__(self):
        """
        Initialize the aiohttp session when entering the context manager.

        Returns:
            AsyncWebCrawler: The current instance.
        """
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Close the aiohttp session when exiting the context manager.

        Args:
            exc_type: The type of exception thrown, if any.
            exc_val: The exception instance.
            exc_tb: The traceback.
        """
        await self.session.close()
        
    async def arun(self, url, extraction_strategy=None):
        """
        Asynchronously crawl the given URL and extract relevant content using the
        given extraction strategy.

        Args:
            url (str): The URL to crawl.
            extraction_strategy (ExtractionStrategy): An optional extraction strategy
                to use for extracting content. If not provided, a default extraction
                strategy is used.

        Returns:
            ScrapingResult: An instance containing the raw and extracted content.

        Raises:
            Exception: If there is an error crawling the URL.
        """
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    if extraction_strategy:
                        extracted_content = await extraction_strategy.extract(html)
                    else:
                        extracted_content = clean_body_content(extract_body_content(html))
                    await asyncio.sleep(random.uniform(1, 3))
                    return ScrapingResult(
                        raw_content=html,
                        extracted_content=extracted_content
                    )
                else:
                    raise Exception(f"HTTP {response.status} error for URL: {url}")
        except Exception as e:
            if self.verbose:
                print(f"Error crawling {url}: {str(e)}")
            raise

class ScrapingResult:
    def __init__(self, raw_content, extracted_content):
        """
        Initialize a ScrapingResult instance.

        Args:
            raw_content (str): The raw, unprocessed content from the crawled URL.
            extracted_content (str): The extracted content from the crawled URL, using
                the specified extraction strategy.

        Attributes:
            raw_content (str): The raw, unprocessed content from the crawled URL.
            extracted_content (str): The extracted content from the crawled URL, using
                the specified extraction strategy.
        """
        self.raw_content = raw_content
        self.extracted_content = extracted_content

def extract_body_content(html_content):
    """
    Extract the body content from the given HTML content.

    Args:
        html_content (str): The HTML content to extract the body from.

    Returns:
        str: The body content as a string, or an empty string if no body is found.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    """
    Clean the given body content by removing unwanted elements and formatting the text.

    Args:
        body_content (str): The HTML body content to clean.

    Returns:
        str: The cleaned body content as a string.
    """

    soup = BeautifulSoup(body_content, "html.parser")
    for element in soup(["script", "style", "nav", "footer", "header"]):
        element.decompose()
    text = soup.get_text(separator="\n")
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = "\n".join(chunk for chunk in chunks if chunk)
    return text
