import requests
from PIL import Image, ImageDraw, ImageFont
import os, re

USERNAME = "Bismay-exe"
ASSETS_DIR = "assets/generated"
CARD_TEMPLATE = "assets/card.png"
README_FILE = "README.md"

# Create output folder
os.makedirs(ASSETS_DIR, exist_ok=True)

# Fetch repos (public only)
repos = requests.get(
    f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=updated"
).json()

cards_md = []

for repo in repos:
    repo_name = repo["name"]
    repo_desc = repo["description"] or ""
    repo_link = repo["html_url"]

    # Open card background
    card = Image.open(CARD_TEMPLATE).convert("RGBA")
    draw = ImageDraw.Draw(card)

    try:
        font_title = ImageFont.truetype("arial.ttf", 28)
        font_desc = ImageFont.truetype("arial.ttf", 18)
    except:
        font_title = ImageFont.load_default()
        font_desc = ImageFont.load_default()

    # Write repo name + description
    draw.text((40, 40), repo_name, font=font_title, fill="white")
    draw.text((40, 90), repo_desc[:80], font=font_desc, fill="white")

    # Save card
    output_path = f"{ASSETS_DIR}/{repo_name}-card.png"
    card.save(output_path)

    # Markdown entry (relative path works in GitHub README)
    card_md = (
        f'<a href="{repo_link}">\n'
        f'  <img src="./{output_path}" width="400" />\n'
        f'</a>'
    )
    cards_md.append(card_md)

# Group cards into rows of 2
rows = []
for i in range(0, len(cards_md), 2):
    rows.append("<p align='center'>\n" + "\n".join(cards_md[i:i+2]) + "\n</p>")

new_cards_section = (
    "<!-- CARDS-START -->\n" + "\n\n".join(rows) + "\n<!-- CARDS-END -->"
)

# Read README
with open(README_FILE, "r", encoding="utf-8") as f:
    readme_content = f.read()

# Replace existing section or append if missing
if re.search(r"<!-- CARDS-START -->.*<!-- CARDS-END -->", readme_content, flags=re.S):
    new_readme = re.sub(
        r"<!-- CARDS-START -->.*<!-- CARDS-END -->",
        new_cards_section,
        readme_content,
        flags=re.S,
    )
else:
    new_readme = readme_content.strip() + "\n\n" + new_cards_section

# Write updated README
with open(README_FILE, "w", encoding="utf-8") as f:
    f.write(new_readme)

print("✅ README.md updated with repo cards")
