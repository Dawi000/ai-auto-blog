import os
import random
import datetime
import google.generativeai as genai

# 1. API KEY - GitHub Secrets se aayegi
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-3.8-flash")

# 2. TUMHARE 12 TOPICS
TOPICS = [
"5 Best Free AI Tools I Use Every Day",
"7 AI Tools That Actually Save Time",
"I Tested 5 Free AI Image Generators - 1 Shocked Me",
"Best Free AI Image Tool for YouTube Thumbnails",
"I Wrote 10 Blogs With AI - Here Is What Happened",
"Best AI Writing Tool for Beginners",
"10 ChatGPT Prompts I Use Daily",
"ChatGPT vs Gemini - I Used Both For 30 Days",
"How I Made My First 100 Dollars With AI Tools",
"3 Real Ways To Make Money With AI - No Scam",
"Canva AI Review - Honest After 1 Month Use",
"CapCut AI Review - Worth It Or Waste",
]

# 3. AAJ KA TOPIC CHUNO + LABEL BANAO
topic = random.choice(TOPICS)

if "Image" in topic:
    label = "AI Image Tools"
elif "Writing" in topic or "Blogs With AI" in topic:
    label = "AI Writing Tools"
elif "ChatGPT" in topic or "Gemini" in topic:
    label = "ChatGPT"
elif "Money" in topic or "100 Dollars" in topic:
    label = "Make Money"
elif "Review" in topic or "Canva" in topic or "CapCut" in topic:
    label = "Reviews"
else:
    label = "AI Tools"

# 4. HUMAN PROMPT - GLOBAL AUDIENCE
prompt = f"""
You are a real human blogger from USA, you have 5 years experience testing AI tools. You write for GLOBAL audience.
Topic: {topic}
Write in simple INTERNATIONAL ENGLISH, 100% HUMAN style for GLOBAL audience - USA, UK, Australia, Germany, Canada and all over the world. Use simple words that everyone can understand. Do NOT mention any specific country, city, or location like Pakistan, Lahore, India, USA. Write like a global blogger.

HUMAN RULES - Follow strictly:
1. Write like you are talking to a friend, use I, me, my experience. Example: "I tried this tool last week and honestly..."
2. Use contractions: don't, can't, it's, you'll - never write full formal form.
3. Mix short and long sentences. Some 5-word sentences. Some long.
4. Start 2-3 paras with personal story: "When I first tried..."
5. Add 1 mistake / honest opinion: "I didn't like this part..."
6. Add 1 question to reader: "Have you tried this?"
7. No robotic words: "In conclusion, Furthermore, Moreover, Delve, In today's digital world" - NEVER use these.
8. Use simple words, no fancy words.

You MUST return:
SEO_TITLE: [60 char]
META_DESCRIPTION: [155 char]
IMAGE_ALT: [10 words]
TAGS: [5 tags]
---
Then 800 words HTML: H1, H2, H3, bullets, 1 comparison table, 3 FAQs + Final Verdict with your honest opinion.
Use dollars ($).
"""

# 5. AI SE LIKHWAO
print(f"Writing about: {topic} | Label: {label}")
response = model.generate_content(prompt)
ai_text = response.text

# 6. FINAL FILE BANAO - LABEL KE SAATH
final = f"""<!-- BLOGGER LABEL: {label} -->
<!-- TOPIC: {topic} -->
{ai_text}
"""

# 7. FILE SAVE KARO
today = datetime.date.today().strftime("%Y-%m-%d")
os.makedirs("output", exist_ok=True)
filename = f"output/blog-{today}.md"
with open(filename, "w", encoding="utf-8") as f:
    f.write(final)

print(f"Done! Saved to {filename}")
