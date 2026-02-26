#!/bin/bash
# AI Conversation Archive Search - Easy Launcher (Mac/Linux)
# Run with: bash START_MAC_LINUX.sh

echo "================================================"
echo "AI Conversation Archive Search"
echo "================================================"
echo ""

# Check if first run
if [ ! -f config.txt ]; then
    echo "FIRST TIME SETUP"
    echo "================"
    echo ""
    read -p "Enter path to your conversation exports: " VAULT_PATH
    echo "$VAULT_PATH" > config.txt
    echo ""
    echo "Installing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo ""
        echo "ERROR: Failed to install dependencies"
        echo "Try running: pip install -r requirements.txt"
        read -p "Press enter to exit"
        exit 1
    fi
    echo ""
    echo "Dependencies installed!"
    echo ""
    echo "Indexing your conversations..."
    python embed_vault.py --index
    if [ $? -ne 0 ]; then
        echo ""
        echo "ERROR: Failed to index conversations"
        echo "Check that VAULT_PATH is correct in embed_vault.py"
        read -p "Press enter to exit"
        exit 1
    fi
    echo ""
    echo "Setup complete!"
    echo ""
fi

# Load vault path
VAULT_PATH=$(cat config.txt)

echo "Starting search daemon..."
echo "Keep this terminal open while using Claude Desktop"
echo ""
echo "Status: RUNNING"
echo "Vault: $VAULT_PATH"
echo ""
echo "Press Ctrl+C to stop"
echo "================================================"
echo ""

python search_daemon.py
