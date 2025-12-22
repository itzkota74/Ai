import os, sqlite3, datetime

# Database setup
conn = sqlite3.connect('automation/db.sqlite')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    timestamp TEXT
)''')
conn.commit()

# Mock AI generator
def generate_content(prompt):
    return f"<h2>AI Generated Content for {prompt}</h2><p>Discover top products, guides, and tools in {prompt}. Click the affiliate link below!</p>"

# Landing page generator
def create_landing_page(niche):
    content = generate_content(niche)
    html = f"""
    <html><head><title>{niche} Deals</title></head>
    <body>
        <h1>{niche} Deals & Tips!</h1>
        {content}
        <a href='https://www.example.com/affiliate/{niche.replace(' ','_')}' target='_blank'>Start Now</a>
    </body></html>
    """
    filename = f"automation/{niche.replace(' ','_')}_landing.html"
    with open(filename, 'w') as f:
        f.write(html)
    print(f"[+] Landing page created: {filename}")

# Lead collector
def collect_lead(name, email):
    c.execute('INSERT INTO leads (name,email,timestamp) VALUES (?,?,?)', (name,email,str(datetime.datetime.now())))
    conn.commit()
    print(f"[+] Lead collected: {name} | {email}")

# Run automation
niches = ["AI Tools", "Fitness Gadgets", "Crypto Guides", "NFT Tips", "Micro SaaS Tools"]
for niche in niches:
    create_landing_page(niche)
    collect_lead(f"TestUser_{niche}", f"{niche.lower().replace(' ','')}@example.com")

print("[+] Automation run complete.")
