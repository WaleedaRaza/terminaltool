# 🌐 Networking Tool Copilot

An AI-powered terminal copilot that intercepts networking commands, sends them to a local server with LLM integration, and returns annotated explanations inline and via a web dashboard.

## 🚀 Features

- **Real-time Command Analysis**: Execute networking commands and get AI-powered explanations
- **OS-Specific Command Suggestions**: Automatically detects your OS and suggests appropriate commands
- **Smart Error Handling**: When commands fail, get helpful alternatives and explanations
- **Web Dashboard**: Beautiful, modern UI for command execution and analysis
- **Configurable LLM Integration**: Support for OpenAI and Anthropic APIs
- **Command Validation**: Security-focused command validation and sanitization

## 🏗️ Architecture

### Core Components

```
networking_tool/
├── src/
│   ├── core/                    # Core business logic
│   │   ├── command_executor.py  # Command execution and process management
│   │   ├── command_processor.py # Main orchestration and LLM integration
│   │   ├── command_validator.py # Security validation and sanitization
│   │   ├── command_helper.py    # OS-specific command suggestions
│   │   ├── llm_client.py       # LLM API integration (OpenAI/Anthropic)
│   │   └── command_templates.py # LLM prompt templates
│   ├── cli/                     # Command-line interface
│   │   └── main.py             # CLI entry point
│   ├── web/                     # Web server components
│   │   └── server.py           # FastAPI server implementation
│   └── renderers/               # Output formatting
│       └── terminal_renderer.py # Rich terminal output
├── tests/                       # Test suite
├── config.py                    # Configuration management
├── setup.py                     # Interactive setup script
├── simple_web.py               # Standalone web server
└── netcopilot_config.json      # User configuration file
```

### Data Flow

1. **Command Input** → User enters networking command via web UI or CLI
2. **Validation** → `CommandValidator` checks security and syntax
3. **Execution** → `CommandExecutor` runs the command safely
4. **LLM Analysis** → `LLMClient` sends output to AI for explanation
5. **Rendering** → Results formatted and displayed in web UI

## 🛠️ Setup for Team Members

### Prerequisites

- Python 3.8+
- OpenAI API key (or Anthropic API key)
- Internet connection for LLM API calls

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/WaleedaRaza/terminaltool.git
   cd terminaltool
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API key:**
   ```bash
   python3 setup.py
   ```
   Follow the prompts to enter your OpenAI API key.

4. **Start the web server:**
   ```bash
   python3 simple_web.py
   ```

5. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

### Alternative Setup Methods

#### Method 1: Direct API Key Configuration
```bash
python3 -c "from config import set_api_key; set_api_key('your-api-key-here')"
```

#### Method 2: Environment Variable (Legacy)
```bash
export OPENAI_API_KEY="your-api-key-here"
python3 simple_web.py
```

#### Method 3: Manual Configuration File
Edit `netcopilot_config.json`:
```json
{
  "openai_api_key": "your-api-key-here",
  "llm_provider": "openai",
  "llm_model": "gpt-4",
  "llm_temperature": 0.3,
  "llm_max_tokens": 1000,
  "llm_timeout": 30,
  "web_port": 3000,
  "web_host": "127.0.0.1"
}
```

## 🔧 Configuration

### API Keys

#### OpenAI
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Use the setup script or edit the config file

#### Anthropic (Alternative)
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Create a new API key
3. Set `"llm_provider": "anthropic"` in config

### Configuration Options

| Setting | Default | Description |
|---------|---------|-------------|
| `openai_api_key` | `""` | Your OpenAI API key |
| `llm_provider` | `"openai"` | LLM provider (`openai` or `anthropic`) |
| `llm_model` | `"gpt-4"` | Model to use for analysis |
| `llm_temperature` | `0.3` | Creativity level (0.0-1.0) |
| `llm_max_tokens` | `1000` | Maximum response length |
| `llm_timeout` | `30` | API timeout in seconds |
| `web_port` | `3000` | Web server port |
| `web_host` | `"127.0.0.1"` | Web server host |

## 📁 File Architecture Deep Dive

### Core Components

#### `src/core/command_processor.py`
**Purpose**: Main orchestration layer that coordinates command execution and LLM analysis.

**Key Functions**:
- `process_command()`: Main entry point for command processing
- `_get_explanation()`: Handles LLM integration
- `_create_error_explanation()`: Formats error responses with suggestions

**Integration Points**:
- Uses `CommandExecutor` for safe command execution
- Uses `LLMClient` for AI analysis
- Uses `CommandValidator` for security checks
- Uses `CommandHelper` for OS-specific suggestions

#### `src/core/command_executor.py`
**Purpose**: Safely executes system commands with timeout and error handling.

**Key Features**:
- Process isolation and timeout management
- Return code and output capture
- Error output separation
- Security-focused execution

**Supported Commands**:
- Network diagnostics: `ping`, `traceroute`, `ifconfig`, `netstat`
- DNS tools: `dig`, `nslookup`
- Routing: `route`, `arp`
- And more...

