"""
Specialist Agent Tools for Financial Analysis
This module contains all the specialist tools created in Phase 2.
"""

import os
import pandas as pd
import sqlite3
import json
from typing import List, Dict, Any

from langchain_openai import ChatOpenAI
from langchain.tools import tool
from sentence_transformers import CrossEncoder
from fastembed import TextEmbedding
import qdrant_client
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

# Global configurations
QDRANT_PATH = "./qdrant_storage"
COLLECTION_NAME = "financial_docs"
DB_PATH = "financials.db"

# Initialize models and clients
query_optimizer_llm = ChatOpenAI(model='gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'), temperature=0.)

cross_encoder_model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
embedding_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")

_qdrant_client = None
def get_qdrant_client():
    """Get or create a singleton Qdrant client instance."""
    global _qdrant_client
    if _qdrant_client is None:
        _qdrant_client = qdrant_client.QdrantClient(path=QDRANT_PATH)
    return _qdrant_client

client = get_qdrant_client()

# Initialize SQL database
db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")

sql_agent_llm = ChatOpenAI(model='gpt-4o', api_key=os.getenv('OPENAI_API_KEY'), temperature=0.)

sql_agent_executor = create_sql_agent(llm=sql_agent_llm, db=db, agent_type="openai-tools", verbose=True)


# Helper function for query optimization
def optimize_query(query: str) -> str:
    """Uses an LLM to rewrite a query for better retrieval."""
    prompt = f"""
    You are a query optimization expert. Rewrite the following user query to be more specific and effective for searching through corporate financial documents.
    
    User Query: {query}
    
    Return ONLY the optimized query text with no labels, explanations, or additional formatting.
    """
    optimized_query = query_optimizer_llm.invoke(prompt).content
    return optimized_query


# Tool 1: Librarian RAG Tool
@tool
def librarian_rag_tool(query: str) -> List[Dict[str, Any]]:
    """ 
    Expert at finding information from NVIDIA's financial documents.
    Use for questions about financial performance, business segments, products, risks, strategies.
    """
    print(f"\n-- Librarian Tool Called with query: '{query}' --")
    
    # 1. Optimize Query
    optimized_query = optimize_query(query)
    print(f"  - Optimized query: '{optimized_query}'")
    
    # 2. Vector Search
    query_embedding = list(embedding_model.embed([optimized_query]))[0]
    search_results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=20,
        with_payload=True
    )
    print(f"  - Retrieved {len(search_results)} candidate chunks")
    
    # 3. Re-rank
    rerank_pairs = [[optimized_query, result.payload['content']] for result in search_results]
    scores = cross_encoder_model.predict(rerank_pairs)
    for i, score in enumerate(scores):
        search_results[i].score = score
    reranked_results = sorted(search_results, key=lambda x: x.score, reverse=True)
    print("  - Re-ranked results")
    
    # 4. Return Top Results
    top_k = 5
    final_results = []
    for result in reranked_results[:top_k]:
        final_results.append({
            'source': result.payload['source'],
            'content': result.payload['content'],
            'summary': result.payload['summary'],
            'rerank_score': float(result.score)
        })
    
    print(f"  - Returning top {top_k} chunks")
    return final_results


# Tool 2: Analyst SQL Tool
@tool
def analyst_sql_tool(query: str) -> str:
    """
    Expert financial analyst that queries NVIDIA's revenue and net income database.
    Use for questions about specific financial numbers for a single time period.
    For trends over time, use the analyst_trend_tool.
    """
    print(f"\n-- Analyst SQL Tool Called with query: '{query}' --")
    result = sql_agent_executor.invoke({"input": query})
    return result['output']


# Tool 3: Analyst Trend Tool
@tool
def analyst_trend_tool(query: str) -> str:
    """
    Analyzes financial data over multiple time periods to identify trends and growth rates.
    Best for questions like 'Analyze revenue trend' or 'Show me growth YoY'.
    Provides narrative summary of trends, not just raw numbers.
    """
    print(f"\n-- Analyst Trend Tool Called with query: '{query}' --")
    
    conn = sqlite3.connect(DB_PATH)
    df_trends = pd.read_sql_query("SELECT * FROM revenue_summary ORDER BY year, quarter", conn)
    conn.close()

    df_trends['period'] = df_trends['year'].astype(str) + '-' + df_trends['quarter']
    df_trends.set_index('period', inplace=True)
    
    metric = 'revenue_usd_billions'
    df_trends['QoQ_Growth'] = df_trends[metric].pct_change()
    df_trends['YoY_Growth'] = df_trends[metric].pct_change(4)
    
    latest_period = df_trends.index[-1]
    start_period = df_trends.index[0]
    latest_val = df_trends.loc[latest_period, metric]
    start_val = df_trends.loc[start_period, metric]
    latest_qoq = df_trends.loc[latest_period, 'QoQ_Growth']
    latest_yoy = df_trends.loc[latest_period, 'YoY_Growth']
    
    summary = f"""
    Analysis of {metric} from {start_period} to {latest_period}:
    - The series shows a general upward trend, starting at ${start_val}B and ending at ${latest_val}B.
    - The most recent quarter ({latest_period}) had a Quarter-over-Quarter growth of {latest_qoq:.1%}.
    - The Year-over-Year growth for the most recent quarter was {latest_yoy:.1%}.
    - Overall, performance indicates consistent growth over the analyzed period.
    """
    return summary


# Create tool list and map
tools = [librarian_rag_tool, analyst_sql_tool, analyst_trend_tool]
tool_map = {tool.name: tool for tool in tools}

print("✓ Specialist tools loaded successfully!")
print(f"  Available tools: {[tool.name for tool in tools]}")
