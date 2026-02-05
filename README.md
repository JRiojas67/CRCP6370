# CRCP6370 - AI in the Metaverse

This repository contains chatbot implementations for the AI in the Metaverse class.

## Chatbots Available

### 1. AI-Powered Chatbot with Claude & ChatGPT (`chatbot_ai.py`) ⭐ NEW

A sophisticated chatbot that integrates with both **Anthropic's Claude** and **OpenAI's ChatGPT** APIs. Switch between AI providers on the fly!

**Features:**
- 🤖 Dual AI provider support (Claude & ChatGPT)
- 💬 Conversation history management
- 🔄 Switch between AI providers during conversation
- 📜 View conversation history
- 🎯 Command-based interface
- 🔒 Secure API key management with environment variables

### 2. Simple Rule-Based Chatbot (`chatbot.py`)

A basic rule-based chatbot with no external dependencies.

### 3. Advanced NLTK Chatbot (`chatbot_advanced.py`)

A chatbot using NLTK for natural language processing.

---

## Quick Start: AI-Powered Chatbot

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install anthropic openai python-dotenv
```

### Step 2: Get API Keys

1. **Claude API Key** (Optional but recommended):
   - Visit: https://console.anthropic.com/
   - Sign up or log in
   - Navigate to API Keys section
   - Create a new API key

2. **ChatGPT API Key** (Optional but recommended):
   - Visit: https://platform.openai.com/api-keys
   - Sign up or log in
   - Create a new API key

### Step 3: Configure API Keys

1. Copy the example environment file:
   ```bash
   cp env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```env
   ANTHROPIC_API_KEY=sk-ant-api03-...
   OPENAI_API_KEY=sk-...
   ```

   **Note:** You only need to set the keys for the services you want to use. If you only have one API key, that's fine!

### Step 4: Run the Chatbot

**Terminal:**
```bash
python3 chatbot_ai.py
```

**Web browser (all on port 5500):**

Run `python3 server.py` — the app and API both run on **port 5500**.  
Then open **http://127.0.0.1:5500** in your browser. Same origin = no 404, 405, or 403 errors.

(Do not start the “Live Server” extension on 5500 at the same time, or the port will conflict.)

**VSCode:**
- Press `F5` to run with debugging
- Run from integrated terminal: `python3 chatbot_ai.py` or `python3 server.py`

---

## Usage Guide

### Commands

Once the chatbot is running, you can use these commands:

- `/claude` - Switch to Claude AI
- `/chatgpt` or `/gpt` - Switch to ChatGPT
- `/clear` - Clear conversation history
- `/history` - View conversation history
- `/help` - Show help message
- `/quit` or `/exit` - Exit the chatbot

### Example Conversation

```
🤖 AI-Powered Chatbot (Claude & ChatGPT)
============================================================

Current provider: CLAUDE

You: Hello! Can you help me with Python programming?

[CLAUDE] Thinking...

AI: Hello! I'd be happy to help you with Python programming. 
What specific aspect would you like to learn about or work on? 
I can assist with syntax, best practices, debugging, or explain 
concepts. What would you like to start with?

You: /chatgpt

✓ Switched to ChatGPT

You: What's the difference between lists and tuples?

[CHATGPT] Thinking...

AI: Lists and tuples are both sequence types in Python, but they 
have key differences: Lists are mutable (can be modified), while 
tuples are immutable (cannot be changed after creation)...
```

---

## VSCode Setup

### Recommended Extensions

- **Python** (by Microsoft) - Python language support
- **Python Debugger** - Debugging support

### Running in VSCode

1. **Using the Run Button:**
   - Open `chatbot_ai.py`
   - Click the ▶️ Run button in the top-right corner
   - Select "Run Python File in Terminal"

2. **Using Debugging:**
   - Press `F5` or go to Run > Start Debugging
   - Select "Python: Current File" configuration

3. **Using Terminal:**
   - Open integrated terminal (`Ctrl+`` ` or `Cmd+`` `)
   - Run: `python3 chatbot_ai.py`

---

## Project Structure

```
CRCP6370/
├── chatbot_ai.py          # AI-powered chatbot (Claude & ChatGPT)
├── chatbot.py             # Simple rule-based chatbot
├── chatbot_advanced.py    # NLTK-based chatbot
├── requirements.txt       # Python dependencies
├── env.example            # Example environment variables file
├── .env                   # Your API keys (create this, not in git)
└── README.md              # This file
```

---

## Troubleshooting

### "No API keys found" Error

- Make sure you've created a `.env` file in the project root
- Verify your API keys are correctly set in `.env`
- Check that `python-dotenv` is installed: `pip install python-dotenv`

### "Module not found" Error

- Install dependencies: `pip install -r requirements.txt`
- Make sure you're using Python 3.8 or higher
- Check your Python interpreter in VSCode (bottom-right corner)

### API Errors

- **Rate Limits:** Both APIs have rate limits. If you hit them, wait a moment and try again.
- **Invalid API Key:** Double-check your API keys in the `.env` file
- **Network Issues:** Check your internet connection

### 405 Method Not Allowed (chatbot / index.html)

- **Endpoint:** Your app sends **POST** to **`/api/chat`**. The server only allows **OPTIONS** and **POST** on that URL.
- **Typical causes:**
  1. **Wrong URL** – Use the same server for page and API. Run `python3 server.py` and open **http://127.0.0.1:5500** (not file:// and not a different port).
  2. **Wrong method** – The chat UI uses POST for `/api/chat`; the server allows OPTIONS and POST.
  3. **403** – The server sends CORS headers; if you still see 403, ensure you’re opening http://127.0.0.1:5500 after starting `python3 server.py`.
- **Quick check:** In DevTools → Network, the request to `/api/chat` should be **POST** and the URL should be **http://127.0.0.1:5500/api/chat** (same origin as the page).

### VSCode Issues

- **Python not found:** Install Python 3.8+ and select it in VSCode
- **Terminal issues:** Use the integrated terminal in VSCode (`Ctrl+`` `)

---

## API Costs

**Important:** Both Claude and ChatGPT APIs are **paid services** (though they may offer free credits):

- **Claude:** Check pricing at https://www.anthropic.com/pricing
- **ChatGPT:** Check pricing at https://openai.com/pricing

Monitor your usage to avoid unexpected charges!

---

## Next Steps

- Customize the chatbot's behavior
- Add more AI providers
- Create a web interface
- Add conversation persistence
- Implement streaming responses
- Add voice input/output

---

## License

This project is for educational purposes as part of CRCP6370 - AI in the Metaverse class.
