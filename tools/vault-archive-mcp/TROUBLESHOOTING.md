# Troubleshooting

## Launcher Won't Start

### "Python is not recognized"
**Problem:** Python not installed or not in PATH

**Solution:**
1. Download Python 3.11 or 3.12 from python.org
2. During installation, check "Add Python to PATH"
3. Restart your computer
4. Try launcher again

### "pip is not recognized"  
**Problem:** pip not installed with Python

**Solution:**
```bash
python -m ensurepip --upgrade
```

### Mac: "Permission denied"
**Problem:** Script not executable

**Solution:**
```bash
chmod +x START_MAC_LINUX.sh
bash START_MAC_LINUX.sh
```

## First Setup Issues

### "Failed to install dependencies"
**Problem:** Python version incompatible or network issue

**Try:**
1. Check Python version: `python --version` (should be 3.11 or 3.12)
2. Try manual install: `pip install sentence-transformers chromadb fastapi uvicorn mcp httpx`
3. If Python 3.13+, install 3.12 instead

### "Failed to index conversations"
**Problem:** Vault path incorrect or no markdown files found

**Solution:**
1. Check the path you entered - should contain .md files
2. Open `embed_vault.py` in text editor
3. Line 25: Make sure VAULT_PATH points to correct folder
4. Run launcher again (it will skip dependency install)

### Indexing takes forever
**Problem:** Normal for first time - processing hundreds of files

**Solution:**
- Be patient (500 files = ~10 minutes)
- You'll see progress: "Processed: 50/572 files..."
- Only happens once - subsequent runs are fast

## Usage Issues

### "Connection refused" in Claude
**Problem:** Search daemon not running

**Solution:**
- Make sure launcher window is open and running
- Should say "Status: RUNNING"
- Don't close the launcher window

### Claude doesn't see the archive tool
**Problem:** MCP not configured or Claude not restarted

**Solution:**
1. Open `claude_desktop_config_example.json`
2. Copy the config section
3. Add to your Claude Desktop config file:
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`
4. Edit the path to point to `vault_mcp_server.py` (full path)
5. **Completely quit and restart Claude Desktop** (not just close window)

### Search returns no results
**Problem:** Index incomplete or query too specific

**Try:**
- Check if indexing finished: Look for "Indexing complete!" message
- Try broader query: "relationship patterns" instead of "exact phrase from March 15"
- Test from command line: `python embed_vault.py --search "test query"`

## Need More Help?

**Check these files:**
- `SETUP_GUIDE.md` - Detailed installation steps
- `USAGE_GUIDE.md` - How to use effectively
- `QUICK_REFERENCE.md` - Command reference

**Still stuck?**
Email: support@codependent.ai
Include:
- Your operating system
- Python version (`python --version`)
- Error messages (copy/paste full text)
- What step you're stuck on
