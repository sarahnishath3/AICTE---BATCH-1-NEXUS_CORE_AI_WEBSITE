> ⚠️ **DEPRECATED**: This document contains phantom commands and outdated patterns.
> 
> For up-to-date documentation, please see:
> - [Quick Start Guide](getting-started/02-quick-start.md) - 3 commands to first skill
> - [CLI Reference](reference/CLI_REFERENCE.md) - Complete command reference
> - [Documentation Hub](README.md) - All documentation
>
> *This file is kept for historical reference only.*

---

# Quick Reference - Nexus Core Cheat Sheet

**Version:** 3.6.0 | **Quick Commands** | **One-Page Reference**

---

## Installation

```bash
# Basic installation
pip install nexus-core

# With all platforms
pip install nexus-core[all-llms]

# Development mode
pip install -e ".[all-llms,dev]"
```

---

## CLI Commands

### Documentation Scraping

```bash
# Scrape with preset config
nexus-core create --config react

# Scrape custom site
nexus-core create --base-url https://docs.example.com --name my-framework

# Rebuild without re-scraping
nexus-core create --config react --skip-scrape

# Async scraping (2-3x faster)
nexus-core create --config react --async
```

### GitHub Repository Analysis

```bash
# Basic analysis
nexus-core create https://github.com/facebook/react

# Deep C3.x analysis (patterns, tests, guides)
nexus-core create https://github.com/vercel/next.js --analysis-depth c3x

# With GitHub token (higher rate limits)
GITHUB_TOKEN=ghp_... nexus-core create https://github.com/org/repo
```

### PDF Extraction

```bash
# Extract from PDF
nexus-core create --pdf manual.pdf --name product-manual

# With OCR (scanned PDFs)
nexus-core create --pdf scanned.pdf --enable-ocr

# Large PDF (chunked processing)
nexus-core create --pdf large.pdf --pdf-pages-per-chunk 50
```

### Multi-Source Scraping

```bash
# Unified scraping (docs + GitHub + PDF)
nexus-core create --config configs/unified/react-unified.json

# Merge separate sources
nexus-core merge-sources \
  --docs output/react-docs \
  --github output/react-github \
  --output output/react-complete
```

### AI Enhancement

```bash
# API mode (fast, costs ~$0.15-0.30)
export ANTHROPIC_API_KEY=sk-ant-...
nexus-core enhance output/react/

# LOCAL mode (free, uses Claude Code Max)
nexus-core enhance output/react/ --mode LOCAL

# Background enhancement
nexus-core enhance output/react/ --background

# Monitor background enhancement
nexus-core enhance-status output/react/ --watch

# Apply a workflow preset during create
nexus-core create ./my-project --enhance-workflow security-focus

# Chain multiple workflow presets
nexus-core create ./my-project \
  --enhance-workflow security-focus \
  --enhance-workflow minimal
```

### Enhancement Workflow Presets

```bash
# List all available workflows (bundled + user)
nexus-core workflows list

# Show the YAML content of a workflow
nexus-core workflows show security-focus

# Copy a bundled workflow to user dir for editing
nexus-core workflows copy security-focus

# Copy multiple bundled workflows at once
nexus-core workflows copy security-focus minimal api-documentation

# Install a custom YAML file as a user workflow
nexus-core workflows add ./my-workflow.yaml

# Install multiple YAML files at once
nexus-core workflows add ./wf-a.yaml ./wf-b.yaml

# Install with a custom name (single file only)
nexus-core workflows add ./my-workflow.yaml --name my-custom-name

# Remove a user workflow (bundled presets cannot be removed)
nexus-core workflows remove my-workflow

# Remove multiple user workflows at once
nexus-core workflows remove wf-a wf-b

# Validate a workflow by name or file path
nexus-core workflows validate security-focus
nexus-core workflows validate ./my-workflow.yaml
```

**Bundled presets:** `default`, `minimal`, `security-focus`, `architecture-comprehensive`, `api-documentation`
**User presets dir:** `~/.config/nexus-core/workflows/`

