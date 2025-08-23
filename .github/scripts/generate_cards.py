import os
import requests
from PIL import Image, ImageDraw, ImageFont

# Config
USERNAME = "Bismay-exe"
BACKGROUND = "assets/card2.png"
OUTPUT_DIR = "assets/generated"
README_PATH = "README.md"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Fetch all public repos (default order = last updated)
url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"
repos = requests.get(url).json()

cards_md = ["## 📦 My Projects\n"]

row = []
for i, repo in enumerate(repos, start=1):
    name = repo["name"]
    description = repo["description"] or "No description"
    stars = repo["stargazers_count"]
    forks = repo["forks_count"]

    # --- Generate card image ---
    img = Image.open(BACKGROUND).convert("RGBA")
    draw = ImageDraw.Draw(img)

    font_big = ImageFont.truetype(FONT, 40)
    font_small = ImageFont.truetype(FONT, 20)

    draw.text((50, 50), name, font=font_big, fill="white")
    draw.text((50, 120), description[:60], font=font_small, fill="white")
    draw.text((50, 180), f"⭐ {stars}   🍴 {forks}", font=font_small, fill="white")

    output_path = os.path.join(OUTPUT_DIR, f"{name}-card.png")
    img.save(output_path)

    # --- Add to README section ---
    repo_link = f"https://github.com/{USERNAME}/{name}"
    card_md = f'<a href="{repo_link}">\n  <img src="https://raw.githubusercontent.com/{USERNAME}/{USERNAME}/main/{output_path}" width="400" />\n</a>'

    if i % 2 == 0 or i == len(repos):  # 2 per row
        cards_md.append("<p align=\"center\">\n" + "\n".join(row) + "\n</p>\n")
        row = []

# --- Update README.md ---
if os.path.exists(README_PATH):
    with open(README_PATH, "r", encoding="utf-8") as f:
        readme_content = f.read()
else:
    readme_content = ""

start_marker = "<!-- CARDS-START -->"
end_marker = "<!-- CARDS-END -->"

before = readme_content.split(start_marker)[0]
after = readme_content.split(end_marker)[-1] if end_marker in readme_content else ""

new_cards_section = start_marker + "\n" + "\n".join(cards_md) + "\n" + end_marker
new_readme = before + new_cards_section + after

with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(new_readme)

print("✅ README.md updated with repo cards")
