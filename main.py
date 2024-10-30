import streamlit as st
import asyncio
from scrape import AsyncWebCrawler
from extraction_strategy import LLMExtractionStrategy, SimpleTextExtractionStrategy
import polars as pl
from bs4 import BeautifulSoup
import aiohttp
from typing import List, Dict

st.set_page_config(
    page_title="AI Scraper",
    page_icon="🌐",
    layout="wide"
)

if 'scraping_results' not in st.session_state:
    st.session_state.scraping_results = []

class WebSearcher:
    def __init__(self):
        """
        Initialize a WebSearcher instance.

        Attributes:
            headers (dict): Default HTTP headers to use for web search requests.
        """
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    async def search(self, query: str, engine: str = "google", num_results: int = 5) -> List[str]:
        """
        Asynchronously search the web using the given search engine and query.

        Args:
            query (str): The search query.
            engine (str): The search engine to use. Defaults to "google".
            num_results (int): The number of results to return. Defaults to 5.

        Returns:
            List[str]: A list of URLs matching the search query.
        """
        if engine == "google":
            base_url = f"https://www.google.com/search?q={query}"
        else:
            base_url = f"https://www.bing.com/search?q={query}"
            
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(base_url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    if engine == "google":
                        results = soup.select('.yuRUbf > a')
                    else:
                        results = soup.select('h2 > a')
                        
                    urls = []
                    for result in results[:num_results]:
                        url = result.get('href')
                        if url and url.startswith('http'):
                            urls.append(url)
                    return urls
                return []

async def process_urls(urls: List[str], extraction_instruction: str, use_llm: bool = True) -> List[Dict]:
    results = []
    if use_llm:
        strategy = LLMExtractionStrategy(instruction=extraction_instruction)
    else:
        strategy = SimpleTextExtractionStrategy()
        
    async with AsyncWebCrawler(verbose=True) as crawler:
        for url in urls:
            try:
                with st.spinner(f'Processing {url}...'):
                    result = await crawler.arun(url, strategy)
                    if result.extracted_content:
                        results.append({
                            'URL': url,
                            'Extracted Content': result.extracted_content
                        })
            except Exception as e:
                st.error(f"Error processing {url}: {str(e)}")
    return results

def create_polars_dataframe(results: List[Dict]) -> pl.DataFrame:
    """Create a Polars DataFrame from the results."""
    if not results:
        return pl.DataFrame(schema={'URL': str, 'Extracted Content': str})
    return pl.DataFrame(results)

def export_to_csv(df: pl.DataFrame) -> bytes:
    """Export Polars DataFrame to CSV."""
    return df.write_csv().encode('utf-8')

st.title('🌐 AI Scraper')
st.markdown("""
This application allows you to search the web and extract specific information using AI-powered analysis.
""")

st.sidebar.header("Configuration")
search_engine = st.sidebar.selectbox(
    "Search Engine",
    ["Google", "Bing"],
    help="Select the search engine to use"
)
use_llm = st.sidebar.checkbox(
    "Use LLM for extraction",
    value=True,
    help="Use AI to extract specific information (slower but more accurate)"
)
num_results = st.sidebar.slider(
    "Number of results",
    min_value=1,
    max_value=10,
    value=3,
    help="Number of search results to process"
)

search_query = st.text_input(
    "Search Query",
    help="Enter your search query"
)

extraction_instruction = st.text_area(
    "Extraction Instructions",
    placeholder="Example: Extract product names and prices" if use_llm else "Simple text extraction will be used",
    help="Specify what information to extract from the pages",
    disabled=not use_llm
)

if st.button('Search and Extract', type='primary'):
    if not search_query:
        st.warning("Please enter a search query")
    elif use_llm and not extraction_instruction:
        st.warning("Please provide extraction instructions when using LLM")
    else:
        try:
            searcher = WebSearcher()
            with st.spinner('Searching...'):
                urls = asyncio.run(
                    searcher.search(
                        search_query,
                        engine=search_engine.lower(),
                        num_results=num_results
                    )
                )
            if urls:
                st.success(f"Found {len(urls)} URLs")
                results = asyncio.run(
                    process_urls(urls, extraction_instruction, use_llm)
                )
                if results:
                    st.session_state.scraping_results = results
                    df = create_polars_dataframe(results)
                    st.dataframe(
                        df.to_pandas(),
                        use_container_width=True,
                        height=400
                    )
                    st.download_button(
                        "Download Results (CSV)",
                        export_to_csv(df),
                        "scraping_results.csv",
                        "text/csv",
                        key='download-csv'
                    )
                    st.subheader("Statistics")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total URLs Processed", len(urls))
                    with col2:
                        st.metric("Successful Extractions", len(results))
                else:
                    st.warning("No content could be extracted from the URLs")
            else:
                st.warning("No search results found")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if st.session_state.scraping_results:
    if st.checkbox("Show previous results"):
        previous_df = create_polars_dataframe(st.session_state.scraping_results)
        st.dataframe(
            previous_df.to_pandas(),
            use_container_width=True,
            height=400
        )
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Made with ❤️ using Streamlit and Polars</p>
</div>
""", unsafe_allow_html=True)
if st.sidebar.button("Clear Cache"):
    st.session_state.scraping_results = []
    st.experimental_rerun()
