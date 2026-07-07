from langchain.tools import tool
from bs4 import BeautifulSoup
from tavily import TavilyClient
from dotenv import load_dotenv
import os
import requests
from rich import print

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> dict:
    """
    Search the web for up-to-date information using Tavily.
    
    Args:
        query: The search query.

    Returns:
        A dictionary containing search results.
    """
    result = tavily.search(
        query=query,
        max_results=5
    )

    output=[]

    for r in result['results']:
        output.append(
            f"Title:{r['title']}\nUrl:{r['url']}\nSnippet:{r['content'][:300]}"
        )
    
    return "\n-------\n".join(output)

@tool
def scrape_url(url: str) -> str:
    """
    Safely scrape and return clean text content from a given URL for deeper reading.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(url, headers=headers, timeout=8)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unwanted tags
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator="\n")

        cleaned_text = "\n".join(
            line.strip() for line in text.splitlines() if line.strip()
        )

        return cleaned_text[:2000]  # limit output size

    except requests.exceptions.Timeout:
        return "Error: Request timed out while fetching the page."

    except requests.exceptions.RequestException as e:
        return f"Error: Request failed - {str(e)}"

    except Exception as e:
        return f"Error: Unexpected scraping error - {str(e)}"
    

print(scrape_url.invoke("https://www.ndtv.com/india-news/no-car-wash-penalty-on-water-misuse-as-mumbai-faces-supply-crisis-11645568"))

# print(web_search.invoke("What are the recent news of water crisis in mumbai?"))