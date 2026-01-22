"""
Utility functions for the Financial Chatbot
"""
import pandas as pd
from typing import Any
from config import RESPONSE_CONFIG


def format_result(result: Any) -> str:
    """
    Format result for display
    
    Args:
        result: The result to format (can be str, int, float, Series, DataFrame)
        
    Returns:
        Formatted string representation of the result
    """
    if isinstance(result, str):
        return result
    
    if isinstance(result, (int, float)):
        if pd.isna(result) or result == 0:
            return f"0 ({RESPONSE_CONFIG['empty_result_message']})"
        
        if isinstance(result, float):
            if RESPONSE_CONFIG['use_thousand_separator']:
                return f"{result:,.{RESPONSE_CONFIG['decimal_places']}f}"
            return f"{result:.{RESPONSE_CONFIG['decimal_places']}f}"
        else:
            if RESPONSE_CONFIG['use_thousand_separator']:
                return f"{result:,}"
            return str(result)
    
    if isinstance(result, pd.Series):
        if len(result) == 0:
            return RESPONSE_CONFIG['empty_result_message']
        return "\n" + result.to_string()
    
    if isinstance(result, pd.DataFrame):
        if len(result) == 0:
            return RESPONSE_CONFIG['empty_result_message']
        return "\n" + result.to_string()
    
    return str(result)


def clean_code(code: str) -> str:
    """
    Clean generated code by removing markdown artifacts
    
    Args:
        code: The generated code string
        
    Returns:
        Cleaned code string
    """
    # Remove markdown code blocks
    if "```" in code:
        parts = code.split("```")
        code = parts[1] if len(parts) > 1 else code
    
    # Remove python language identifier
    if code.lower().startswith("python"):
        code = code[6:].strip()
    
    return code.strip()


def validate_dataframes(holdings_df: pd.DataFrame, trades_df: pd.DataFrame) -> tuple[bool, str]:
    """
    Validate that dataframes are properly loaded
    
    Args:
        holdings_df: Holdings DataFrame
        trades_df: Trades DataFrame
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if holdings_df is None or len(holdings_df) == 0:
        return False, "Holdings DataFrame is empty or not loaded"
    
    if trades_df is None or len(trades_df) == 0:
        return False, "Trades DataFrame is empty or not loaded"
    
    return True, ""


def get_data_summary(holdings_df: pd.DataFrame, trades_df: pd.DataFrame) -> str:
    """
    Get a summary of the loaded data
    
    Args:
        holdings_df: Holdings DataFrame
        trades_df: Trades DataFrame
        
    Returns:
        Summary string
    """
    summary = f"""
📊 Data Summary:
   Holdings: {len(holdings_df):,} records
   Trades: {len(trades_df):,} records
   
   Holdings Columns: {', '.join(holdings_df.columns)}
   Trades Columns: {', '.join(trades_df.columns)}
"""
    return summary
