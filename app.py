"""
NeoStats AI Engineer Use Case - Advanced Chatbot with RAG and Web Search
Features:
- Retrieval-Augmented Generation (RAG) for document knowledge
- Live web search integration
- Multiple LLM providers (OpenAI, Groq, Gemini)
- Concise and Detailed response modes
"""

import streamlit as st
import os
import sys
import logging
from datetime import datetime
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from models.llm import get_llm
from utils.rag import get_rag_system
from utils.web_search import get_web_searcher
from config.config import (
    DEFAULT_LLM_PROVIDER,
    RESPONSE_MODES,
    DEFAULT_RESPONSE_MODE,
    ENABLE_RAG,
    ENABLE_WEB_SEARCH,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Streamlit page configuration
st.set_page_config(
    page_title="NeoStats AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main { padding: 2rem; }
    .stTabs [data-baseweb="tab-list"] button { font-size: 1.1rem; }
    .chat-message { 
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        text-align: right;
    }
    .assistant-message {
        background-color: #f5f5f5;
    }
    .context-box {
        background-color: #fff9c4;
        border-left: 4px solid #fbc02d;
        padding: 1rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'rag_system' not in st.session_state:
    st.session_state.rag_system = get_rag_system() if ENABLE_RAG else None
if 'web_searcher' not in st.session_state:
    st.session_state.web_searcher = get_web_searcher() if ENABLE_WEB_SEARCH else None
if 'llm_provider' not in st.session_state:
    st.session_state.llm_provider = DEFAULT_LLM_PROVIDER
if 'response_mode' not in st.session_state:
    st.session_state.response_mode = DEFAULT_RESPONSE_MODE


def get_response_with_context(
    messages, 
    system_prompt, 
    use_rag=True, 
    use_web_search=True, 
    query=None
):
    """
    Get LLM response with context from RAG and web search
    
    Args:
        messages: Chat history
        system_prompt: System prompt
        use_rag: Whether to use RAG
        use_web_search: Whether to use web search
        query: User query for context retrieval
        
    Returns:
        Tuple of (response_text, context_sources)
    """
    try:
        context_sources = []
        augmented_system_prompt = system_prompt
        
        # Retrieve from RAG
        rag_context = ""
        if use_rag and st.session_state.rag_system and query:
            try:
                chunks = st.session_state.rag_system.retrieve_relevant_chunks(query)
                if chunks:
                    rag_context = st.session_state.rag_system.format_context(chunks)
                    context_sources.append({
                        'type': 'RAG',
                        'content': rag_context
                    })
            except Exception as e:
                logger.error(f"RAG retrieval error: {str(e)}")
        
        # Perform web search
        web_context = ""
        if use_web_search and st.session_state.web_searcher and query:
            try:
                search_results = st.session_state.web_searcher.search(query, num_results=3)
                if search_results:
                    web_context = st.session_state.web_searcher.format_search_results(search_results)
                    context_sources.append({
                        'type': 'Web Search',
                        'content': web_context
                    })
            except Exception as e:
                logger.error(f"Web search error: {str(e)}")
        
        # Combine contexts
        if rag_context or web_context:
            augmented_system_prompt = f"""{system_prompt}

{rag_context}

{web_context}

Please use the above information to provide an informed answer."""
        
        # Prepare messages
        formatted_messages = [SystemMessage(content=augmented_system_prompt)]
        
        for msg in messages:
            if msg["role"] == "user":
                formatted_messages.append(HumanMessage(content=msg["content"]))
            else:
                formatted_messages.append(AIMessage(content=msg["content"]))
        
        # Get LLM response
        llm = get_llm(provider=st.session_state.llm_provider)
        response = llm.invoke(formatted_messages)
        
        return response.content, context_sources
    
    except Exception as e:
        error_msg = f"Error getting response: {str(e)}"
        logger.error(error_msg)
        return error_msg, []


def instructions_page():
    """Instructions and setup page"""
    st.title("🤖 NeoStats AI Chatbot - Setup Guide")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("## 🔧 Installation")
        st.markdown("""
        Install required dependencies:
        ```bash
        pip install -r requirements.txt
        ```
        """)
    
    with col2:
        st.markdown("## 📝 API Keys Required")
        st.markdown("""
        - **OpenAI**: [Get API Key](https://platform.openai.com/api-keys)
        - **Groq**: [Get API Key](https://console.groq.com/keys)
        - **Gemini**: [Get API Key](https://aistudio.google.com/app/apikey)
        - **Google Search** (Optional): [Get API Key](https://developers.google.com/custom-search/v1/overview)
        """)
    
    st.markdown("## 📂 Folder Structure")
    st.code("""
    project/
    ├── config/
    │   └── config.py              # API keys & settings
    ├── models/
    │   ├── llm.py                 # LLM providers
    │   └── embeddings.py          # Embedding models
    ├── utils/
    │   ├── rag.py                 # RAG functionality
    │   └── web_search.py          # Web search
    ├── app.py                     # Main Streamlit app
    └── requirements.txt
    """)
    
    st.markdown("## 🎯 Features")
    st.markdown("""
    ✅ **RAG Integration**: Reference local documents and knowledge bases
    ✅ **Live Web Search**: Real-time information retrieval
    ✅ **Multi-LLM Support**: OpenAI, Groq, Google Gemini
    ✅ **Response Modes**: Switch between concise and detailed responses
    ✅ **Chat History**: Maintain conversation context
    ✅ **Error Handling**: Comprehensive try/except blocks
    """)
    
    st.markdown("## ⚙️ Configuration")
    st.info("""
    Set environment variables in `.env` file or directly in `config/config.py`:
    - OPENAI_API_KEY
    - GROQ_API_KEY
    - GEMINI_API_KEY
    - GOOGLE_SEARCH_API_KEY
    - DEFAULT_LLM_PROVIDER
    """)


def chat_page():
    """Main chat interface"""
    st.title("💬 Chat with AI Assistant")
    
    # Sidebar controls
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # LLM Provider selection
        st.session_state.llm_provider = st.selectbox(
            "Select LLM Provider",
            options=["openai", "groq", "gemini"],
            index=0
        )
        
        # Response mode selection
        st.session_state.response_mode = st.selectbox(
            "Response Mode",
            options=list(RESPONSE_MODES.keys()),
            format_func=lambda x: f"{x.capitalize()} - {RESPONSE_MODES[x]['description']}"
        )
        
        # System prompt customization
        st.markdown("### System Prompt")
        response_mode = RESPONSE_MODES.get(st.session_state.response_mode, {})
        default_prompt = response_mode.get('system_prompt', 'You are a helpful AI assistant.')
        system_prompt = st.text_area(
            "Customize system prompt:",
            value=default_prompt,
            height=100,
            key="system_prompt"
        )
        
        # RAG controls
        if ENABLE_RAG:
            st.markdown("### 📚 RAG Settings")
            
            # Document upload
            uploaded_files = st.file_uploader(
                "Upload documents (TXT, PDF)",
                type=["txt", "pdf"],
                accept_multiple_files=True
            )
            
            if uploaded_files:
                if st.button("📤 Ingest Documents", key="ingest_btn"):
                    with st.spinner("Processing documents..."):
                        try:
                            # Save uploaded files to temp location
                            temp_dir = tempfile.mkdtemp()
                            file_paths = []
                            
                            for uploaded_file in uploaded_files:
                                file_path = os.path.join(temp_dir, uploaded_file.name)
                                with open(file_path, 'wb') as f:
                                    f.write(uploaded_file.getbuffer())
                                file_paths.append(file_path)
                            
                            # Ingest documents
                            results = st.session_state.rag_system.ingest_documents(file_paths)
                            
                            st.success(f"✅ Documents ingested! ({results['successful']} successful)")
                            if results['errors']:
                                st.warning(f"⚠️ {len(results['errors'])} errors occurred")
                        
                        except Exception as e:
                            st.error(f"Error ingesting documents: {str(e)}")
            
            # Clear vector store button
            if st.button("🗑️ Clear Vector Store"):
                st.session_state.rag_system.clear_vector_store()
                st.success("Vector store cleared")
        
        # Feature toggles
        st.markdown("### Feature Toggles")
        use_rag = st.checkbox("Use RAG", value=ENABLE_RAG, disabled=not ENABLE_RAG)
        use_web_search = st.checkbox("Use Web Search", value=ENABLE_WEB_SEARCH, disabled=not ENABLE_WEB_SEARCH)
        
        # Clear chat history
        if st.button("🧹 Clear Chat History"):
            st.session_state.chat_history = []
            st.success("Chat history cleared")
    
    # Chat display
    st.markdown("### Chat History")
    chat_container = st.container()
    
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.write(msg["content"])
            else:
                with st.chat_message("assistant"):
                    st.write(msg["content"])
                    
                    # Display context sources
                    if "context_sources" in msg and msg["context_sources"]:
                        with st.expander("📖 View sources"):
                            for source in msg["context_sources"]:
                                st.markdown(f"**{source['type']}**")
                                st.markdown(source['content'])
    
    # User input
    st.markdown("---")
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.chat_input("Type your message...", key="chat_input")
    
    with col2:
        send_button = st.button("Send", use_container_width=True)
    
    if (user_input and send_button) or (user_input and not user_input.startswith("/")):
        # Prevent empty messages
        if not user_input.strip():
            st.warning("Please enter a message")
            return
        
        try:
            # Add user message to history
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Get system prompt
            response_mode = RESPONSE_MODES.get(st.session_state.response_mode, {})
            system_prompt = st.session_state.get("system_prompt", response_mode.get('system_prompt', 'You are a helpful AI assistant.'))
            
            # Get response with context
            with st.spinner("Generating response..."):
                response, context_sources = get_response_with_context(
                    st.session_state.chat_history[:-1],  # Exclude current user message
                    system_prompt,
                    use_rag=use_rag,
                    use_web_search=use_web_search,
                    query=user_input
                )
            
            # Add assistant message to history
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response,
                "context_sources": context_sources
            })
            
            # Refresh page to show new message
            st.rerun()
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
            logger.error(f"Chat error: {str(e)}")


def main():
    """Main app entry point"""
    # Navigation
    page = st.sidebar.radio(
        "Navigation",
        ["📖 Setup Instructions", "💬 Chat"]
    )
    
    if page == "📖 Setup Instructions":
        instructions_page()
    else:
        chat_page()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray; font-size: 0.8rem;'>
        NeoStats AI Engineer Use Case | Powered by Streamlit | 
        <a href='https://github.com'>GitHub</a>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()