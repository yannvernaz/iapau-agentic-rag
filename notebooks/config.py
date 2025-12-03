"""
Configuration file for the Streamlit GUI
Centralized configuration management
"""

import os
from pathlib import Path


class Config:
    """Configuration settings for the Financial AI Agents application."""

    # LLM Configuration
    LLM_BASE_URL = 'https://api.openai.com/v1/'
    LLM_API_KEY = os.environ.get('OPENAI_API_KEY')
    LLM_MODEL_GATEKEEPER = 'gpt-4o'
    LLM_MODEL_SUPERVISIOR = 'gpt-4.1'
    LLM_MODEL_AUDITOR = 'gpt-4o'
    LLM_MODEL_SYNTHETISER = 'gpt-4o'

    
    # Embedding Configuration
    EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
    
    # Cross-Encoder Configuration
    CROSS_ENCODER_PATH = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    
    # Database Paths (relative to notebooks directory)
    QDRANT_PATH = "./qdrant_storage"
    COLLECTION_NAME = "financial_docs"
    DB_PATH = "financials.db"
    TABLE_NAME = "revenue_summary"
    
    # Data Files
    COMPANY_TICKER = "NVDA"
    CSV_FILENAME = "revenue_summary.csv"
    ENRICHED_CHUNKS_FILE = "enriched_chunks.json"
    
    # SEC Data Configuration
    SEC_FILINGS = {
        '10-K': 1,
        '10-Q': 4,
        '8-K': 1,
        'DEF 14A': 1
    }
    
    # Processing Configuration
    CHUNK_MAX_CHARS = 2048
    CHUNK_COMBINE_UNDER = 256
    CHUNK_NEW_AFTER = 1800
    
    # Retrieval Configuration
    INITIAL_RETRIEVAL_LIMIT = 20
    TOP_K_RESULTS = 5
    
    # Agent Configuration
    MAX_ITERATIONS = 10
    VERIFICATION_THRESHOLD = 3
    
    # UI Configuration
    ITEMS_PER_PAGE = 10
    
    @classmethod
    def get_notebooks_dir(cls):
        """Get the path to the notebooks directory."""
        return Path(__file__).parent.parent / 'notebooks'
    
    @classmethod
    def get_data_path(cls, filename: str):
        """Get the full path to a data file in the notebooks directory."""
        return cls.get_notebooks_dir() / filename
    
    @classmethod
    def validate(cls):
        """Validate configuration settings."""
        issues = []
        
        # Check if cross-encoder path exists
        if not Path(cls.CROSS_ENCODER_PATH).exists():
            issues.append(f"Cross-encoder model not found at {cls.CROSS_ENCODER_PATH}")
        
        # Check if notebooks directory exists
        if not cls.get_notebooks_dir().exists():
            issues.append(f"Notebooks directory not found at {cls.get_notebooks_dir()}")
        
        return issues


# Validate configuration on import
validation_issues = Config.validate()
if validation_issues:
    print("⚠️ Configuration Validation Warnings:")
    for issue in validation_issues:
        print(f"  - {issue}")
