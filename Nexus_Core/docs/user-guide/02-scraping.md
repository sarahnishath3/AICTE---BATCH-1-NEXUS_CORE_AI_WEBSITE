# Scraping Guide

> **Nexus Core v3.6.0**
> **Complete guide to all scraping options**

---

## Overview

Nexus Core can extract knowledge from **17 types of sources**:

| Source | Command | Best For |
|--------|---------|----------|
| **Documentation** | `create <url>` | Web docs, tutorials, API refs |
| **GitHub** | `create <repo>` | Source code, issues, releases |
| **PDF** | `create <file.pdf>` | Manuals, papers, reports |
| **Local** | `create <./path>` | Your projects, internal code |
| **Word** | `create <file.docx>` | Reports, specifications |
| **EPUB** | `create <file.epub>` | E-books, long-form docs |
| **Video** | `create <url/file>` | Tutorials, presentations |
| **Jupyter** | `create <file.ipynb>` | Data science, experiments |
| **Local HTML** | `create <file.html>` | Offline docs, saved pages |
| **OpenAPI** | `create <spec.yaml>` | API specs, Swagger docs |
| **AsciiDoc** | `create <file.adoc>` | Technical documentation |
| **PowerPoint** | `create <file.pptx>` | Slide decks, presentations |
| **RSS/Atom** | `create <feed.rss>` | Blog feeds, news sources |
| **Man Pages** | `create <cmd.1>` | Unix command documentation |
| **Confluence** | `confluence` | Team wikis, knowledge bases |
| **Notion** | `notion` | Workspace docs, databases |
| **Slack/Discord** | `chat` | Chat history, discussions |

---

## Documentation Scraping

### Basic Usage

```bash
# Auto-detect and scrape
nexus-core create https://docs.react.dev/

# With custom name
nexus-core create https://docs.react.dev/ --name react-docs

# With description
nexus-core create https://docs.react.dev/ \
  --description "React JavaScript library documentation"
```

### Using Preset Configs

```bash
# List available presets
nexus-core estimate --all

# Use preset
nexus-core create --config react
nexus-core create --config django
nexus-core create --config fastapi
```

**Available presets:** See `configs/` directory in repository.

### Custom Configuration

All configs must use the unified format with a `sources` array (since v2.11.0):

```bash
# Create config file
cat > configs/my-docs.json << 'EOF'
{
  "name": "my-framework",
  "description": "My framework documentation",
  "sources": [
    {
      "type": "documentation",
      "base_url": "https://docs.example.com/",
      "max_pages": 200,
      "rate_limit": 0.5,
      "selectors": {
        "main_content": "article",
        "title": "h1"
      },
      "url_patterns": {
        "include": ["/docs/", "/api/"],
        "exclude": ["/blog/", "/search"]
      }
    }
  ]
}
EOF

# Use config
nexus-core create --config configs/my-docs.json
```

> **Note:** Omit `main_content` from `selectors` to let Nexus Core auto-detect
> the best content element (`main`, `article`, `div[role="main"]`, etc.).

See [Config Format](../reference/CONFIG_FORMAT.md) for all options.

### Advanced Options

```bash
# Limit pages (for testing)
nexus-core create <url> --max-pages 50

# Adjust rate limit
nexus-core create <url> --rate-limit 1.0

# Parallel workers (faster)
nexus-core create <url> --workers 5 --async

# Dry run (preview)
nexus-core create <url> --dry-run

# Resume interrupted
nexus-core create <url> --resume

# Fresh start (ignore cache)
nexus-core create <url> --fresh
```

---

## GitHub Repository Scraping

### Basic Usage

```bash
# By repo name
nexus-core create facebook/react

# With explicit flag
nexus-core create  facebook/react

# With custom name
nexus-core create  facebook/react --name react-source
```

### With GitHub Token

```bash
# Set token for higher rate limits
export GITHUB_TOKEN=ghp_...

# Use token
nexus-core create  facebook/react
```

**Benefits of token:**
- 5000 requests/hour vs 60
- Access to private repos
- Higher GraphQL limits

### What Gets Extracted

| Data | Default | Flag to Disable |
|------|---------|-----------------|
| Source code | ✅ | `--scrape-only` |
| README | ✅ | - |
| Issues | ✅ | `--no-issues` |
| Releases | ✅ | `--no-releases` |
| Changelog | ✅ | `--no-changelog` |

### Control What to Fetch

```bash
# Skip issues (faster)
nexus-core create  facebook/react --no-issues

# Limit issues
nexus-core create  facebook/react --max-issues 50

# Scrape only (no build)
nexus-core create  facebook/react --scrape-only

# Non-interactive (CI/CD)
nexus-core create  facebook/react --non-interactive
```

---

## PDF Extraction

### Basic Usage

