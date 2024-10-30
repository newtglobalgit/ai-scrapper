from bs4 import BeautifulSoup
import json

class Parser:
    @staticmethod 
    def parse_html(html_content, parser="html.parser"):
        """Parse HTML content using BeautifulSoup"""
        return BeautifulSoup(html_content, parser)
    
    @staticmethod
    def extract_text(soup, selector):
        """Extract text from elements matching CSS selector"""
        elements = soup.select(selector)
        return [element.get_text(strip=True) for element in elements]
    
    @staticmethod
    def extract_links(soup, selector): 
        """Extract links from elements matching CSS selector"""
        elements = soup.select(selector)
        return [element.get('href') for element in elements if element.get('href')]

    @staticmethod
    def parse_json_content(extracted_content):
        """Parse JSON content from extracted text"""
        try:
            if isinstance(extracted_content, str):
                return json.loads(extracted_content)
            return extracted_content
        except json.JSONDecodeError:
            return None
