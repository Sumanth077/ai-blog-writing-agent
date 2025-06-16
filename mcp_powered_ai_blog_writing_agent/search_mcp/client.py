import asyncio
import os
import json

from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

# --- Configuration ---
PAT = os.environ.get("CLARIFAI_PAT")
if not PAT:
    raise ValueError("CLARIFAI_PAT environment variable not set!")

# MCP model endpoint
url = "https://api.clarifai.com/v2/ext/mcp/v1/users/sumanth/apps/mcp-examples/models/blog_writing_search_mcp"
transport = StreamableHttpTransport(url=url, headers={"Authorization": "Bearer " + PAT})

async def main():
    print("=== SerpAPI MCP Server ===\n")

    async with Client(transport) as client:
        # 1. List available tools
        print("Available tools:")
        try:
            tools = await client.list_tools()
            for tool in tools:
                print(f"- {tool.name}: {tool.description}")
        except Exception as e:
            print(f"Error listing tools: {e}")
            return

        print("\n" + "="*50 + "\n")

        # 2. Multi-Engine Search
        print("Testing: multi_engine_search...")
        try:
            result = await client.call_tool(
                "multi_engine_search",
                {"query": "AI in healthcare", "engine": "google", "location": "United States"}
            )
            response_data = json.loads(result[0].text)
            if isinstance(response_data, list):
                print("Top 5 links:")
                for link in response_data:
                    print(f"- {link}")
            else:
                print("Unexpected response format: not a list")

        except Exception as e:
            print(f"Error: {e}")

        print("\n" + "="*50 + "\n")

        # 3. Extract content from links
        print("Testing: extract_web_content_from_links...")
        try:
            links = [
                "https://pmc.ncbi.nlm.nih.gov/articles/PMC8285156/",
                "https://www.foreseemed.com/artificial-intelligence-in-healthcare",
                "https://news.harvard.edu/gazette/story/2025/03/how-ai-is-transforming-medicine-healthcare/"
            ]
            result = await client.call_tool("extract_web_content_from_links", {"urls": links})
            response_data = json.loads(result[0].text)
            for url, content in response_data.items():
                print(f"\nURL: {url}\nExtracted Content (first 500 chars):\n{content[:500]}")
        except Exception as e:
            print(f"Error: {e}")

        print("\n" + "="*50 + "\n")

        # 4. Keyword research
        print("Testing: keyword_research...")
        try:
            result = await client.call_tool(
                "keyword_research",
                {"topic": "home automation"}
            )
            response_data = json.loads(result[0].text)
            print("Keyword research results:")
            for item in response_data:
                print(f"- Keyword: {item.get('keyword')}, Popularity: {item.get('relative_popularity_score')}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())




# import asyncio
# import os
# import json

# from fastmcp import Client
# from fastmcp.client.transports import StreamableHttpTransport

# # --- Configuration ---
# # Make sure to set your Clarifai PAT and SERPER_API_KEY as environment variables
# PAT = os.environ.get("CLARIFAI_PAT")

# if not PAT:
#     raise ValueError("CLARIFAI_PAT environment variable not set!")

# # Construct the MCP model URL
# # url = f"https://api.clarifai.com/v2/ext/mcp/v1/users/sumanth/apps/mcp-examples/models/search-mcp-server"
# url = "https://api.clarifai.com/v2/ext/mcp/v1/users/sumanth/apps/mcp-examples/models/search-mcp-server"
# transport = StreamableHttpTransport(url=url, headers={"Authorization": "Bearer " + PAT})

# async def main():
#     print("=== SerpAPI MCP Server ===\n")

#     async with Client(transport) as client:
#         # 1. List available tools
#         print("Available tools:")
#         try:
#             tools = await client.list_tools()
#             for tool in tools:
#                 print(f"- {tool.name}: {tool.description}")
#         except Exception as e:
#             print(f"Error listing tools: {e}")
#             return
        
#         print("\n" + "="*50 + "\n")

#         # 2. Example: Multi-Engine Search Tool
#         print("Testing: Multi-Engine Search Tool...")
#         try:
#             result = await client.call_tool(
#                 "multi_engine_search",
#                 {"query": "AI in healthcare", "engine": "bing", "location": "Canada"}
#             )
#             # Print the first organic result's title if it exists
#             response_data = json.loads(result[0].text)
#             first_result_title = response_data.get('organic_results', [{}])[0].get('title', 'N/A')
#             print(f"First search result title: {first_result_title}")

#         except Exception as e:
#             print(f"Error: {e}")
        
#         print("\n" + "="*50 + "\n")

#         # 3. Example: Structured SERP Data Extraction Tool
#         print("Testing: Structured SERP Data Extraction Tool...")
#         try:
#             result = await client.call_tool(
#                 "structured_serp_data_extraction",
#                 {"query": "best python courses"}
#             )
#             response_data = json.loads(result[0].text)
#             print(f"Extracted keys: {list(response_data.keys())}")
#             if 'related_questions' in response_data and response_data['related_questions']:
#                  print(f"First related question: {response_data['related_questions'][0].get('question')}")


#         except Exception as e:
#             print(f"Error: {e}")

#         print("\n" + "="*50 + "\n")

#         # 4. Example: Keyword Research and SEO Automation Tool
#         print("Testing: Keyword Research and SEO Automation Tool...")
#         try:
#             result = await client.call_tool(
#                 "keyword_research",
#                 {"topic": "home automation"}
#             )
#             response_data = json.loads(result[0].text)
#             print("Keyword research results:")
#             for item in response_data:
#                 print(f"- Keyword: {item.get('keyword')}, Popularity: {item.get('relative_popularity_score')}")

#         except Exception as e:
#             print(f"Error: {e}")

# if __name__ == "__main__":
#     asyncio.run(main()) 