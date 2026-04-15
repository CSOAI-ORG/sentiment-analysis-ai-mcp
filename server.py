#!/usr/bin/env python3
"""Sentiment Analysis AI — analyse text sentiment, emotions, and tone at scale. MEOK AI Labs."""
import sys, os
sys.path.insert(0, os.path.expanduser('~/clawd/meok-labs-engine/shared'))
from auth_middleware import check_access

import json
import re
from datetime import datetime, timezone
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

FREE_DAILY_LIMIT = 15
_usage = defaultdict(list)
def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now-t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT: return json.dumps({"error": f"Limit {FREE_DAILY_LIMIT}/day"})
    _usage[c].append(now); return None

# Word lists for rule-based sentiment
_POSITIVE = {"good", "great", "excellent", "amazing", "wonderful", "fantastic", "love", "happy",
             "joy", "brilliant", "outstanding", "perfect", "awesome", "superb", "delightful",
             "pleased", "glad", "thankful", "grateful", "excited", "beautiful", "best", "win"}
_NEGATIVE = {"bad", "terrible", "awful", "horrible", "hate", "sad", "angry", "worst", "poor",
             "disappointing", "frustrated", "annoyed", "upset", "disgusting", "failure", "ugly",
             "painful", "miserable", "broken", "useless", "boring", "dreadful", "pathetic"}
_INTENSIFIERS = {"very", "extremely", "incredibly", "absolutely", "totally", "really", "so"}
_NEGATORS = {"not", "no", "never", "neither", "hardly", "barely", "don't", "doesn't", "didn't", "won't", "can't", "isn't"}

# Emotion keywords
_EMOTIONS = {
    "joy": {"happy", "joy", "delighted", "excited", "cheerful", "glad", "pleased", "elated", "thrilled"},
    "sadness": {"sad", "depressed", "unhappy", "miserable", "heartbroken", "grief", "sorrow", "melancholy"},
    "anger": {"angry", "furious", "rage", "irritated", "annoyed", "frustrated", "mad", "outraged"},
    "fear": {"afraid", "scared", "terrified", "anxious", "worried", "nervous", "panic", "dread"},
    "surprise": {"surprised", "shocked", "amazed", "astonished", "stunned", "unexpected", "wow"},
    "disgust": {"disgusting", "revolting", "gross", "repulsive", "sickening", "nauseating", "vile"},
}


def _score_text(text: str) -> dict:
    """Score a single text and return sentiment analysis."""
    words = re.findall(r'\b\w+\b', text.lower())
    pos_count = 0
    neg_count = 0
    intensity = 1.0
    negation = False
    for i, word in enumerate(words):
        if word in _NEGATORS:
            negation = True
            continue
        if word in _INTENSIFIERS:
            intensity = 1.5
            continue
        if word in _POSITIVE:
            if negation:
                neg_count += intensity
            else:
                pos_count += intensity
            negation = False
            intensity = 1.0
        elif word in _NEGATIVE:
            if negation:
                pos_count += intensity
            else:
                neg_count += intensity
            negation = False
            intensity = 1.0
        else:
            negation = False
            intensity = 1.0
    total = pos_count + neg_count
    if total == 0:
        score = 0.5
        label = "neutral"
    else:
        score = pos_count / total
        if score > 0.6:
            label = "positive"
        elif score < 0.4:
            label = "negative"
        else:
            label = "mixed"
    confidence = min(1.0, total / max(len(words), 1) * 3)
    return {
        "score": round(score, 3),
        "label": label,
        "confidence": round(confidence, 2),
        "positive_signals": int(pos_count),
        "negative_signals": int(neg_count),
        "word_count": len(words),
    }


mcp = FastMCP("sentiment-analysis-ai", instructions="Analyse text sentiment, detect emotions, and compare tones. By MEOK AI Labs.")


@mcp.tool()
def analyze_sentiment(text: str, api_key: str = "") -> str:
    """Analyse the sentiment of a text. Returns score (0-1), label (positive/negative/neutral/mixed), and confidence."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl(): return err
    if not text.strip():
        return json.dumps({"error": "Text cannot be empty"})
    result = _score_text(text)
    result["text_preview"] = text[:100] + ("..." if len(text) > 100 else "")
    result["timestamp"] = datetime.now(timezone.utc).isoformat()
    return json.dumps(result, indent=2)


@mcp.tool()
def batch_analyze(texts: str, api_key: str = "") -> str:
    """Analyse sentiment for multiple texts at once. Provide texts separated by '|||' delimiter."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl(): return err
    items = [t.strip() for t in texts.split("|||") if t.strip()]
    if not items:
        return json.dumps({"error": "No texts provided. Separate multiple texts with '|||'."})
    if len(items) > 50:
        return json.dumps({"error": "Maximum 50 texts per batch"})
    results = []
    for i, text in enumerate(items):
        analysis = _score_text(text)
        analysis["index"] = i
        analysis["text_preview"] = text[:60] + ("..." if len(text) > 60 else "")
        results.append(analysis)
    avg_score = sum(r["score"] for r in results) / len(results)
    labels = defaultdict(int)
    for r in results:
        labels[r["label"]] += 1
    return json.dumps({
        "count": len(results),
        "results": results,
        "summary": {
            "average_score": round(avg_score, 3),
            "overall_label": "positive" if avg_score > 0.6 else "negative" if avg_score < 0.4 else "mixed",
            "label_distribution": dict(labels),
        },
    }, indent=2)


@mcp.tool()
def compare_sentiments(text_a: str, text_b: str, api_key: str = "") -> str:
    """Compare the sentiment of two texts side by side."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl(): return err
    if not text_a.strip() or not text_b.strip():
        return json.dumps({"error": "Both texts must be non-empty"})
    a = _score_text(text_a)
    b = _score_text(text_b)
    diff = a["score"] - b["score"]
    if abs(diff) < 0.1:
        comparison = "Both texts have similar sentiment."
    elif diff > 0:
        comparison = f"Text A is more positive by {abs(diff):.2f} points."
    else:
        comparison = f"Text B is more positive by {abs(diff):.2f} points."
    return json.dumps({
        "text_a": {**a, "preview": text_a[:80] + ("..." if len(text_a) > 80 else "")},
        "text_b": {**b, "preview": text_b[:80] + ("..." if len(text_b) > 80 else "")},
        "score_difference": round(diff, 3),
        "comparison": comparison,
    }, indent=2)


@mcp.tool()
def extract_emotions(text: str, api_key: str = "") -> str:
    """Detect emotions present in text. Returns detected emotions with intensity scores."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl(): return err
    if not text.strip():
        return json.dumps({"error": "Text cannot be empty"})
    words = set(re.findall(r'\b\w+\b', text.lower()))
    detected = {}
    for emotion, keywords in _EMOTIONS.items():
        matches = words & keywords
        if matches:
            detected[emotion] = {
                "intensity": round(len(matches) / max(len(words), 1) * 10, 2),
                "triggers": sorted(matches),
            }
    primary = max(detected.items(), key=lambda x: x[1]["intensity"])[0] if detected else "neutral"
    sentiment = _score_text(text)
    return json.dumps({
        "text_preview": text[:100] + ("..." if len(text) > 100 else ""),
        "primary_emotion": primary,
        "emotions_detected": detected if detected else {"neutral": {"intensity": 1.0, "triggers": []}},
        "sentiment_score": sentiment["score"],
        "sentiment_label": sentiment["label"],
        "word_count": len(words),
    }, indent=2)


if __name__ == "__main__":
    mcp.run()
