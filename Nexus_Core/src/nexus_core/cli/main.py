#!/usr/bin/env python3
"""
Nexus Core - Unified CLI Entry Point

Convert documentation, codebases, and repositories into AI skills.

Usage:
    nexus-core <command> [options]

Commands:
    create               Create skill from any source (auto-detects type)
    enhance              AI-powered enhancement (auto: API or LOCAL mode)
    enhance-status       Check enhancement status (for background/daemon modes)
    package              Package skill into .zip file
    upload               Upload skill to target platform
    install              One-command workflow (scrape + enhance + package + upload)
    install-agent        Install skill to AI agent directories
    estimate             Estimate page count before scraping
    extract-test-examples Extract usage examples from test files
    resume               Resume interrupted scraping job
    config               Configure GitHub tokens, API keys, and settings
    doctor               Health check for dependencies and configuration
    scan                 AI-detect a project's tech stack and emit per-framework configs

Examples:
    nexus-core create https://react.dev
    nexus-core create owner/repo
    nexus-core create ./document.pdf
    nexus-core create configs/unity-spine.json
    nexus-core create configs/unity-spine.json --enhance-workflow unity-game-dev
    nexus-core enhance output/react/
    nexus-core package output/react/
"""

import argparse
import importlib
import sys

from nexus_core.cli import __version__


# Command classes — commands that consume the parsed args namespace directly
# (no _reconstruct_argv hack). New commands should be added here, not to
# COMMAND_MODULES. The legacy table below will shrink as commands migrate.
#
# Why a class instead of a function? It's the pattern CreateCommand already
# uses: `Cls(args).execute() -> int`. Lets the dispatcher pass the namespace
# without each command re-parsing argv.
COMMAND_CLASSES: dict[str, tuple[str, str]] = {
    "create": ("nexus_core.cli.create_command", "CreateCommand"),
    "scan": ("nexus_core.cli.scan_command", "ScanCommand"),
    "doctor": ("nexus_core.cli.doctor", "DoctorCommand"),
}


# Command module mapping (command name -> module path).
#
# Dispatch passes the parsed central namespace straight to module.main(args=...);
# each module's main() accepts an optional `args` and only re-parses argv when
# invoked standalone (the nexus-core-<cmd> entry points). The old
# _reconstruct_argv argv round-trip has been removed.
COMMAND_MODULES = {
    # NOTE: "create", "scan", "doctor" migrated to COMMAND_CLASSES above.
    # Enhancement & packaging
    "enhance": "nexus_core.cli.enhance_command",
    "enhance-status": "nexus_core.cli.enhance_status",
    "package": "nexus_core.cli.package_skill",
    "upload": "nexus_core.cli.upload_skill",
    "install": "nexus_core.cli.install_skill",
    "install-agent": "nexus_core.cli.install_agent",
    # Utilities
    "estimate": "nexus_core.cli.estimate_pages",
    "extract-test-examples": "nexus_core.cli.test_example_extractor",
    "resume": "nexus_core.cli.resume_command",
    "quality": "nexus_core.cli.quality_metrics",
    # Configuration & workflows
    "config": "nexus_core.cli.config_command",
    "workflows": "nexus_core.cli.workflows_command",
    "sync-config": "nexus_core.cli.sync_config",
    # Advanced (less common)
    "stream": "nexus_core.cli.streaming_ingest",
    "update": "nexus_core.cli.incremental_updater",
    "multilang": "nexus_core.cli.multilang_support",
}


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser with subcommands."""
    from nexus_core.cli.parsers import register_parsers

    parser = argparse.ArgumentParser(
        prog="nexus-core",
        description="Convert documentation, GitHub repos, and PDFs into AI skills",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create skill from documentation (auto-detects source type)
  nexus-core create https://docs.react.dev --name react

  # Create skill from GitHub repository
  nexus-core create microsoft/TypeScript --name typescript

  # Create skill from PDF file
  nexus-core create ./documentation.pdf --name mydocs

  # AI-powered enhancement
  nexus-core enhance output/react/

  # Package and upload
  nexus-core package output/react/
  nexus-core upload output/react.zip

For more information: https://github.com/yusufkaraaslan/Nexus_Core
        """,
    )

    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    # Create subparsers
    subparsers = parser.add_subparsers(
        dest="command",
        title="commands",
        description="Available Nexus Core commands",
        help="Command to run",
    )

    # Register all subcommand parsers
    register_parsers(subparsers)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the unified CLI.

    Args:
        argv: Command-line arguments (defaults to sys.argv)

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    if argv is None:
        argv = sys.argv[1:]

    parser = create_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 1

    # Note: ExecutionContext is initialized by individual commands (e.g., create_command,
    # enhance_command) with the correct config_path and source_info. Do NOT initialize
    # it here — commands need to set config_path which requires source detection first.

    # Class-based dispatch (new, preferred): pass parsed args to Command(args).execute()
    class_entry = COMMAND_CLASSES.get(args.command)
    if class_entry is not None:
        # create command: handle --help-* progressive-disclosure flags before execute
        if args.command == "create":
            from nexus_core.cli.arguments.create import add_create_arguments

            help_modes = {
                "_help_web": "web",
                "_help_github": "github",
                "_help_local": "local",
                "_help_pdf": "pdf",
                "_help_word": "word",
                "_help_epub": "epub",
                "_help_video": "video",
                "_help_config": "config",
                "_help_advanced": "advanced",
                "_help_all": "all",
            }
            for attr, mode in help_modes.items():
                if getattr(args, attr, False):
                    help_parser = argparse.ArgumentParser(
                        prog="nexus-core create",
                        description=f"Create skill — {mode} options",
                        formatter_class=argparse.RawDescriptionHelpFormatter,
                    )
                    add_create_arguments(help_parser, mode=mode)
                    help_parser.print_help()
                    return 0

        module_path, class_name = class_entry
        try:
            module = importlib.import_module(module_path)
            command_cls = getattr(module, class_name)
            return int(command_cls(args).execute())
        except KeyboardInterrupt:
            print("\n\nInterrupted by user", file=sys.stderr)
            return 130
        except Exception as e:
            error_msg = str(e) if str(e) else f"{type(e).__name__} occurred"
            print(f"Error: {error_msg}", file=sys.stderr)
            import traceback

            if hasattr(args, "verbose") and getattr(args, "verbose", False):
                traceback.print_exc()
            return 1

    # Module dispatch: pass the already-parsed central namespace straight to
    # module.main(args=...). Each command module's main() accepts an optional
    # `args` and only re-parses argv when called standalone (nexus-core-X
    # entry points). This replaces the old _reconstruct_argv hack, which
    # serialized the namespace back to argv and re-parsed it — fragile and, on
    # commands whose subparser dests drift from the module's own parser (e.g.
    # `workflows`), outright broken ("unrecognized arguments").
    module_name = COMMAND_MODULES.get(args.command)
    if not module_name:
        print(f"Error: Unknown command '{args.command}'", file=sys.stderr)
        parser.print_help()
        return 1

    try:
        module = importlib.import_module(module_name)
        result = module.main(args=args)
        return result if result is not None else 0

    except KeyboardInterrupt:
        print("\n\nInterrupted by user", file=sys.stderr)
        return 130
    except Exception as e:
        error_msg = str(e) if str(e) else f"{type(e).__name__} occurred"
        print(f"Error: {error_msg}", file=sys.stderr)

        # Show traceback in verbose mode
        import traceback

        if hasattr(args, "verbose") and getattr(args, "verbose", False):
            traceback.print_exc()

        return 1


if __name__ == "__main__":
    sys.exit(main())
