"""
Interactive Setup Wizard for Nexus Core

Guides users through installation options on first run.
"""

from pathlib import Path


def show_installation_guide():
    """Show installation options"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║              Nexus Core Setup Guide                    ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

Choose your installation profile:

1️⃣  CLI Only (Skill Generation)
   pip install nexus-core

   Features:
   • Scrape documentation websites
   • Analyze GitHub repositories
   • Extract from PDFs
   • Package skills for all platforms

2️⃣  MCP Integration (Claude Code, Cursor, Windsurf)
   pip install nexus-core[mcp]

   Features:
   • Everything from CLI Only
   • MCP server for Claude Code
   • One-command skill installation
   • HTTP/stdio transport modes

3️⃣  Multi-LLM Support (Gemini, OpenAI)
   pip install nexus-core[all-llms]

   Features:
   • Everything from CLI Only
   • Google Gemini support
   • OpenAI ChatGPT support
   • Enhanced AI features

4️⃣  Everything
   pip install nexus-core[all]

   Features:
   • All features enabled
   • Maximum flexibility

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Current installation: pip install nexus-core
Upgrade with: pip install -U nexus-core[mcp]

For configuration wizard:
  nexus-core config

For help:
  nexus-core --help

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")


def check_first_run():
    """Check if this is first run"""
    flag_file = Path.home() / ".config" / "nexus-core" / ".setup_shown"

    if not flag_file.exists():
        show_installation_guide()

        # Create flag to not show again
        flag_file.parent.mkdir(parents=True, exist_ok=True)
        flag_file.touch()

        input("\nPress Enter to continue...")
        return True

    return False


def main():
    """Show wizard"""
    show_installation_guide()


if __name__ == "__main__":
    main()
