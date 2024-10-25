import streamlit as st
import time
import asyncio
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
    AsyncWebCrawler
)
from extraction_strategy import LLMExtractionStrategy
from parse import parse_with_ollama

st.set_page_config(page_title="AI Scraper", layout="wide")
st.markdown("""
<style>
@keyframes slideIn {
    from { transform: translateX(-100%); }
    to { transform: translateX(0); }
}
@keyframes letterAppear {
    from { 
        opacity: 0;
        transform: translateX(50px);
    }
    to { 
        opacity: 1;
        transform: translateX(0);
    }
}
.slideIn { animation: slideIn 1s; }
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
    100% { transform: translateY(0px); }
}
@keyframes pulse {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.1); opacity: 0.7; }
    100% { transform: scale(1); opacity: 1; }
}
.floating-circle {
    width: 50px;
    height: 50px;
    background-color: #3498db;
    border-radius: 50%;
    margin: 20px auto;
    animation: float 3s ease-in-out infinite, pulse 2s ease-in-out infinite;
}
.letter {
    display: inline-block;
    animation: letterAppear 0.5s forwards;
    opacity: 0;
}
.letter:nth-child(1) { animation-delay: 0.1s; }
.letter:nth-child(2) { animation-delay: 0.2s; }
.letter:nth-child(3) { animation-delay: 0.3s; }
.letter:nth-child(4) { animation-delay: 0.4s; }
.letter:nth-child(5) { animation-delay: 0.5s; }
.letter:nth-child(6) { animation-delay: 0.6s; }
.letter:nth-child(7) { animation-delay: 0.7s; }
.letter:nth-child(8) { animation-delay: 0.8s; }
.letter:nth-child(9) { animation-delay: 0.9s; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
    <h1 style='text-align: center; font-weight: bold;'>
        <span style='color: #FF9933;'>
            <span class="letter">A</span><span class="letter">I</span>
        </span> 
        <span style='color: #138808;'>
            <span class="letter">S</span><span class="letter">c</span><span class="letter">r</span><span class="letter">a</span>
        </span>
        <span style='color: #87CEEB;'>
            <span class="letter">p</span><span class="letter">e</span><span class="letter">r</span>
        </span>
    </h1>
    """, unsafe_allow_html=True)
st.markdown("<p class='slideIn'>Extract and Parse Web Content with AI</p>", unsafe_allow_html=True)

async def process_async_scrape(url, extraction_instruction=None):
    async with AsyncWebCrawler(verbose=True) as crawler:
        if extraction_instruction:
            strategy = LLMExtractionStrategy(
                instruction=extraction_instruction,
                model_name="llama3.1"
            )
        else:
            strategy = None
        result = await crawler.arun(
            url=url,
            extraction_strategy=strategy,
            bypass_cache=True
        )
        return result

if "scraping_mode" not in st.session_state:
    st.session_state.scraping_mode = "Simple"

st.radio(
    "Scraping Mode",
    options=["Simple", "Advanced"],
    index=0,
    horizontal=True,
    key="scraping_mode"
)

url = st.text_input("Enter Website URL", placeholder="https://example.com")
if st.session_state.scraping_mode == "Advanced":
    extraction_instruction = st.text_area(
        "Extraction Instructions",
        placeholder="e.g., Extract only content related to technology"
    )
else:
    extraction_instruction = None
if st.button("Scrape Website"):
    if url:
        with st.spinner("Scraping the website..."):
            try:
                st.markdown("<div class='floating-circle'></div>", unsafe_allow_html=True)
                start_time = time.time()
                if st.session_state.scraping_mode == "Advanced":
                    result = asyncio.run(process_async_scrape(url, extraction_instruction))
                    cleaned_content = result.extracted_content
                else:
                    dom_content = scrape_website(url)
                    body_content = extract_body_content(dom_content)
                    cleaned_content = clean_body_content(body_content)
                scrape_time = time.time() - start_time
                st.success(f"Scraping completed in {scrape_time:.2f} seconds")
                st.session_state.dom_content = cleaned_content
                with st.expander("View Scraped Content", expanded=False):
                    st.text_area("Content", cleaned_content, height=300)
            except ValueError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"An error occurred while scraping the website: {str(e)}")

if "dom_content" in st.session_state:
    st.markdown("<h3 class='slideIn'>Parsing Options</h3>", unsafe_allow_html=True)
    parse_description = st.text_area("Describe what you want to parse", placeholder="Enter parsing instructions here...")
    if st.button("Parse Content"):
        if parse_description:
            with st.spinner("Parsing the content..."):
                st.markdown("<div class='floating-circle'></div>", unsafe_allow_html=True)
                start_time = time.time()
                dom_chunks = split_dom_content(st.session_state.dom_content)
                parsed_result = parse_with_ollama(dom_chunks, parse_description)
                parse_time = time.time() - start_time
                st.success(f"Parsing completed in {parse_time:.2f} seconds")
                st.markdown("<h3 class='fadeIn'>Parsed Results</h3>", unsafe_allow_html=True)
                st.write(parsed_result)
