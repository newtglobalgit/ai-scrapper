from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import sys
import aiohttp
import asyncio

load_dotenv()

SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")

class AsyncWebCrawler:
    def __init__(self, verbose=False):
        self.verbose = verbose
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
        
    async def arun(self, url, extraction_strategy=None, bypass_cache=False):
        try:
            async with self.session.get(url) as response:
                html = await response.text()
                if extraction_strategy:
                    extracted_content = await extraction_strategy.extract(html)
                else:
                    extracted_content = clean_body_content(extract_body_content(html))
                return ScrapingResult(
                    raw_content=html,
                    extracted_content=extracted_content
                )
        except Exception as e:
            if self.verbose:
                print(f"Error crawling {url}: {str(e)}")
            raise

class ScrapingResult:
    def __init__(self, raw_content, extracted_content):
        self.raw_content = raw_content
        self.extracted_content = extracted_content

def scrape_website(website):
    if not SBR_WEBDRIVER:
        raise ValueError("SBR_WEBDRIVER environment variable is not set.")
    print("Connecting to Scraping Browser...")
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
    try:
        with Remote(sbr_connection, options=ChromeOptions()) as driver:
            driver.get(website)
            print("Waiting for captcha to solve...")
            solve_res = driver.execute(
                "executeCdpCommand",
                {
                    "cmd": "Captcha.waitForSolve",
                    "params": {"detectTimeout": 10000},
                },
            )
            print("Captcha solve status:", solve_res["value"]["status"])
            print("Navigated! Scraping page content...")
            html = driver.page_source
            return html
    except Exception as e:
        print(f"Error connecting to Scraping Browser: {str(e)}", file=sys.stderr)
        raise

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