### Packaging & Upload

```bash
# Package for Claude AI
nexus-core package output/react/ --target claude

# Package for all platforms
for platform in claude gemini openai markdown; do
  nexus-core package output/react/ --target $platform
done

# Upload to Claude AI
export ANTHROPIC_API_KEY=sk-ant-...
nexus-core upload output/react-claude.zip --target claude

# Upload to Google Gemini
export GOOGLE_API_KEY=AIza...
nexus-core upload output/react-gemini.tar.gz --target gemini
```

### Complete Workflow

```bash
# One command: fetch → scrape → enhance → package → upload
export ANTHROPIC_API_KEY=sk-ant-...
nexus-core install react --target claude --enhance --upload

# Multi-platform install
nexus-core install react --target claude,gemini,openai --enhance --upload

# Without enhancement or upload
nexus-core install vue --target markdown
```

---

## Common Workflows

### Workflow 1: Quick Skill from Docs

```bash
# 1. Scrape documentation
nexus-core create --config react

# 2. Package for Claude
nexus-core package output/react/ --target claude

# 3. Upload to Claude
export ANTHROPIC_API_KEY=sk-ant-...
nexus-core upload output/react-claude.zip --target claude
```

### Workflow 2: GitHub Repo to Skill

```bash
# 1. Analyze repository with C3.x features
nexus-core create https://github.com/facebook/react --analysis-depth c3x

# 2. Package for multiple platforms
nexus-core package output/react/ --target claude,gemini,openai
```

### Workflow 3: Complete Multi-Source Skill

```bash
# 1. Create unified config (configs/unified/my-framework.json)
{
  "name": "my-framework",
  "sources": {
    "documentation": {"type": "docs", "base_url": "https://docs..."},
    "github": {"type": "github", "repo_url": "https://github..."},
    "pdf": {"type": "pdf", "pdf_path": "manual.pdf"}
  }
}

# 2. Run unified scraping
nexus-core create --config configs/unified/my-framework.json

# 3. Enhance with AI
nexus-core enhance output/my-framework/

# 4. Package and upload
nexus-core package output/my-framework/ --target claude
nexus-core upload output/my-framework-claude.zip --target claude
```

---

## MCP Server

### Starting MCP Server

```bash
# stdio mode (Claude Code, VS Code + Cline)
nexus-core-mcp

# HTTP mode (Cursor, Windsurf, IntelliJ)
nexus-core-mcp --transport http --port 8765
```

### MCP Tools (26 total)

**Core Tools:**
1. `list_configs` - List preset configurations
2. `generate_config` - Generate config from docs URL
3. `validate_config` - Validate config structure
4. `estimate_pages` - Estimate page count
5. `scrape_docs` - Scrape documentation
6. `package_skill` - Package to .zip
7. `upload_skill` - Upload to platform
8. `enhance_skill` - AI enhancement
9. `install_skill` - Complete workflow

**Extended Tools:**
10. `scrape_github` - GitHub analysis
11. `scrape_pdf` - PDF extraction
12. `unified_scrape` - Multi-source scraping
13. `merge_sources` - Merge docs + code
14. `detect_conflicts` - Find discrepancies
15. `split_config` - Split large configs
16. `generate_router` - Generate router skills
17. `add_config_source` - Register git repos
18. `fetch_config` - Fetch configs from git

---

## Environment Variables

```bash
# Claude AI (default platform)
export ANTHROPIC_API_KEY=sk-ant-...

# Google Gemini
export GOOGLE_API_KEY=AIza...

# OpenAI ChatGPT
export OPENAI_API_KEY=sk-...

# GitHub (higher rate limits)
export GITHUB_TOKEN=ghp_...
```

---

## Testing

