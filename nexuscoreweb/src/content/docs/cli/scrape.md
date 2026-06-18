---
title: scrape - Documentation Scraping
description: Scrape documentation websites and convert them into Claude AI skills with automatic categorization and code detection
section: cli
order: 2
---

# scrape - Documentation Scraping

Scrape documentation websites and convert them into AI skills.

## Basic Usage

```bash
nexus-core scrape [OPTIONS]
```

## Quick Examples

```bash
# Use preset config (easiest)
nexus-core scrape --config configs/react.json

# Quick scrape without config
nexus-core scrape --url https://react.dev --name react

# Interactive mode
nexus-core scrape --interactive

# With async mode (3x faster)
nexus-core scrape --config configs/godot.json --async --workers 8
```

## Options

### Required (choose one)

- `--config CONFIG` - Load configuration from file
- `--url URL` - Base documentation URL (with --name)
- `--interactive, -i` - Interactive configuration wizard

### Optional

- `--name NAME` - Skill name
- `--description DESC` - Skill description
- `--max-pages N` - Maximum pages to scrape
- `--skip-scrape` - Skip scraping, use cached data
- `--dry-run` - Preview without actually scraping
- `--async` - Enable async mode (3x faster)
- `--workers N` - Number of parallel workers (default: 4)
- `--enhance` - Enhance with Claude API after scraping
- `--enhance-local` - Enhance with Claude Code (free)

## Preset Configs

Nexus Core includes 24+ ready-to-use configurations:

```bash
# Game Engines
nexus-core scrape --config configs/godot.json
nexus-core scrape --config configs/unity.json

# Web Frameworks
nexus-core scrape --config configs/react.json
nexus-core scrape --config configs/vue.json
nexus-core scrape --config configs/django.json
nexus-core scrape --config configs/fastapi.json

# And 18+ more...
```

## Output Structure

```
output/
├── {name}_data/              # Cached scraped data
│   ├── pages/
│   │   ├── page_0.json
│   │   └── ...
│   └── summary.json
│
└── {name}/                   # Built skill
    ├── SKILL.md             # Main skill file
    ├── references/          # Categorized docs
    │   ├── index.md
    │   ├── getting_started.md
    │   ├── api.md
    │   └── ...
    ├── scripts/
    └── assets/
```

## Advanced Usage

### Custom Config File

```json
{
  "name": "myframework",
  "base_url": "https://docs.myframework.com/",
  "description": "My framework documentation",
  "start_urls": [
    "https://docs.myframework.com/getting-started",
    "https://docs.myframework.com/api"
  ],
  "selectors": {
    "main_content": "article",
    "title": "h1",
    "code_blocks": "pre code"
  },
  "url_patterns": {
    "include": ["/docs/", "/api/"],
    "exclude": ["/blog/", "/community/"]
  },
  "categories": {
    "getting_started": ["intro", "tutorial", "quickstart"],
    "api": ["reference", "api"],
    "guides": ["guide", "how-to"]
  },
  "rate_limit": 0.5,
  "max_pages": 300
}
```

### With Enhancement

```bash
# Local enhancement (free, uses Claude Code)
nexus-core scrape --config configs/react.json --enhance-local

# API enhancement (requires ANTHROPIC_API_KEY)
export ANTHROPIC_API_KEY=sk-ant-...
nexus-core scrape --config configs/react.json --enhance
```

### Async Mode

```bash
# 3x faster with async mode
nexus-core scrape --config configs/godot.json --async --workers 8

# Adjust workers based on CPU cores
nexus-core scrape --config configs/react.json --async --workers 16
```

## Features

- ✅ **llms.txt Support** - Automatically detects and uses LLM-ready docs (10x faster)
- ✅ **Smart Categorization** - Organizes content by topic
- ✅ **Code Detection** - Recognizes 20+ programming languages
- ✅ **Async Scraping** - 3x faster with parallel workers
- ✅ **Intelligent Caching** - 50% faster on re-runs

## Time Estimates

- Small site (50 pages): 2-5 minutes
- Medium site (200 pages): 10-20 minutes
- Large site (500 pages): 30-40 minutes
- With async: ~3x faster

## Next Steps

- [Enhance Command](/docs/cli/enhance) - AI-enhance your skills
- [Package Command](/docs/cli/package) - Package for platforms
- [Usage Guide](/docs/guides/usage) - Complete usage guide
