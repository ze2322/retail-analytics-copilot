<<<<<<< HEAD
import streamlit as st
import json
from agent.graph_hybrid import HybridAgent

# Page config
st.set_page_config(page_title="Retail Analytics Copilot", layout="wide", initial_sidebar_state="expanded")

# Title
st.title("🛍️ Retail Analytics Copilot")
st.markdown("Ask questions about retail analytics and get answers powered by document retrieval and SQL queries.")

# Initialize agent
@st.cache_resource
def load_agent():
    return HybridAgent()

agent = load_agent()

# Sidebar
with st.sidebar:
    st.header("Sample Questions")
    sample_questions = [
        "How many days can unopened beverages be returned?",
        "What was the category with the highest total quantity during summer 1997?",
        "What was the average order value during winter 1997?",
        "What are the top 3 products by revenue of all time?",
        "What was the total revenue for beverages during summer 1997?",
        "Which customer had the best gross margin in 1997?"
    ]
    
    selected_sample = st.selectbox("Or pick a sample question:", [""] + sample_questions)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    # Input
    query = st.text_area(
        "Enter your question:",
        value=selected_sample if selected_sample else "",
        height=100,
        placeholder="e.g., What was the total revenue for beverages?"
    )
    
    # Format hint selector
    format_hint = st.selectbox(
        "Expected output format:",
        ["int", "float", "list[{product:str, revenue:float}]", "{category:str, quantity:int}", "{customer:str, margin:float}"],
        help="Select the expected data type for the answer"
    )

with col2:
    st.markdown("### Quick Guide")
    st.info("""
    **Supported Formats:**
    - `int` - Integer number
    - `float` - Decimal number
    - `list[...]` - List of items
    - `{...}` - Dictionary/object
    """)

# Submit button
if st.button("🔍 Ask Question", type="primary", use_container_width=True):
    if not query.strip():
        st.warning("Please enter a question first!")
    else:
        with st.spinner("Processing question..."):
            result = agent.ask(query, format_hint)
        
        # Display results
        st.success("✅ Answer Generated")
        
        # Display answer prominently at top
        st.subheader("📌 Final Answer", divider="green")
        if result.get("final_answer") is not None:
            answer = result["final_answer"]
            if isinstance(answer, dict):
                # Display dict in a nice format
                for key, value in answer.items():
                    st.metric(label=key.capitalize(), value=value)
            elif isinstance(answer, list):
                # Display list items
                st.write(f"**Total items:** {len(answer)}")
                for idx, item in enumerate(answer, 1):
                    with st.expander(f"Item {idx}", expanded=True):
                        if isinstance(item, dict):
                            for k, v in item.items():
                                st.write(f"**{k}:** {v}")
                        else:
                            st.write(item)
            else:
                st.info(f"## {answer}")
        else:
            st.error("❌ No answer found")
        
        st.divider()
        
        # Create tabs for organized display
        tab1, tab2, tab3 = st.tabs(["Details", "Sources", "Raw JSON"])
        
        with tab1:
            st.subheader("Query Processing")
        
        with tab2:
            st.subheader("📚 Sources & Citations")
            citations = result.get("citations", [])
            if citations:
                st.write(f"**Total sources referenced:** {len(citations)}")
                col_doc, col_db = st.columns(2)
                
                docs = [c for c in citations if "::" in c]
                tables = [c for c in citations if "::" not in c]
                
                with col_doc:
                    if docs:
                        st.write("**📄 Document Chunks:**")
                        for citation in docs:
                            source, chunk = citation.split("::")
                            st.caption(f"- {source} → {chunk}")
                
                with col_db:
                    if tables:
                        st.write("**🗄️ Database Tables:**")
                        for table in tables:
                            st.caption(f"- {table}")
            else:
                st.caption("No citations available")
        
        with tab3:
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.metric("Confidence Score", f"{result.get('confidence', 0):.2f}")
            
            with col_b:
                route = "SQL Query" if result.get("sql") else "Document Retrieval"
                st.metric("Data Source", route)
            
            st.json(result)
        
        # SQL Query (if available)
        if result.get("sql"):
            with st.expander("📊 SQL Query Used"):
                st.code(result["sql"], language="sql")

# Footer
st.divider()
st.markdown("""
---
**Retail Analytics Copilot** | Hybrid RAG + SQL Engine
- 📚 Document retrieval from KPI definitions, product catalog, marketing calendar, and policies
- 🗄️ Direct SQL queries against Northwind database
- 🔄 Automatic fallback from SQL to document retrieval
- 📊 Confidence scoring and source citations
""")
=======
import streamlit as st
import json
from agent.graph_hybrid import HybridAgent

