# AI Blog Writing Assistant

A powerful Streamlit application that uses CrewAI and Clarifai to generate high-quality blog posts on any topic.

## Features

- 🔍 **Intelligent Research**: AI agent gathers comprehensive information using web search
- ✍️ **Expert Writing**: AI content strategist crafts engaging, well-structured blog posts
- 🧠 **Powered by Clarifai**: Uses Gemini 2.5 Pro model via OpenAI-compatible API
- 📄 **Markdown Output**: Clean, formatted blog posts ready for publishing
- 💾 **Download Option**: Save generated content as markdown files

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

You need to set up the following environment variables:

```bash
# Clarifai Personal Access Token
export CLARIFAI_PAT="your_clarifai_personal_access_token_here"

# Serper API Configuration (for web search)
export SERPER_API_KEY="your_serper_dev_api_key_here"
```

#### Getting API Keys:

**Clarifai Personal Access Token (PAT):**
1. Go to [Clarifai Settings](https://clarifai.com/settings/security)
2. Create a Personal Access Token (PAT)
3. Copy the token and use it as `CLARIFAI_PAT`

**Serper API Key:**
1. Go to [Serper.dev](https://serpapi.com/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Use it as `SERPER_API_KEY`

### 3. Run the Application

```bash
streamlit run app.py
```

## Usage

1. **Enter Topic**: Type your blog topic in the input field
2. **Generate**: Click "🚀 Generate Blog" button
3. **Wait**: The AI agents will research and write your blog post
4. **Download**: Use the download button to save the markdown file

## Configuration

The app is currently configured to use:
- **Model**: `gcp/generate/models/gemini-2_5-pro` (Clarifai) - [View Model](https://clarifai.com/gcp/generate/models/gemini-2_5-pro)
- **API Base**: `https://api.clarifai.com/v2/ext/openai/v1`

You can modify these settings in `app.py` if needed.

## Project Structure

```
.
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Troubleshooting

### Import Error: ModuleNotFoundError: No module named 'crewai_tools'

Make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

### Environment Variable Errors

Make sure both `CLARIFAI_PAT` and `SERPER_API_KEY` are set:
```bash
echo $CLARIFAI_PAT
echo $SERPER_API_KEY
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the [MIT License](LICENSE). 