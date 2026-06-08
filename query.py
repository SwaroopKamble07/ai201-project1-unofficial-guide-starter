import os

from dotenv import load_dotenv
from groq import Groq

from embed import retrieve, TOP_K

load_dotenv()

MODEL = "llama-3.3-70b-versatile"

# Chunks with a cosine distance above this are treated as irrelevant and
# dropped before the context is built. This is a backstop for off-topic /
# nonsense questions: if nothing relevant is retrieved, we decline without
# even calling the LLM. Normal housing questions sit well below this.
RELEVANCE_CUTOFF = 0.85

REFUSAL = "I don't have enough information on that."

SYSTEM_PROMPT = """You are The Unofficial Guide, a question-answering assistant about \
student experiences with on-campus housing at the University of Texas at Dallas (UTD).

Follow these rules without exception:
1. Answer ONLY using the information in the CONTEXT provided in the user message. \
Do not use any outside knowledge or anything from your training data.
2. If the CONTEXT does not contain enough information to answer the question, reply with \
exactly this sentence and nothing else: "{refusal}"
3. Never invent details, numbers, names, or facts that are not stated in the CONTEXT.
4. Do not mention or cite source files yourself — the system adds source attribution \
automatically after your answer.

Every part of your answer must be traceable to the CONTEXT.""".format(refusal=REFUSAL)

USER_TEMPLATE = """CONTEXT:
{context}

QUESTION: {question}

Answer using only the CONTEXT above."""


def _client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY not found. Copy .env.example to .env and add your key."
        )
    return Groq(api_key=api_key)


def _build_context(chunks):
    return "\n\n".join(f"[{c['source']}]\n{c['text']}" for c in chunks)


def _unique_sources(chunks):
    sources = []
    for c in chunks:
        if c["source"] not in sources:
            sources.append(c["source"])
    return sources


def ask(question, k=TOP_K):
    """Retrieve relevant chunks, generate a grounded answer, and attach sources.

    Returns a dict: {"answer": str, "sources": list[str]}.
    Source attribution is added programmatically here, never by the LLM.
    """
    chunks = retrieve(question, k=k)
    relevant = [c for c in chunks if c["distance"] <= RELEVANCE_CUTOFF]

    # Nothing relevant retrieved -> decline without calling the LLM.
    if not relevant:
        return {"answer": REFUSAL, "sources": []}

    context = _build_context(relevant)

    client = _client()
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_TEMPLATE.format(context=context, question=question)},
        ],
    )
    answer = response.choices[0].message.content.strip()

    # If the model declined, don't attach sources (the answer isn't grounded
    # in any specific document).
    if answer.lower().startswith("i don't have enough information"):
        return {"answer": REFUSAL, "sources": []}

    return {"answer": answer, "sources": _unique_sources(relevant)}


if __name__ == "__main__":
    test_questions = [
        "Are Canyon Creek Heights apartments furnished?",
        "Are the UTD dorms single occupancy or shared rooms?",
        "What is the best pizza topping?",  # out-of-scope: should be refused
    ]
    for q in test_questions:
        print(f"\n{'=' * 60}")
        print(f"Q: {q}")
        print(f"{'=' * 60}")
        result = ask(q)
        print(f"\nAnswer:\n{result['answer']}")
        if result["sources"]:
            print("\nRetrieved from:")
            for s in result["sources"]:
                print(f"  - {s}")
        else:
            print("\nRetrieved from: (none)")
