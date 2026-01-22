import subprocess

ORG_NAME = "ABC Corp"


def generate_answer(query, context, history):
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

    result = subprocess.run(
        ["ollama", "run", "llama3", prompt],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    answer = result.stdout.strip()
    answer = answer.replace("{ORGANIZATION NAME}", ORG_NAME)

    return answer
