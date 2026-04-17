from bs4 import BeautifulSoup
import requests
from langchain.tools import tool
from rich import print

@tool
def scrape_tool(url: str)->str:
    """
    Scrape and return clean text content from a given URL for a deeper reading
    """

    try:
        print("Scraping:",url)
        resp=requests.get(url, timeout=8, headers={"User-Agent":"Mozilla/5.0"})
        soup=BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script","style","nav","footer"]):
            tag.decompose()
        return soup.get_text(separator=" ",strip=True)[:3000]
    
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
    
