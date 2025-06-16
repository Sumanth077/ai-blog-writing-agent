import streamlit as st
import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import MCPServerAdapter

# Environment variables
CLARIFAI_PAT = os.getenv("CLARIFAI_PAT")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

if not CLARIFAI_PAT:
    st.error("Please set CLARIFAI_PAT environment variable")
    st.stop()

if not SERPER_API_KEY:
    st.error("Please set SERPER_API_KEY environment variable")
    st.stop()

# Configure Clarifai LLM
clarifai_llm = LLM(
    model="openai/openai/chat-completion/models/gpt-4o",
    api_key=CLARIFAI_PAT,
    base_url="https://api.clarifai.com/v2/ext/openai/v1"
)

# MCP Server Configuration
USER_ID = "sumanth"
APP_ID = "mcp-examples"
MODEL_ID = "blog_writing_search_mcp"

server_params = {
    "url": f"https://api.clarifai.com/v2/ext/mcp/v1/users/{USER_ID}/apps/{APP_ID}/models/{MODEL_ID}",
    "headers": {"Authorization": "Bearer " + CLARIFAI_PAT},
    "transport": "streamable-http"
}

# Streamlit App
def main():
    st.set_page_config(page_title="AI Blog Writing Agent", page_icon="📝", layout="wide")
    st.title("📝 AI Blog Writing Agent")
    st.markdown("<h2 style='text-align: center; color: #2E86C1;'><strong>Powered by Clarifai, CrewAI & a Custom SerpAPI MCP Server</strong></h2>", unsafe_allow_html=True)

    st.markdown("""
    **How it works:**
    - ✅ **Planner Agent**: Researches top articles and extracts SEO keywords.
    - ✍️ **Writer Agent**: Writes a full blog post using the research and outline.
    - 🔎 **Editor Agent**: Polishes the final post and formats it in markdown.
    """)

    topic = st.text_input(
        "Enter your blog topic:",
        placeholder="e.g., The Future of Quantum Computing",
        help="Be specific for better results"
    )

    generate_button = st.button("🚀 Generate Blog", type="primary")

    if generate_button:
        if not topic.strip():
            st.error("Please enter a topic for the blog post.")
        else:
            with st.spinner(f"Running agents on: '{topic}'..."):
                try:
                    with MCPServerAdapter(server_params) as mcp_tools:
                        st.info(f"✅ Connected to MCP Server. Tools: {[tool.name for tool in mcp_tools]}")

                        # Agents
                        planner = Agent(
                            role="SEO Researcher and Content Planner",
                            goal="Extract key insights, find SEO keywords, and outline the blog.",
                            backstory="You research top articles and produce outlines optimized for engagement and SEO.",
                            tools=mcp_tools,
                            verbose=True,
                            llm=clarifai_llm,
                            allow_delegation=False
                        )

                        writer = Agent(
                            role="Blog Post Writer",
                            goal="Create a detailed, high-quality blog post using the research and outline.",
                            backstory="You are a writer who specializes in transforming outlines into compelling blog posts.",
                            verbose=True,
                            llm=clarifai_llm,
                            allow_delegation=False
                        )

                        editor = Agent(
                            role="Blog Editor and Formatter",
                            goal="Edit the blog post, correct grammar, and format it in markdown.",
                            backstory="You ensure every blog is well-written, polished, and correctly formatted for publishing.",
                            verbose=True,
                            llm=clarifai_llm,
                            allow_delegation=False
                        )

                        # Tasks
                        plan_task = Task(
                            description=f"""
For the topic "{topic}":

1. Use `multi_engine_search` to find 5 recent, relevant articles.
2. Extract content using `extract_web_content_from_links`.
3. Use `keyword_research` to find SEO keywords.
4. Summarize key findings and generate a structured outline.

The outline should include:
- Title
- Introduction
- 3-4 section headings with bullet points
- Conclusion
""",
                            expected_output="A blog outline with insights, 5-10 SEO keywords, and detailed structure.",
                            agent=planner
                        )

                        write_task = Task(
                            description=f"""
Using the outline and research for "{topic}", write a complete blog post with:

- At least 5–6 paragraphs
- Natural integration of SEO keywords
- Engaging and informative tone
- Clean markdown format

Use examples and factual support where possible.
""",
                            expected_output="Full markdown blog post draft, ready for editing.",
                            agent=writer,
                            context=[plan_task]
                        )

                        edit_task = Task(
                            description=f"""
Edit the blog post for "{topic}":

- Fix grammar and clarity issues
- Enhance tone, transitions, and flow
- Ensure SEO keywords are present naturally
- Format properly in markdown:
    - Use `#` for title
    - `##` for section headers
    - Paragraph spacing and bullet points
    - Bold key phrases if needed

Return the final polished markdown content.
""",
                            expected_output="Final markdown blog post, ready for publishing.",
                            agent=editor,
                            context=[write_task]
                        )

                        # Run the Crew
                        crew = Crew(
                            agents=[planner, writer, editor],
                            tasks=[plan_task, write_task, edit_task],
                            process=Process.sequential,
                            verbose=1
                        )
                        result = crew.kickoff()

                        final_output = result.output if hasattr(result, "output") else str(result)

                        st.success("✅ Blog post generated successfully!")
                        st.markdown("---")
                        st.markdown(final_output, unsafe_allow_html=False)

                        st.download_button(
                            label="📥 Download as Markdown",
                            data=final_output,
                            file_name=f"{topic.replace(' ', '_').lower()}_blog.md",
                            mime="text/markdown"
                        )

                except Exception as e:
                    st.error(f"An error occurred: {e}")

    with st.sidebar:
        st.header("⚙️ Configuration")
        st.markdown("**MCP Server:**")
        st.code(f"USER_ID: {USER_ID}\nAPP_ID: {APP_ID}\nMODEL_ID: {MODEL_ID}", language="text")
        st.markdown("**LLM Config:**")
        st.markdown("- Model: `gpt-4o` via Clarifai")
        st.markdown("- Base URL: `https://api.clarifai.com`")

        st.header("🛠️ Features")
        st.markdown("- Research via search + content extraction")
        st.markdown("- Keyword generation for SEO")
        st.markdown("- Plan → Write → Edit flow with agents")

        st.warning("⚠️ Keep your API keys secure. Ensure the MCP server is live on Clarifai.")

