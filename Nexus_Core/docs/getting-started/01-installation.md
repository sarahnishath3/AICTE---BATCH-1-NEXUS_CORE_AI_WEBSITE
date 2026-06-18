# Installation Guide

> **Nexus Core v3.6.0**

Get Nexus Core installed and running in under 5 minutes.

---

## System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| **Python** | 3.10 | 3.11 or 3.12 |
| **RAM** | 4 GB | 8 GB+ |
| **Disk** | 500 MB | 2 GB+ |
| **OS** | Linux, macOS, Windows (WSL) | Linux, macOS |

---

## Quick Install

### Option 1: pip (Recommended)

```bash
# Basic installation
pip install nexus-core

# With all platform support
pip install nexus-core[all-llms]

# Verify installation
nexus-core --version
```

### Option 2: pipx (Isolated)

```bash
# Install pipx if not available
pip install pipx
pipx ensurepath

# Install nexus-core
pipx install nexus-core[all-llms]
```

### Option 3: Development (from source)

```bash
# Clone repository
git clone https://github.com/yusufkaraaslan/Nexus_Core.git
cd Nexus_Core

# Install in editable mode
pip install -e ".[all-llms,dev]"

# Verify
nexus-core --version
```

---

## Installation Options

### Minimal Install

Just the core functionality:

```bash
pip install nexus-core
```

**Includes:**
- Documentation scraping
- Basic packaging
- Local enhancement (Claude Code)

### Full Install

All features and platforms:

```bash
pip install nexus-core[all-llms]
```

**Includes:**
- Claude AI support
- Google Gemini support
- OpenAI ChatGPT support
- MiniMax AI support
- All vector databases
- MCP server
- Cloud storage (S3, GCS, Azure)

### Custom Install

Install only what you need:

```bash
# Specific platform only
pip install nexus-core[gemini]      # Google Gemini
pip install nexus-core[openai]      # OpenAI
pip install nexus-core[minimax]     # MiniMax AI
pip install nexus-core[chroma]      # ChromaDB

# Multiple extras
pip install nexus-core[gemini,openai,chroma]

# Development
pip install nexus-core[dev]
```

---

## Available Extras

| Extra | Description | Install Command |
|-------|-------------|-----------------|
| `gemini` | Google Gemini support | `pip install nexus-core[gemini]` |
| `openai` | OpenAI ChatGPT support | `pip install nexus-core[openai]` |
| `minimax` | MiniMax AI support | `pip install nexus-core[minimax]` |
| `mcp` | MCP server | `pip install nexus-core[mcp]` |
| `chroma` | ChromaDB export | `pip install nexus-core[chroma]` |
| `weaviate` | Weaviate export | `pip install nexus-core[weaviate]` |
| `qdrant` | Qdrant export | `pip install nexus-core[qdrant]` |
| `faiss` | FAISS export | `pip install nexus-core[faiss]` |
| `s3` | AWS S3 storage | `pip install nexus-core[s3]` |
| `gcs` | Google Cloud Storage | `pip install nexus-core[gcs]` |
| `azure` | Azure Blob Storage | `pip install nexus-core[azure]` |
| `embedding` | Embedding server | `pip install nexus-core[embedding]` |
| `video` | YouTube/video transcript extraction | `pip install nexus-core[video]` |
| `video-full` | + Whisper transcription, scene detection | `pip install nexus-core[video-full]` |
| `jupyter` | Jupyter Notebook extraction | `pip install nexus-core[jupyter]` |
| `asciidoc` | AsciiDoc document processing | `pip install nexus-core[asciidoc]` |
| `pptx` | PowerPoint presentation extraction | `pip install nexus-core[pptx]` |
| `rss` | RSS/Atom feed extraction | `pip install nexus-core[rss]` |
| `confluence` | Confluence wiki extraction | `pip install nexus-core[confluence]` |
| `notion` | Notion workspace extraction | `pip install nexus-core[notion]` |
| `chat` | Slack/Discord export extraction | `pip install nexus-core[chat]` |
| `all-llms` | All LLM platforms | `pip install nexus-core[all-llms]` |
| `all` | Everything | `pip install nexus-core[all]` |
| `dev` | Development tools | `pip install nexus-core[dev]` |

