# Chatbot Personality Guide

## How to Run the Chatbot in Terminal

### Method 1: Direct Python Command
```bash
python3 chatbot_ai.py
```

### Method 2: In VSCode
- Press `F5` to debug
- Or click the Run button in the editor
- Or use the integrated terminal: `python3 chatbot_ai.py`

## Available Personalities

The chatbot comes with 9 built-in personalities:

1. **friendly** - Warm, enthusiastic, uses emojis, very supportive
2. **professional** - Formal, business-oriented, clear and concise
3. **funny** - Witty, playful, makes jokes and puns
4. **sarcastic** - Dry humor, witty remarks, a bit cheeky
5. **wise** - Thoughtful, philosophical, asks deep questions
6. **casual** - Laid-back, talks like a friend, everyday language
7. **creative** - Imaginative, thinks outside the box, artistic
8. **kid-friendly** - Perfect for children! Simple language, positive, fun, uses emojis, age-appropriate and safe
9. **default** - Helpful, kind, balanced (default personality)

## Commands

### Personality Commands
- `/personality <name>` - Change to a specific personality
  - Example: `/personality funny`
  - Example: `/personality professional`
  
- `/personalities` - List all available personalities with descriptions

### Other Commands
- `/claude` - Switch to Claude AI
- `/chatgpt` or `/gpt` - Switch to ChatGPT
- `/clear` - Clear conversation history
- `/history` - View conversation history
- `/help` - Show all commands
- `/quit` or `/exit` - Exit the chatbot

## Example Usage

### Funny Personality
```
You: /personality funny
✓ Personality changed to: funny

You: Tell me a joke
[CLAUDE] Thinking...

AI: Why don't scientists trust atoms? Because they make up everything! 😄
```

### Kid-Friendly Personality
```
You: /personality kid-friendly
✓ Personality changed to: kid-friendly

You: What is the sun?
[CLAUDE] Thinking...

AI: The sun is a super bright star! 🌞 It's like a giant ball of fire in the sky that gives us light and warmth. It's so big that you could fit over a million Earths inside it! The sun helps plants grow and makes our days bright and happy! ✨
```

## Custom Personality

You can also create custom personalities by modifying the code. The personality is set via a system prompt that tells the AI how to behave.

## Tips

1. **Change personality anytime**: Use `/personality <name>` to switch personalities mid-conversation
2. **Personality affects all responses**: The personality you choose affects how the AI responds to all your messages
3. **Clear history when changing**: The chatbot automatically clears history when you change personalities to avoid confusion
4. **Works with both AI providers**: Personalities work with both Claude and ChatGPT
