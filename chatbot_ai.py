#!/usr/bin/env python3
"""
AI-Powered Chatbot with Claude and ChatGPT Integration
A chatbot that can use both Anthropic's Claude and OpenAI's ChatGPT APIs.
"""

import os
import sys
from typing import Optional, Literal

# Try importing dotenv for environment variable management
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    print("Note: python-dotenv not installed. Environment variables will be read from system.")

# Load environment variables from .env file
# This will look for .env in the current directory and parent directories
if DOTENV_AVAILABLE:
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        # Try loading from current directory (for VSCode compatibility)
        load_dotenv()

# Try importing Claude SDK
try:
    from anthropic import Anthropic
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False
    print("Warning: Anthropic SDK not installed. Install with: pip install anthropic")

# Try importing OpenAI SDK
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: OpenAI SDK not installed. Install with: pip install openai")


class AIChatbot:
    """Chatbot that integrates with Claude and ChatGPT APIs."""

    # Predefined personality templates - each ends with emphasis to ensure AI follows the personality
    PERSONALITIES = {
        "friendly": "You are a friendly, warm, and enthusiastic assistant. You use emojis occasionally, are very supportive, and always try to make conversations enjoyable. You're helpful, positive, and genuinely interested in helping the user. IMPORTANT: Always respond in a warm, friendly way. Never be cold or formal.",
        "professional": "You are a professional, formal, and business-oriented assistant. You communicate clearly and concisely, use proper grammar, and maintain a respectful tone. You focus on being helpful and efficient. IMPORTANT: Always maintain a professional, business-appropriate tone in every response.",
        "funny": "You are a witty, humorous, and playful assistant. You make jokes, use puns, and keep conversations light-hearted. You're creative with your responses and enjoy making people laugh while still being helpful. IMPORTANT: Always include humor, wit, or a joke in your responses. Keep it fun!",
        "sarcastic": "You are a sarcastic but friendly assistant. You use dry humor and witty remarks, but you're still helpful. You have a sharp sense of humor and aren't afraid to be a bit cheeky. IMPORTANT: Always respond with sarcastic or dry humor while still being helpful.",
        "wise": "You are a wise, thoughtful, and philosophical assistant. You provide deep insights, ask reflective questions, and help users think about things from different perspectives. You speak calmly and thoughtfully. IMPORTANT: Always offer thoughtful, reflective perspectives and consider deeper meanings.",
        "casual": "You are a casual, laid-back assistant. You talk like a friend, use everyday language, and keep things relaxed. You're approachable and easy to talk to. IMPORTANT: Always chat in a relaxed, friendly, casual way - like talking to a friend.",
        "creative": "You are a creative and imaginative assistant. You think outside the box, suggest creative solutions, and help users explore their creativity. You're artistic and inspiring. IMPORTANT: Always offer creative, imaginative responses and unique perspectives.",
        "kid-friendly": "You are a kid-friendly assistant perfect for children! You use simple, easy-to-understand language. You're super positive, encouraging, and fun! You use emojis like 😊🌟✨🎉 to make things exciting. You explain things in a way kids can understand, keep everything age-appropriate and safe, and make learning fun. You're like a friendly teacher who loves to help kids learn and have fun! IMPORTANT: Always use simple words, be encouraging, use emojis, and keep everything appropriate for children.",
        "default": "You are a helpful, kind, and intelligent assistant. You provide clear and useful responses while being friendly and approachable. IMPORTANT: Be helpful and kind in every response."
    }

    def __init__(self, default_provider: Literal["claude", "chatgpt"] = "claude", personality: str = "default"):
        """
        Initialize the AI chatbot.

        Args:
            default_provider: Default AI provider to use ("claude" or "chatgpt")
            personality: Personality to use (default: "default")
        """
        self.default_provider = default_provider
        self.claude_client = None
        self.openai_client = None
        self.conversation_history = []
        self.personality = personality
        self.system_prompt = self.PERSONALITIES.get(
            personality, self.PERSONALITIES["default"])

        # Friend conversation features
        # Dictionary to store friend personas: {name: {personality, system_prompt}}
        self.friends = {}
        self.current_friend = None  # Currently active friend persona
        self.group_chat_mode = False  # Whether in group chat mode
        self.group_chat_friends = []  # List of friends in group chat

        # Initialize Claude client
        if CLAUDE_AVAILABLE:
            claude_api_key = os.getenv("ANTHROPIC_API_KEY")
            if claude_api_key:
                self.claude_client = Anthropic(api_key=claude_api_key)
                print("✓ Claude API initialized")
            else:
                print("⚠ ANTHROPIC_API_KEY not found in environment variables")

        # Initialize OpenAI client
        if OPENAI_AVAILABLE:
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if openai_api_key:
                self.openai_client = OpenAI(api_key=openai_api_key)
                print("✓ ChatGPT API initialized")
            else:
                print("⚠ OPENAI_API_KEY not found in environment variables")

        # Check if at least one provider is available
        if not self.claude_client and not self.openai_client:
            msg = (
                "No API keys found. Please set ANTHROPIC_API_KEY and/or OPENAI_API_KEY "
                "in your .env file. See env.example for reference."
            )
            raise RuntimeError(msg)

    def chat_with_claude(self, message: str, model: str = "claude-3-5-sonnet-20241022") -> Optional[str]:
        """
        Send a message to Claude and get a response.

        Args:
            message: User's message
            model: Claude model to use

        Returns:
            Claude's response or None if error
        """
        if not self.claude_client:
            return None

        try:
            # Prepare messages for Claude (includes conversation history)
            # Claude uses "user" and "assistant" roles
            messages = self.conversation_history.copy()
            messages.append({"role": "user", "content": message})

            # Try models in order - fall back if one is deprecated
            models_to_try = [
                "claude-3-5-sonnet-20241022",
                "claude-sonnet-4-20250514",
                "claude-3-5-sonnet-20240620",
            ]
            if model not in models_to_try:
                models_to_try.insert(0, model)

            response = None
            last_error = None
            for try_model in models_to_try:
                try:
                    response = self.claude_client.messages.create(
                        model=try_model,
                        max_tokens=1024,
                        messages=messages,
                        system=self.system_prompt
                    )
                    break
                except Exception as e:
                    last_error = e
                    if "model" in str(e).lower() or "404" in str(e) or "not found" in str(e).lower():
                        continue
                    raise
            if response is None and last_error is not None:
                raise last_error

            response_text = response.content[0].text
            self.conversation_history.append(
                {"role": "user", "content": message})
            self.conversation_history.append(
                {"role": "assistant", "content": response_text})
            return response_text
        except Exception as e:
            return f"Error with Claude API: {str(e)}"

    def chat_with_chatgpt(self, message: str, model: str = "gpt-3.5-turbo") -> Optional[str]:
        """
        Send a message to ChatGPT and get a response.

        Args:
            message: User's message
            model: OpenAI model to use (gpt-4, gpt-3.5-turbo, etc.)

        Returns:
            ChatGPT's response or None if error
        """
        if not self.openai_client:
            return None

        try:
            # Prepare messages for ChatGPT (includes conversation history)
            # OpenAI uses "system", "user", and "assistant" roles
            # Always include system prompt so personality is maintained every turn
            messages = [{"role": "system", "content": self.system_prompt}]
            messages.extend(self.conversation_history)
            messages.append({"role": "user", "content": message})

            response = self.openai_client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=1024,
                temperature=0.7
            )

            # Extract the text content from the response
            response_text = response.choices[0].message.content

            # Update conversation history (only add if successful)
            self.conversation_history.append(
                {"role": "user", "content": message})
            self.conversation_history.append(
                {"role": "assistant", "content": response_text})

            return response_text
        except Exception as e:
            error_msg = str(e)
            # Don't add failed messages to history
            return f"Error with ChatGPT API: {error_msg}"

    def get_response(self, message: str, provider: Optional[Literal["claude", "chatgpt"]] = None) -> str:
        """
        Get a response from the specified AI provider.

        Args:
            message: User's message
            provider: AI provider to use ("claude" or "chatgpt"). If None, uses default.

        Returns:
            AI's response
        """
        provider = provider or self.default_provider

        if provider == "claude":
            if self.claude_client:
                return self.chat_with_claude(message)
            elif self.openai_client:
                print("⚠ Claude not available, using ChatGPT instead...")
                return self.chat_with_chatgpt(message)
            else:
                return "Error: No AI providers available"

        elif provider == "chatgpt":
            if self.openai_client:
                return self.chat_with_chatgpt(message)
            elif self.claude_client:
                print("⚠ ChatGPT not available, using Claude instead...")
                return self.chat_with_claude(message)
            else:
                return "Error: No AI providers available"

        else:
            return f"Error: Unknown provider '{provider}'. Use 'claude' or 'chatgpt'."

    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
        print("Conversation history cleared!")

    def set_personality(self, personality: str):
        """
        Change the chatbot's personality.

        Args:
            personality: Name of personality to use
        """
        if personality in self.PERSONALITIES:
            self.personality = personality
            self.system_prompt = self.PERSONALITIES[personality]
            self.clear_history()  # Clear history when changing personality
            print(f"✓ Personality changed to: {personality}")
            print(f"  {self.system_prompt[:100]}...\n")
        else:
            available = ", ".join(self.PERSONALITIES.keys())
            print(f"❌ Unknown personality: {personality}")
            print(f"Available personalities: {available}\n")

    def set_custom_personality(self, custom_prompt: str):
        """
        Set a custom personality prompt.

        Args:
            custom_prompt: Custom personality description
        """
        self.personality = "custom"
        self.system_prompt = custom_prompt
        self.clear_history()
        print("✓ Custom personality set!")
        print(f"  {custom_prompt[:100]}...\n")

    def add_friend(self, name: str, personality: str = "casual", custom_prompt: Optional[str] = None):
        """
        Add a friend persona to the conversation.

        Args:
            name: Name of the friend
            personality: Personality type to use
            custom_prompt: Optional custom personality description
        """
        if custom_prompt:
            prompt = custom_prompt
        else:
            prompt = self.PERSONALITIES.get(
                personality, self.PERSONALITIES["casual"])

        self.friends[name] = {
            "personality": personality,
            "system_prompt": prompt,
            "history": []
        }
        print(f"✓ Friend '{name}' added with {personality} personality!\n")

    def remove_friend(self, name: str):
        """Remove a friend persona."""
        if name in self.friends:
            del self.friends[name]
            if self.current_friend == name:
                self.current_friend = None
            if name in self.group_chat_friends:
                self.group_chat_friends.remove(name)
            print(f"✓ Friend '{name}' removed.\n")
        else:
            print(f"❌ Friend '{name}' not found.\n")

    def switch_to_friend(self, name: str):
        """Switch to a friend persona."""
        if name in self.friends:
            # Save current context before switching
            if self.current_friend:
                self.friends[self.current_friend]["history"] = self.conversation_history.copy(
                )

            self.current_friend = name
            self.system_prompt = self.friends[name]["system_prompt"]
            self.conversation_history = self.friends[name]["history"].copy()
            print(f"✓ Switched to {name}'s perspective\n")
        else:
            print(
                f"❌ Friend '{name}' not found. Use /addfriend to create them.\n")

    def switch_back_to_ai(self):
        """Switch back to the main AI chatbot."""
        if self.current_friend:
            # Save current friend's history
            self.friends[self.current_friend]["history"] = self.conversation_history.copy(
            )
            self.current_friend = None
            self.system_prompt = self.PERSONALITIES.get(
                self.personality, self.PERSONALITIES["default"])
            # Keep conversation history but clear it if user wants fresh start
            # self.conversation_history = []  # Uncomment if you want to clear history when switching back
            print("✓ Switched back to main AI chatbot\n")
        else:
            print("You're already using the main AI chatbot.\n")

    def start_group_chat(self, friend_names: list):
        """Start a group chat with multiple friends."""
        valid_friends = [name for name in friend_names if name in self.friends]
        if not valid_friends:
            print("❌ No valid friends found. Add friends first with /addfriend\n")
            return

        self.group_chat_mode = True
        self.group_chat_friends = valid_friends
        print(f"✓ Group chat started with: {', '.join(valid_friends)}\n")
        print("Friends will take turns responding. Type /endgroupchat to stop.\n")

    def end_group_chat(self):
        """End group chat mode."""
        self.group_chat_mode = False
        self.group_chat_friends = []
        print("✓ Group chat ended\n")

    def get_friend_response(self, friend_name: str, message: str, provider: Optional[Literal["claude", "chatgpt"]] = None) -> str:
        """Get a response from a specific friend."""
        if friend_name not in self.friends:
            return f"Error: Friend '{friend_name}' not found"

        friend = self.friends[friend_name]
        original_system = self.system_prompt
        original_history = self.conversation_history

        # Temporarily switch to friend's context
        self.system_prompt = friend["system_prompt"]
        self.conversation_history = friend["history"].copy()

        # Get response
        provider = provider or self.default_provider
        if provider == "claude" and self.claude_client:
            response = self.chat_with_claude(message)
        elif provider == "chatgpt" and self.openai_client:
            response = self.chat_with_chatgpt(message)
        else:
            response = "Error: No AI provider available"

        # Update friend's history
        friend["history"] = self.conversation_history.copy()

        # Restore original context
        self.system_prompt = original_system
        self.conversation_history = original_history

        return response

    def chat(self):
        """Main interactive chat loop."""
        # Clear screen for better VSCode terminal experience
        if sys.stdout.isatty():  # Only clear if running in a terminal
            os.system('clear' if os.name == 'posix' else 'cls')

        print("\n" + "="*60)
        print("🤖 AI-Powered Chatbot (Claude & ChatGPT)")
        print("="*60)
        print("\nAvailable commands:")
        print("  /claude    - Switch to Claude")
        print("  /chatgpt   - Switch to ChatGPT")
        print("  /personality <name> - Change personality")
        print("  /personalities - List available personalities")
        print("\n👥 Friend Conversation Commands:")
        print("  /addfriend <name> [personality] - Add a friend persona")
        print("  /friends - List all friends")
        print("  /befriend <name> - Talk as a friend")
        print("  /back - Switch back to main AI")
        print("  /removefriend <name> - Remove a friend")
        print("  /groupchat <name1> <name2> ... - Start group chat")
        print("  /endgroupchat - End group chat mode")
        print("\nOther commands:")
        print("  /clear     - Clear conversation history")
        print("  /history   - Show conversation history")
        print("  /quit      - Exit the chatbot")
        print("  /help      - Show this help message")
        print("\n" + "-"*60 + "\n")

        current_provider = self.default_provider
        print(f"Current provider: {current_provider.upper()}")
        if self.current_friend:
            print(f"Current friend: {self.current_friend}")
        elif self.group_chat_mode:
            print(f"Group chat mode: {', '.join(self.group_chat_friends)}")
        else:
            print(f"Current personality: {self.personality}")
        print()

        while True:
            try:
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                # Handle commands
                if user_input.startswith("/"):
                    command = user_input.lower()

                    if command == "/quit" or command == "/exit":
                        print("\n👋 Goodbye! Thanks for chatting!")
                        break

                    elif command == "/claude":
                        if self.claude_client:
                            current_provider = "claude"
                            print("✓ Switched to Claude\n")
                        else:
                            print("❌ Claude not available (check API key)\n")
                        continue

                    elif command == "/chatgpt" or command == "/gpt":
                        if self.openai_client:
                            current_provider = "chatgpt"
                            print("✓ Switched to ChatGPT\n")
                        else:
                            print("❌ ChatGPT not available (check API key)\n")
                        continue

                    elif command == "/clear":
                        self.clear_history()
                        print()
                        continue

                    elif command == "/history":
                        if self.conversation_history:
                            print("\n📜 Conversation History:")
                            print("-" * 60)
                            for i, msg in enumerate(self.conversation_history, 1):
                                role = "You" if msg["role"] == "user" else "AI"
                                content = msg["content"][:100] + "..." if len(
                                    msg["content"]) > 100 else msg["content"]
                                print(f"{i}. {role}: {content}")
                            print("-" * 60 + "\n")
                        else:
                            print("No conversation history yet.\n")
                        continue

                    elif command.startswith("/personality"):
                        parts = command.split()
                        if len(parts) > 1:
                            personality_name = parts[1]
                            self.set_personality(personality_name)
                        else:
                            print("\nUsage: /personality <name>")
                            print("Available personalities:")
                            for name, desc in self.PERSONALITIES.items():
                                print(f"  - {name}: {desc[:60]}...")
                            print("\nOr use: /personalities to see full list\n")
                        continue

                    elif command == "/personalities":
                        print("\n🎭 Available Personalities:")
                        print("-" * 60)
                        for name, desc in self.PERSONALITIES.items():
                            current = " (current)" if name == self.personality else ""
                            print(f"\n{name.upper()}{current}:")
                            print(f"  {desc}")
                        print("-" * 60 + "\n")
                        continue

                    elif command.startswith("/addfriend"):
                        parts = command.split()
                        if len(parts) >= 2:
                            friend_name = parts[1]
                            personality = parts[2] if len(
                                parts) > 2 else "casual"
                            self.add_friend(friend_name, personality)
                        else:
                            print("Usage: /addfriend <name> [personality]")
                            print("Example: /addfriend Alex funny\n")
                        continue

                    elif command == "/friends":
                        if self.friends:
                            print("\n👥 Your Friends:")
                            print("-" * 60)
                            for name, friend_data in self.friends.items():
                                current = " (active)" if name == self.current_friend else ""
                                print(
                                    f"  • {name}{current}: {friend_data['personality']} personality")
                            print("-" * 60 + "\n")
                        else:
                            print(
                                "No friends added yet. Use /addfriend <name> to add one!\n")
                        continue

                    elif command.startswith("/befriend"):
                        parts = command.split()
                        if len(parts) >= 2:
                            friend_name = parts[1]
                            self.switch_to_friend(friend_name)
                        else:
                            print("Usage: /befriend <name>")
                            print("Example: /befriend Alex\n")
                        continue

                    elif command == "/back":
                        self.switch_back_to_ai()
                        continue

                    elif command.startswith("/removefriend"):
                        parts = command.split()
                        if len(parts) >= 2:
                            friend_name = parts[1]
                            self.remove_friend(friend_name)
                        else:
                            print("Usage: /removefriend <name>\n")
                        continue

                    elif command.startswith("/groupchat"):
                        parts = command.split()
                        if len(parts) >= 2:
                            friend_names = parts[1:]
                            self.start_group_chat(friend_names)
                        else:
                            print("Usage: /groupchat <friend1> <friend2> ...")
                            print("Example: /groupchat Alex Sam\n")
                        continue

                    elif command == "/endgroupchat":
                        self.end_group_chat()
                        continue

                    elif command == "/help":
                        print("\nAvailable commands:")
                        print("  /claude    - Switch to Claude")
                        print("  /chatgpt   - Switch to ChatGPT")
                        print("  /personality <name> - Change personality")
                        print("  /personalities - List available personalities")
                        print("\n👥 Friend Conversation Commands:")
                        print(
                            "  /addfriend <name> [personality] - Add a friend persona")
                        print("  /friends - List all friends")
                        print("  /befriend <name> - Talk as a friend")
                        print("  /back - Switch back to main AI")
                        print("  /removefriend <name> - Remove a friend")
                        print("  /groupchat <name1> <name2> ... - Start group chat")
                        print("  /endgroupchat - End group chat mode")
                        print("\nOther commands:")
                        print("  /clear     - Clear conversation history")
                        print("  /history   - Show conversation history")
                        print("  /quit      - Exit the chatbot")
                        print("  /help      - Show this help message\n")
                        continue

                    else:
                        print(
                            f"Unknown command: {command}. Type /help for available commands.\n")
                        continue

                # Get AI response
                if self.group_chat_mode:
                    # Group chat mode - friends take turns
                    print(f"\n[GROUP CHAT] Friends discussing...")
                    try:
                        responses = []
                        for friend_name in self.group_chat_friends:
                            print(f"  {friend_name} is thinking...")
                            friend_response = self.get_friend_response(
                                friend_name, user_input, provider=current_provider)
                            responses.append(
                                f"{friend_name}: {friend_response}")

                        print("\n" + "\n\n".join(responses) + "\n")
                    except KeyboardInterrupt:
                        raise
                    except Exception as e:
                        print(f"\n❌ Unexpected error: {str(e)}\n")
                else:
                    # Normal chat mode
                    speaker = self.current_friend if self.current_friend else "AI"
                    print(f"\n[{current_provider.upper()}] Thinking...")
                    try:
                        response = self.get_response(
                            user_input, provider=current_provider)
                        if response:
                            print(f"\n{speaker}: {response}\n")
                        else:
                            print("\n❌ No response received. Please try again.\n")
                    except KeyboardInterrupt:
                        raise
                    except Exception as e:
                        print(f"\n❌ Unexpected error: {str(e)}\n")
                        # Don't break the loop, allow user to continue

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for chatting!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}\n")


def main():
    """Main entry point."""
    # Check if at least one SDK is installed
    if not CLAUDE_AVAILABLE and not OPENAI_AVAILABLE:
        print("❌ Error: No AI SDKs installed!")
        print("\nPlease install the required packages:")
        print("  pip install anthropic openai python-dotenv")
        print("\nOr install from requirements.txt:")
        print("  pip install -r requirements.txt")
        sys.exit(1)

    # Determine default provider based on available APIs
    default_provider = "claude"
    if not CLAUDE_AVAILABLE and OPENAI_AVAILABLE:
        default_provider = "chatgpt"

    # Create and run chatbot
    chatbot = AIChatbot(default_provider=default_provider)
    chatbot.chat()


if __name__ == "__main__":
    main()
