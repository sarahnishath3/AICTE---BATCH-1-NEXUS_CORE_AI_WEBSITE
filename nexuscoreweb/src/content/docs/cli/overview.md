---
title: CLI Overview
description: Overview of all Nexus Core CLI commands - scrape, enhance, package, and upload skills for multiple platforms
section: cli
order: 1
---

# CLI Overview

Nexus Core provides a comprehensive command-line interface for creating, enhancing, and deploying AI skills across multiple platforms.

## Available Commands

### Core Commands

| Command | Purpose | Time | Example |
|---------|---------|------|---------|
| [`scrape`](/docs/cli/scrape) | Scrape documentation websites | 20-40 min | `nexus-core scrape --config configs/react.json` |
| [`github`](/docs/cli/github) | Scrape GitHub repositories | 5-10 min | `nexus-core github --repo facebook/react` |
| [`pdf`](/docs/cli/pdf) | Extract content from PDFs | 5-15 min | `nexus-core pdf --pdf manual.pdf --name myskill` |
| [`unified`](/docs/cli/unified) | Multi-source scraping | 30-45 min | `nexus-core unified --config configs/react_unified.json` |

### Processing Commands

| Command | Purpose | Time | Example |
|---------|---------|------|---------|
| [`enhance`](/docs/cli/enhance) | AI-enhance skills | 30-60 sec | `nexus-core enhance output/react/` |
| [`package`](/docs/cli/package) | Package for platforms | Instant | `nexus-core package output/react/ --target claude` |
| [`upload`](/docs/cli/upload) | Upload to LLM platforms | 5-10 sec | `nexus-core upload output/react.zip` |

### Utility Commands

| Command | Purpose | Time | Example |
|---------|---------|------|---------|
| [`config`](/docs/cli/config) | Configure tokens & settings | Instant | `nexus-core config --github` |
| [`resume`](/docs/cli/resume) | Resume interrupted jobs | Variable | `nexus-core resume abc123` |
| `estimate` | Estimate page count | 1-2 min | `nexus-core estimate --config configs/react.json` |
| `validate` | Validate config files | Instant | `nexus-core validate configs/react.json` |
| `install` | One-command install | Variable | `nexus-core install output/react.zip` |

## Quick Reference

### Complete Workflow

```bash
# 1. Scrape documentation
nexus-core scrape --config configs/react.json

# 2. Enhance with AI
nexus-core enhance output/react/

# 3. Package for platform
nexus-core package output/react/ --target claude

# 4. Upload to platform
nexus-core upload output/react.zip
```

### Multi-Platform Workflow

```bash
# Scrape once
nexus-core scrape --config configs/react.json

# Package for all platforms
nexus-core package output/react/ --target claude
nexus-core package output/react/ --target gemini
nexus-core package output/react/ --target openai
nexus-core package output/react/ --target markdown

# Upload to platforms
nexus-core upload output/react.zip --target claude
nexus-core upload output/react-gemini.tar.gz --target gemini
nexus-core upload output/react-openai.zip --target openai
```

## Command Categories

### Source Commands

Extract content from various sources:
- **scrape** - Documentation websites
- **github** - GitHub repositories
- **pdf** - PDF documents
- **unified** - Multiple sources combined

### Processing Commands

Transform and package skills:
- **enhance** - AI-powered improvement
- **package** - Platform-specific packaging
- **upload** - Deploy to LLM platforms

## Common Options

Most commands support these options:

- `--config CONFIG` - Load configuration from file
- `--name NAME` - Skill name
- `--output DIR` - Output directory
- `--help` - Show command help

## Configuration Management (v2.7.0)

New in v2.7.0: Interactive configuration wizard and job resumption.

### Setup GitHub Tokens

```bash
# Interactive wizard for multi-profile token management
nexus-core config --github

# Set up multiple profiles (personal, work, etc.)
# Configure rate limit strategies (prompt, wait, switch, fail)
# Test connections and view rate limits
```

### Configure API Keys

```bash
# Set up API keys for AI enhancement
nexus-core config --api-keys

# Supported: Claude (Anthropic), Google Gemini, OpenAI ChatGPT
# Browser integration opens API key creation pages
# Secure storage with 600 permissions
```

### Resume Interrupted Jobs

```bash
# List all resumable jobs
nexus-core resume --list

# Resume specific job from checkpoint
nexus-core resume abc123def456

# Clean up old job files
nexus-core resume --clean
```

**Auto-resume features:**
- Automatic checkpoints every 60 seconds (configurable)
- Resume from network interruptions
- Continue after rate limit resets
- Recover from system crashes

## Getting Help

```bash
# General help
nexus-core --help

# Command-specific help
nexus-core scrape --help
nexus-core github --help
nexus-core package --help
nexus-core config --help
nexus-core resume --help
```

## Next Steps

**Source Commands:**
- [Scrape Command](/docs/cli/scrape) - Documentation scraping
- [GitHub Command](/docs/cli/github) - Repository scraping
- [Unified Command](/docs/cli/unified) - Multi-source scraping

**Processing Commands:**
- [Enhance Command](/docs/cli/enhance) - AI enhancement
- [Package Command](/docs/cli/package) - Multi-platform packaging
- [Upload Command](/docs/cli/upload) - Platform deployment

**Configuration (v2.7.0):**
- [Config Command](/docs/cli/config) - Token & settings management
- [Resume Command](/docs/cli/resume) - Job resumption
