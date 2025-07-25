# AI Code Interpreter & CSV Analyzer

A powerful web application that combines AI-powered code interpretation with intelligent CSV data analysis. The system uses a smart router to automatically direct requests to specialized agents for optimal results.

## Features

### 🤖 Smart Router Agent
- Automatically routes requests to the appropriate specialized agent
- Handles both programming and data analysis queries intelligently
- No manual agent selection required

### 📊 CSV Analysis Agent
- Upload and analyze CSV files
- Writer rankings and episode counts
- Statistical analysis and data exploration
- Column information and data preview
- Grouping and filtering capabilities

### 🐍 Python Code Agent
- Execute Python code safely
- Generate QR codes
- Create functions and scripts
- Programming assistance and debugging
- Code examples and tutorials

### 🎨 Modern Web Interface
- Clean, dark-themed UI
- Real-time chat interface
- File upload with drag-and-drop
- Responsive design
- Download generated files

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or download the project**
   ```bash
   cd CodeInterpreterAgent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Open your browser**
   Navigate to `http://localhost:5000`

## Usage

### CSV Analysis
1. Upload a CSV file using the "Upload CSV" button
2. Ask questions about your data:
   - "Calculate me the writers from the most written one to less"
   - "Show me the first 10 rows"
   - "How many episodes are in season 1?"
   - "What columns are available?"

### Python Programming
1. Ask for code help:
   - "Write a function to calculate fibonacci numbers"
   - "Create a simple calculator"
   - "Generate a QR code for 'Hello World'"
   - "Show me how to sort a list"

### Smart Routing
The system automatically determines whether your request needs:
- **CSV Agent**: For data analysis, statistics, and CSV-related queries
- **Python Agent**: For programming tasks, code generation, and QR codes

## Project Structure

```
CodeInterpreterAgent/
├── app.py                 # Main Flask application
├── router_agent.py        # Smart routing logic
├── csv_agent.py          # CSV analysis agent
├── python_agent.py       # Python code agent
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
├── templates/
│   └── index.html        # Web interface
├── csv_uploads/          # Uploaded CSV files
├── generated_files/      # Generated QR codes and files
└── venv/                 # Virtual environment
```

## API Endpoints

- `GET /` - Main web interface
- `POST /upload_csv` - Upload CSV files
- `POST /chat` - Send messages to AI agents
- `GET /get_chat_history` - Retrieve chat history
- `POST /clear_chat` - Clear chat history
- `GET /download/<filename>` - Download generated files

## Dependencies

- **Flask**: Web framework
- **OpenAI**: AI language models
- **LangChain**: AI agent framework
- **Pandas**: Data analysis
- **QRCode**: QR code generation
- **Pillow**: Image processing

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `FLASK_ENV`: Set to 'development' for debug mode

### Customization
- Modify agent prompts in respective agent files
- Adjust UI styling in `templates/index.html`
- Configure file upload limits in `app.py`

## Security Features

- Secure file upload validation
- Session-based chat history
- Environment variable protection
- Safe code execution environment

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   - Ensure your API key is set in the `.env` file
   - Check that the key is valid and has sufficient credits

2. **File Upload Issues**
   - Ensure uploaded files are valid CSV format
   - Check file size limits

3. **Port Already in Use**
   - Change the port in `app.py` or stop other Flask applications

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please check the troubleshooting section or create an issue in the project repository.