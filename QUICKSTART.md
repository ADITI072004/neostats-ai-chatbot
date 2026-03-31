# 🚀 Quick Start Guide

Get the NeoStats AI Chatbot up and running in 5 minutes!

## Prerequisites

- Python 3.8+
- An API key from at least one LLM provider (Groq/OpenAI/Gemini)

## Installation (5 minutes)

### 1. Clone/Extract Project

```bash
cd /path/to/NeoStats_AI_UseCase
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

**Copy the template:**

```bash
cp .env.example .env
```

**Edit `.env` file and add your API keys:**

```env
# Required: At least one LLM provider
GROQ_API_KEY=gsk_xxxxxxxxxxxx
# OR
OPENAI_API_KEY=sk-xxxxxxxxxxxx
# OR
GEMINI_API_KEY=AIzaxxxxxxxxxxxx

# Optional: For web search
GOOGLE_SEARCH_API_KEY=xxxxx
GOOGLE_SEARCH_ENGINE_ID=xxxxx
```

### 5. Run the App

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

---

## Getting API Keys (Choose One)

### ✅ **Groq** (Recommended - Free & Fast)

1. Visit https://console.groq.com/keys
2. Sign up (free)
3. Create API key
4. Copy to `.env`

### 💳 **OpenAI** (Premium Quality)

1. Visit https://platform.openai.com/api-keys
2. Create API key
3. Set up billing
4. Copy to `.env`

### 🎯 **Google Gemini** (Free Tier)

1. Visit https://aistudio.google.com/app/apikey
2. Click "Get API Key"
3. Create free API key
4. Copy to `.env`

---

## First Steps

### 1️⃣ **Start Chatting**

- Type a message and hit Enter
- Select your LLM provider in sidebar
- Choose concise or detailed response mode

### 2️⃣ **Upload Documents (Optional)**

- Sidebar → Upload documents
- Select PDF or TXT files
- Click "Ingest Documents"
- Ask questions about your docs

### 3️⃣ **Enable Web Search (Optional)**

- Check "Use Web Search" in sidebar
- Chatbot will search web for current info
- See sources in "View sources"

---

## Common Commands

| Action                 | How                                   |
| ---------------------- | ------------------------------------- |
| Change AI Provider     | Sidebar → "Select LLM Provider"       |
| Change Response Length | Sidebar → "Response Mode"             |
| Upload Documents       | Sidebar → "Upload documents" → Ingest |
| Clear History          | Sidebar → "Clear Chat History" button |
| Clear Vector Store     | Sidebar → "Clear Vector Store" button |
| Customize AI Behavior  | Sidebar → Edit "System Prompt"        |

---

## Troubleshooting

### "API key not configured"

✅ **Fix**: Add API key to `.env` and restart the app

### "ModuleNotFoundError"

✅ **Fix**: Run `pip install -r requirements.txt`

### "Port already in use"

✅ **Fix**: Change port in `.streamlit/config.toml`:

```toml
[server]
port = 8502  # Try different number
```

### Documents not found

✅ **Fix**: Upload documents first, then ask questions

### Slow responses

✅ **Fix**: Use Groq provider (fastest), or reduce `MAX_TOKENS`

---

## Example Usage

### Chat Example 1: General Q&A

```
User: "What are the benefits of meditation?"
Assistant: [Concise or detailed response]
```

### Chat Example 2: Document Q&A (with RAG)

```
1. Upload your meditation guide PDF
2. Ask: "According to my document, what meditation techniques are mentioned?"
Assistant: [References your document] "Your guide mentions..."
```

### Chat Example 3: Live Information (with Web Search)

```
User: "What are the latest Python releases in 2024?"
Assistant: [Searches web] "According to recent sources..."
```

---

## File Structure Quick Reference

```
NeoStats_AI_UseCase/
├── app.py ........................... Main chatbot interface
├── config/config.py ................. Configuration & API keys
├── models/
│   ├── llm.py ....................... LLM providers
│   └── embeddings.py ................ Embedding models
├── utils/
│   ├── rag.py ....................... Document processing
│   └── web_search.py ................ Web search
├── .env ............................. Your API keys (create from .env.example)
├── requirements.txt ................. Python dependencies
└── README.md ........................ Full documentation
```

---

## Next Steps

### For Basic Usage

✅ Run the app and start chatting!

### For Document Analysis

✅ Upload PDFs/TXT files and ask about them

### For Production Deployment

✅ See [DEPLOYMENT.md](DEPLOYMENT.md) for Streamlit Cloud setup

### For Advanced Features

✅ See [FEATURES.md](FEATURES.md) for detailed feature guide

---

## Tips for Best Results

1. **Be Specific**: Ask clear, specific questions
2. **Provide Context**: Add background info if needed
3. **Use Right Mode**: Concise for quick answers, Detailed for learning
4. **Upload Relevant Docs**: RAG works best with on-topic documents
5. **Check Sources**: Review document/web sources for accuracy

---

## Getting Help

- 📖 **Full Docs**: See [README.md](README.md)
- 🎓 **Features**: See [FEATURES.md](FEATURES.md)
- 🚀 **Deployment**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- 💬 **Issues**: Open GitHub issue or check code comments

---

## Performance Tips

- **Faster responses**: Use Groq provider
- **Better quality**: Use OpenAI
- **Free tier**: Use Gemini or Groq
- **Shorter responses**: Use Concise mode
- **Faster retrieval**: Upload fewer documents

---

**You're all set! Start chatting! 🎉**

Questions? Check the full [README.md](README.md)
