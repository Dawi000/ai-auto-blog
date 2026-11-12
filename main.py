import os, random, datetime, requests, json, time, re

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
    prompt = f"""
    You are an expert SEO blogger from USA writing for GLOBAL audience.
    Topic: {topic}
    Write in simple US ENGLISH. Do NOT mention Pakistan, Lahore, India, or any country.
    
    You MUST return in this exact format:
    SEO_TITLE: [60 characters catchy SEO title with main keyword]
    META_DESCRIPTION: [155 characters SEO description]
    IMAGE_ALT: [SEO image description, 10 words]
    TAGS: [tag1, tag2, tag3, tag4, tag5]
    ---
    Then write 800 words HTML blog: H1 title, H2, H3, bullets, short paras, end with 3 FAQs + verdict.
    Use dollars ($), global examples. HTML only.
    """
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

    # SEO parts nikalna
    seo_title = topic
    meta_desc = ""
    img_alt = topic
    tags = ""
    try:
        if "SEO_TITLE:" in content:
            seo_title = content.split("SEO_TITLE:")[1].split("\n")[0].strip()
        if "META_DESCRIPTION:" in content:
            meta_desc = content.split("META_DESCRIPTION:")[1].split("\n")[0].strip()
        if "IMAGE_ALT:" in content:
            img_alt = content.split("IMAGE_ALT:")[1].split("\n")[0].strip()
        if "TAGS:" in content:
            tags = content.split("TAGS:")[1].split("\n")[0].strip()
        if "---" in content:
            content = content.split("---",1)[1]
    except:
        pass

    t = topic.replace(" ", "%20")
    img = f"https://image.pollinations.ai/prompt/{t}%20tech%20minimal?width=800&height=450&nologo=true"
    
    final = f"""<!-- SEO TITLE: {seo_title} -->
<!-- META DESCRIPTION: {meta_desc} -->
<!-- TAGS: {tags} -->
<h1>{seo_title}</h1>
<p><img src="{img}" alt="{img_alt}" title="{img_alt}" style="width:100%;border-radius:12px" /></p>
<p><em>Image: {img_alt}</em></p>
{content}
<hr>
<p><b>Tags:</b> {tags}</p>
"""
    fname = f"post-{datetime.date.today()}.html"
    with open(fname, "w", encoding="utf-8") as f:
        f.write(final)
    print(f"Done: {fname} | SEO: {seo_title}")

main()
