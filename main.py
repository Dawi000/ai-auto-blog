import os, random, datetime, requests, time

GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_KEY:
    GEMINI_KEY = GEMINI_KEY.strip()

# دنیا میں ہائی CPM والے ٹاپکس
TOPICS = [
    "Best AI Tools to Make Money Online in 2025",
    "Best Web Hosting for Bloggers Review",
    "Best VPN for Streaming Netflix 2025",
    "ChatGPT Prompts to Earn Money",
    "Best AI Video Generator Free Without Watermark",
    "Best AI Tools for YouTube Automation",
    "Best AI Image Generator for Business Logo",
    "How to Start Faceless YouTube Channel with AI",
    "Best Free AI Tools for Students",
    "Best AI Writing Tools Better Than ChatGPT",
    "Best Credit Cards for Travel Rewards 2025",
    "Top AI Tools for Small Business Growth"
]

def generate_post(num):
    topic = random.choice(TOPICS)
    print(f"Topic {num}: {topic}")

    prompt = f"""
    Topic: {topic}
    Write in ENGLISH only.
    Task: Write a complete SEO blog post.
    Structure:
    1. First line: SEO_TITLE: <60 char title>
    2. Second line: META_DESC: <155 char description>
    3. Third line: TAGS: <5 tags comma separated>
    4. Then ---ARTICLE---
    5. Then full HTML article: <h1> with topic, <p> with image caption like "Image: {topic}", then <h2>, <h3>, <ul>, <p>, 800+ words, human tone, no AI words. End with 3 FAQs.
    """

    headers = {"x-goog-api-key": GEMINI_KEY, "Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    content = None
    for model in ["gemini-3.8-flash", "gemini-2.5-flash-lite"]:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
            r = requests.post(url, headers=headers, json=data, timeout=120)
            if r.status_code == 200:
                content = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                break
        except Exception as e:
            print(e)
            time.sleep(5)

    if not content:
        print("Failed")
        return

    # Image auto generate
    safe_topic = topic.replace(" ", "%20")
    img_url = f"https://image.pollinations.ai/prompt/{safe_topic}%20professional%20modern%20tech%20background?width=1280&height=720&nologo=true&seed={random.randint(1,9999)}"

    final_html = f'<img src="{img_url}" alt="{topic}" style="width:100%;border-radius:12px;" />\n' + content
    
    filename = f"post-{datetime.date.today()}-{num}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(final_html)
    print(f"Saved {filename}")

# دن میں 2 پوسٹ
generate_post(1)
time.sleep(10)
generate_post(2)