# Page config
st.set_page_config(page_title="Retail Analytics Copilot", layout="wide", initial_sidebar_state="expanded")

# Title
st.title("🛍️ Retail Analytics Copilot")
st.markdown("Ask questions about retail analytics and get answers powered by document retrieval and SQL queries.")

# Initialize agent
@st.cache_resource
def load_agent():
    return HybridAgent()

agent = load_agent()

# Sidebar
with st.sidebar:
    st.header("Sample Questions")
    sample_questions = [
        "How many days can unopened beverages be returned?",
        "What was the category with the highest total quantity during summer 1997?",
        "What was the average order value during winter 1997?",
        "What are the top 3 products by revenue of all time?",
        "What was the total revenue for beverages during summer 1997?",
        "Which customer had the best gross margin in 1997?"
    ]
    
    selected_sample = st.selectbox("Or pick a sample question:", [""] + sample_questions)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    # Input
    query = st.text_area(
        "Enter your question:",
        value=selected_sample if selected_sample else "",
        height=100,
        placeholder="e.g., What was the total revenue for beverages?"
    )
    
    # Format hint selector
    format_hint = st.selectbox(
        "Expected output format:",
        ["int", "float", "list[{product:str, revenue:float}]", "{category:str, quantity:int}", "{customer:str, margin:float}"],
        help="Select the expected data type for the answer"
    )

with col2:
    st.markdown("### Quick Guide")
    st.info("""
    **Supported Formats:**
    - `int` - Integer number
    - `float` - Decimal number
    - `list[...]` - List of items
    - `{...}` - Dictionary/object
    """)

# Submit button
if st.button("🔍 Ask Question", type="primary", use_container_width=True):
    if not query.strip():
        st.warning("Please enter a question first!")
    else:
        with st.spinner("Processing question..."):
            result = agent.ask(query, format_hint)
        
        # Display results
        st.success("✅ Answer Generated")
        
        # Display answer prominently at top
        st.subheader("📌 Final Answer", divider="green")
        if result.get("final_answer") is not None:
            answer = result["final_answer"]
            if isinstance(answer, dict):
                # Display dict in a nice format
                for key, value in answer.items():
                    st.metric(label=key.capitalize(), value=value)
            elif isinstance(answer, list):
                # Display list items
                st.write(f"**Total items:** {len(answer)}")
                for idx, item in enumerate(answer, 1):
                    with st.expander(f"Item {idx}", expanded=True):
                        if isinstance(item, dict):
                            for k, v in item.items():
                                st.write(f"**{k}:** {v}")
                        else:
                            st.write(item)
            else:
                st.info(f"## {answer}")
        else:
            st.error("❌ No answer found")
        
        st.divider()
        
        # Create tabs for organized display
        tab1, tab2, tab3 = st.tabs(["Details", "Sources", "Raw JSON"])
        
        with tab1:
            st.subheader("Query Processing")
        
        with tab2:
            st.subheader("📚 Sources & Citations")
            citations = result.get("citations", [])
            if citations:
                st.write(f"**Total sources referenced:** {len(citations)}")
                col_doc, col_db = st.columns(2)
                
                docs = [c for c in citations if "::" in c]
                tables = [c for c in citations if "::" not in c]
                
                with col_doc:
                    if docs:
                        st.write("**📄 Document Chunks:**")
                        for citation in docs:
                            source, chunk = citation.split("::")
                            st.caption(f"- {source} → {chunk}")
                
                with col_db:
                    if tables:
                        st.write("**🗄️ Database Tables:**")
                        for table in tables:
                            st.caption(f"- {table}")
            else:
                st.caption("No citations available")
        
        with tab3:
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.metric("Confidence Score", f"{result.get('confidence', 0):.2f}")
            
            with col_b:
                route = "SQL Query" if result.get("sql") else "Document Retrieval"
                st.metric("Data Source", route)
            
            st.json(result)
        
        # SQL Query (if available)
        if result.get("sql"):
            with st.expander("📊 SQL Query Used"):
                st.code(result["sql"], language="sql")

# Footer
st.divider()
st.markdown("""
---
**Retail Analytics Copilot** | Hybrid RAG + SQL Engine
- 📚 Document retrieval from KPI definitions, product catalog, marketing calendar, and policies
- 🗄️ Direct SQL queries against Northwind database
- 🔄 Automatic fallback from SQL to document retrieval
- 📊 Confidence scoring and source citations
""")
>>>>>>> 8e017c34374abf24b249e7e3dbbfa14b453c5c75
