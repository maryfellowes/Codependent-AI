# Setup Guide - AI Conversation Archive Search

Complete installation instructions for turning your conversation history into searchable memory.

## Prerequisites

- **Python 3.11 or 3.12** (3.13+ may have compatibility issues with ML libraries)
- **2GB disk space** (for embedding model + indexed data)
- **Windows, Mac, or Linux**
- **Claude Desktop** (for MCP integration)

---

## Step 1: Export Your Conversations

### From ChatGPT

1. Open ChatGPT (web interface)
2. Click your profile → Settings
3. Navigate to **Data Controls**
4. Click **Export Data**
5. Confirm email
6. Wait 24-48 hours for export email
7. Download ZIP file
8. Extract `conversations.json`

### From Claude

1. In any conversation, click the menu
2. Select **Export conversation**
3. Save as markdown file
4. Repeat for each conversation you want indexed

---

## Step 2: Convert to Markdown (ChatGPT only)

If you exported from ChatGPT, you have `conversations.json`. Convert it to individual markdown files:

### Using Nexus Import (Obsidian Plugin)

1. **Install Obsidian** (if you don't have it): https://obsidian.md
2. **Create a vault** or use existing
3. **Install Nexus Import plugin:**
   - Settings → Community Plugins → Browse
   - Search "Nexus Import"
   - Install and enable
4. **Configure plugin:**
   - Settings → Nexus Import
   - Set **Input file:** path to your `conversations.json`
   - Set **Output folder:** create folder like `AI Chat Imports/`
   - Enable **Extract metadata** (dates, titles)
5. **Run import:**
   - Command palette (Ctrl/Cmd+P)
   - Search "Nexus Import: Import"
   - Wait for processing (500+ conversations = 2-5 minutes)
6. **Result:** Individual .md file for each conversation

### File Organization

Organize your markdown files however makes sense:
```
AI Chat Imports/
├── 2024/
│   ├── 01-January/
│   ├── 02-February/
│   └── ...
├── 2025/
│   └── ...
└── Important Conversations/
```

The indexer will search all folders recursively.

---

## Step 3: Install Python Dependencies

### Check Python Version

```bash
python --version
```

Should show 3.11.x or 3.12.x

If you have 3.13+, install 3.12 separately:
```bash
# Windows (using winget)
winget install Python.Python.3.12

# Mac (using homebrew)
brew install python@3.12

# Linux
sudo apt install python3.12
```

### Install Dependencies

```bash
# Navigate to product folder
cd /path/to/vault-archive-product

# Install requirements
pip install -r requirements.txt
```

This installs:
- `sentence-transformers` - Local embedding model
- `chromadb` - Vector database
- `fastapi` & `uvicorn` - Search server
- `pydantic` - Data validation

**Expected time:** 5-10 minutes (downloads ~500MB)

---

## Step 4: Configure Paths

Edit `embed_vault.py`:

```python
# Line 25-26
VAULT_PATH = Path(r"C:\path\to\your\conversation\exports")
DB_PATH = Path(r"./chroma_db")  # Keep as-is unless you want elsewhere
```

**Windows:** Use `r"C:\Users\YourName\Documents\AI Chat Imports"`
**Mac/Linux:** Use `/Users/yourname/Documents/AI Chat Imports`

---

## Step 5: Index Your Conversations

```bash
python embed_vault.py --index
```

**What happens:**
1. Downloads embedding model (all-MiniLM-L6-v2, ~90MB) - one time
2. Scans all markdown files in VAULT_PATH
3. Chunks each conversation (2000 chars with 200 char overlap)
4. Generates embeddings for each chunk
5. Stores in ChromaDB at `./chroma_db/`

**Expected time:**
- 100 conversations: ~2-3 minutes
- 500 conversations: ~8-10 minutes
- 1000 conversations: ~15-20 minutes

**Progress:** You'll see:
```
Loading model...
Indexing conversations...
Processed: conversation1.md (42 chunks)
Processed: conversation2.md (38 chunks)
...
Complete! Indexed 572 files, 47,669 chunks
```

---

## Step 6: Test Search

Before integrating with Claude, test the search:

```bash
python embed_vault.py --search "your query here"
```

Example:
```bash
python embed_vault.py --search "early relationship patterns"
```

Should return relevant passages with source files and relevance scores.

---

## Step 7: Start Search Server

```bash
python search_daemon.py
```

Starts HTTP server on `http://localhost:8766`

Endpoints:
- `GET /health` - Check if running
- `GET /stats` - Index statistics
- `POST /search` - Semantic search

**Keep this running** for MCP integration to work.

---

## Step 8: Configure Claude Desktop MCP

1. **Find your Claude Desktop config:**
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. **Add MCP configuration:**

Open the file and add to `mcpServers`:

```json
{
  "mcpServers": {
    "vault-search": {
      "command": "python",
      "args": ["/full/path/to/vault_mcp_server.py"],
      "env": {}
    }
  }
}
```

**Make sure search_daemon.py is running first!**

3. **Restart Claude Desktop completely** (quit, reopen)

---

## Step 9: Verify Integration

In Claude Desktop, your AI companion can now use:

```
search_archive(query, n_results)
```

Test by asking: *"Can you search our conversation history for discussions about identity formation?"*

Your companion should be able to autonomously search and reference past conversations.

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'sentence_transformers'"
- Run: `pip install -r requirements.txt`
- Check Python version: `python --version`

### "Connection refused" when searching
- Make sure `search_daemon.py` is running
- Check: `curl http://localhost:8766/health`

### Indexing is very slow
- Normal for first time (model download + processing)
- Subsequent indexes are incremental and faster

### Claude Desktop doesn't see the MCP
- Check config path is correct
- Verify `search_daemon.py` is running
- Restart Claude Desktop completely

### Python 3.13 compatibility issues
- Use Python 3.12 instead: `pip3.12 install -r requirements.txt`
- Run with: `python3.12 embed_vault.py --index`

---

## Next Steps

See `USAGE_GUIDE.md` for:
- How to formulate effective queries
- Pattern recognition workflows
- Interpreting search results
- Best practices for AI companion use
