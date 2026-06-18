# Nexus Core — Claude Code Plugin

Transform 18 source types into AI-ready skills and RAG knowledge, directly from Claude Code.

## Installation

### From the Official Plugin Directory

```
/plugin install nexus-core@claude-plugin-directory
```

Or browse for it in `/plugin > Discover`.

### Local Installation (for development)

```bash
claude --plugin-dir ./path/to/nexus-core-plugin
```

### Prerequisites

The plugin requires `nexus-core` to be installed:

```bash
pip install nexus-core[mcp]
```

## What's Included

### MCP Server (40 tools)

The plugin bundles the Nexus Core MCP server providing tools for:
- Scraping documentation, GitHub repos, PDFs, videos, and 13 other source types
- Packaging skills for 21+ LLM platforms
- Exporting to vector databases (Weaviate, Chroma, FAISS, Qdrant)
- Managing configs, workflows, and sources

### Slash Commands

| Command | Description |
|---------|-------------|
| `/nexus-core:create-skill <source>` | Create a skill from any source (auto-detects type) |
| `/nexus-core:sync-config <config>` | Sync config URLs against live docs |
| `/nexus-core:install-skill <source>` | End-to-end: fetch, scrape, enhance, package, install |

### Agent Skill

The **skill-builder** skill is automatically available to Claude. It detects source types and uses the appropriate MCP tools to build skills autonomously.

## Usage Examples

```
# Create a skill from a documentation site
/nexus-core:create-skill https://react.dev

# Create from a GitHub repo, targeting LangChain
/nexus-core:create-skill pallets/flask --target langchain

# Full install workflow with AI enhancement
/nexus-core:install-skill https://fastapi.tiangolo.com --enhance

# Sync an existing config
/nexus-core:sync-config react
```

Or just ask Claude naturally:
> "Create an AI skill from the React documentation"
> "Scrape the Flask GitHub repo and package it for OpenAI"
> "Export my skill to a Chroma vector database"

The skill-builder agent skill will automatically detect the intent and use the right tools.

## Remote MCP Alternative

By default, the plugin runs the MCP server locally via `python -m nexus_core.mcp.server_fastmcp`. To use a remote server instead, edit `.mcp.json`:

```json
{
  "nexus-core": {
    "type": "http",
    "url": "https://your-hosted-server.com/mcp"
  }
}
```

## Supported Source Types

Documentation (web), GitHub repos, PDFs, Word docs, EPUBs, videos, local codebases, Jupyter notebooks, HTML files, OpenAPI specs, AsciiDoc, PowerPoint, RSS/Atom feeds, man pages, Confluence, Notion, Slack/Discord exports.

## License

MIT — https://github.com/yusufkaraaslan/Nexus_Core
