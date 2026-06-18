---
name: nexus-core
description: Generate LLM skills from documentation, codebases, and GitHub repositories
---

# Nexus Core

## Prerequisites

```bash
pip install nexus-core
# Or: uv pip install nexus-core
```

## Commands

| Source | Command |
|--------|---------|
| Local code | `nexus-core create ./path` |
| Docs URL | `nexus-core create https://docs.example.com` |
| GitHub | `nexus-core create owner/repo` |
| PDF | `nexus-core create document.pdf` |

## Quick Start

```bash
# Analyze local codebase
nexus-core create /path/to/project --name my-skill

# Package for Claude
yes | nexus-core package output/my-skill/ --no-open
```

## Options

| Flag | Description |
|------|-------------|
| `--preset quick/standard/comprehensive` | Analysis preset |
| `--skip-patterns` | Skip pattern detection |
| `--skip-test-examples` | Skip test extraction |

---

