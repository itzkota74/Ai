import os
import sqlite3
from datetime import datetime

# === DB setup ===
conn = sqlite3.connect('leads.db')
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    timestamp TEXT
)
''')
conn.commit()

# === Mock AI Content Generator ===
def generate_content(prompt):
    # Mocks an AI response without API
    return f"<h2>Affiliate Landing Page for {prompt}</h2><p>Discover top tips and products in {prompt}. Click below!</p>"

# === Landing Page Creation ===
def create_landing_page(niche):
    content = generate_content(niche)
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{niche} Affiliate Page</title>
    </head>
    <body>
        <h1>{niche} Deals & Tips!</h1>
        {content}
        <a href='https://www.example.com/affiliate/{niche.replace(' ','_')}' target='_blank'>Start Now</a>
    </body>
    </html>
    """
    filename = f"{niche.replace(' ','_')}_landing.html"
    with open(filename, "w") as f:
        f.write(html)
    print(f"[+] Landing page generated: {filename}")

# === Mock Lead Collection ===
def collect_lead(name, email):
    c.execute('INSERT INTO leads (name,email,timestamp) VALUES (?,?,?)', (name,email,str(datetime.now())))
    conn.commit()
    print(f"[+] Lead collected: {name} | {email}")

# === Automation Runner ===
niches = ["AI Tools", "Fitness Gadgets", "Crypto Guides"]
for niche in niches:
    create_landing_page(niche)
    collect_lead(f"TestUser_{niche}", f"{niche.lower().replace(' ','')}@example.com")

print("[+] Automation completed successfully")