```bash
# Run all tests (1,880+)
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src/nexus_core --cov-report=html

# Fast tests only (skip slow tests)
pytest tests/ -m "not slow"

# Specific test category
pytest tests/test_mcp*.py -v             # MCP tests
pytest tests/test_*_integration.py -v    # Integration tests
pytest tests/test_*_e2e.py -v            # E2E tests
```

---

## Code Quality

```bash
# Linting with Ruff
ruff check .                 # Check for issues
ruff check --fix .           # Auto-fix issues
ruff format .                # Format code

# Run before commit
ruff check . && ruff format --check . && pytest tests/ -v
```

---

## Preset Configurations (24)

**Web Frameworks:**
- `react`, `vue`, `angular`, `svelte`, `nextjs`

**Python:**
- `django`, `flask`, `fastapi`, `sqlalchemy`, `pytest`

**Game Development:**
- `godot`, `pygame`, `unity`

**Tools & Libraries:**
- `docker`, `kubernetes`, `terraform`, `ansible`

**Unified (Docs + GitHub):**
- `react-unified`, `vue-unified`, `nextjs-unified`, etc.

**List all configs:**
```bash
nexus-core list-configs
```

---

## Tips & Tricks

### Speed Up Scraping

```bash
# Use async mode (2-3x faster)
nexus-core create --config react --async

# Rebuild without re-scraping
nexus-core create --config react --skip-scrape
```

### Save API Costs

```bash
# Use LOCAL mode for free AI enhancement
nexus-core enhance output/react/ --mode LOCAL

# Or skip enhancement entirely
nexus-core install react --target claude --no-enhance
```

### Large Documentation

```bash
# Generate router skill (>500 pages)
nexus-core generate-router output/large-docs/

# Split configuration
nexus-core split-config configs/large.json --output configs/split/
```

### Debugging

```bash
# Verbose output
nexus-core create --config react --verbose

# Dry run (no actual scraping)
nexus-core create --config react --dry-run

# Show config without scraping
nexus-core validate-config configs/react.json
```

### Batch Processing

```bash
# Process multiple configs
for config in react vue angular svelte; do
  nexus-core install $config --target claude
done

# Parallel processing
nexus-core install react --target claude &
nexus-core install vue --target claude &
wait
```

---

## File Locations

**Configurations:**
- Preset configs: `nexus-core-configs/official/*.json`
- Custom configs: `configs/*.json`

**Output:**
- Scraped data: `output/{name}_data/`
- Built skills: `output/{name}/`
- Packages: `output/{name}-{platform}.{zip|tar.gz}`

**MCP:**
- Server: `src/nexus_core/mcp/server_fastmcp.py`
- Tools: `src/nexus_core/mcp/tools/*.py`

**Tests:**
- All tests: `tests/test_*.py`
- Fixtures: `tests/fixtures/`

---

## Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| `NetworkError` | Connection failed | Check URL, internet connection |
| `InvalidConfigError` | Bad config | Validate with `validate-config` |
| `RateLimitError` | Too many requests | Increase `rate_limit` in config |
| `ScrapingError` | Scraping failed | Check selectors, URL patterns |
| `APIError` | Platform API failed | Check API key, quota |

---

## Getting Help

```bash
# Command help
nexus-core --help
nexus-core create --help
nexus-core install --help

# Version info
nexus-core --version

# Check configuration
nexus-core validate-config configs/my-config.json
```

**Documentation:**
- [Full README](../README.md)
- [Usage Guide](guides/USAGE.md)
- [API Reference](reference/API_REFERENCE.md)
- [Troubleshooting](../TROUBLESHOOTING.md)

**Links:**
- GitHub: https://github.com/yusufkaraaslan/Nexus_Core
- PyPI: https://pypi.org/project/nexus-core/
- Issues: https://github.com/yusufkaraaslan/Nexus_Core/issues

---

**Version:** 3.6.0 | **Test Count:** 1,880+ | **MCP Tools:** 26 | **Platforms:** 16+ (Claude, Gemini, OpenAI, LangChain, LlamaIndex, ChromaDB, FAISS, Cursor, Windsurf, and more)
