# Friend Conversation Guide

## Overview

Your chatbot now supports friend personas and group conversations! You can create multiple friend personas with different personalities and have them talk to each other or with you.

## New Commands

### Friend Management

#### `/addfriend <name> [personality]`
Add a new friend persona to your chatbot.

**Examples:**
```
/addfriend Alex
/addfriend Sam funny
/addfriend Jordan professional
/addfriend Taylor creative
```

**Available personalities for friends:**
- friendly, professional, funny, sarcastic, wise, casual, creative, kid-friendly, default

#### `/friends`
List all your friends and their personalities.

**Example:**
```
/friends

👥 Your Friends:
------------------------------------------------------------
  • Alex: casual personality
  • Sam: funny personality (active)
  • Jordan: professional personality
------------------------------------------------------------
```

#### `/befriend <name>`
Switch to talk as a specific friend. The chatbot will respond from that friend's perspective.

**Example:**
```
/befriend Alex
✓ Switched to Alex's perspective

You: What do you think about pizza?
Alex: Oh man, pizza is the best! 🍕 I could eat it every day!
```

#### `/back`
Switch back to the main AI chatbot (stop talking as a friend).

**Example:**
```
/back
✓ Switched back to main AI chatbot
```

#### `/removefriend <name>`
Remove a friend persona.

**Example:**
```
/removefriend Alex
✓ Friend 'Alex' removed.
```

### Group Chat Mode

#### `/groupchat <friend1> <friend2> ...`
Start a group chat where multiple friends discuss your messages together.

**Example:**
```
/groupchat Alex Sam Jordan
✓ Group chat started with: Alex, Sam, Jordan

Friends will take turns responding. Type /endgroupchat to stop.

You: What should we do this weekend?

[GROUP CHAT] Friends discussing...
  Alex is thinking...
  Sam is thinking...
  Jordan is thinking...

Alex: We could go hiking! The weather is perfect for it! 🏔️

Sam: Hiking? I'd rather go to the movies! 🎬 But I'm down for whatever!

Jordan: Both sound good, but we should check everyone's availability first. Let me create a group chat to coordinate.
```

#### `/endgroupchat`
End group chat mode and return to normal conversation.

**Example:**
```
/endgroupchat
✓ Group chat ended
```

## Example Conversation Flow

### Scenario 1: One-on-One with a Friend

```
You: /addfriend Alex funny
✓ Friend 'Alex' added with funny personality!

You: /befriend Alex
✓ Switched to Alex's perspective

You: Tell me a joke
Alex: Why don't scientists trust atoms? Because they make up everything! 😄

You: /back
✓ Switched back to main AI chatbot
```

### Scenario 2: Group Chat

```
You: /addfriend Alex casual
✓ Friend 'Alex' added with casual personality!

You: /addfriend Sam funny
✓ Friend 'Sam' added with funny personality!

You: /addfriend Jordan professional
✓ Friend 'Jordan' added with professional personality!

You: /groupchat Alex Sam Jordan
✓ Group chat started with: Alex, Sam, Jordan

You: What's the best programming language?

[GROUP CHAT] Friends discussing...
  Alex is thinking...
  Sam is thinking...
  Jordan is thinking...

Alex: I'd say Python! It's super easy to learn and super versatile.

Sam: Python? More like Python't stop coding! 😂 But seriously, JavaScript is where it's at for web stuff!

Jordan: Both are excellent choices. Python excels in data science and automation, while JavaScript is essential for web development. The "best" language depends on your specific use case.
```

### Scenario 3: Switching Between Friends

```
You: /befriend Alex
✓ Switched to Alex's perspective

You: What's your favorite hobby?
Alex: I love playing video games! Especially RPGs. What about you?

You: /befriend Sam
✓ Switched to Sam's perspective

You: What's your favorite hobby?
Sam: I'm all about cooking! 🍳 Trying new recipes is my jam! Want to come over for dinner?
```

## Tips

1. **Each friend has their own memory**: When you switch to a friend, they remember previous conversations with you.

2. **Friends in group chat respond independently**: Each friend gives their own unique perspective based on their personality.

3. **Mix personalities**: Create friends with different personalities to get diverse viewpoints!

4. **Save conversations**: Friends remember their conversation history even when you switch away.

5. **Combine with personalities**: You can still use `/personality` to change the main AI's personality, separate from your friends.

## Use Cases

- **Brainstorming**: Create friends with different expertise and have them discuss ideas
- **Debates**: Set up friends with opposing views and watch them debate
- **Storytelling**: Have friends collaborate on stories
- **Learning**: Create a teacher friend and a student friend for educational conversations
- **Entertainment**: Just have fun chatting with your AI friends!

## Quick Start

1. Add some friends:
   ```
   /addfriend Alex funny
   /addfriend Sam professional
   /addfriend Jordan creative
   ```

2. Start a group chat:
   ```
   /groupchat Alex Sam Jordan
   ```

3. Ask a question and watch them discuss!

4. Or talk to one friend:
   ```
   /befriend Alex
   ```

Enjoy your friend conversations! 🎉
