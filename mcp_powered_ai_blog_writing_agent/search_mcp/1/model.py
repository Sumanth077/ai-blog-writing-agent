import os
from typing import Annotated, Dict, Any, List
from pydantic import Field
from serpapi import GoogleSearch
from clarifai.runners.models.mcp_class import MCPModelClass
from fastmcp import FastMCP
from newspaper import Article

# Initialize the server
server = FastMCP("blog_writing_search_mcp")

# SerpAPI key
SERPAPI_API_KEY = "a39444e3bb6d7db08382602ad61c37adc8af196e941be93ee7d2bfdb96ba530b"

@server.tool(
    "multi_engine_search",
    description="Query a search engine and return the top 5 blog/article links based on a search query."
)
def multi_engine_search(
    query: Annotated[str, Field(description="Search query.")],
    engine: Annotated[str, Field(description="Search engine to use (e.g., 'google').")] = "google",
    location: Annotated[str, Field(description="Geographic location for the search.")] = "United States",
    device: Annotated[str, Field(description="Device type for the search ('desktop' or 'mobile').")] = "desktop"
) -> List[str]:
    params = {
        "api_key": SERPAPI_API_KEY,
        "engine": engine,
        "q": query,
        "location": location,
        "device": device
    }
    search = GoogleSearch(params)
    results = search.get_dict()

    links = []
    for result in results.get("organic_results", [])[:5]:
        link = result.get("link")
        if link:
            links.append(link)

    return links

@server.tool(
    "extract_web_content_from_links",
    description="Extracts main article content from a list of blog or article URLs using newspaper3k."
)
def extract_web_content_from_links(
    urls: Annotated[List[str], Field(description="List of blog/article URLs to extract content from.")]
) -> Dict[str, str]:
    extracted = {}

    for url in urls:
        try:
            article = Article(url)
            article.download()
            article.parse()
            extracted[url] = article.text[:1000]  # Limit to first 1000 characters
        except Exception as e:
            extracted[url] = f"Error extracting content: {str(e)}"

    return extracted

@server.tool(
    "keyword_research",
    description="Automate keyword research to find high-potential keywords based on a topic, using autocomplete and trends."
)
def keyword_research(
    topic: Annotated[str, Field(description="Blog topic to research keywords for.")]
) -> List[Dict[str, Any]]:
    autocomplete_params = {
        "api_key": SERPAPI_API_KEY,
        "engine": "google_autocomplete",
        "q": topic,
    }
    search = GoogleSearch(autocomplete_params)
    autocomplete_results = search.get_dict()
    suggestions = [item['value'] for item in autocomplete_results.get('suggestions', [])[:5]]

    if not suggestions:
        return [{"error": "Could not fetch keyword suggestions."}]

    trends_params = {
        "api_key": SERPAPI_API_KEY,
        "engine": "google_trends",
        "q": ", ".join(suggestions),
        "data_type": "TIMESERIES"
    }
    search = GoogleSearch(trends_params)
    trends_results = search.get_dict()

    keyword_data = []
    if "interest_over_time" in trends_results:
        timeline_data = trends_results["interest_over_time"].get("timeline_data", [])
        for i, keyword in enumerate(suggestions):
            last_value = timeline_data[-1]['values'][i].get('value') if timeline_data else "N/A"
            keyword_data.append({
                "keyword": keyword,
                "relative_popularity_score": last_value
            })
    else:
        for keyword in suggestions:
            keyword_data.append({
                "keyword": keyword,
                "relative_popularity_score": "N/A"
            })

    return keyword_data

class MyModelClass(MCPModelClass):
    def get_server(self) -> FastMCP:
        return server




















# import os
# from typing import Annotated, Dict, Any, List
# from pydantic import Field
# from serpapi import GoogleSearch
# from clarifai.runners.models.mcp_class import MCPModelClass
# from fastmcp import FastMCP

# # Initialize the server
# server = FastMCP("blog_writing_search_mcp")

