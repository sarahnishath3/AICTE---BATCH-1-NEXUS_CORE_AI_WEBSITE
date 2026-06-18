# Quick Start Guide

> **Nexus Core v3.6.0**  
> **Create your first skill in 3 commands**

---

## The 3 Commands

```bash
# 1. Install Nexus Core
pip install nexus-core

# 2. Create a skill from any source
nexus-core create https://docs.django.com/

# 3. Package it for your AI platform
nexus-core package output/django --target claude
```

**That's it!** You now have `output/django-claude.zip` ready to upload.

---

## What You Can Create From

The `create` command auto-detects your source:

| Source Type | Example Command |
|-------------|-----------------|
| **Documentation** | `nexus-core create https://docs.react.dev/` |
| **GitHub Repo** | `nexus-core create facebook/react` |
| **Local Code** | `nexus-core create ./my-project` |
| **PDF File** | `nexus-core create manual.pdf` |
| **Word Document** | `nexus-core create report.docx` |
| **EPUB Book** | `nexus-core create book.epub` |
| **Video** | `nexus-core create https://youtube.com/watch?v=...` |
| **Jupyter Notebook** | `nexus-core create analysis.ipynb` |
| **Local HTML (file)** | `nexus-core create page.html` |
| **Local HTML (directory)** | `nexus-core create ./mirror_output/site/` |
| **OpenAPI Spec** | `nexus-core create api-spec.yaml` |
| **AsciiDoc** | `nexus-core create guide.adoc` |
| **PowerPoint** | `nexus-core create slides.pptx` |
| **RSS/Atom Feed** | `nexus-core create feed.rss` |
| **Man Page** | `nexus-core create grep.1` |
| **Confluence** | `nexus-core create --space-key  DEV` |
| **Notion** | `nexus-core create --database-id  abc123` |
| **Slack/Discord** | `nexus-core create --chat-export-path  slack-export/` |
| **Config File** | `nexus-core create configs/custom.json` |

For an existing project where you don't know yet which frameworks you need skills for, use `nexus-core scan <dir>` — it AI-detects the stack and emits one config per framework. See [Scan a project](05-scan-a-project.md).

---

## Examples by Source

### Documentation Website

```bash
# React documentation
nexus-core create https://react.dev/
nexus-core package output/react --target claude

# Django documentation  
nexus-core create https://docs.djangoproject.com/
nexus-core package output/django --target claude
```

### GitHub Repository

```bash
# React source code
nexus-core create facebook/react
nexus-core package output/react --target claude

# Your own repo
nexus-core create yourusername/yourrepo
nexus-core package output/yourrepo --target claude
```

### Local Project

```bash
# Your codebase
nexus-core create ./my-project
nexus-core package output/my-project --target claude

# Specific directory
cd ~/projects/my-api
nexus-core create .
nexus-core package output/my-api --target claude
```

### PDF Document

```bash
# Technical manual
nexus-core create manual.pdf --name product-docs
nexus-core package output/product-docs --target claude

# Research paper
nexus-core create paper.pdf --name research
nexus-core package output/research --target claude
```

### Video

```bash
# YouTube video transcript
nexus-core create https://www.youtube.com/watch?v=dQw4w9WgXcQ --name tutorial
nexus-core package output/tutorial --target claude
```

### Jupyter Notebook

```bash
# Data science notebook
nexus-core create analysis.ipynb --name ml-analysis
nexus-core package output/ml-analysis --target claude
```

### PowerPoint / Word / EPUB

```bash
# PowerPoint slides
nexus-core create presentation.pptx --name quarterly-review

# Word document
nexus-core create spec.docx --name api-spec

# EPUB book
nexus-core create rust-book.epub --name rust-guide
```

### Confluence / Notion / Slack

```bash
# Confluence wiki space
nexus-core create --space-key  DEV --name team-docs

# Notion workspace
nexus-core create --database-id  abc123 --name product-wiki

# Slack/Discord export
nexus-core create --chat-export-path  slack-export/ --name team-chat
```

---

## Common Options

### Specify a Name

```bash
nexus-core create https://docs.example.com/ --name my-docs
```

### Add Description

```bash
nexus-core create facebook/react --description "React source code analysis"
```

### Dry Run (Preview)

```bash
nexus-core create https://docs.react.dev/ --dry-run
```

### Skip Enhancement (Faster)