#### `src/core/llm_client.py`
**Purpose**: Manages communication with LLM APIs (OpenAI/Anthropic).

**Key Features**:
- Multi-provider support (OpenAI, Anthropic, Mock)
- Automatic fallback to mock responses
- Configurable models and parameters
- Error handling and retry logic

**API Integration**:
- OpenAI Chat Completions API
- Anthropic Messages API
- Mock responses for development

#### `src/core/command_validator.py`
**Purpose**: Validates and sanitizes commands for security.

**Security Features**:
- Dangerous command blocking (`rm`, `sudo`, etc.)
- Character set validation
- Command length limits
- Networking command detection

#### `src/core/command_helper.py`
**Purpose**: Provides OS-specific command suggestions and alternatives.

**OS Detection**:
- macOS: `ifconfig`, `traceroute`, `dig`
- Linux: `ip addr`, `ss`, `dig`
- Windows: `ipconfig`, `tracert`, `nslookup`

### Web Components

#### `simple_web.py`
**Purpose**: Standalone FastAPI web server with modern UI.

**Features**:
- Real-time command execution
- User-friendly error handling
- Clickable command suggestions
- Responsive design

**API Endpoints**:
- `GET /`: Main web interface
- `POST /api/execute`: Command execution API

### Configuration Management

#### `config.py`
**Purpose**: Centralized configuration management.

**Features**:
- JSON-based configuration storage
- Environment variable fallback
- Interactive setup
- API key management

#### `setup.py`
**Purpose**: Interactive setup script for new users.

**Workflow**:
1. Check existing configuration
2. Prompt for API key
3. Validate and save settings
4. Provide next steps

## 🧪 Testing

### Run All Tests
```bash
python3 -m pytest tests/
```

### Test Specific Components
```bash
# Test command execution
python3 -m pytest tests/test_command_executor.py

# Test LLM client
python3 -m pytest tests/test_llm_client.py

# Test command validation
python3 -m pytest tests/test_command_validator.py
```

### Manual Testing
```bash
# Test LLM configuration
python3 test_llm.py

# Test web API
curl -X POST http://localhost:3000/api/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "ifconfig"}'
```

## 🚀 Usage Examples

### Web Interface
1. Start the server: `python3 simple_web.py`
2. Open [http://localhost:3000](http://localhost:3000)
3. Click command suggestions or type your own
4. View AI-powered analysis

### Command Line
```bash
# Basic command execution
python3 -m src.cli.main execute "ifconfig"

# Interactive mode
python3 -m src.cli.main interactive

# Help
python3 -m src.cli.main --help
```

### Supported Commands

#### Network Diagnostics
- `ifconfig` / `ipconfig` - Interface configuration
- `ping -c 1 127.0.0.1` - Connectivity test
- `traceroute 8.8.8.8` - Route analysis
- `netstat -an` - Connection status

#### DNS Tools
- `dig google.com` - DNS lookup
- `nslookup google.com` - Name resolution

#### Routing
- `route -n` - Routing table
- `arp -a` - ARP cache

## 🔒 Security Considerations

### Command Validation
- Blocks dangerous commands (`rm`, `sudo`, `dd`)
- Validates character sets
- Enforces length limits
- Detects networking commands

### Process Isolation
- Timeout protection
- Output sanitization
- Error handling
- Resource limits

### API Security
- API key management
- Request validation
- Error sanitization
- Rate limiting (via LLM providers)

## 🐛 Troubleshooting

### Common Issues

#### "LLM service unavailable"
**Cause**: API key not configured or invalid
**Solution**: 
```bash
python3 setup.py
# or
python3 -c "from config import set_api_key; set_api_key('your-key')"
```

#### "Command not found"
**Cause**: OS-specific command differences
**Solution**: Use command suggestions or check OS compatibility

#### "Permission denied"
**Cause**: Command requires elevated privileges
**Solution**: Use alternative commands or check system permissions

#### "SyntaxError: invalid syntax"
**Cause**: JavaScript code outside HTML strings
**Solution**: Ensure all JS is inside HTML strings in Python files

### Debug Mode
```bash
# Enable debug logging
export PYTHONPATH=src
python3 -c "import logging; logging.basicConfig(level=logging.DEBUG)"
python3 simple_web.py
```

### Configuration Reset
```bash
# Remove configuration file
rm netcopilot_config.json

# Re-run setup
python3 setup.py
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Code Style
- Follow PEP 8
- Use type hints
- Add docstrings
- Write tests for new features

### Testing
```bash
# Run tests with coverage
python3 -m pytest tests/ --cov=src

# Run linting
python3 -m flake8 src/

# Run type checking
python3 -m mypy src/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT models
- Anthropic for Claude models
- FastAPI for web framework
- Rich for terminal formatting
- The networking community for command examples

---

**Need help?** Open an issue or check the troubleshooting section above. 