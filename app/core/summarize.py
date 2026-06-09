import google.generativeai as genai

genai.configure(api_key="TWOJ_GEMINI_API_KEY")

async def summarize_with_ai(posts):
    text = "\n".join(
        [f"- {p['title']} ({p['source']}) — {p['url']}" for p in posts]
    )

    prompt = f"""
    Na podstawie poniższych wyników z internetu:

    {text}

    Zrób raport:
    - najważniejsze trendy
    - powtarzające się opinie
    - kontrowersje
    - wnioski
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text
