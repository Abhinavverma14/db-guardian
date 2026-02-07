import os

try:
    from openai import OpenAI
    client = OpenAI()
    OPENAI_AVAILABLE = True
except:
    OPENAI_AVAILABLE = False


def generate_explanation(event_text):

    # Try LLM if available
    if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": f"Explain this database incident simply: {event_text}"}],
                temperature=0.2
            )
            return response.choices[0].message.content
        except:
            pass

    # Fallback explanation (local)
    return f"""
Database Safety Alert:

An unusual or destructive database operation was detected.

Event:
{event_text}

A protective snapshot was automatically created to prevent potential data loss.
"""
