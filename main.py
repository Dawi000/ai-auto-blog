
import os
import random
import datetime
import requests
import time
from urllib.parse import quote

GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "").strip()

TOPICS = [
    "Best AI Tools to Make Money Online in 2026",
    "Best Web Hosting for Bloggers Review",
    "Best VPN for Streaming Netflix",
    "ChatGPT Prompts to Earn Money",
    "Best AI Video Generator Free",
    "Best AI Tools for YouTube Automation",
    "Best AI Image Generator for Business Logo",
    "How to Start Faceless YouTube Channel with AI",
    "Best Free AI Tools for Students",
    "Best AI Writing Tools",
    "Best Credit Cards for Travel Rewards",
    "Top AI Tools for Small Business Growth"
]

def generate_post(num):
    topic = random.choice(TOPICS)
    print(f"\nTopic {num}: {topic}")

    if not GEMINI_KEY:
        print("ERROR: GEMINI_API_KEY secret is missing!")
        return

    prompt = f"""
Topic: {topic}

Write a complete, original SEO blog post in English.

Requirements:
1. SEO title under 60 characters.
2. Meta description under 155 characters.
3. Five relevant tags.
4. Complete HTML article.
5. Use H1, H2, H3, paragraphs and lists.
6. At least 800 words.
7. Natural, helpful and human writing.
8. Include three useful FAQs.
9. Do not invent product features or prices.
10. End with a helpful conclusion.

Return exactly this format:

SEO_TITLE: Your title
META_DESC: Your description
TAGS: tag1, tag2, tag3, tag4, tag5
---ARTICLE---
<h1>Article heading</h1>
<p>Article content...</p>
"""

    models = [
        "gemini-3.8-flash",
        "gemini-3.5-flash-lite"
    ]

    content = None

    for model in models:
        print(f"Trying model: {model}")

        url = (
            "https://generativelanguage.googleapis.com/"
            f"v1beta/models/{model}:generateContent"
        )

        headers = {
            "x-goog-api-key": GEMINI_KEY,
            "Content-Type": "application/json"
        }

        data = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 8192
            }
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=180
            )

            if response.status_code != 200:
                print("API ERROR:", response.status_code)
                print("DETAILS:", response.text[:2000])
                continue

            result = response.json()

            candidates = result.get("candidates", [])

            if not candidates:
                print("ERROR: No candidates returned.")
                print(result)
                continue

            parts = candidates[0].get("content", {}).get("parts", [])
            content = "".join(
                part.get("text", "") for part in parts
            ).strip()

            if content:
                print("SUCCESS: Article generated!")
                break

            print("ERROR: Empty article response.")

        except requests.exceptions.RequestException as e:
            print("NETWORK ERROR:", str(e))

        except Exception as e:
            print("OTHER ERROR:", str(e))

        time.sleep(3)

    if not content:
        print("FAILED: All Gemini models failed.")
        return

    article = content.split("---ARTICLE---", 1)

    if len(article) != 2:
        print("ERROR: Article format is incorrect.")
        print(content[:1000])
        return

    article_html = article[1].strip()

    if not article_html:
        print("ERROR: Empty HTML article.")
        return

    safe_topic = quote(topic, safe="")
    img_url = (
        f"https://image.pollinations.ai/prompt/"
        f"{safe_topic}%20professional%20tech%20background"
        f"?width=1280&height=720&nologo=true"
        f"&seed={random.randint(1,9999)}"
    )

    final_html = f"""
<img src="{img_url}"
alt="{topic}"
style="width:100%;border-radius:12px;" />

{article_html}
"""

    filename = f"post-{datetime.date.today()}-{num}.html"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"SUCCESS: Saved {filename}")
    print(f"Article size: {len(final_html)} characters")


generate_post(1)
time.sleep(10)
generate_post(2)
