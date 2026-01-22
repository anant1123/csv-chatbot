# 💰 Financial Chatbot - Groq LLM Powered

A conversational AI chatbot that answers questions about financial data using natural language. Powered by Groq's LLM API and designed to handle complex queries about holdings and trades.

## ✨ Features

- 🤖 **Natural Language Queries**: Ask questions in plain English
- 📅 **Smart Date Handling**: Supports multiple date formats (04/03/20, 04-03-2020, etc.)
- 🔍 **Case-Insensitive Search**: Works with any text casing
- 📊 **Complex Analysis**: Handles aggregations, filtering, and comparisons
- 🧪 **Comprehensive Testing**: Built-in test suite for validation
- ⚙️ **Configurable**: Easy-to-modify configuration files

## 📁 Project Structure

```
assignment/
│
├── config/
│   ├── __init__.py
│   └── config.py              # Configuration settings
│
├── data/
│   ├── holdings.csv           # Holdings data (place your file here)
│   └── trades.csv             # Trades data (place your file here)
│
├── src/
│   ├── __init__.py
│   ├── chatbot.py            # Main chatbot class
│   └── utils.py              # Utility functions
│
├── tests/
│   ├── __init__.py
│   └── test_chatbot.py       # Test cases
│
├── main.py                    # Entry point
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## 🚀 Installation

### 1. Clone or Download

```bash
cd assignment
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Groq API key
# Get your key from: https://console.groq.com/keys
```


## 💻 Usage

### Interactive Mode (Default)

```bash
python main.py
```

This starts an interactive session where you can ask questions:

```
❓ Your question: Total quantity for Garfield with OpenDate 04-03-2020
Show generated code? (y/n, default=n): n

💡 Answer: 99,810,636.00
```

### With Data Summary

```bash
python main.py --show-summary
```

### Test Mode

Run all test cases:

```bash
python main.py --mode test
```

Or run tests directly:

```bash
python tests/test_chatbot.py
```

## 📝 Example Queries

### Date Queries
```
- Total quantity for Garfield with OpenDate 04-03-2020
- Total Qty for garfield on opendate 04/03/20
- How much quantity does GARFIELD have on 4 march 2020
```

### Aggregation Queries
```
- Total number of holdings for Garfield
- Total number of trades for HoldCo 1
- Which funds performed better based on yearly Profit and Loss
```

### Analysis Queries
```
- Show me top 5 portfolios by total value
- What is the average quantity across all holdings?
- List all unique portfolio names
```

## ⚙️ Configuration

All configuration is centralized in `config/config.py`:

### Model Configuration
```python
MODEL_CONFIG = {
    "model_name": "llama-3.3-70b-versatile",
    "temperature": 0.1,
    "max_tokens": None,
}
```

### Chatbot Configuration
```python
CHATBOT_CONFIG = {
    "show_code_by_default": False,
    "enable_date_normalization": True,
    "enable_case_insensitive_search": True,
}
```

### Response Formatting
```python
RESPONSE_CONFIG = {
    "decimal_places": 2,
    "use_thousand_separator": True,
    "show_empty_result_message": True,
    "empty_result_message": "No results found",
}
```

## 🧪 Testing

The project includes comprehensive test suites:

1. **Date Format Variations**: Tests different date formats
2. **Assignment Questions**: Tests required assignment queries
3. **Edge Cases**: Tests error handling and invalid inputs

Run tests:
```bash
python tests/test_chatbot.py
```

## 🔧 How It Works

1. **User asks a question** in natural language
2. **Groq LLM generates Python code** to answer the question
3. **Code is executed safely** with pandas operations
4. **Result is formatted** and returned to the user

### Example Flow

```
User: "Total quantity for Garfield on 04-03-2020"
  ↓
LLM generates:
  result = holdings_df[
      holdings_df['PortfolioName'].str.lower() == 'garfield'
  ][
      holdings_df['OpenDate'] == pd.to_datetime('04-03-2020')
  ]['Qty'].sum()
  ↓
Execute code
  ↓
Format result: "99,810,636.00"
```

## 🛡️ Safety Features

- ✅ Safe code execution in isolated environment
- ✅ Input validation for dataframes
- ✅ Error handling for invalid queries
- ✅ Date normalization to prevent errors
- ✅ Case-insensitive matching

## 📚 Dependencies

- **pandas**: Data manipulation and analysis
- **numpy**: Numerical operations
- **groq**: Groq API client
- **python-dotenv**: Environment variable management

## 🐛 Troubleshooting

### "GROQ_API_KEY not found"
- Make sure you've created a `.env` file
- Add your API key: `GROQ_API_KEY=your_key_here`

### "Data file not found"
- Ensure `holdings.csv` and `trades.csv` are in the `data/` folder
- Check file names match exactly

### "Execution error"
- Try showing the generated code with `show_code=True`
- Check if your query is clear and specific


## 🤝 Contributing

Feel free to submit issues or pull requests for improvements!

## 📧 Support

For questions or issues, please create an issue in the repository.

---

**Happy Querying! 🎉**
