# import os
# import requests
# from dotenv import load_dotenv
# from crewai.tools import tool   # ✅ sirf decorator use karna hai
#
# load_dotenv()
#
# SCRAPINGDOG_API_KEY = os.getenv("SCRAPINGDOG_API_KEY")
# print("Loaded API Key:", SCRAPINGDOG_API_KEY)
#
# @tool("scrapingdog_search")
# def scrapingdog_search(query: str) -> dict:
#     """Use Scrapingdog API to search Google results"""
#     url = "https://api.scrapingdog.com/google"
#     params = {
#         "api_key": SCRAPINGDOG_API_KEY,
#         "query": query,
#         "num": 5   # Top 5 results
#     }
#     resp = requests.get(url, params=params)
#     try:
#         return resp.json()
#     except Exception as e:
#         return {"error": str(e), "text": resp.text}

import os
import requests
from dotenv import load_dotenv
from crewai.tools import tool
from typing import Dict, Any

load_dotenv()

SCRAPINGDOG_API_KEY = os.getenv("SCRAPINGDOG_API_KEY")

# Create the actual function first
def _scrapingdog_search_function(search_params: Dict[str, Any]) -> str:
    """
    Actual search function that does the work.
    """
    # Extract query from dictionary
    if 'query' in search_params and search_params['query']:
        query = search_params['query']
    else:
        # Build query from available parameters (YAML style)
        query_parts = []
        if 'product_name' in search_params:
            query_parts.append(search_params['product_name'])
        if 'target_audience' in search_params:
            query_parts.append(search_params['target_audience'])
        if 'description' in search_params:
            query_parts.append(search_params['description'])

        # Fallback: use all values to create a query
        if not query_parts:
            query_parts = [str(v) for v in search_params.values() if v and str(v).strip()]

        query = " ".join(query_parts) if query_parts else "market trends"

    print(f"🔍 Searching for: {query}")

    url = "https://api.scrapingdog.com/google"
    params = {
        "api_key": SCRAPINGDOG_API_KEY,
        "query": query,
        "num": 5  # Top 5 results
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()

        # Format the results as a readable string
        if isinstance(data, list):
            results = []
            for i, item in enumerate(data[:5], 1):
                title = item.get('title', 'No title')
                link = item.get('link', 'No link')
                snippet = item.get('snippet', 'No description')
                results.append(f"{i}. {title}\n   URL: {link}\n   Description: {snippet}\n")

            return "\n".join(results) if results else "No search results found."

        return f"Search results: {str(data)[:500]}..."  # Truncate if too long

    except requests.exceptions.RequestException as e:
        return f"Search API error: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

# Create the tool wrapper
@tool("scrapingdog_search")
def scrapingdog_search(search_params: Dict[str, Any]) -> str:
    """Tool wrapper for scrapingdog search"""
    return _scrapingdog_search_function(search_params)

# Export both the function and the tool
scrapingdog_function = _scrapingdog_search_function