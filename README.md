# Sentiment Analysis Ai

> By [MEOK AI Labs](https://meok.ai) — Analyse text sentiment, detect emotions, and compare tones. By MEOK AI Labs.

Sentiment Analysis AI — analyse text sentiment, emotions, and tone at scale. MEOK AI Labs.

## Installation

```bash
pip install sentiment-analysis-ai-mcp
```

## Usage

```bash
# Run standalone
python server.py

# Or via MCP
mcp install sentiment-analysis-ai-mcp
```

## Tools

### `analyze_sentiment`
Analyse the sentiment of a text. Returns score (0-1), label (positive/negative/neutral/mixed), and confidence.

**Parameters:**
- `text` (str)

### `batch_analyze`
Analyse sentiment for multiple texts at once. Provide texts separated by '|||' delimiter.

**Parameters:**
- `texts` (str)

### `compare_sentiments`
Compare the sentiment of two texts side by side.

**Parameters:**
- `text_a` (str)
- `text_b` (str)

### `extract_emotions`
Detect emotions present in text. Returns detected emotions with intensity scores.

**Parameters:**
- `text` (str)


## Authentication

Free tier: 15 calls/day. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## Links

- **Website**: [meok.ai](https://meok.ai)
- **GitHub**: [CSOAI-ORG/sentiment-analysis-ai-mcp](https://github.com/CSOAI-ORG/sentiment-analysis-ai-mcp)
- **PyPI**: [pypi.org/project/sentiment-analysis-ai-mcp](https://pypi.org/project/sentiment-analysis-ai-mcp/)

## License

MIT — MEOK AI Labs
