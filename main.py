"""
Main entry point for Financial Chatbot
Interactive mode for asking questions about financial data
"""
import sys
import argparse
import pandas as pd
from groq import Groq

from config import GROQ_API_KEY, HOLDINGS_FILE, TRADES_FILE
from src import GrokFinancialChatbot, validate_dataframes, get_data_summary


def load_data():
    """Load the CSV data files"""
    print("\n📂 Loading data...")
    try:
        holdings_df = pd.read_csv(HOLDINGS_FILE)
        trades_df = pd.read_csv(TRADES_FILE)
        
        # Validate dataframes
        is_valid, error_msg = validate_dataframes(holdings_df, trades_df)
        if not is_valid:
            print(f"❌ Error: {error_msg}")
            sys.exit(1)
        
        print(f"✅ Holdings: {len(holdings_df):,} records")
        print(f"✅ Trades: {len(trades_df):,} records")
        
        return holdings_df, trades_df
    except FileNotFoundError as e:
        print(f"❌ Error: Data file not found - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        sys.exit(1)


def initialize_chatbot(holdings_df, trades_df):
    """Initialize the chatbot with data"""
    if not GROQ_API_KEY:
        print("❌ Error: GROQ_API_KEY not found in environment variables")
        print("Please set GROQ_API_KEY in your .env file")
        sys.exit(1)
    
    try:
        client = Groq(api_key=GROQ_API_KEY)
        print("✅ Groq API initialized")
        
        chatbot = GrokFinancialChatbot(holdings_df, trades_df, client)
        return chatbot
    except Exception as e:
        print(f"❌ Error initializing chatbot: {e}")
        sys.exit(1)


def interactive_mode(chatbot):
    """Run the chatbot in interactive mode"""
    print("\n" + "="*80)
    print("💬 INTERACTIVE MODE (type 'quit' or 'exit' to exit)")
    print("="*80)
    print("\n📝 Tips:")
    print("  • Try different date formats: 04/03/20, 04-03-2020, etc.")
    print("  • Case doesn't matter: garfield, GARFIELD, Garfield all work")
    print("  • Ask complex questions - the LLM will figure it out!")
    print("\n📌 Commands:")
    print("  • 'help' - Show this help message")
    print("  • 'summary' - Show data summary")
    print("  • 'quit' or 'exit' - Exit the program\n")
    
    while True:
        try:
            question = input("❓ Your question: ").strip()
            
            # Handle commands
            if question.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if question.lower() == 'help':
                print("\n📝 Available commands:")
                print("  • Ask any question about your financial data")
                print("  • Type 'summary' to see data overview")
                print("  • Type 'quit' or 'exit' to exit")
                continue
            
            if question.lower() == 'summary':
                summary = get_data_summary(chatbot.holdings_df, chatbot.trades_df)
                print(summary)
                continue
            
            if not question:
                continue
            
            # Ask if user wants to see code
            show_code_input = input("Show generated code? (y/n, default=n): ").strip().lower()
            show_code = show_code_input == 'y'
            
            # Get answer
            answer = chatbot.ask(question, show_code=show_code)
            print(f"\n💡 Answer: {answer}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Financial Chatbot - Ask questions about your financial data")
    parser.add_argument(
        '--mode',
        choices=['interactive', 'test'],
        default='interactive',
        help='Run mode: interactive (default) or test'
    )
    parser.add_argument(
        '--show-summary',
        action='store_true',
        help='Show data summary on startup'
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*80)
    print("💰 Financial Chatbot powered by Groq LLM")
    print("="*80)
    
    # Load data
    holdings_df, trades_df = load_data()
    
    # Initialize chatbot
    chatbot = initialize_chatbot(holdings_df, trades_df)
    print("\n🎉 Chatbot ready!")
    
    # Show summary if requested
    if args.show_summary:
        summary = get_data_summary(holdings_df, trades_df)
        print(summary)
    
    # Run in selected mode
    if args.mode == 'interactive':
        interactive_mode(chatbot)
    elif args.mode == 'test':
        print("\n🧪 Running tests...")
        from tests import run_all_tests
        run_all_tests()


if __name__ == "__main__":
    main()
