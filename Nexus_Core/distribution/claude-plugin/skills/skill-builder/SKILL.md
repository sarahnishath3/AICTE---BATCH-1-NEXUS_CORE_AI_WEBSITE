---
name: skill-builder
description: Automatically detect source types and build AI skills using Nexus Core. Use when the user wants to create skills from documentation, repos, PDFs, videos, or other knowledge sources.
---

# Skill Builder

You have access to the Nexus Core MCP server which provides 40 tools for converting knowledge sources into AI-ready skills.

## When to Use This Skill

Use this skill when the user:
- Wants to create an AI skill from a documentation site, GitHub repo, PDF, video, or other source
- Needs to convert documentation into a format suitable for LLM consumption
- Wants to update or sync existing skills with their source documentation
- Needs to export skills to vector databases (Weaviate, Chroma, FAISS, Qdrant)
- Asks about scraping, converting, or packaging documentation for AI

## Source Type Detection

Automatically detect the source type from user input:

| Input Pattern | Source Type | Tool to Use |
|---------------|-------------|-------------|
| `https://...` (not GitHub/YouTube) | Documentation | `scrape_docs` |
| `owner/repo` or `github.com/...` | GitHub | `scrape_github` |
| `*.pdf` | PDF | `scrape_pdf` |
| YouTube/Vimeo URL or video file | Video | `scrape_video` |
| Local directory path | Codebase | `scrape_codebase` |
| `*.ipynb`, `*.html`, `*.yaml` (OpenAPI), `*.adoc`, `*.pptx`, `*.rss`, `*.1`-`.8` | Various | `scrape_generic` |
| JSON config file | Unified | Use config with `scrape_docs` |

## Recommended Workflow

1. **Detect source type** from the user's input
2. **Generate or fetch config** using `generate_config` or `fetch_config` if needed
3. **Estimate scope** with `estimate_pages` for documentation sites
4. **Scrape the source** using the appropriate scraping tool
5. **Enhance** with `enhance_skill` if the user wants AI-powered improvements
6. **Package** with `package_skill` for the target platform
7. **Export to vector DB** if requested using `export_to_*` tools

## Available MCP Tools

### Config Management
- `generate_config` — Generate a scraping config from a URL
- `list_configs` — List available preset configs
- `validate_config` — Validate a config file

### Scraping (use based on source type)
- `scrape_docs` — Documentation sites
- `scrape_github` — GitHub repositories
- `scrape_pdf` — PDF files
- `scrape_video` — Video transcripts
- `scrape_codebase` — Local code analysis
- `scrape_generic` — Jupyter, HTML, OpenAPI, AsciiDoc, PPTX, RSS, manpage, Confluence, Notion, chat

### Post-processing
- `enhance_skill` — AI-powered skill enhancement
- `package_skill` — Package for target platform
- `upload_skill` — Upload to platform API
- `install_skill` — End-to-end install workflow

### Advanced
- `detect_patterns` — Design pattern detection in code
- `extract_test_examples` — Extract usage examples from tests
- `build_how_to_guides` — Generate how-to guides from tests
- `split_config` — Split large configs into focused skills
- `export_to_weaviate`, `export_to_chroma`, `export_to_faiss`, `export_to_qdrant` — Vector DB export