> **Video visual deps:** After installing `nexus-core[video-full]`, run `nexus-core create --setup` to auto-detect your GPU (NVIDIA/AMD/CPU) and install the correct PyTorch variant + easyocr.

---

## Post-Installation Setup

### 1. Configure API Keys (Optional)

For AI enhancement and uploads:

```bash
# Interactive configuration wizard
nexus-core config

# Or set environment variables
export ANTHROPIC_API_KEY=sk-ant-...
export GITHUB_TOKEN=ghp_...
```

### 2. Verify Installation

```bash
# Check version
nexus-core --version

# See all commands
nexus-core --help

# Test configuration
nexus-core config --test
```

### 3. Quick Test

```bash
# List available presets
nexus-core estimate --all

# Do a dry run
nexus-core create https://docs.python.org/3/ --dry-run
```

---

## Platform-Specific Notes

### macOS

```bash
# Using Homebrew Python
brew install python@3.12
pip3.12 install nexus-core[all-llms]

# Or with pyenv
pyenv install 3.12
pyenv global 3.12
pip install nexus-core[all-llms]
```

### Linux (Ubuntu/Debian)

```bash
# Install Python and pip
sudo apt update
sudo apt install python3-pip python3-venv

# Install nexus-core
pip3 install nexus-core[all-llms]

# Make available system-wide
sudo ln -s ~/.local/bin/nexus-core /usr/local/bin/
```

### Windows

**Recommended:** Use WSL2

```powershell
# Or use Windows directly (PowerShell)
python -m pip install nexus-core[all-llms]

# Add to PATH if needed
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";$env:APPDATA\Python\Python312\Scripts", "User")
```

### Docker

```bash
# Pull image
docker pull skillseekers/nexus-core:latest

# Run
docker run -it --rm \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  -v $(pwd)/output:/output \
  skillseekers/nexus-core \
  nexus-core create https://docs.react.dev/
```

---

## Troubleshooting

### "command not found: nexus-core"

```bash
# Add pip bin to PATH
export PATH="$HOME/.local/bin:$PATH"

# Or reinstall with --user
pip install --user --force-reinstall nexus-core
```

### Permission denied

```bash
# Don't use sudo with pip
# Instead:
pip install --user nexus-core

# Or use a virtual environment
python3 -m venv venv
source venv/bin/activate
pip install nexus-core[all-llms]
```

### Import errors

```bash
# For development installs, ensure editable mode
pip install -e .

# Check installation
python -c "import nexus_core; print(nexus_core.__version__)"
```

### Version conflicts

```bash
# Use virtual environment
python3 -m venv nexus-core-env
source nexus-core-env/bin/activate
pip install nexus-core[all-llms]
```

---

## Upgrade

```bash
# Upgrade to latest
pip install --upgrade nexus-core

# Upgrade with all extras
pip install --upgrade nexus-core[all-llms]

# Check current version
nexus-core --version

# See what's new
pip show nexus-core
```

---

## Uninstall

```bash
pip uninstall nexus-core

# Clean up config (optional)
rm -rf ~/.config/nexus-core/
rm -rf ~/.cache/nexus-core/
```

---

## Next Steps

- [Quick Start Guide](02-quick-start.md) - Create your first skill in 3 commands
- [Your First Skill](03-your-first-skill.md) - Complete walkthrough

---

## Getting Help

```bash
# Command help
nexus-core --help
nexus-core create --help

# Documentation
# https://github.com/yusufkaraaslan/Nexus_Core/tree/main/docs

# Issues
# https://github.com/yusufkaraaslan/Nexus_Core/issues
```
