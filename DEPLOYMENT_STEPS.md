# 🚀 Streamlit Cloud Deployment Checklist

## Step 1: Update Your API Keys (IMPORTANT)

Edit `.streamlit/secrets.toml` and add your API keys:

```bash
# Open the file in VS Code
code .streamlit/secrets.toml
```

**Recommended Setup (Free Options):**
- **Groq API** (REQUIRED for basic chat):
  1. Go to https://console.groq.com/keys
  2. Sign up/Login (Free tier available)
  3. Copy your API key to `GROQ_API_KEY = "gsk_..."`

- **Optional - OpenAI** (if you have credits):
  1. Get key from https://platform.openai.com/api-keys
  2. Add to `OPENAI_API_KEY`

- **Optional - Google Gemini**:
  1. Get key from https://ai.google.dev/
  2. Add to `GEMINI_API_KEY`

- **Optional - Web Search**:
  - Leave empty to use DuckDuckGo (free, no key needed)

---

## Step 2: Initialize Git (if not already done)

```powershell
# Check if git is initialized
git status

# If not initialized, run:
git init
git add .
git commit -m "NeoStats AI Chatbot - Ready for deployment"
```

---

## Step 3: Create GitHub Repository

### Option A: Using GitHub Web Interface
1. Go to https://github.com/new
2. Create new repository (any name, e.g., "neostats-ai-chatbot")
3. Copy the repository URL

### Option B: Using GitHub CLI
```powershell
# Install GitHub CLI if needed
# Then authenticate and create repo
gh repo create neostats-ai-chatbot --public --source=. --remote=origin --push
```

---

## Step 4: Push Code to GitHub

```powershell
# Add remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/neostats-ai-chatbot.git

# Rename branch to main (if needed)
git branch -M main

# Push code
git push -u origin main
```

---

## Step 5: Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud**: https://share.streamlit.io/
2. **Login with GitHub** (authorize if needed)
3. **Click "New app"** button
4. **Select your repository**:
   - Owner: Your GitHub username
   - Repository: neostats-ai-chatbot
   - Branch: main
   - File path: app.py
5. **Click "Deploy"**

The app will deploy in 2-3 minutes. Streamlit shows a live deployment log.

---

## Step 6: Add Secrets on Streamlit Cloud

**After deployment completes:**

1. **Click the hamburger menu (≡)** in top right
2. **Click "Settings"**
3. **Go to "Secrets" tab**
4. **Copy your API keys from `.streamlit/secrets.toml`:**
   ```toml
   GROQ_API_KEY = "gsk_..."
   OPENAI_API_KEY = "sk_..."
   GEMINI_API_KEY = "AIza..."
   GOOGLE_SEARCH_API_KEY = "..."
   GOOGLE_SEARCH_ENGINE_ID = "..."
   DEFAULT_LLM_PROVIDER = "groq"
   ENABLE_RAG = true
   ENABLE_WEB_SEARCH = true
   MAX_TOKENS = 1000
   TEMPERATURE = 0.7
   ```
5. **Click "Save"**
6. **Streamlit auto-reloads** with your secrets

---

## Step 7: Test Your Deployed App

1. **Streamlit shows your live URL**: `https://[your-app-name].streamlit.app`
2. **Test the chatbot**:
   - ✅ Chat without documents (uses default LLM)
   - ✅ Upload a PDF/TXT file (tests RAG)
   - ✅ Toggle response modes (Concise↔Detailed)
   - ✅ Switch LLM providers

---

## Troubleshooting

### App Shows "No module found"
- Ensure `requirements.txt` is correct
- Check Streamlit deployment logs

### API Key Not Working
- Verify key is correct in Secrets
- Try simple test in Chat
- Check provider supports the request

### App Runs Slow First Time
- Normal! First load downloads ~91MB embedding model
- Subsequent reloads are instant

### Secret Not Updating
- Click the menu and "Rerun app"
- Or wait 30 seconds for auto-refresh

---

## Result

Your chatbot will be live at: **https://[your-app-name].streamlit.app**

Share this URL with anyone! They can use the chatbot immediately.

---

## Quick Links

- [Streamlit Cloud](https://share.streamlit.io/)
- [GitHub New Repo](https://github.com/new)
- [Groq API Keys](https://console.groq.com/keys)
- [OpenAI API Keys](https://platform.openai.com/api-keys)
