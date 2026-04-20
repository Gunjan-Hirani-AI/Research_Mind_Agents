from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from rich import print

from dotenv import load_dotenv
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippets."""
    results = tavily.search(query, max_results=5)
    
    if(results):
        web_data = results['results']
    
    print(web_data)
    return web_data
        
@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        res = requests.get(url, timeout=8, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(res.text, 'html.parser')
        
        #print("soup",soup)
        
        for tag in soup(['script', 'style', 'header', 'footer','nav']):
            tag.decompose()
        
        return soup.get_text(separator="", strip=True)[:5000]
        
    except Exception as e:
        return f"Error fetching URL: {e}"
    
    
#web_scrape.invoke({"url":"https://crex.com/player/virat-kohli-4I/matches"})