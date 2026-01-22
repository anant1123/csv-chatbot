"""
Test cases for Financial Chatbot
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from groq import Groq
from src import GrokFinancialChatbot
from config import GROQ_API_KEY, HOLDINGS_FILE, TRADES_FILE


def load_data():
    """Load the CSV data files"""
    print("Loading data...")
    holdings_df = pd.read_csv(HOLDINGS_FILE)
    trades_df = pd.read_csv(TRADES_FILE)
    print(f"✅ Holdings: {len(holdings_df):,} records")
    print(f"✅ Trades: {len(trades_df):,} records")
    return holdings_df, trades_df


def initialize_chatbot(holdings_df, trades_df):
    """Initialize the chatbot with data"""
    client = Groq(api_key=GROQ_API_KEY)
    print("✅ Groq API initialized")
    
    chatbot = GrokFinancialChatbot(holdings_df, trades_df, client)
    print("\n🎉 Chatbot ready!")
    return chatbot


def test_date_format_variations(chatbot):
    """Test different date format variations"""
    print("\n" + "="*80)
    print("TEST 1: Date Format Variations")
    print("="*80)
    
    test_queries = [
        "Total quantity for Garfield with OpenDate 04-03-2020",
        "Total Qty for garfield on opendate 04/03/20",
        "How much quantity does GARFIELD have on 4 march 2020",
        "list how many times strategy1 use as asset"
    ]
    
    results = []
    for q in test_queries:
        answer = chatbot.ask(q, show_code=True)
        print(f"💡 Answer: {answer}")
        print("-" * 80)
        results.append((q, answer))
    
    return results


def test_assignment_questions(chatbot):
    """Test the required assignment questions"""
    print("\n" + "="*80)
    print("TEST 2: Required Assignment Questions")
    print("="*80)
    
    assignment_qs = [
        "Total number of holdings for Garfield",
        "Total number of trades for HoldCo 1",
        "Which funds performed better based on yearly Profit and Loss",
    ]
    
    results = []
    for q in assignment_qs:
        answer = chatbot.ask(q, show_code=True)
        print(f"💡 Answer: {answer}")
        print("-" * 80)
        results.append((q, answer))
    
    return results


def test_edge_cases(chatbot):
    """Test edge cases and error handling"""
    print("\n" + "="*80)
    print("TEST 3: Edge Cases")
    print("="*80)
    
    edge_cases = [
        "What is the weather today?",  # Should return "cannot find answer"
        "Who is the president?",  # Should return "cannot find answer"
        "Total holdings for NonExistentFund",  # Should return 0 or "not found"
    ]
    
    results = []
    for q in edge_cases:
        answer = chatbot.ask(q, show_code=True)
        print(f"💡 Answer: {answer}")
        print("-" * 80)
        results.append((q, answer))
    
    return results


def run_all_tests():
    """Run all test suites"""
    print("\n" + "🧪 RUNNING ALL TESTS " + "="*60)
    
    # Load data
    holdings_df, trades_df = load_data()
    
    # Initialize chatbot
    chatbot = initialize_chatbot(holdings_df, trades_df)
    
    # Run tests
    date_results = test_date_format_variations(chatbot)
    assignment_results = test_assignment_questions(chatbot)
    edge_results = test_edge_cases(chatbot)
    
    print("\n" + "="*80)
    print("✅ ALL TESTS COMPLETED")
    print("="*80)
    
    return {
        "date_tests": date_results,
        "assignment_tests": assignment_results,
        "edge_tests": edge_results
    }


if __name__ == "__main__":
    run_all_tests()
