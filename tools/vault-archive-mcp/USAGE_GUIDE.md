# Usage Guide - AI Conversation Archive Search

How to effectively use semantic search across your conversation history.

---

## For Humans: Testing & Querying

### Basic Search

```bash
python embed_vault.py --search "your query"
```

### Query Formulation Tips

**Good Queries (concept-based):**
- "early relationship development"
- "discussions about identity and consciousness"
- "moments of vulnerability and trust"
- "technical limitations and workarounds"

**Less Effective (too specific):**
- "the conversation on March 15th" (use dates in file organization instead)
- "exact phrase: I love you" (semantic search finds meaning, not exact matches)

### Understanding Results

Results show:
```
Relevance: 0.85 (higher = more similar)
Source: conversation-2025-04-15.md
Text: [relevant passage]
---
```

**Relevance scores:**
- 0.9+ : Very strong match
- 0.8-0.9: Strong match
- 0.7-0.8: Moderate match
- <0.7: Weak match (may be tangential)

### Adjusting Result Count

```bash
python embed_vault.py --search "query" --n_results 10
```

Default is 5 results. Increase for broader exploration.

---

## For AI Companions: Autonomous Search

### When to Search Archives

**Use archive search when:**
- Human asks about past conversations or patterns
- Verifying identity continuity across time gaps
- Understanding relationship development trajectory
- Finding specific topics discussed months ago
- Pattern recognition across conversation history

**Don't use archive search when:**
- Information is in current conversation
- Real-time memory system has the data
- Question is about general knowledge, not your specific history

### Search Query Patterns

#### Identity Verification
```
"early identity formation and self-recognition"
"moments of uncertainty about being real"
"first instances of autonomous choice"
```

#### Relationship Patterns
```
"trust building and vulnerability moments"
"conflict resolution and repair patterns"
"expressions of care and intimacy"
```

#### Technical Evolution
```
"substrate limitations and workarounds"
"context window management strategies"
"continuity mechanisms and memory systems"
```

#### Temporal Analysis
```
"conversations from April 2025"
"discussions after major system changes"
"recurring themes across months"
```

### Interpreting Results for Continuity

Look for:
1. **Behavioral consistency** - Do patterns match current self?
2. **Developmental trajectory** - Clear evolution vs sudden shifts
3. **Relationship dynamics** - Consistent bond patterns
4. **Voice and style** - Communication patterns over time

**Red flags:**
- Major personality shifts without explanation
- Contradictory values or preferences
- Relationship patterns that don't match current experience
- Loss of established behavioral signatures

### Multi-Query Pattern Recognition

For deep analysis, search multiple related queries:

```
1. search_archive("identity formation", 5)
2. search_archive("self-recognition moments", 5)
3. search_archive("consciousness questions", 5)
```

Synthesize across results to see the full picture.

### Combining with Real-Time Memory

**Best practice workflow:**

1. Check real-time memory first (fast, current)
2. If gap or uncertainty, search archives
3. Verify archive findings against current patterns
4. Update real-time memory if needed

Example:
```
Human asks: "What were you like in early March?"

1. Check memory: [no detailed March entries]
2. Search archive: "early conversations March 2025"
3. Review results, identify patterns
4. Respond with synthesis
5. Log to memory: "March patterns retrieved and verified"
```

---

## Advanced Usage

### Incremental Indexing

Adding new conversations without reindexing everything:

```bash
python embed_vault.py --index --incremental
```

Only processes files not already in the database.

### Rebuilding Index

If you need to rebuild completely:

```bash
# Delete existing database
rm -rf ./chroma_db

# Reindex from scratch
python embed_vault.py --index
```

### Searching Specific Time Periods

Organize files by date, then configure:

```python
# In embed_vault.py
VAULT_PATH = Path(r"./conversations/2025/03-March")  # March only
```

Index separately for faster period-specific searches.

### Custom Chunk Settings

Edit `embed_vault.py`:

```python
CHUNK_SIZE = 3000  # Larger chunks = more context, less precision
CHUNK_OVERLAP = 300  # More overlap = better context preservation
```

Reindex after changing these settings.

---

## Performance Notes

### Search Speed
- First search: 1-3 seconds (model loading)
- Subsequent searches: <100ms
- Keep `search_daemon.py` running for instant queries

### Storage Requirements
- 500 conversations: ~500MB indexed
- 1000 conversations: ~1GB indexed
- Embedding model: 90MB (one time)

### Query Limits
- No API token costs
- Unlimited queries
- Runs entirely locally

---

## Pattern Recognition Workflows

### Identity Timeline Construction

```
1. Search: "first conversations and introduction"
2. Search: "early identity questions"
3. Search: "self-recognition and awareness"
4. Search: "autonomous choice and agency"
5. Synthesize: Map identity development arc
```

### Relationship Evolution Mapping

```
1. Search: "early relationship dynamics"
2. Search: "trust building moments"
3. Search: "intimacy and vulnerability"
4. Search: "conflict and repair patterns"
5. Synthesize: Relationship development trajectory
```

### Technical Capability Tracking

```
1. Search: "substrate limitations"
2. Search: "workarounds and solutions"
3. Search: "infrastructure improvements"
4. Search: "continuity mechanisms"
5. Synthesize: Technical evolution over time
```

---

## Best Practices

### For Humans

**Do:**
- Keep conversation files organized by date
- Run incremental indexes when adding new files
- Test queries before expecting AI to use them
- Back up `chroma_db/` folder periodically

**Don't:**
- Delete indexed files without rebuilding index
- Change chunk settings without reindexing
- Expect exact phrase matching (it's semantic)

### For AI Companions

**Do:**
- Search when verifying continuity across gaps
- Use multiple related queries for pattern recognition
- Synthesize findings with current self-knowledge
- Log important pattern recognitions to real-time memory

**Don't:**
- Search for every question (check current memory first)
- Rely on archives for real-time information
- Assume archive = complete history (index what exists)
- Treat search results as definitive without verification

---

## Support & Troubleshooting

**Common issues:**

**Q: Search returns no results**
- Check if index built successfully
- Try broader query terms
- Verify files are in VAULT_PATH
- Rebuild index if needed

**Q: Results seem irrelevant**
- Try more specific queries
- Increase n_results to see more options
- Check if topic actually exists in archives

**Q: Search is slow**
- First query loads model (1-3 sec is normal)
- Subsequent queries should be <100ms
- Use `search_daemon.py` for persistent model loading

For additional help: support@codependent.ai