```bash
# Direct file
nexus-core create manual.pdf --name product-manual

# With explicit command
nexus-core create --pdf manual.pdf --name docs
```

### OCR for Scanned PDFs

```bash
# Enable OCR
nexus-core create --pdf scanned.pdf --ocr
```

**Requirements:**
```bash
pip install nexus-core[pdf-ocr]
# Also requires: tesseract-ocr (system package)
```

### Password-Protected PDFs

```bash
# In config file
{
  "name": "secure-docs",
  "pdf_path": "protected.pdf",
  "password": "secret123"
}
```

### Page Range

```bash
# Extract specific pages (via config)
{
  "pdf_path": "manual.pdf",
  "page_range": [1, 100]
}
```

---

## Local Codebase Analysis

### Basic Usage

```bash
# Current directory
nexus-core create .

# Specific directory
nexus-core create ./my-project

# With explicit command
nexus-core create ./my-project
```

### Analysis Presets

```bash
# Quick analysis (1-2 min)
nexus-core create ./my-project --preset quick

# Standard analysis (5-10 min) - default
nexus-core create ./my-project --preset standard

# Comprehensive (20-60 min)
nexus-core create ./my-project --preset comprehensive
```

### What Gets Analyzed

| Feature | Quick | Standard | Comprehensive |
|---------|-------|----------|---------------|
| Code structure | ✅ | ✅ | ✅ |
| API extraction | ✅ | ✅ | ✅ |
| Comments | - | ✅ | ✅ |
| Patterns | - | ✅ | ✅ |
| Test examples | - | - | ✅ |
| How-to guides | - | - | ✅ |
| Config patterns | - | - | ✅ |

### Language Filtering

```bash
# Specific languages
nexus-core create ./my-project \
  --languages Python,JavaScript

# File patterns
nexus-core create ./my-project \
  --file-patterns "*.py,*.js"
```

### Skip Features

```bash
# Skip heavy features
nexus-core create ./my-project \
  --skip-dependency-graph \
  --skip-patterns \
  --skip-test-examples
```

---

## Video Extraction

### Basic Usage

```bash
# YouTube video
nexus-core create https://www.youtube.com/watch?v=dQw4w9WgXcQ

# Local video file
nexus-core create presentation.mp4

# With explicit command
nexus-core create --video-url  https://www.youtube.com/watch?v=...
```

### Visual Analysis

```bash
# Install full video support (includes Whisper + scene detection)
pip install nexus-core[video-full]
nexus-core create --setup  # auto-detect GPU and install PyTorch

# Extract with visual analysis
nexus-core create --video-url <url> --visual
```

**Requirements:**
```bash
pip install nexus-core[video]        # Transcript only
pip install nexus-core[video-full]   # + Whisper, scene detection
```

---

## Word Document Extraction

### Basic Usage

```bash
# Extract from .docx
nexus-core create report.docx --name project-report

# With explicit command
nexus-core create report.docx
```

**Handles:** Text, tables, headings, images, embedded metadata.

---

## EPUB Extraction

### Basic Usage

```bash
# Extract from .epub
nexus-core create programming-guide.epub --name guide

# With explicit command
nexus-core create programming-guide.epub
```

**Handles:** Chapters, metadata, table of contents, embedded images.

---

## Jupyter Notebook Extraction

### Basic Usage

```bash
# Extract from .ipynb
nexus-core create analysis.ipynb --name data-analysis

# With explicit command
nexus-core create analysis.ipynb
```

**Requirements:**
```bash
pip install nexus-core[jupyter]
```

**Extracts:** Markdown cells, code cells, cell outputs, execution order.

---

## Local HTML Extraction

### Basic Usage

```bash
# Extract from .html
nexus-core create docs.html --name offline-docs

# With explicit command
nexus-core create docs.html
```

**Handles:** Full HTML parsing, text extraction, link resolution.

---

## OpenAPI/Swagger Extraction

### Basic Usage

```bash
# Extract from OpenAPI spec
nexus-core create api-spec.yaml --name my-api

# With explicit command
nexus-core create api-spec.yaml
```

**Extracts:** Endpoints, request/response schemas, authentication info, examples.

---

## AsciiDoc Extraction

### Basic Usage

```bash
# Extract from .adoc
nexus-core create guide.adoc --name dev-guide

# With explicit command
nexus-core create guide.adoc
```

**Requirements:**
```bash
pip install nexus-core[asciidoc]
```

**Handles:** Sections, code blocks, tables, cross-references, includes.

---

## PowerPoint Extraction

### Basic Usage

```bash
# Extract from .pptx
nexus-core create slides.pptx --name presentation

# With explicit command
nexus-core create slides.pptx
```

**Requirements:**
```bash
pip install nexus-core[pptx]
```

**Extracts:** Slide text, speaker notes, images, tables, slide order.

---

## RSS/Atom Feed Extraction

