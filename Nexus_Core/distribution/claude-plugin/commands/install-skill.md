---
description: One-command skill creation and packaging for a target platform
---

# Install Skill

End-to-end workflow: create a skill from any source, then package it for a target LLM platform.

## Usage

```
/nexus-core:install-skill <source> [--target <platform>] [--preset <level>]
```

## Instructions

When the user provides a source via `$ARGUMENTS`:

1. Parse the arguments: extract source, `--target` (default: claude), `--preset` (default: quick).
2. Run the create command:
   ```bash
   nexus-core create "$SOURCE" --preset "$PRESET" --output ./output
   ```
3. Find the generated skill directory (look for the directory containing SKILL.md in ./output/).
4. Run the package command for the target platform:
   ```bash
   nexus-core package "$SKILL_DIR" --target "$TARGET"
   ```
5. Report what was created and where to find the packaged output.

## Target Platforms

`claude` (default), `openai`, `gemini`, `langchain`, `llama-index`, `haystack`, `markdown`, `chroma`, `weaviate`, `faiss`, `qdrant`, `pinecone`, `deepseek`, `kimi`, `qwen`, `fireworks`, `openrouter`, `together`, `minimax`, `opencode`, `ibm-bob`

> **IDE-specific installs** (`cursor`, `windsurf`, `continue`, `cline`) are not standalone `--target` values. Use `nexus-core install-agent` or manually copy the output from `--target markdown` or `--target claude`.

## Examples

```
/nexus-core:install-skill https://react.dev --target claude
/nexus-core:install-skill pallets/flask --target langchain -p standard
/nexus-core:install-skill ./docs/api.pdf --target openai
```
