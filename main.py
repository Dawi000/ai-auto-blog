import os, random, datetime, requests, json, time

GEMINI_KEY = os.environ.get("GEMINI_API_KEY").strip()

TOPICS = [
"5 Best Free AI Tools for Students in 2025",
"Top 10 AI Tools for YouTubers to Grow Fast",
"ChatGPT vs Gemini vs Claude - Best AI for Blogging",
"7 Free AI Image Generators Better Than Midjourney",
"How to Make Money with AI Tools - Beginner Guide",
]

MODELS = ["gemini-3.8-flash", "gemini-2.5-flash-lite", "gemini-3-flash-preview"]

def main():
    topic = random.choice(TOPICS)
prompt = f"You are an expert tech blogger from USA writing for a GLOBAL audience. Topic: {topic}. Write 800 words in simple US ENGLISH. Do NOT mention Pakistan, Lahore, India, or any specific country. Use dollars ($), global examples, and write for readers in USA, UK, Canada, Australia and all over the world. Use H1 title, H2, H3, bullets, short paras, end with 3 FAQs + verdict. HTML only."
    headers = {"x-goog-api-key": GEMINI_KEY, "Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    content = None
    for model in MODELS:
        for attempt in range(3):
            try:
                print(f"Trying {model} attempt {attempt+1}")
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
                r = requests.post(url, headers=headers, json=data, timeout=120)
                print("Status:", r.status_code)
                if r.status_code == 200:
                    content = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                    break
                else:
                    print(r.text[:300])
                    time.sleep(10)
            except Exception as e:
                print(f"Error: {e}, retrying...")
                time.sleep(10)
        if content:
            break

    if not content:
        raise SystemExit("API failed after all retries")

    t = topic.replace(" ", "%20")
    img = f"https://image.pollinations.ai/prompt/{t}%20tech%20minimal?width=800&height=450&nologo=true"
    final = f'<p><img src="{img}" style="width:100%;border-radius:12px" /></p>\n' + content
    fname = f"post-{datetime.date.today()}.html"
    with open(fname, "w", encoding="utf-8") as f:
        f.write(final)
    print(f"Done: {fname}")

main()