if __name__ == "__main__":
    main()

































# import streamlit as st
# import os
# from crewai import Agent, Task, Crew, Process, LLM
# from crewai_tools import MCPServerAdapter

# # Environment variables
# CLARIFAI_PAT = os.getenv("CLARIFAI_PAT")
# SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# if not CLARIFAI_PAT:
#     st.error("Please set CLARIFAI_PAT environment variable")
#     st.stop()

# if not SERPER_API_KEY:
#     st.error("Please set SERPER_API_KEY environment variable")
#     st.stop()

# # Configure Clarifai LLM
# clarifai_llm = LLM(
#     model="openai/openai/chat-completion/models/gpt-4o",
#     api_key=CLARIFAI_PAT,
#     base_url="https://api.clarifai.com/v2/ext/openai/v1"
# )

# # --- MCP Server Configuration ---
# USER_ID = "sumanth"
# APP_ID = "mcp-examples"
# MODEL_ID = "blog_writing_search_mcp" 

# server_params = {
#     "url": f"https://api.clarifai.com/v2/ext/mcp/v1/users/{USER_ID}/apps/{APP_ID}/models/{MODEL_ID}",
#     "headers": {"Authorization": "Bearer " + CLARIFAI_PAT},
#     "transport": "streamable-http"
# }

# # Streamlit App
# def main():
#     st.set_page_config(page_title="AI Blog Writing Agent", page_icon="📝", layout="wide")
#     st.title("📝 AI Blog Writing Agent")
#     st.markdown("<h2 style='text-align: center; color: #2E86C1;'><strong>Powered by Clarifai, CrewAI & a Custom SerpAPI MCP Server</strong></h2>", unsafe_allow_html=True)

#     st.markdown("""
    
#     **How it works:**
#     - ✅ **Planner Agent**: Performs in-depth research by finding top articles, extracting their content, and identifying key SEO terms.
#     - ✍️ **Writer Agent**: Crafts an engaging, well-structured blog post based on the rich research and data provided by the Planner.
#     - 🔎 **Editor Agent**: Polishes the post for clarity, grammar, style, and ensures it aligns with SEO best practices.
#     """)

#     # Input section
#     with st.container():
#         topic = st.text_input(
#             "Enter your blog topic:",
#             placeholder="e.g., The Future of Quantum Computing",
#             help="Be specific for better results"
#         )
        
#         generate_button = st.button("🚀 Generate Blog", type="primary")

#     # Generation section
#     if generate_button:
#         if not topic.strip():
#             st.error("Please enter a topic for the blog post.")
#         else:
#             with st.spinner(f"Connecting to MCP Server and running agents on: '{topic}'..."):
#                 try:
#                     with MCPServerAdapter(server_params) as mcp_tools:
#                         st.info(f"✅ Connected to MCP Server. Available tools: {[tool.name for tool in mcp_tools]}")

#                         # Define Agents within the context of the tools
#                         planner = Agent(
#                             role="Content Strategist and SEO Expert",
#                             goal="Analyze a given topic, perform comprehensive web research to gather in-depth information and identify target keywords, and then create a detailed content outline for a blog post.",
#                             backstory="You are a master content strategist with a knack for SEO. You excel at dissecting topics, finding high-quality information from across the web, and creating actionable content plans that result in top-ranking articles.",
#                             tools=mcp_tools,
#                             verbose=True,
#                             llm=clarifai_llm,
#                             allow_delegation=False
#                         )

