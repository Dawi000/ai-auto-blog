import os, random, datetime
import google.generativeai as genai

GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

TOPICS = [
"5 Best Free AI Tools for Students in 2025",
"Top 10 AI Tools for YouTubers to Grow Fast",
"ChatGPT vs Gemini vs Claude - Best AI for Blogging",
"7 Free AI Image Generators Better Than Midjourney",
"How to Make Money with AI Tools - Beginner Guide",
"Best AI Tools for Video Editing - No Watermark",
"AI Tools for Resume Writing That Get You Hired"
]

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

HUMAN_PROMPT = """
You are a human blogger from Pakistan writing for AI Tools Nest.
Topic: {topic}
Write in ENGLISH, human style, 800 words.
- Catchy title H1
- Hook first 2 lines: I tested...
- Use H2, H3, bullets, short paras
- Add table if possible
- Humanize, use I/you, contractions
- No AI words: delve, unleash, revolutionize
- End with 3 FAQs + verdict
- HTML format only
- After write ---META--- and 150 char meta description
"""

def get_image(title):
    t = title.replace(" ", "%20")
    return f"https://image.pollinations.ai/prompt/{t}%20tech%20minimal?width=800&height=450&nologo=true"

def main():
    topic = random.choice(TOPICS)
    prompt = HUMAN_PROMPT.format(topic=topic)
    res = model.generate_content(prompt)
    content = res.text
    img = get_image(topic)
    final = f'<p><img src="{img}" style="width:100%;border-radius:12px" /></p>\n' + content
    fname = f"post-{datetime.date.today()}.html"
    with open(fname, "w", encoding="utf-8") as f:
        f.write(final)
    print(f"Done: {fname}")

main()