### Basic Usage

```bash
# Extract from RSS feed
nexus-core create blog.rss --name blog-archive

# Atom feed
nexus-core create updates.atom --name updates

# With explicit command
nexus-core create blog.rss
```

**Requirements:**
```bash
pip install nexus-core[rss]
```

**Extracts:** Articles, titles, dates, authors, categories.

---

## Man Page Extraction

### Basic Usage

```bash
# Extract from man page
nexus-core create curl.1 --name curl-manual

# With explicit command
nexus-core create curl.1
```

**Handles:** Sections (NAME, SYNOPSIS, DESCRIPTION, OPTIONS, etc.), formatting.

---

## Confluence Wiki Extraction

### Basic Usage

```bash
# From Confluence API
nexus-core create \
  --conf-base-url https://wiki.example.com \
  --space-key DEV \
  --name team-docs

# From Confluence export directory
nexus-core create --conf-export-path ./confluence-export/
```

**Requirements:**
```bash
pip install nexus-core[confluence]
```

**Extracts:** Pages, page trees, attachments, labels, spaces.

---

## Notion Extraction

### Basic Usage

```bash
# From Notion API
export NOTION_API_KEY=secret_...
nexus-core create --database-id abc123 --name product-wiki

# From Notion export directory
nexus-core create --notion-export-path ./notion-export/
```

**Requirements:**
```bash
pip install nexus-core[notion]
```

**Extracts:** Pages, databases, blocks, properties, relations.

---

## Slack/Discord Chat Extraction

### Basic Usage

```bash
# From Slack export
nexus-core create --chat-export-path  slack-export/ --name team-discussions

# From Discord export
nexus-core create --chat-export-path  discord-export/ --name server-archive
```

**Requirements:**
```bash
pip install nexus-core[chat]
```

**Extracts:** Messages, threads, channels, reactions, attachments.

---

## Common Scraping Patterns

### Pattern 1: Test First

```bash
# Dry run to preview
nexus-core create <source> --dry-run

# Small test scrape
nexus-core create <source> --max-pages 10

# Full scrape
nexus-core create <source>
```

### Pattern 2: Iterative Development

```bash
# Scrape without enhancement (fast)
nexus-core create <source> --enhance-level 0

# Review output
ls output/my-skill/
cat output/my-skill/SKILL.md

# Enhance later
nexus-core enhance output/my-skill/
```

### Pattern 3: Parallel Processing

```bash
# Fast async scraping
nexus-core create <url> --async --workers 5

# Even faster (be careful with rate limits)
nexus-core create <url> --async --workers 10 --rate-limit 0.2
```

### Pattern 4: Resume Capability

```bash
# Start scraping
nexus-core create <source>
# ...interrupted...

# Resume later
nexus-core resume --list
nexus-core resume <job-id>
```

---

## Troubleshooting Scraping

### "No content extracted"

**Problem:** Wrong CSS selectors

**Solution:**
```bash
# First, try without a main_content selector (auto-detection)
# The scraper tries: main, div[role="main"], article, .content, etc.
nexus-core create <url> --dry-run

# If auto-detection fails, find the correct selector:
curl -s <url> | grep -i 'article\|main\|content'

# Then specify it in your config's source:
{
  "sources": [{
    "type": "documentation",
    "base_url": "https://...",
    "selectors": {
      "main_content": "div.content"
    }
  }]
}
```

### "Rate limit exceeded"

**Problem:** Too many requests

**Solution:**
```bash
# Slow down
nexus-core create <url> --rate-limit 2.0

# Or use GitHub token for GitHub repos
export GITHUB_TOKEN=ghp_...
```

### "Too many pages"

**Problem:** Site is larger than expected

**Solution:**
```bash
# Estimate first
nexus-core estimate configs/my-config.json

# Limit pages
nexus-core create <url> --max-pages 100

# Adjust URL patterns
{
  "url_patterns": {
    "exclude": ["/blog/", "/archive/", "/search"]
  }
}
```

### "Memory error"

**Problem:** Site too large for memory

**Solution:**
```bash
# Use streaming mode
nexus-core create <url> --streaming

# Or smaller chunks
nexus-core create <url> --chunk-tokens 500
```

---

## Performance Tips

| Tip | Command | Impact |
|-----|---------|--------|
| Use presets | `--config react` | Faster setup |
| Async mode | `--async --workers 5` | 3-5x faster |
| Skip enhancement | `--enhance-level 0` | Skip 60 sec |
| Use cache | `--skip-scrape` | Instant rebuild |
| Resume | `--resume` | Continue interrupted |

---

## Next Steps

- [Enhancement Guide](03-enhancement.md) - Improve skill quality
- [Packaging Guide](04-packaging.md) - Export to platforms
- [Config Format](../reference/CONFIG_FORMAT.md) - Advanced configuration
