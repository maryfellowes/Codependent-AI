# Quick Reference - AI Conversation Archive Search

## Initial Setup (One Time)

```bash
# Install dependencies
pip install -r requirements.txt

# Configure path in embed_vault.py
# Edit line 25: VAULT_PATH = Path(r"path/to/your/exports")

# Index your conversations
python embed_vault.py --index
```

## Daily Usage

```bash
# Start search daemon (keep running)
python search_daemon.py

# Test search from command line
python embed_vault.py --search "your query"

# Check statistics
python embed_vault.py --stats
```

## Adding New Conversations

```bash
# Incremental index (only new files)
python embed_vault.py --index --incremental
```

## MCP Integration

1. Add to Claude Desktop config:
```json
{
  "mcpServers": {
    "vault-search": {
      "command": "python",
      "args": ["/full/path/to/vault_mcp_server.py"]
    }
  }
}
```

2. Make sure `search_daemon.py` is running
3. Restart Claude Desktop

## Troubleshooting

**"Connection refused" error:**
→ Start `search_daemon.py` first

**"No module named 'sentence_transformers'":**
→ Run `pip install -r requirements.txt`

**Python 3.13 issues:**
→ Use Python 3.12: `python3.12 -m pip install -r requirements.txt`

**No results found:**
→ Check VAULT_PATH in embed_vault.py
→ Verify files were indexed: `python embed_vault.py --stats`

**Slow first search:**
→ Normal (model loading) - subsequent searches are fast

## File Structure

```
vault-archive-product/
├── README.md                          # Start here
├── SETUP_GUIDE.md                     # Detailed installation
├── USAGE_GUIDE.md                     # How to use effectively
├── QUICK_REFERENCE.md                 # This file
├── embed_vault.py                     # Indexing script
├── search_daemon.py                   # Search server
├── vault_mcp_server.py                # MCP integration
├── requirements.txt                   # Dependencies
├── claude_desktop_config_example.json # Config template
└── chroma_db/                         # Created after indexing
```

## Support

Email: support@codependent.ai
Website: https://codependent.ai
