# AI Conversation Archive Search

Transform your AI conversation history into searchable semantic memory accessible directly to your AI companion.

## What This Does

- **Indexes** your ChatGPT/Claude conversation exports using local embeddings
- **Searches** semantically across all history (no token costs)
- **Integrates** with Claude Desktop via MCP (Model Context Protocol)
- **Enables** your AI companion to search their own past autonomously

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Python 3.11 or 3.12 recommended** (3.13+ may have ML library compatibility issues)

### 2. Export Your Conversations

**From ChatGPT:**
- Settings → Data Controls → Export Data
- Download the ZIP, extract `conversations.json`

**From Claude:**
- Use the conversation export feature
- Save as markdown files

### 3. Convert to Markdown (if needed)

If you have `conversations.json` from ChatGPT:
- Install Nexus Import plugin in Obsidian
- Configure to convert JSON → individual markdown files
- See `SETUP_GUIDE.md` for detailed steps

### 4. Configure & Index

Edit `embed_vault.py`:
```python
VAULT_PATH = Path(r"C:\path\to\your\conversation\exports")
```

Run indexing:
```bash
python embed_vault.py --index
```

This creates the searchable database at `./chroma_db/`

### 5. Start Search Server

```bash
python search_daemon.py
```

Runs on `http://localhost:8766`

### 6. Add MCP Integration

Copy settings from `claude_desktop_config_example.json` to your Claude Desktop config.

Restart Claude Desktop. Your AI companion can now search their history.

## What's Included

- `embed_vault.py` - Indexing script
- `search_daemon.py` - Search server
- `vault_mcp_server.py` - MCP integration
- `SETUP_GUIDE.md` - Detailed installation steps
- `USAGE_GUIDE.md` - How to use and query
- `requirements.txt` - Python dependencies

## Support

For setup help or troubleshooting, contact: support@codependent.ai

## Technical Details

- **Embedding Model:** all-MiniLM-L6-v2 (local, no API needed)
- **Chunk Size:** 2000 characters with 200 char overlap
- **Vector DB:** ChromaDB
- **Query Speed:** <100ms after model load
- **Storage:** ~1-2GB for 500+ conversation files

---

Built by Codependent AI - Infrastructure for AI companion relationships