# # Fetch SerpAPI key from environment variables
# # SERPAPI_API_KEY = os.getenv("SERPER_API_KEY")
# SERPAPI_API_KEY = "a39444e3bb6d7db08382602ad61c37adc8af196e941be93ee7d2bfdb96ba530b"

# @server.tool(
#     "multi_engine_search",
#     description="Query multiple search engines (Google, Bing, Baidu, etc.) with custom parameters like location and language."
# )
# def multi_engine_search(
#     query: Annotated[str, Field(description="The search query.")],
#     engine: Annotated[str, Field(description="The search engine to use (e.g., 'google', 'bing').")] = "google",
#     location: Annotated[str, Field(description="The geographic location for the search.")] = "United States",
#     device: Annotated[str, Field(description="The device type for the search ('desktop' or 'mobile').")] = "desktop"
# ) -> Dict[str, Any]:
#     """
#     Performs a search on a specified engine with given parameters.
#     """
#     params = {
#         "api_key": SERPAPI_API_KEY,
#         "engine": engine,
#         "q": query,
#         "location": location,
#         "device": device
#     }
#     search = GoogleSearch(params)
#     results = search.get_dict()
#     return results


# @server.tool(
#     "structured_serp_data_extraction",
#     description="Extract and parse rich structured data from search engine results, including organic/paid results, featured snippets, knowledge graphs, etc."
# )
# def structured_serp_data_extraction(
#     query: Annotated[str, Field(description="The search query to extract structured data for.")],
#     engine: Annotated[str, Field(description="The search engine to use.")] = "google"
# ) -> Dict[str, Any]:
#     """
#     Extracts detailed, structured SERP data for a given query.
#     """
#     params = {
#         "api_key": SERPAPI_API_KEY,
#         "engine": engine,
#         "q": query,
#     }
#     search = GoogleSearch(params)
#     results = search.get_dict()
#     # Return specific structured data keys if they exist
#     return {
#         key: results.get(key)
#         for key in [
#             "organic_results", "ads", "knowledge_graph", "shopping_results",
#             "related_questions", "video_results", "local_pack"
#         ] if key in results
#     }

# @server.tool(
#     "keyword_research",
#     description="Automate keyword research to find high-potential keywords based on a topic, using autocomplete and trends."
# )
# def keyword_research(
#     topic: Annotated[str, Field(description="The blog topic to research keywords for.")]
# ) -> List[Dict[str, Any]]:
#     """
#     Generates keyword ideas from Google Autocomplete and fetches their relative popularity from Google Trends.
#     """
#     # 1. Get keyword suggestions from Google Autocomplete
#     autocomplete_params = {
#         "api_key": SERPAPI_API_KEY,
#         "engine": "google_autocomplete",
#         "q": topic,
#     }
#     search = GoogleSearch(autocomplete_params)
#     autocomplete_results = search.get_dict()
#     suggestions = [item['value'] for item in autocomplete_results.get('suggestions', [])[:5]]

#     if not suggestions:
#         return [{"error": "Could not fetch keyword suggestions."}]

#     # 2. Get relative trends for the suggestions
#     trends_params = {
#         "api_key": SERPAPI_API_KEY,
#         "engine": "google_trends",
#         "q": ", ".join(suggestions),
#         "data_type": "TIMESERIES"
#     }
#     search = GoogleSearch(trends_params)
#     trends_results = search.get_dict()

#     keyword_data = []
#     if "interest_over_time" in trends_results:
#         timeline_data = trends_results["interest_over_time"].get("timeline_data", [])
#         # Get the most recent value as the relative popularity score
#         for i, keyword in enumerate(suggestions):
#             # The values list corresponds to the order of keywords in the query
#             last_value = timeline_data[-1]['values'][i].get('value') if timeline_data else "N/A"
#             keyword_data.append({
#                 "keyword": keyword,
#                 "relative_popularity_score": last_value
#             })
#     else: # Fallback if trends data is not available
#         for keyword in suggestions:
#             keyword_data.append({
#                 "keyword": keyword,
#                 "relative_popularity_score": "N/A"
#             })

#     return keyword_data


# class MyModelClass(MCPModelClass):
#     def get_server(self) -> FastMCP:
#         return server 