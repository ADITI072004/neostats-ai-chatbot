# 🚀 Deployment Guide for NeoStats AI

## Deployment to Streamlit Cloud

This guide walks you through deploying the NeoStats AI chatbot to Streamlit Cloud for free hosting.

### Prerequisites

- GitHub account
- Streamlit Cloud account (free at https://streamlit.io/cloud)
- Project repository on GitHub

### Step-by-Step Deployment

#### 1. Prepare Your Repository

**Ensure your GitHub repository has:**

```
NeoStats_AI_UseCase/
├── app.py
├── requirements.txt
├── config/
├── models/
├── utils/
├── .gitignore
└── README.md
```

**Important: Make sure `.env` is in `.gitignore`** (it should never be committed)

#### 2. Create `.streamlit/secrets.toml`

**Create a new file**: `.streamlit/secrets.toml`

```toml
# LLM API Keys
OPENAI_API_KEY = "sk-..."
GROQ_API_KEY = "gsk_..."
GEMINI_API_KEY = "AIza..."

# Optional: Web Search
GOOGLE_SEARCH_API_KEY = "..."
GOOGLE_SEARCH_ENGINE_ID = "..."

# Config
DEFAULT_LLM_PROVIDER = "groq"
ENABLE_RAG = true
ENABLE_WEB_SEARCH = true
```

**Add `.streamlit/` to `.gitignore`:**

```
.streamlit/secrets.toml
```

#### 3. Push to GitHub

```bash
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

#### 4. Deploy on Streamlit Cloud

1. **Go to** [Streamlit Cloud](https://share.streamlit.io/)
2. **Click** "New app"
3. **Select your GitHub repository**
4. **Choose the branch** (main)
5. **Set the main file path** to `app.py`
6. **Click** "Deploy"

#### 5. Add Secrets on Streamlit Cloud

1. **In your app page**, click the **▶ (hamburger menu)** → **Settings**
2. **Go to "Secrets"** tab
3. **Paste your secrets** from `.streamlit/secrets.toml`
4. **Click Save**

⚠️ **Important**: Secrets are stored securely and NOT visible in the repository.

#### 6. Verify Deployment

1. **Wait for the app to load** (may take 1-2 minutes first time)
2. **Test the chat functionality**
3. **Upload a test document** to verify RAG works
4. **Try web search** if enabled

### Advanced Configuration

#### Custom Domain (Optional)

1. Go to App Settings → Custom Domain
2. Add your domain
3. Update DNS records as instructed

#### Environment Variables

Streamlit Cloud automatically loads variables from `secrets.toml` as environment variables.

To add more settings:

```python
import streamlit as st

api_key = st.secrets["OPENAI_API_KEY"]
```

#### Managing Costs

- **Groq**: Recommended for free tier (very fast, free)
- **OpenAI**: Charges per token (keep temperature lower for cost savings)
- **Gemini**: Free tier available

### Troubleshooting Deployment

#### Issue: "ModuleNotFoundError"

**Solution**: Check `requirements.txt` has all dependencies

```bash
pip freeze > requirements.txt
```

#### Issue: "API key not found"

**Solution**: Verify secrets are added in Streamlit Cloud settings

#### Issue: App loads slowly

**Solution**:

- First load takes longer (normal)
- Move document processing to background if needed
- Optimize chunk size

#### Issue: "Permission denied" on file operations

**Solution**:

- Streamlit Cloud has read-only filesystem
- Use `tempfile` for temp files (already implemented)
- Store vector DB in memory or use cloud storage

### Monitoring & Logging

#### View App Logs

1. **In Streamlit Cloud**, click **▶ (menu)** → **Manage app**
2. **Go to "Logs"** section
3. **Watch real-time logs** during usage

#### Error Tracking

All errors are logged with:

```python
logger.error(f"Error: {str(e)}")
```

Check logs for debugging issues.

### Updating Your App

**To deploy updates:**

1. **Make changes locally**

```bash
git add .
git commit -m "Update feature"
git push origin main
```

2. **Streamlit Cloud auto-deploys** (usually within seconds)

3. **Monitor the "Logs" section** to see if deployment succeeded

### Performance Optimization

#### For RAG with Large Documents

```python
# In config.py
CHUNK_SIZE = 300  # Smaller chunks = faster
CHUNK_OVERLAP = 30
TOP_K_DOCUMENTS = 2  # Retrieve fewer docs
```

#### For Faster Responses

```python
# Use Groq (fastest free option)
DEFAULT_LLM_PROVIDER = "groq"
MAX_TOKENS = 500  # Shorter responses
```

### Backup & Recovery

#### Backup Vector Database

The vector database is stored locally. To preserve it:

1. **Download from your local instance:**

```bash
# Vector store is in ./data/vector_db
```

2. **Upload to cloud storage** (AWS S3, Google Cloud Storage, etc.) if needed

### Scaling Considerations

For larger deployments, consider:

1. **Dedicated Docker Container** (Heroku, Railway, etc.)
2. **Cloud Database** for vector store (Pinecone, Weaviate, Qdrant)
3. **Load Balancing** for multiple instances
4. **CDN** for static assets

### Cost Estimates (Monthly)

| Provider        | Free      | Paid                     |
| --------------- | --------- | ------------------------ |
| Streamlit Cloud | Free      | Custom                   |
| Groq            | Free      | Free (unlimited)         |
| OpenAI          | -         | $0.01-0.10 per 1K tokens |
| Gemini          | Free tier | Custom                   |
| Google Search   | -         | Custom                   |

### Support & Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Streamlit Community**: https://discuss.streamlit.io
- **LangChain Docs**: https://python.langchain.com
- **GitHub Issues**: Create an issue in your repository

---

**Your app is now live! Share the URL with anyone to collaborate.**
