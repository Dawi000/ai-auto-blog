import os, random, datetime, requests, json

GEMINI_KEY = os.environ.get("GEMINI_API_KEY").strip()

TOPICS = [
"5 Best Free AI Tools for Students in 2025",
"Top 10 AI Tools for YouTubers to Grow Fast",
"ChatGPT vs Gemini vs Claude - Best AI for Blogging",
"7 Free AI Image Generators Better Than Midjourney",
"How to Make Money with AI Tools - Beginner Guide",
]

def main():
    topic = random.choice(TOPICS)
    prompt = f"You are a human blogger from Pakistan. Topic: {topic}. Write 800 words in ENGLISH, human style, H1 title, H2, H3, bullets, short paras, end with 3 FAQs + verdict. HTML only. No AI words like delve, unleash."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {"x-goog-api-key": GEMINI_KEY, "Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    r = requests.post(url, headers=headers, json=data, timeout=60)
    print("Status:", r.status_code)
    if r.status_code != 200:
        print(r.text[:500])
        raise SystemExit("API failed")
    content = r.json()["candidates"][0]["content"]["parts"][0]["text"]
    t = topic.replace(" ", "%20")
    img = f"https://image.pollinations.ai/prompt/{t}%20tech%20minimal?width=800&height=450&nologo=true"
    final = f'<p><img src="{img}" style="width:100%;border-radius:12px" /></p>\n' + content
    fname = f"post-{datetime.date.today()}.html"
    with open(fname, "w", encoding="utf-8") as f:
        f.write(final)
    print(f"Done: {fname}")

main()
