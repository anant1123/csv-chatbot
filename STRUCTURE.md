# 📊 Project Structure Overview

## Complete File Tree

```
assignment/
│
├── 📁 config/                      # Configuration files
│   ├── __init__.py                 # Package initialization
│   └── config.py                   # Main configuration (MODEL, API, etc.)
│
├── 📁 data/                        # Data files
│   ├── holdings.csv                # Holdings data (copy here)
│   └── trades.csv                  # Trades data (copy here)
│
├── 📁 src/                         # Source code
│   ├── __init__.py                 # Package initialization
│   ├── chatbot.py                  # GrokFinancialChatbot class
│   └── utils.py                    # Helper functions
│
├── 📁 tests/                       # Test suite
│   ├── __init__.py                 # Package initialization
│   └── test_chatbot.py             # All test cases
│
├── 📄 main.py                      # Main entry point
├── 📄 setup_data.py                # Data setup helper
├── 📄 requirements.txt             # Python dependencies
├── 📄 .env.example                 # Environment template
├── 📄 .gitignore                   # Git ignore rules
├── 📄 README.md                    # Full documentation
├── 📄 QUICKSTART.md                # Quick setup guide
└── 📄 STRUCTURE.md                 # This file
```

## 📋 File Descriptions

### Configuration (`config/`)

**config.py**
- Model settings (model name, temperature)
- Chatbot settings (date handling, case sensitivity)
- Response formatting (decimal places, separators)
- System prompt template
- Paths to data files

### Source Code (`src/`)

**chatbot.py**
- `GrokFinancialChatbot` class - Main chatbot logic
- `_normalize_dates()` - Converts date columns to datetime
- `_build_lookup_maps()` - Creates case-insensitive mappings
- `_call_grok()` - Calls Groq API with prompts
- `_execute_code()` - Safely runs generated Python code
- `ask()` - Main method to ask questions

**utils.py**
- `format_result()` - Formats answers for display
- `clean_code()` - Cleans generated code
- `validate_dataframes()` - Validates data loading
- `get_data_summary()` - Shows data overview

### Tests (`tests/`)

**test_chatbot.py**
- `test_date_format_variations()` - Tests different date formats
- `test_assignment_questions()` - Tests required queries
- `test_edge_cases()` - Tests error handling
- `run_all_tests()` - Runs complete test suite

### Main Files

**main.py**
- Command-line argument parsing
- Interactive mode for user queries
- Integration of all components
- Error handling and user feedback

**setup_data.py**
- Copies CSV files from project root to assignment/data/
- Quick setup helper

## 🔄 Data Flow

```
User Question
    ↓
main.py (Interactive Mode)
    ↓
GrokFinancialChatbot.ask()
    ↓
_call_grok() → Groq API → Python Code
    ↓
_execute_code() → Execute on DataFrames
    ↓
format_result() → Formatted Answer
    ↓
Display to User
```

## ⚙️ Configuration Flow

```
.env file
    ↓
config/config.py
    ↓
src/chatbot.py
    ↓
main.py
```

## 🧪 Testing Flow

```
tests/test_chatbot.py
    ↓
Load Data (holdings.csv, trades.csv)
    ↓
Initialize GrokFinancialChatbot
    ↓
Run Test Suites:
  - Date Format Tests
  - Assignment Question Tests
  - Edge Case Tests
    ↓
Display Results
```

## 📦 Dependencies

```
pandas      → Data manipulation
numpy       → Numerical operations
groq        → Groq API client
python-dotenv → Environment variables
```

## 🎯 Key Features by File

### config/config.py
- ✅ Centralized configuration
- ✅ Easy model switching
- ✅ Customizable formatting
- ✅ System prompt management

### src/chatbot.py
- ✅ Date normalization
- ✅ Case-insensitive search
- ✅ Safe code execution
- ✅ Error handling

### src/utils.py
- ✅ Result formatting
- ✅ Code cleaning
- ✅ Data validation
- ✅ Summary generation

### main.py
- ✅ Interactive CLI
- ✅ Command arguments
- ✅ User-friendly interface
- ✅ Help system

### tests/test_chatbot.py
- ✅ Comprehensive testing
- ✅ Multiple test types
- ✅ Detailed output
- ✅ Easy to run

## 🚀 Usage Patterns

### Quick Start
```bash
python setup_data.py  # Copy data files
python main.py        # Run chatbot
```

### With Options
```bash
python main.py --show-summary    # Show data on startup
python main.py --mode test       # Run tests
```

### Direct Testing
```bash
python tests/test_chatbot.py     # Run test suite directly
```

## 🔐 Security

- ✅ API keys in `.env` (not committed to git)
- ✅ Safe code execution environment
- ✅ Input validation
- ✅ Error handling

## 📝 Customization Points

1. **Model Settings** → `config/config.py` → `MODEL_CONFIG`
2. **Response Format** → `config/config.py` → `RESPONSE_CONFIG`
3. **Prompt Template** → `config/config.py` → `SYSTEM_PROMPT_TEMPLATE`
4. **Test Cases** → `tests/test_chatbot.py` → Add new functions

## 🎨 Code Organization Principles

1. **Separation of Concerns**: Config, source, tests are separate
2. **Reusability**: Utils can be imported anywhere
3. **Testability**: All components are testable
4. **Configurability**: Settings in one place
5. **Maintainability**: Clear structure, well-documented

---

**This structure makes the project:**
- Easy to understand ✅
- Easy to maintain ✅
- Easy to extend ✅
- Easy to test ✅
