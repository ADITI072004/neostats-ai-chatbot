# 📚 Features Guide - NeoStats AI Chatbot

## 1. RAG (Retrieval-Augmented Generation)

### What is RAG?

RAG allows the chatbot to reference your own documents, creating responses based on your data rather than just general knowledge.

### How to Use RAG

#### Step 1: Prepare Documents

- **Supported formats**: TXT, PDF
- **Optimal file size**: 1-50 MB per file
- **Language**: Currently supports English (can be extended)

#### Step 2: Upload Documents

1. Go to **Chat** page
2. In the sidebar, click **📚 RAG Settings**
3. Drag and drop or select documents
4. Click **📤 Ingest Documents**

```
Process Flow:
Document Upload
    ↓
Text Extraction (PDF/TXT)
    ↓
Text Chunking (500 tokens each)
    ↓
Embedding Generation
    ↓
Vector Store (FAISS)
    ↓
Ready for Queries
```

#### Step 3: Ask Questions About Your Documents

- Simply ask questions in the chat
- The system automatically retrieves relevant chunks
- Context is added to the LLM's system prompt
- Response includes source citations

### RAG Configuration

| Setting                | Default | Effect                                                             |
| ---------------------- | ------- | ------------------------------------------------------------------ |
| `CHUNK_SIZE`           | 500     | Smaller = more granular retrieval, larger = more context per chunk |
| `CHUNK_OVERLAP`        | 50      | Overlap ensures smooth context transitions                         |
| `TOP_K_DOCUMENTS`      | 3       | Number of document chunks to retrieve                              |
| `SIMILARITY_THRESHOLD` | 0.5     | Minimum relevance score (0.0-1.0)                                  |

### RAG Best Practices

✅ **Do:**

- Upload documents related to your topic
- Use clear, well-structured documents
- Keep documents updated
- Ask specific questions

❌ **Don't:**

