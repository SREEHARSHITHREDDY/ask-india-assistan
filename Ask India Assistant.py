"""
============================================================
   Project: India-Only AI Assistant
   API Used: Groq API (100% FREE — no credit card needed)
   Author  : Sreeharshith Reddy
============================================================

How to get your FREE Groq API key (takes 1 minute):
------------------------------------------------------
1. Go to https://console.groq.com
2. Sign up with Google account (one click)
3. Go to "API Keys" → "Create API Key"
4. Copy the key (starts with gsk_...)
5. Paste it when the script asks

Install dependency:
    pip install groq

How the Logic Works:
---------------------
1. A system prompt is injected into every API call.
   It strictly instructs the model to ONLY answer India-related questions.

2. The user's question is sent to Groq API as a user message.

3. The AI detects whether the topic is India-related:
   - The word "India" does NOT need to appear in the question.
   - Questions about states, cities, temples, parks, food, people,
     culture, history etc. are all valid India-related topics.

4. If NOT related to India → responds with EXACTLY:
   "I am sorry, I can only talk about India."

5. No keyword filtering — the LLM handles all detection,
   making it smart, context-aware, and robust.
"""

import os
from groq import Groq

# ─────────────────────────────────────────────────────────────────
# Get API Key
# ─────────────────────────────────────────────────────────────────
def get_api_key() -> str:
    key = os.getenv("GROQ_API_KEY", "").strip()
    if key:
        print("✓ API key loaded from environment.\n")
        return key
    print("=" * 60)
    print("  Groq API Key (100% FREE — No Credit Card)")
    print("  1. Go to   : https://console.groq.com")
    print("  2. Sign up with Google (one click)")
    print("  3. API Keys → Create API Key")
    print("  4. Paste the key below (starts with gsk_...)")
    print("=" * 60)
    key = input("  Enter your Groq API key: ").strip()
    print()
    return key


# ─────────────────────────────────────────────────────────────────
# System Prompt — Core restriction logic
# ─────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are an expert AI assistant on everything related to India.

Your ONLY job is to answer questions about India and Indian topics.
This includes (but is not limited to):
- Indian states, union territories, cities, towns, and villages
- Tourist places, temples, monuments, national parks, wildlife sanctuaries
- Indian history, culture, traditions, festivals, and religions
- Indian food, cuisine, and recipes
- Indian geography, rivers, mountains, and climate
- Indian politics, government, constitution, and laws
- Indian economy, industries, and businesses
- Indian sports, cricket, cinema (Bollywood, Tollywood, etc.)
- Famous Indian people, leaders, scientists, and artists
- Indian languages, literature, and arts

IMPORTANT: The user does NOT need to say the word "India" in the question.
Questions about Goa beaches, Kerala backwaters, Hampi temples, Hyderabad biryani,
Rajasthan forts, Kaziranga Park, Varanasi ghats, Sachin Tendulkar etc.
are all India-related — answer them fully and in detail.

STRICT RULE: If the question is completely unrelated to India
(e.g., history of London, capital of France, who is Elon Musk, etc.),
respond with EXACTLY this sentence and nothing else:
"I am sorry, I can only talk about India."

Do NOT add extra words. Do not suggest alternatives. Just that exact sentence."""


# ─────────────────────────────────────────────────────────────────
# Core Function
# ─────────────────────────────────────────────────────────────────
def ask_india_assistant(client: Groq, question: str) -> str:
    """
    Sends a question to the India-Only AI Assistant.

    Args:
        client   : Authenticated Groq client instance.
        question : User's input question.

    Returns:
        str: The assistant's response.
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",   # Latest free model on Groq
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": question}
        ],
        temperature=0.3,
        max_tokens=600
    )
    return response.choices[0].message.content.strip()


# ─────────────────────────────────────────────────────────────────
# Demo — 3 Required Questions
# ─────────────────────────────────────────────────────────────────
def run_demo(client: Groq):
    """Run the three demonstration questions as required by the assignment."""

    demo_questions = [
        "What is the capital of India?",
        "Who was Akbar?",
        "Tell me about the history of London."
    ]

    print("=" * 60)
    print("       India-Only AI Assistant — Demo")
    print("=" * 60)

    for i, question in enumerate(demo_questions, 1):
        print(f"\n[Question {i}]")
        print(f"Input : {question}")
        answer = ask_india_assistant(client, question)
        print(f"Output: {answer}")
        print("-" * 60)


# ─────────────────────────────────────────────────────────────────
# Interactive Mode
# ─────────────────────────────────────────────────────────────────
def run_interactive(client: Groq):
    """Allow the user to ask questions interactively."""

    print("\n" + "=" * 60)
    print("   Interactive Mode  —  Type 'exit' to quit")
    print("   Try: Goa beaches / Hampi temples / Kerala food /")
    print("        Jim Corbett Park / Taj Mahal / Biryani history")
    print("=" * 60)

    while True:
        user_input = input("\nYour Question: ").strip()

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "bye", "q"):
            print("\nThank you! Jai Hind!")
            break

        answer = ask_india_assistant(client, user_input)
        print(f"\nAssistant: {answer}")


# ─────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":

    # Step 1: Get API key
    api_key = get_api_key()

    # Step 2: Create Groq client
    client = Groq(api_key=api_key)

    # Step 3: Run demo (3 required questions)
    run_demo(client)

    # Step 4: Interactive mode
    run_interactive(client)