```bash
nexus-core create https://docs.react.dev/ --enhance-level 0
```

### Use a Preset

```bash
# Quick analysis (1-2 min)
nexus-core create ./my-project --preset quick

# Comprehensive analysis (20-60 min)
nexus-core create ./my-project --preset comprehensive
```

---

## Package for Different Platforms

### Claude AI (Default)

```bash
nexus-core package output/my-skill/
# Creates: output/my-skill-claude.zip
```

### Google Gemini

```bash
nexus-core package output/my-skill/ --target gemini
# Creates: output/my-skill-gemini.tar.gz
```

### OpenAI ChatGPT

```bash
nexus-core package output/my-skill/ --target openai
# Creates: output/my-skill-openai.zip
```

### LangChain

```bash
nexus-core package output/my-skill/ --target langchain
# Creates: output/my-skill-langchain/ directory
```

### Multiple Platforms

```bash
for platform in claude gemini openai; do
  nexus-core package output/my-skill/ --target $platform
done
```

---

## Upload to Platform

### Upload to Claude

```bash
export ANTHROPIC_API_KEY=sk-ant-...
nexus-core upload output/my-skill-claude.zip --target claude
```

### Upload to Gemini

```bash
export GOOGLE_API_KEY=AIza...
nexus-core upload output/my-skill-gemini.tar.gz --target gemini
```

### Auto-Upload After Package

```bash
export ANTHROPIC_API_KEY=sk-ant-...
nexus-core package output/my-skill/ --target claude --upload
```

---

## Complete One-Command Workflow

Use `install` for everything in one step:

```bash
# Complete: scrape → enhance → package → upload
export ANTHROPIC_API_KEY=sk-ant-...
nexus-core install --config react --target claude

# Skip upload
nexus-core install --config react --target claude --no-upload
```

---

## Output Structure

After running `create`, you'll have:

```
output/
├── django/                    # The skill
│   ├── SKILL.md              # Main skill file
│   ├── references/           # Organized documentation
│   │   ├── index.md
│   │   ├── getting_started.md
│   │   └── api_reference.md
│   └── .nexus-core/       # Metadata
│
└── django-claude.zip         # Packaged skill (after package)
```

---

## Time Estimates

| Source Type | Size | Time |
|-------------|------|------|
| Small docs (< 50 pages) | ~10 MB | 2-5 min |
| Medium docs (50-200 pages) | ~50 MB | 10-20 min |
| Large docs (200-500 pages) | ~200 MB | 30-60 min |
| GitHub repo (< 1000 files) | varies | 5-15 min |
| Local project | varies | 2-10 min |
| PDF (< 100 pages) | ~5 MB | 1-3 min |

*Times include scraping + enhancement (level 2). Use `--enhance-level 0` to skip enhancement.*

---

## Quick Tips

### Test First with Dry Run

```bash
nexus-core create https://docs.example.com/ --dry-run
```

### Use Presets for Faster Results

```bash
# Quick mode for testing
nexus-core create https://docs.react.dev/ --preset quick
```

### Skip Enhancement for Speed

```bash
nexus-core create https://docs.react.dev/ --enhance-level 0
nexus-core enhance output/react/  # Enhance later
```

### Check Available Configs

```bash
nexus-core estimate --all
```

### Resume Interrupted Jobs

```bash
nexus-core resume --list
nexus-core resume <job-id>
```

---

## Next Steps

- [Your First Skill](03-your-first-skill.md) - Complete walkthrough
- [Core Concepts](../user-guide/01-core-concepts.md) - Understand how it works
- [Scraping Guide](../user-guide/02-scraping.md) - All scraping options

---

## Troubleshooting

### "command not found"

```bash
# Add to PATH
export PATH="$HOME/.local/bin:$PATH"
```

### "No module named 'nexus_core'"

```bash
# Reinstall
pip install --force-reinstall nexus-core
```

### Scraping too slow

```bash
# Use async mode
nexus-core create https://docs.react.dev/ --async --workers 5
```

### Out of memory

```bash
# Use streaming mode
nexus-core package output/large-skill/ --streaming
```

---

## See Also

- [Installation Guide](01-installation.md) - Detailed installation
- [CLI Reference](../reference/CLI_REFERENCE.md) - All commands
- [Config Format](../reference/CONFIG_FORMAT.md) - Custom configurations