- Upload documents in unsupported formats
- Expect RAG to work without documents uploaded
- Upload sensitive information (it's stored locally)

### Advanced RAG Usage

#### Clear Vector Store

If you want to start fresh:

1. Click **🗑️ Clear Vector Store** in sidebar
2. Upload new documents

#### Check What's Indexed

After ingestion, look for:

- ✅ Success message with file count
- Check **View sources** in responses to see retrieved chunks

---

## 2. Live Web Search Integration

### What is Web Search?

When the LLM doesn't have enough information from its training data or your documents, it can search the web for real-time information.

### How Web Search Works

```
User Query
    ↓
Check if RAG has info
    ↓
If not sufficient → Web Search
    ↓
Format Results
    ↓
Include in LLM Prompt
    ↓
Generate Response
```

### Web Search Providers

#### Option 1: Google Search API (Recommended)

- **Accuracy**: High
- **Speed**: Fast
- **Cost**: Free tier (100 searches/day)
- **Setup**: Requires API keys

#### Option 2: DuckDuckGo (Fallback)

- **Accuracy**: Good
- **Speed**: Fast
- **Cost**: Free
- **Privacy**: Better privacy

### Enabling Web Search

**In `.env` file:**

```env
ENABLE_WEB_SEARCH=true

# For Google (optional)
GOOGLE_SEARCH_API_KEY=your_key_here
GOOGLE_SEARCH_ENGINE_ID=your_engine_id_here
```

### Using Web Search

1. **Automatic**: Toggle **Use Web Search** in sidebar
2. **Check results**: Click **📖 View sources** to see where information came from
3. **No setup needed**: Falls back to DuckDuckGo automatically

### Web Search Configuration

| Setting        | Default    | Note                              |
| -------------- | ---------- | --------------------------------- |
| Search Results | 3-5        | Number of web results to retrieve |
| Provider       | DuckDuckGo | Falls back if Google keys missing |

### Web Search Limitations

⚠️ **Note:**

- Limited to public web content
- May return promotional/low-quality results
- Subject to search engine rate limits
- Requires internet connection

---

## 3. Response Modes

### Concise Mode

**Best for:**

- Quick answers
- Quick information needs
- Users on limited time
- Mobile usage

**What it does:**

- Limits response to ~200 words
- Focuses on key points
- Removes excessive details
- No lengthy examples

**Example:**

```
Q: "What is machine learning?"
A: "Machine learning is a branch of AI that enables
systems to learn and improve from data without
explicit programming. Algorithms identify patterns
in data to make predictions or decisions."
```

### Detailed Mode

**Best for:**

- In-depth learning
- Complex topics
- Research
- Professional use

**What it does:**

- Provides comprehensive responses
- Includes explanations and examples
- Covers multiple perspectives
- Adds context and background

**Example:**

```
Q: "What is machine learning?"
A: "Machine learning is a subset of artificial intelligence
that focuses on developing algorithms that can learn from
and make predictions on data.

There are three main types:
1. Supervised Learning - Learning from labeled data
2. Unsupervised Learning - Finding patterns without labels
3. Reinforcement Learning - Learning through interaction

Applications include...
[Full detailed response]
```

### Switching Modes

1. **In Sidebar**: Select "Response Mode" dropdown
2. **Choose**:
   - ✨ Concise
   - 📖 Detailed

Changes take effect immediately on next message.

### Custom System Prompts

You can customize how the AI behaves:

1. **Scroll to "System Prompt"** in sidebar
2. **Edit the text** to modify behavior
3. **Examples:**

**For a teacher:**

```
You are an expert educator. Explain concepts clearly
with examples. Always break down complex topics into
simpler parts. Use analogies when helpful.
```

**For a code reviewer:**

```
You are an expert code reviewer. Analyze code for
security, performance, and best practices. Provide
specific improvement suggestions with code examples.
```

**For a creative writer:**

```
You are a creative writing assistant. Help craft
engaging narratives with vivid descriptions and
compelling dialogue.
```

---

## 4. LLM Provider Selection

### Supported Providers

#### Groq (Default)

- **Speed**: ⚡⚡⚡⚡⚡ (Fastest)
- **Quality**: ⭐⭐⭐⭐ (Excellent)
- **Cost**: 💰 Free
- **Best for**: All purposes, especially speed-critical tasks
- **Models**: Llama 3.1, Mixtral

#### OpenAI (Premium)

- **Speed**: ⚡⚡⚡ (Good)
- **Quality**: ⭐⭐⭐⭐⭐ (Best)
- **Cost**: 💰💰💰 (Paid)
- **Best for**: High-quality responses, creative tasks
- **Models**: GPT-4, GPT-4o, GPT-3.5-turbo

#### Google Gemini (Balanced)

- **Speed**: ⚡⚡⚡⚡ (Very good)
- **Quality**: ⭐⭐⭐⭐⭐ (Excellent)
- **Cost**: 💰 Free tier available
- **Best for**: Balanced performance and quality
- **Models**: Gemini 1.5 Pro/Flash

### Switching Providers

1. **In Sidebar**: Select "Select LLM Provider"
2. **Choose**: openai, groq, or gemini
3. **Ensure API key** is configured in `.env`

### Provider Comparison

| Feature        | Groq      | OpenAI | Gemini    |
| -------------- | --------- | ------ | --------- |
| Speed          | Fastest   | Fast   | Very Fast |
| Quality        | Excellent | Best   | Excellent |
| Cost           | Free      | Paid   | Free/Paid |
| Availability   | High      | High   | High      |
| Context Window | Large     | Large  | Large     |

---

## 5. Advanced Features

### Chat History Management

**Persistence:**

- ✅ Saved during session
- ❌ Not saved after refresh (by design)
- Use **Clear Chat History** button to reset

**Export Conversation:**

```
Copy/paste from browser or implement custom export
```

### Batch Document Processing

**For multiple documents:**

1. Select all files at once
2. Click **Ingest Documents**
3. System processes in sequence

### Document Management

```
Document Lifecycle:
Upload → Extraction → Chunking → Embedding → Storage
```

**Check ingestion status:**

- Success message shows file count
- ✅ Successful count
- ❌ Failed count with errors

---

## 6. Troubleshooting Features

### RAG Issues

**Problem**: "No relevant documents found"

- **Solution**: Your documents may not match the query. Try uploading more relevant documents.

**Problem**: Slow document processing

- **Solution**: Reduce `CHUNK_SIZE` or process fewer files at once

**Problem**: Vector store errors

- **Solution**: Clear vector store and re-upload documents

### Web Search Issues

**Problem**: "No search results"

- **Solution**: Check internet connection, or the query may be too specific

**Problem**: Slow search

- **Solution**: App falls back to DuckDuckGo if Google is slow (normal)

### LLM Issues

**Problem**: "API key not found"

- **Solution**: Add API key to `.env` file and restart app

**Problem**: Slow response generation

- **Solution**: Switch to Groq (fastest), reduce MAX_TOKENS

---

## 7. Example Workflows

### Workflow 1: Research Assistant

1. Upload research papers or notes
2. Use **Detailed** response mode
3. Ask questions about content
4. Enable web search for current information
5. Use Gemini for balanced response quality

### Workflow 2: Quick Answers

1. Disable RAG (if not needed)
2. Use **Concise** response mode
3. Use Groq for speed
4. Ask direct questions

### Workflow 3: Document Analysis

1. Upload business documents
2. Use **Detailed** response mode
3. Ask for summaries and insights
4. Check sources for data validation
5. Use OpenAI for highest quality

### Workflow 4: Real-time Information

1. Enable web search
2. Use **Concise** mode for quick facts
3. Ask current events questions
4. Check web sources for verification

---

## 🎓 Tips & Tricks

### Better RAG Results

- Use specific questions
- Ask about document content directly
- Start with "Based on the documents I uploaded..."

### Better Web Search

- Be specific with queries
- Include keywords from your actual question
- Check multiple sources if concerned about accuracy

### Better LLM Responses

- Use clear, specific prompts
- Adjust system prompt for your use case
- Use response mode matching your need
- Provide context in follow-up questions

### Cost Optimization

- Use Groq for free, fast responses
- OpenAI for high-quality needs only
- Keep token limits reasonable (500-1000)
- Use concise mode to reduce token usage

---

## 📊 Feature Comparison Matrix

| Feature        | Status       | Requires Setup | Free  |
| -------------- | ------------ | -------------- | ----- |
| Chat           | ✅ Always    | No             | Yes   |
| RAG            | ✅ Enabled   | No             | Yes   |
| Web Search     | ✅ Enabled   | Optional       | Yes\* |
| Groq           | ✅ Enabled   | API Key        | Yes   |
| OpenAI         | ✅ Available | API Key        | No    |
| Gemini         | ✅ Available | API Key        | Yes\* |
| Response Modes | ✅ Enabled   | No             | Yes   |

\*Free tiers available

---

**Need help? Check README.md or open an issue on GitHub!**
