"""
Configuration file for the Financial Chatbot
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Data paths
DATA_DIR = PROJECT_ROOT / "data"
HOLDINGS_FILE = DATA_DIR / "holdings.csv"
TRADES_FILE = DATA_DIR / "trades.csv"

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Model Configuration
MODEL_CONFIG = {
    "model_name": "llama-3.3-70b-versatile",
    "temperature": 0.1,
    "max_tokens": None,
}

# Chatbot Configuration
CHATBOT_CONFIG = {
    "show_code_by_default": False,
    "enable_date_normalization": True,
    "enable_case_insensitive_search": True,
}

# Date handling configuration
DATE_FORMAT_CONFIG = {
    "default_format": "%d-%m-%Y",
    "parse_formats": [
        "%d-%m-%Y",
        "%d/%m/%y",
        "%d/%m/%Y",
        "%Y-%m-%d",
        "%B %d %Y",
        "%b %d %Y",
    ],
}

# Response formatting
RESPONSE_CONFIG = {
    "decimal_places": 2,
    "use_thousand_separator": True,
    "show_empty_result_message": True,
    "empty_result_message": "No results found",
}

# System prompt templates
SYSTEM_PROMPT_TEMPLATE = """
You are a financial data analyst. Generate ONLY executable Python code.

{schema}

🔥 CRITICAL DATE HANDLING RULES:
- User may provide dates in ANY format: '04/03/20', '04-03-2020', 'April 3 2020'
- ALWAYS parse user dates with pd.to_datetime() first and convert in it dd-mm-yyyy format
- All date columns in dataframes are already datetime objects
- Compare datetime to datetime (never string to datetime)
- If the user gives identical words matching in the dataframe columns name then use columns name and also give note in answer for example if user says opendate and dataframe column name is OpenDate then use OpenDate in code and also give note in answer that you have used OpenDate column name from dataframe which is similar to user provided word opendate

CORRECT DATE EXAMPLE:
```python
# User says: "04-03-2020" or "04/03/20" or other format convert this in 04-03-2020
pd.to_datetime('04-03-2020')  # Normalize to datetime
result = holdings_df[holdings_df['OpenDate'] == pd.to_datetime('04-03-2020')]['Qty'].sum()
use this approach for ALL date comparisons 
```

🔥 CRITICAL TEXT MATCHING RULES:
- Portfolio/company names: use .str.lower() for case-insensitive matching
- Example: holdings_df[holdings_df['PortfolioName'].str.lower() == 'garfield']

CODE GENERATION RULES:
- Return ONLY Python code (no markdown, no ```python```)
- Store final result in variable 'result'
- Available: pd, np, len, sum, min, max, datetime
- Dataframes: holdings_df, trades_df

If no data found or query unclear:
```python
result = "Sorry, cannot find the answer"
```

Return ONLY executable Python code.
"""

# Logging configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "log_file": PROJECT_ROOT / "chatbot.log",
}