#                         writer = Agent(
#                             role="Expert Content Creator",
#                             goal="Write a compelling and informative blog post based on a detailed content outline, incorporating research summaries and SEO keywords.",
#                             backstory="You are a skilled writer who can transform structured outlines and research data into engaging, human-readable narratives. You specialize in making complex topics accessible and interesting for a tech-savvy audience.",
#                             verbose=True,
#                             llm=clarifai_llm,
#                             allow_delegation=False
#                         )

#                         editor = Agent(
#                             role="Senior Language and Style Editor",
#                             goal="Review and refine a blog post for clarity, tone, grammar, and style, ensuring it is polished, professional, and aligned with SEO goals.",
#                             backstory="With a keen eye for detail, you are an experienced editor who ensures every piece of content is flawless. You improve readability, flow, and check for consistent tone and brand voice.",
#                             verbose=True,
#                             llm=clarifai_llm,
#                             allow_delegation=False
#                         )

#                         # Define Tasks
#                         plan_task = Task(
#                             description=f"""
#                             For the topic '{topic}', perform the following steps:
#                             1.  First, use the `multi_engine_search` tool to find the top 5 most relevant and recent blog posts or articles.
#                             2.  Next, take the list of URLs from the previous step and use the `extract_web_content_from_links` tool to get the text content of each page.
#                             3.  Then, use the `keyword_research` tool with the original topic to generate a list of high-potential SEO keywords.
#                             4.  Finally, synthesize all the gathered information. Summarize the key points and common themes from the web content. Based on this, create a detailed blog post outline. The outline must include an introduction, several body sections with talking points, and a conclusion.
#                             """,
#                             expected_output="""A comprehensive content plan including:
#                             - A summary of insights from the web research.
#                             - A list of 5-10 recommended SEO keywords.
#                             - A detailed blog post outline with a title, introduction, section headers, and bullet points for each section.""",
#                             agent=planner
#                         )

#                         write_task = Task(
#                             description=f"""
#                             Using the content plan for the topic '{topic}', write a full, engaging, and well-structured blog post.
#                             - The post should be at least 5-6 paragraphs long.
#                             - It must be informative, easy to read, and align with the tone defined in the plan.
#                             - Naturally weave in the provided SEO keywords throughout the text.
#                             - Use the research summary to add depth, examples, and facts.
#                             """,
#                             expected_output="A complete, well-written blog post formatted in clean markdown, ready for the editor.",
#                             agent=writer,
#                             context=[plan_task]
#                         )

#                         edit_task = Task(
#                             description=f"""
#                             Review and perfect the blog post on '{topic}'.
#                             - Correct all grammatical and spelling errors.
#                             - Improve sentence structure, clarity, and flow.
#                             - Ensure the tone is consistent and the language is compelling.
#                             - Verify that the SEO keywords from the plan have been included naturally.
                            
#                             Format the final output as clean markdown, ensuring it's ready for publication:
#                             - A compelling title using #
#                             - Section headers using ##
#                             - Proper paragraph breaks and bullet points.
#                             - Bold text for emphasis where appropriate.
#                             """,
#                             expected_output="The final, polished, and perfectly formatted markdown version of the blog post, ready for publishing.",
#                             agent=editor,
#                             context=[write_task]
#                         )

#                         # Create and run the Crew
#                         crew = Crew(
#                             agents=[planner, writer, editor],
#                             tasks=[plan_task, write_task, edit_task],
#                             process=Process.sequential,
#                             verbose=1
#                         )
#                         result = crew.kickoff()

#                         st.success("✅ Blog post generated successfully!")
#                         st.markdown("---")
#                         st.markdown(result)
                        
#                         st.download_button(
#                             label="📥 Download as Markdown",
#                             data=result,
#                             file_name=f"{topic.replace(' ', '_').lower()}_blog.md",
#                             mime="text/markdown"
#                         )

#                 except Exception as e:
#                     st.error(f"An error occurred: {e}")

#     # Sidebar
#     with st.sidebar:
#         st.header("⚙️ Configuration")
#         st.markdown("**MCP Server Details:**")
#         st.code(f"USER_ID: {USER_ID}\nAPP_ID: {APP_ID}\nMODEL_ID: {MODEL_ID}", language="text")

#         st.markdown("**LLM Configuration:**")
#         st.markdown(f"- **Model:** `gemini-2_5-pro`")
#         st.markdown(f"- **API Base:** `api.clarifai.com`")
        
#         st.header("🛠️ Features")
#         st.markdown("- **Advanced Research**: Finds and reads top articles on a topic.")
#         st.markdown("- **SEO Optimization**: Performs keyword research.")
#         st.markdown("- **Structured Workflow**: Uses a Plan, Write, Edit process.")
        
#         st.warning("⚠️ Keep your API keys secure. Ensure the MCP server is running on Clarifai for this app to work.")

# if __name__ == "__main__":
#     main() 