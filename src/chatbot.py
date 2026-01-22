"""
Financial Chatbot powered by Groq LLM
"""
import pandas as pd
import numpy as np
from groq import Groq
from typing import Any
from datetime import datetime
import warnings

from config import (
    MODEL_CONFIG,
    CHATBOT_CONFIG,
    SYSTEM_PROMPT_TEMPLATE,
)
from .utils import format_result, clean_code

warnings.filterwarnings('ignore')


class GrokFinancialChatbot:
    """
    A chatbot that uses Groq LLM to answer questions about financial data
    """
    
    def __init__(self, holdings_df: pd.DataFrame, trades_df: pd.DataFrame, grok_client: Groq):
        """
        Initialize the chatbot
        
        Args:
            holdings_df: DataFrame containing holdings data
            trades_df: DataFrame containing trades data
            grok_client: Initialized Groq API client
        """
        self.holdings_df = holdings_df.copy()
        self.trades_df = trades_df.copy()
        self.client = grok_client
        
        print("\n🔧 Applying fixes...")
        
        # FIX #1: Normalize dates to datetime objects
        if CHATBOT_CONFIG['enable_date_normalization']:
            self._normalize_dates()
        
        # FIX #2: Build case-insensitive maps
        if CHATBOT_CONFIG['enable_case_insensitive_search']:
            self._build_lookup_maps()
        
        self.schema = self._get_schema()
        print("✅ Chatbot initialized with all fixes applied")
    
    def _normalize_dates(self):
        """Convert all date columns to datetime objects"""
        for df_name, df in [("Holdings", self.holdings_df), ("Trades", self.trades_df)]:
            for col in df.columns:
                if 'date' in col.lower():
                    try:
                        df[col] = pd.to_datetime(df[col], errors='coerce', infer_datetime_format=True)
                        print(f"  ✓ Normalized {df_name}.{col}")
                    except:
                        pass
    
    def _build_lookup_maps(self):
        """Build case-insensitive lookup dictionaries"""
        # Column name maps
        self.holdings_cols = {c.lower(): c for c in self.holdings_df.columns}
        self.trades_cols = {c.lower(): c for c in self.trades_df.columns}
        
        print(f"  ✓ Built column maps")
    
    def _get_schema(self) -> str:
        """Generate enhanced schema with date info"""
        return f"""
DATASETS AVAILABLE:

1. holdings_df ({len(self.holdings_df)} records)
   Columns: {', '.join(self.holdings_df.columns)}
   
2. trades_df ({len(self.trades_df)} records)
   Columns: {', '.join(self.trades_df.columns)}

IMPORTANT: All dates are normalized to datetime objects.
"""
    
    def _call_grok(self, user_query: str) -> str:
        """
        Call Groq with enhanced date-handling instructions
        
        Args:
            user_query: The user's question
            
        Returns:
            Generated Python code
        """
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(schema=self.schema)
        
        response = self.client.chat.completions.create(
            model=MODEL_CONFIG['model_name'],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            temperature=MODEL_CONFIG['temperature']
        )
        
        code = response.choices[0].message.content.strip()
        return clean_code(code)
    
    def _execute_code(self, code: str):
        """
        Safely execute generated code
        
        Args:
            code: Python code to execute
            
        Returns:
            Result of code execution or error message
        """
        try:
            local_vars = {
                "holdings_df": self.holdings_df,
                "trades_df": self.trades_df,
                "pd": pd,
                "np": np,
                "len": len,
                "sum": sum,
                "min": min,
                "max": max,
                "datetime": datetime
            }
            
            exec(code, {}, local_vars)
            return local_vars.get("result", "No result variable found")
            
        except Exception as e:
            return f"Execution error: {str(e)}"
    
    def ask(self, query: str, show_code: bool = None) -> str:
        """
        Ask a question and get answer
        
        Args:
            query: The question to ask
            show_code: Whether to show generated code (uses config default if None)
            
        Returns:
            Formatted answer
        """
        if show_code is None:
            show_code = CHATBOT_CONFIG['show_code_by_default']
        
        print(f"\n🤔 Question: {query}")
        print("   Thinking...")
        
        code = self._call_grok(query)
        
        if show_code:
            print(f"\n📝 Generated Code:\n{code}\n")
        
        result = self._execute_code(code)
        formatted = format_result(result)
        
        return formatted
