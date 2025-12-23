#!/data/data/com.termux/files/usr/bin/bash

# ----------------------------
# Ultra Automated Copilot CLI Setup
# ----------------------------

# 1️⃣ Variables
REPO_SSH="git@github.com:github/copilot-cli.git"
BASE_DIR="$HOME/copilot-cli"

# 2️⃣ Install dependencies
echo "[INFO] Installing required packages..."
pkg update -y
pkg install -y git nodejs python curl

# 3️⃣ Clone the repository
if [ ! -d "$BASE_DIR" ]; then
    echo "[INFO] Cloning Copilot CLI repository..."
    git clone "$REPO_SSH" "$BASE_DIR"
else
    echo "[INFO] Repository already exists, pulling latest changes..."
    cd "$BASE_DIR" || exit
    git pull origin main
fi

# 4️⃣ Navigate into the repo
cd "$BASE_DIR" || exit

# 5️⃣ Install Node.js dependencies
echo "[INFO] Installing Node.js dependencies..."
npm install

# 6️⃣ Optional: Install Python dependencies if required
if [ -f "requirements.txt" ]; then
    echo "[INFO] Installing Python dependencies..."
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
fi

# 7️⃣ Make CLI executable
chmod +x copilot

# 8️⃣ Completion message
echo "✅ Copilot CLI setup complete!"
echo "Run it with: $BASE_DIR/copilot"
