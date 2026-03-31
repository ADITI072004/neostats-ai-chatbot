# 🛠️ Development & Maintenance Guide

## Development Workflow

### Setting Up for Development

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/NeoStats_AI_UseCase.git
cd NeoStats_AI_UseCase

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies (with dev tools)
pip install -r requirements.txt
pip install black flake8 pytest

# 4. Setup environment
cp .env.example .env
# Edit .env with your API keys

# 5. Run app in development mode
streamlit run app.py --logger.level=debug
```

### Code Style

**Formatting with Black**

```bash
black app.py models/ utils/ config/
```

**Linting with Flake8**

```bash
flake8 app.py models/ utils/ config/
```

### Version Control

```bash
# Create feature branch
git checkout -b feature/your-feature

# Make changes
git add .
git commit -m "feat: add your feature description"

# Push to GitHub
git push origin feature/your-feature

# Create Pull Request on GitHub
# → Merge after review
```

---

## Project Modules

### `config/config.py`

**Purpose**: Centralized configuration

**Modify for**:

- Adding new API keys → `OPENAI_API_KEY = os.getenv(...)`
- New features flags → `ENABLE_FEATURE = os.getenv(...)`
- Changing defaults → Update the `os.getenv()` calls

**Example**: Add Claude API

```python
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")
```

### `models/llm.py`

**Purpose**: LLM provider implementations

**Modify for**:

- Adding new LLM provider → Add method `_create_provider()`
- Adjusting parameters → Update provider initialization

**Example**: Add Anthropic Claude

```python
@staticmethod
def _create_claude(model: str = None, ...):
    from langchain_anthropic import ChatAnthropic
    return ChatAnthropic(api_key=CLAUDE_API_KEY, ...)
```

### `models/embeddings.py`

**Purpose**: Embedding model handling

**Modify for**:

- Adding embedding providers
- Switching default embedding model

**Example**: Add Cohere embeddings

```python
if self.provider.lower() == "cohere":
    from langchain_cohere import CohereEmbeddings
    self.model = CohereEmbeddings(cohere_api_key=COHERE_KEY)
```

### `utils/rag.py`

**Purpose**: RAG system (document processing)

**Modify for**:

- Adding document format support (DOCX, Excel)
- Changing chunking strategy
- Adjusting retrieval logic

**Example**: Add DOCX support

```python
elif file_extension == '.docx':
    from docx import Document
    doc = Document(file_path)
    content = '\n'.join([p.text for p in doc.paragraphs])
```

### `utils/web_search.py`

**Purpose**: Web search integration

**Modify for**:

- Adding new search providers
- Adjusting result formatting
- Changing search parameters

**Example**: Add Bing search

```python
def _init_bing_search(self):
    from bing_search_api import BingSearcher
    self.bing = BingSearcher(api_key=BING_API_KEY)
```

### `app.py`

**Purpose**: Streamlit UI

**Modify for**:

- Changing UI layout
- Adding new pages
- Modifying chat interface
- Adjusting sidebar controls

**Example**: Add Analysis page

```python
elif page == "Analysis":
    analysis_page()
```

---

## Adding New Features

### 1. Add Document Format Support

**Files to modify**:

- `utils/rag.py` → Add format handler
- `app.py` → Update file uploader accept_multiple_files

**Steps**:

```python
# In utils/rag.py, add to _load_and_split_document():
elif file_extension == '.docx':
    from docx import Document
    doc = Document(file_path)
    content = '\n'.join([p.text for p in doc.paragraphs])
```

### 2. Add New Response Mode

**Files to modify**:

- `config/config.py` → Add to RESPONSE_MODES
- `app.py` → Automatically reads from config

**Steps**:

```python
# In config/config.py:
RESPONSE_MODES = {
    "technical": {
        "description": "Code-focused, technical responses",
        "system_prompt": "You are a technical expert..."
    },
    # ... existing modes
}
```

### 3. Add New LLM Provider

**Files to modify**:

- `config/config.py` → Add API key
- `models/llm.py` → Add factory method
- `app.py` → Update provider list

**Steps**:

```python
# 1. config/config.py
MYMODEL_API_KEY = os.getenv("MYMODEL_API_KEY", "")

# 2. models/llm.py
@staticmethod
def _create_mymodel(model, temp, tokens):
    from langchain_mymodel import ChatMyModel
    return ChatMyModel(api_key=MYMODEL_API_KEY, ...)

# 3. app.py - auto-reads from llm_provider list
st.session_state.llm_provider = st.selectbox(
    "Select LLM", ["openai", "groq", "gemini", "mymodel"]
)
```

### 4. Add Chat Memory/Context

**Implementation**:

```python
# Add to app.py session state initialization
if 'conversation_summary' not in st.session_state:
    st.session_state.conversation_summary = ""

# Periodically summarize
if len(st.session_state.chat_history) % 10 == 0:
    summary = llm.summarize(st.session_state.chat_history)
    st.session_state.conversation_summary = summary
```

### 5. Add Multi-turn Context

**Files to modify**: `app.py`

**Implementation**:

```python
# Keep last N messages for context
CONTEXT_WINDOW = 5

relevant_messages = st.session_state.chat_history[-CONTEXT_WINDOW:]
for msg in relevant_messages:
    formatted_messages.append(...)
```

---

## Troubleshooting Guide

### Common Issues & Fixes

#### Issue: "Module not found" error

```
Error: ModuleNotFoundError: No module named 'langchain_groq'

Fix:
1. pip install -r requirements.txt
2. pip install langchain-groq
3. Restart app: streamlit run app.py
```

#### Issue: "API key not found"

```
Error: ValueError: Groq API key not configured

