import os
from openai import OpenAI

ORG_NAME = "ABC Corp"

# Initialize OpenAI client (key comes from Streamlit Secrets)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_answer(query, context, history):
    # Build conversation history
    history_text = ""
    for h in history[-5:]:
        history_text += f"User: {h['q']}\nAssistant: {h['a']}\n"

    context_text = "\n\n".join(context)

    prompt = f"""
You are an HR policy assistant.

STRICT RULES:
- Use ONLY the provided policy excerpts.
- Do NOT quote long passages.
- Paraphrase and summarize clearly in simple language.
- Do NOT add assumptions, opinions, or commentary.
- If the policy does not contain the answer, say exactly:
  "The policy does not specify this information."
- Keep answers professional, concise, and human-friendly.

Conversation so far:
{history_text}

Policy excerpts:
{context_text}

User question:
{query}

Answer:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    answer = response.choices[0].message.content.strip()
    answer = answer.replace("{ORGANIZATION NAME}", ORG_NAME)

    return answer
