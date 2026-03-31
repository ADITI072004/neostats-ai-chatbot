# 🤖 NeoStats AI Engineer Use Case

> An advanced AI chatbot with Retrieval-Augmented Generation (RAG), live web search, and multiple LLM providers.

## � Live Demo

**Try it now**: [https://aditi072004-neostats-ai-chatbot.streamlit.app](https://aditi072004-neostats-ai-chatbot.streamlit.app)

## �📋 Overview

NeoStats AI is a sophisticated chatbot application that combines:

- **RAG (Retrieval-Augmented Generation)**: Reference your own documents and knowledge bases
- **Live Web Search**: Real-time information retrieval from the internet
- **Multi-LLM Support**: OpenAI, Groq, and Google Gemini
- **Response Modes**: Switch between concise and detailed responses
- **Modern UI**: Built with Streamlit for ease of use

## ✨ Features

### 1. **Retrieval-Augmented Generation (RAG)**

- Upload and process local documents (TXT, PDF)
- Semantic search using vector embeddings
- Documents are chunked and embedded for efficient retrieval
- Context-aware responses using retrieved documents

### 2. **Live Web Search Integration**

- Real-time web search when LLM lacks knowledge
- Supports Google Search API (primary) and DuckDuckGo (fallback)
- Seamlessly integrate search results into LLM responses
- Display source citations

### 3. **Multiple LLM Providers**

- **OpenAI**: GPT-4, GPT-4o, GPT-3.5-turbo
- **Groq**: Llama 3.1, Mixtral models (fast and cost-effective)
- **Google Gemini**: Gemini 1.5 Pro/Flash

### 4. **Response Modes**

- **Concise**: Short, summarized replies (best for quick answers)
- **Detailed**: Expanded, in-depth responses (best for learning)
- Easy switching within the UI

### 5. **Error Handling & Logging**

- Comprehensive try/except blocks throughout
- Structured logging for debugging
- User-friendly error messages

## 🗂️ Project Structure

```
NeoStats_AI_UseCase/
├── config/
│   └── config.py              # Configuration & environment variables
├── models/
│   ├── llm.py                 # LLM provider implementations
│   └── embeddings.py          # Embedding models for RAG
├── utils/
│   ├── rag.py                 # RAG system (document processing, retrieval)
│   ├── web_search.py          # Web search functionality
│   └── __init__.py
├── data/
│   ├── documents/             # Uploaded documents (auto-created)
│   └── vector_db/             # Vector database (FAISS)
├── logs/
│   └── app.log               # Application logs (auto-created)
├── app.py                     # Main Streamlit application
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8+
- pip or conda

### 2. Installation

**Clone the repository** (if using Git)

```bash
git clone https://github.com/ADITI072004/neostats-ai-chatbot.git
cd neostats-ai-chatbot
```

**Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Install dependencies**

```bash
pip install -r requirements.txt
```

### 3. Configuration

**Create a `.env` file** (copy from `.env.example`)

```bash
cp .env.example .env
```

**Add your API keys to `.env`:**

```env
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...
GEMINI_API_KEY=AIza...
GOOGLE_SEARCH_API_KEY=... (optional)
```

Alternatively, set environment variables directly in `config/config.py`

### 4. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 How to Use

### Chat Interface

1. Navigate to the **Chat** page
2. Select your preferred **LLM Provider** from the sidebar
3. Choose a **Response Mode** (Concise or Detailed)
4. Customize the **System Prompt** if desired
5. Type your message and press Enter or click Send

### Uploading Documents (RAG)

1. In the sidebar, click **Upload documents**
2. Select TXT or PDF files from your computer
3. Click **📤 Ingest Documents**
4. Wait for processing (extracted text is chunked and embedded)
5. Your documents' context is now available in responses

### Using Web Search

- **Automatic**: Web search is used automatically when the chatbot doesn't have enough context
- **Manual**: Web search results are displayed in "View sources" expander
- Requires Google Search API key (optional - falls back to DuckDuckGo)

## ⚙️ Configuration Guide

### LLM Providers

**OpenAI** (Premium quality)

```env
DEFAULT_LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini  # or gpt-4o, gpt-3.5-turbo
```

**Groq** (Fast & cost-effective)

```env
DEFAULT_LLM_PROVIDER=groq
GROQ_API_KEY=gsk_...
GROQ_MODEL=llama-3.1-70b-versatile  # or mixtral, llama-3.1-8b-instant
```

**Google Gemini** (Balanced)

```env
DEFAULT_LLM_PROVIDER=gemini
GEMINI_API_KEY=AIza...
GEMINI_MODEL=gemini-1.5-flash  # or gemini-1.5-pro
```

### RAG Settings

- `CHUNK_SIZE`: Size of text chunks (default: 500 tokens)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 50 tokens)
- `TOP_K_DOCUMENTS`: Number of documents to retrieve (default: 3)
- `SIMILARITY_THRESHOLD`: Minimum similarity score (default: 0.5)

### Response Generation

- `MAX_TOKENS`: Maximum response length (default: 1000)
- `TEMPERATURE`: Creativity level 0.0-1.0 (default: 0.7)

## 🔑 Getting API Keys

### OpenAI

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up or log in
3. Create a new API key
4. Copy and paste into `.env`

### Groq

1. Visit [Groq Console](https://console.groq.com/keys)
2. Sign up (free tier available)
3. Create API key
4. Add to `.env`

### Google Gemini

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Get API Key"
3. Create new API key
4. Copy to `.env`

### Google Search (Optional)

1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Custom Search API
4. Create a Custom Search Engine ID
5. Add both to `.env`

## 📦 Dependencies

### Core

- **streamlit**: Web UI framework
- **langchain**: LLM orchestration framework
- **python-dotenv**: Environment variable management

### LLM Providers

- **langchain-groq**: Groq integration
- **langchain-openai**: OpenAI integration
- **langchain-google-genai**: Google Gemini integration

### RAG & Embeddings

- **sentence-transformers**: Embedding generation
- **faiss-cpu**: Vector database
- **langchain-huggingface**: HuggingFace embeddings integration
- **langchain-community**: FAISS wrapper

### Document Processing

- **PyPDF2**: PDF text extraction

### Web Search

- **duckduckgo-search**: DuckDuckGo search (fallback)
- **google-api-python-client**: Google Search API

## 🚀 Deployment

### ✨ Live Instance

**The application is already deployed and live!**

- **Live URL**: [https://aditi072004-neostats-ai-chatbot.streamlit.app](https://aditi072004-neostats-ai-chatbot.streamlit.app)
- **Status**: ✅ Fully operational with RAG, Web Search, and Multi-LLM support
- **Repository**: [https://github.com/ADITI072004/neostats-ai-chatbot](https://github.com/ADITI072004/neostats-ai-chatbot)

**Try it now!** No installation needed - just visit the link above.

### Streamlit Cloud (Recommended)

1. **Push to GitHub**

   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [Streamlit Cloud](https://streamlit.io/cloud)
   - Connect your GitHub account
   - Select your repository
   - Click "Deploy"

3. **Add Secrets**
   - In Streamlit Cloud, go to Settings → Secrets
   - Add your API keys in the secrets manager (not in code)

4. **Share Your App**
   - Get a public URL like `https://yourusername-appname.streamlit.app`

### Docker (Optional)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

Run with:

```bash
docker build -t neostats-ai .
docker run -p 8501:8501 neostats-ai
```

## 🐛 Troubleshooting

### Issue: "API key not configured"

**Solution**: Check that your `.env` file exists and contains valid API keys

### Issue: "Vector store not found"

**Solution**: Upload and ingest documents first using the RAG interface

### Issue: Web search not working

**Solution**: Google Search API key is optional; the app falls back to DuckDuckGo automatically

### Issue: Slow embedding generation

**Solution**: Use a smaller embedding model:

```env
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2  # Faster
```

### Issue: Out of memory (large documents)

**Solution**: Reduce `CHUNK_SIZE` or process documents in smaller batches

## 📊 Performance Tips

1. **Use Groq for Speed**: Fastest LLM provider
2. **Adjust Chunk Size**: Smaller chunks = faster retrieval, larger chunks = more context
3. **Limit TOP_K_DOCUMENTS**: Fewer documents = faster responses
4. **Use Embeddings Cache**: Vector store persists across sessions

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is provided as-is for educational and commercial use.

## 📧 Support

For issues or questions:

- Open an issue on GitHub
- Check the troubleshooting section above
- Review the inline code comments

## 🎯 Future Enhancements

- [ ] Support for more document formats (DOCX, Excel, etc.)
- [ ] Multi-file batch processing
- [ ] Advanced filtering and metadata-based retrieval
- [ ] Integration with databases
- [ ] Multi-language support
- [ ] Conversation memory with summaries
- [ ] Cost tracking for API usage

## 🌟 Acknowledgments

Built with:

- [Streamlit](https://streamlit.io) - Web UI
- [LangChain](https://langchain.com) - LLM Framework
- [Sentence Transformers](https://www.sbert.net) - Embeddings
- [FAISS](https://faiss.ai) - Vector Database

---

**Made with ❤️ for the NeoStats AI Engineer Use Case**
