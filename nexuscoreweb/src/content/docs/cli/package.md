---
title: package - Package Skills
description: Package skills for multiple platforms - Claude AI, Google Gemini, OpenAI ChatGPT, or universal Markdown export
section: cli
order: 6
---

# package - Package Skills

Package skills for deployment to multiple LLM platforms.

## Basic Usage

```bash
nexus-core package INPUT_DIR [OPTIONS]
```

## Quick Examples

```bash
# Package for Claude (default)
nexus-core package output/react/

# Package for specific platform
nexus-core package output/react/ --target gemini
nexus-core package output/react/ --target openai
nexus-core package output/react/ --target markdown

# Package for all platforms
nexus-core package output/react/ --target claude
nexus-core package output/react/ --target gemini
nexus-core package output/react/ --target openai
nexus-core package output/react/ --target markdown
```

## Options

- `--target PLATFORM` - Target platform (claude, gemini, openai, markdown)
- `--output FILE` - Custom output filename

## Supported Platforms

### Claude AI (Default)

```bash
nexus-core package output/react/
# Creates: output/react.zip
```

**Format:**
- ZIP archive
- YAML frontmatter in SKILL.md
- References folder structure

**Use for:** Claude Code, Claude Desktop, claude.ai

### Google Gemini

```bash
nexus-core package output/react/ --target gemini
# Creates: output/react-gemini.tar.gz
```

**Prerequisites:**
```bash
pip install nexus-core[gemini]
```

**Format:**
- tar.gz archive
- Plain markdown (no YAML)
- `system_instructions.md` instead of SKILL.md
- Gemini-specific metadata

**Use for:** Google AI Studio, Gemini API

### OpenAI ChatGPT

```bash
nexus-core package output/react/ --target openai
# Creates: output/react-openai.zip
```

**Prerequisites:**
```bash
pip install nexus-core[openai]
```

**Format:**
- ZIP archive
- Plain text instructions
- Vector store files
- OpenAI Assistant configuration

**Use for:** ChatGPT, OpenAI Assistants API

### Generic Markdown

```bash
nexus-core package output/react/ --target markdown
# Creates: output/react-markdown.zip
```

**Format:**
- ZIP archive
- Pure markdown (no frontmatter)
- Universal compatibility
- Manifest.json with metadata

**Use for:** Any LLM, offline docs, self-hosting

## Platform Comparison

| Feature | Claude | Gemini | OpenAI | Markdown |
|---------|--------|--------|--------|----------|
| **Format** | ZIP | tar.gz | ZIP | ZIP |
| **Frontmatter** | ✅ YAML | ❌ | ❌ | ❌ |
| **Size** | Optimized | Compressed | Indexed | Universal |
| **Upload API** | ✅ | ✅ | ✅ | ❌ |

## Output Files

### Claude AI

```
react.zip
├── SKILL.md              # YAML frontmatter + markdown
└── references/
    ├── index.md
    ├── getting-started.md
    └── api-reference.md
```

### Google Gemini

```
react-gemini.tar.gz
├── system_instructions.md    # Plain markdown
├── references/
│   └── ...
└── gemini_metadata.json
```

### OpenAI ChatGPT

```
react-openai.zip
├── assistant_instructions.txt    # Plain text
├── vector_store_files/
│   └── ...
└── openai_metadata.json
```

### Generic Markdown

```
react-markdown.zip
├── README.md
├── DOCUMENTATION.md
├── references/
│   └── ...
└── manifest.json
```

## Multi-Platform Workflow

```bash
# 1. Scrape once
nexus-core scrape --config configs/react.json

# 2. Enhance once
nexus-core enhance output/react/

# 3. Package for all platforms
nexus-core package output/react/ --target claude
nexus-core package output/react/ --target gemini
nexus-core package output/react/ --target openai
nexus-core package output/react/ --target markdown

# Result:
# - output/react.zip (Claude)
# - output/react-gemini.tar.gz (Gemini)
# - output/react-openai.zip (OpenAI)
# - output/react-markdown.zip (Universal)
```

## File Size

Typical skill sizes:

| Size Category | Pages | Typical Size | Example |
|---------------|-------|--------------|---------|
| Small | 10-50 | 5-20 KB | Tutorial docs |
| Medium | 50-200 | 20-100 KB | Framework docs |
| Large | 200-500 | 100-500 KB | Complete API |

Check size:
```bash
ls -lh output/react*.zip
```

## Platform Limits

| Platform | Max File Size | Typical Size |
|----------|--------------|--------------|
| Claude AI | ~25 MB | 10-500 KB |
| Google Gemini | ~100 MB | 10-500 KB |
| OpenAI ChatGPT | ~512 MB vector store | 10-500 KB |
| Generic Markdown | No limit | 10-500 KB |

## Troubleshooting

### "SKILL.md not found"

Make sure you scraped first:
```bash
nexus-core scrape --config configs/react.json
nexus-core package output/react/
```

### "Invalid target platform"

Use valid platforms:
```bash
# Valid
--target claude
--target gemini
--target openai
--target markdown

# Invalid
--target anthropic  ❌
--target google     ❌
```

### Wrong file format

Each platform requires specific format:
- Claude/OpenAI/Markdown: `.zip`
- Gemini: `.tar.gz`

Use `--target` parameter correctly.

## Next Steps

- [Upload Command](/docs/cli/upload) - Upload to platforms
- [Multi-LLM Support](/docs/manual/platforms/multi-llm-support) - Platform details
- [Upload Guide](/docs/guides/upload-guide) - Complete upload guide