Fix:
1. Check .env file exists
2. Verify key is correct (test on provider's website)
3. Restart app (streamlit caches imports)
4. Check environment: echo $GROQ_API_KEY
```

#### Issue: "Vector store not initialized"

```
Error: Vector store is None

Fix:
1. Upload documents first using UI
2. Check logs for ingestion errors
3. Verify VECTOR_DB_PATH is writable
4. Clear and re-ingest: Clear Vector Store button
```

#### Issue: Slow document processing

```
Slow: Taking >2 minutes to ingest 10MB PDF

Fix:
1. Reduce CHUNK_SIZE (e.g., 300 from 500)
2. Process fewer files at once
3. Use smaller embedding model
4. Close other processes (free RAM)
```

#### Issue: Web search returns no results

```
Error: No search results found

Fix:
1. This is normal for very specific queries
2. Check internet connection
3. Try broader search terms
4. Verify Google Search API keys (if using)
```

### Debug Mode

**Enable debug logging**:

```bash
streamlit run app.py --logger.level=debug
```

**Check logs**:

```bash
tail -f logs/app.log
```

**Add debug prints**:

```python
import logging
logger = logging.getLogger(__name__)
logger.debug(f"Debug info: {variable}")
```

---

## Testing

### Manual Testing

```python
# Test individual modules
python -c "from models.llm import get_llm; llm = get_llm('groq'); print(llm)"
python -c "from utils.rag import get_rag_system; rag = get_rag_system(); print('RAG OK')"
python -c "from utils.web_search import get_web_searcher; ws = get_web_searcher(); print('Search OK')"
```

### Automated Testing (Optional)

```bash
# Create tests/test_llm.py
import pytest
from models.llm import LLMFactory

def test_groq_creation():
    llm = LLMFactory.create_llm("groq")
    assert llm is not None

def test_embedding_initialization():
    from models.embeddings import get_embedding_model
    model = get_embedding_model()
    assert model is not None

# Run tests
pytest tests/ -v
```

---

## Performance Optimization

### Caching Results

```python
# In app.py
@st.cache_resource
def get_cached_rag_system():
    return get_rag_system()

# Use cached version
rag = get_cached_rag_system()
```

### Reducing Token Usage

```python
# In config.py
MAX_TOKENS = 500  # Reduce from 1000
TEMPERATURE = 0.5  # Lower = faster
```

### Batch Processing

```python
# Process multiple files at once
def ingest_multiple_documents(directory):
    files = glob.glob(f"{directory}/*.pdf")
    results = rag_system.ingest_documents(files)
    return results
```

---

## Monitoring & Analytics

### User Activity Logging

```python
# Add to app.py
def log_user_activity(activity_type, details):
    with open('logs/user_activity.log', 'a') as f:
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp} | {activity_type} | {details}\n")

# Use when events occur
log_user_activity("DOCUMENT_UPLOAD", f"file={filename}")
```

### Cost Tracking

```python
# Track token usage per provider
def log_token_usage(provider, prompt_tokens, completion_tokens):
    cost = calculate_cost(provider, prompt_tokens, completion_tokens)
    logger.info(f"Provider: {provider}, Cost: ${cost:.4f}")
```

---

## Deployment Updates

### Pushing Updates to Streamlit Cloud

```bash
# 1. Make changes locally
# 2. Test: streamlit run app.py
# 3. Commit and push
git add .
git commit -m "fix: update feature xyz"
git push origin main

# Streamlit Cloud auto-deploys!
# Monitor: Check "Logs" tab in Streamlit Cloud dashboard
```

### Database Migration (If Using)

```python
# Add migration support for future use
def migrate_vector_store():
    """Migrate from FAISS to cloud-based vector DB"""
    # Load from FAISS
    old_store = FAISS.load_local(...)

    # Convert to cloud format
    # Upload to Pinecone/Weaviate/Qdrant
    pass
```

---

## Code Review Checklist

Before pushing code, verify:

- [ ] All error cases handled with try/except
- [ ] Logging added for debugging
- [ ] API keys in config, not hardcoded
- [ ] Code follows existing patterns
- [ ] Docstrings added to functions
- [ ] Requirements.txt updated if new packages
- [ ] No sensitive data in logs/prints
- [ ] Tested locally
- [ ] Code formatted with black
- [ ] No unused imports (check flake8)

---

## Maintenance Schedule

### Daily

- Monitor app uptime
- Check error logs
- Review user feedback

### Weekly

- Update dependencies (pip list --outdated)
- Review usage statistics
- Check cost/quota usage

### Monthly

- Security audit
- Performance review
- Feature request analysis
- Update documentation

### Quarterly

- Plan new features
- Review architecture
- Consider refactoring
- Update presentation

---

## Common Enhancement Ideas

### Quick Wins (1-2 hours)

- [ ] Add dark mode toggle
- [ ] Improve UI styling
- [ ] Add keyboard shortcuts
- [ ] Save conversations to file

### Medium Tasks (half day)

- [ ] Add conversation history persistence
- [ ] Implement User authentication
- [ ] Add cost calculator
- [ ] Multi-language UI

### Larger Projects (1-2 days)

- [ ] Vector store migration to cloud
- [ ] Advanced document filtering
- [ ] Batch processing interface
- [ ] Analytics dashboard
- [ ] Integration with Slack/Discord

---

## Resources

- [Streamlit Docs](https://docs.streamlit.io)
- [LangChain Documentation](https://python.langchain.com)
- [FAISS Documentation](https://faiss.ai)
- [Sentence Transformers](https://www.sbert.net)

---

**Happy coding! Keep the project maintained and continuously improve! 🚀**
