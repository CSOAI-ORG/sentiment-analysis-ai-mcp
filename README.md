<div align="center">

# Sentiment Analysis Ai MCP

**MCP server for sentiment analysis ai mcp operations**

[![PyPI](https://img.shields.io/pypi/v/meok-sentiment-analysis-ai-mcp)](https://pypi.org/project/meok-sentiment-analysis-ai-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Sentiment Analysis Ai MCP provides AI-powered tools via the Model Context Protocol (MCP).

## Tools

| Tool | Description |
|------|-------------|
| `analyze_sentiment` | Analyse the sentiment of a text. Returns score (0-1), label (positive/negative/n |
| `batch_analyze` | Analyse sentiment for multiple texts at once. Provide texts separated by '|||' d |
| `compare_sentiments` | Compare the sentiment of two texts side by side. |
| `extract_emotions` | Detect emotions present in text. Returns detected emotions with intensity scores |

## Installation

```bash
pip install meok-sentiment-analysis-ai-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "sentiment-analysis-ai": {
      "command": "python",
      "args": ["-m", "meok_sentiment_analysis_ai_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 4 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
