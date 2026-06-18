#!/usr/bin/env python3
"""
Tests for CLI Parser System

Tests the modular parser registration system.
"""

import argparse
import pytest

from nexus_core.cli.parsers import (
    PARSERS,
    SubcommandParser,
    get_parser_names,
    register_parsers,
)
from nexus_core.cli.parsers.package_parser import PackageParser


class TestParserRegistry:
    """Test parser registry functionality."""

    def test_all_parsers_registered(self):
        """Test that all parsers are registered."""
        assert len(PARSERS) == 19, f"Expected 19 parsers, got {len(PARSERS)}"

    def test_get_parser_names(self):
        """Test getting list of parser names."""
        names = get_parser_names()
        assert len(names) == 19
        assert "create" in names
        assert "package" in names
        assert "upload" in names
        assert "config" in names
        assert "workflows" in names

    def test_all_parsers_are_subcommand_parsers(self):
        """Test that all parsers inherit from SubcommandParser."""
        for parser in PARSERS:
            assert isinstance(parser, SubcommandParser)

    def test_all_parsers_have_required_properties(self):
        """Test that all parsers have name, help, description."""
        for parser in PARSERS:
            assert hasattr(parser, "name")
            assert hasattr(parser, "help")
            assert hasattr(parser, "description")
            assert isinstance(parser.name, str)
            assert isinstance(parser.help, str)
            assert isinstance(parser.description, str)
            assert len(parser.name) > 0
            assert len(parser.help) > 0

    def test_all_parsers_have_add_arguments_method(self):
        """Test that all parsers implement add_arguments."""
        for parser in PARSERS:
            assert hasattr(parser, "add_arguments")
            assert callable(parser.add_arguments)

    def test_no_duplicate_parser_names(self):
        """Test that all parser names are unique."""
        names = [p.name for p in PARSERS]
        assert len(names) == len(set(names)), "Duplicate parser names found!"


class TestParserCreation:
    """Test parser creation functionality."""

    def test_package_parser_creates_subparser(self):
        """Test that PackageParser creates valid subparser."""
        main_parser = argparse.ArgumentParser()
        subparsers = main_parser.add_subparsers()

        package_parser = PackageParser()
        subparser = package_parser.create_parser(subparsers)

        assert subparser is not None
        assert package_parser.name == "package"

    def test_register_parsers_creates_all_subcommands(self):
        """Test that register_parsers creates all subcommands."""
        main_parser = argparse.ArgumentParser()
        subparsers = main_parser.add_subparsers(dest="command")

        # Register all parsers
        register_parsers(subparsers)

        # Test that existing commands can be parsed
        test_commands = [
            "config --show",
            "package output/test/",
            "upload test.zip",
            "enhance output/test/",
            "estimate test.json",
        ]

        for cmd in test_commands:
            args = main_parser.parse_args(cmd.split())
            assert args.command is not None


class TestSpecificParsers:
    """Test specific parser implementations."""

    def test_package_parser_arguments(self):
        """Test PackageParser has correct arguments."""
        main_parser = argparse.ArgumentParser()
        subparsers = main_parser.add_subparsers(dest="command")

        package_parser = PackageParser()
        package_parser.create_parser(subparsers)

        args = main_parser.parse_args(["package", "output/test/"])
        assert args.command == "package"
        assert args.skill_directory == "output/test/"

        args = main_parser.parse_args(["package", "output/test/", "--target", "gemini"])
        assert args.target == "gemini"

        args = main_parser.parse_args(["package", "output/test/", "--target", "ibm-bob"])
        assert args.target == "ibm-bob"

        args = main_parser.parse_args(["package", "output/test/", "--no-open"])
        assert args.no_open is True


class TestCurrentCommands:
    """Test current CLI commands after Grand Unification."""

    def test_all_current_commands_registered(self):
        """Test that all current commands are registered."""
        names = get_parser_names()

        # Commands that survived the Grand Unification
        # (individual scraper commands removed; use 'create' instead)
        current_commands = [
            "config",
            "create",
            "enhance",
            "enhance-status",
            "package",
            "upload",
            "estimate",
            "extract-test-examples",
            "install-agent",
            "install",
            "resume",
            "stream",
            "update",
            "multilang",
            "quality",
            "doctor",
            "workflows",
            "sync-config",
        ]

        for cmd in current_commands:
            assert cmd in names, f"Command '{cmd}' not found in parser registry!"

    def test_removed_scraper_commands_not_present(self):
        """Test that individual scraper commands were removed."""
        names = get_parser_names()

        removed_commands = [
            "scrape",
            "github",
            "pdf",
            "video",
            "word",
            "epub",
            "jupyter",
            "html",
            "openapi",
            "asciidoc",
            "pptx",
            "rss",
            "manpage",
            "confluence",
            "notion",
            "chat",
        ]

        for cmd in removed_commands:
            assert cmd not in names, f"Removed command '{cmd}' still in parser registry!"

    def test_command_count_matches(self):
        """Test that we have exactly 19 commands."""
        assert len(PARSERS) == 19
        assert len(get_parser_names()) == 19


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


def _capture_module_parser(module_main):
    """Capture the parser a module main() builds, without running it.

    Spies on ArgumentParser.parse_args: main(args=None) builds its parser and
    calls parse_args(), at which point we grab the parser and abort.
    """
    captured = {}

    class _Sentinel(Exception):
        pass

    original_parse = argparse.ArgumentParser.parse_args

    def spy_parse(self_parser, *_a, **_k):
        captured["parser"] = self_parser
        raise _Sentinel

    argparse.ArgumentParser.parse_args = spy_parse
    try:
        module_main(args=None)
    except _Sentinel:
        pass
    except SystemExit:
        # Some mains exit before parsing when an optional dep is missing
        # (e.g. install without the mcp extra).
        pass
    finally:
        argparse.ArgumentParser.parse_args = original_parse
    if "parser" not in captured:
        pytest.skip("module main() exited before building its parser (optional dep missing)")
    return captured["parser"]


class TestCentralModuleParserSync:
    """Central parsers must accept every flag the command modules define.

    A flag defined in a module's main() parser but missing from the central
    SubcommandParser is REJECTED by the unified CLI with 'unrecognized
    arguments' before main() ever runs — backfill_parser_defaults can only
    patch absent attributes, not rescue rejected flags. These were real
    shipping bugs (estimate --unlimited, update --apply-update, ...).
    """

    @pytest.fixture(scope="class")
    def central_parser(self):
        from nexus_core.cli.main import create_parser

        return create_parser()

    @pytest.mark.parametrize(
        "argv",
        [
            ["estimate", "x.json", "--unlimited"],
            ["estimate", "x.json", "--timeout", "5"],
            ["update", "dir/", "--generate-package", "pkg.json"],
            ["update", "dir/", "--apply-update", "pkg.json"],
            ["quality", "dir/", "--output", "report.json"],
            ["stream", "big.md", "--streaming-overlap-chars", "100"],
            ["stream", "big.md", "--batch-size", "10", "--checkpoint", "c.json"],
            ["stream", "big.md", "--output", "out/"],
            ["multilang", "dir/", "--report"],
            ["multilang", "dir/", "--export", "out/"],
            ["multilang", "dir/", "--languages", "en", "es", "--detect"],
        ],
    )
    def test_previously_drifted_flags_parse(self, central_parser, argv):
        args = central_parser.parse_args(argv)
        assert args.command == argv[0]

    def _module_parser(self, module_main):
        """Capture the parser a module main() builds, without running it."""
        return _capture_module_parser(module_main)

    @pytest.mark.parametrize(
        "command,module_path",
        [
            ("estimate", "nexus_core.cli.estimate_pages"),
            ("update", "nexus_core.cli.incremental_updater"),
            ("quality", "nexus_core.cli.quality_metrics"),
            ("stream", "nexus_core.cli.streaming_ingest"),
            ("multilang", "nexus_core.cli.multilang_support"),
        ],
    )
    def test_no_module_flag_missing_from_central(self, central_parser, command, module_path):
        """Drift guard: every option dest in the module parser must exist in
        the central subcommand parser (so the unified CLI accepts it)."""
        import importlib

        module = importlib.import_module(module_path)
        module_parser = self._module_parser(module.main)

        # Find the central subparser for this command
        subparsers_action = next(
            a for a in central_parser._actions if isinstance(a, argparse._SubParsersAction)
        )
        central_sub = subparsers_action.choices[command]

        central_dests = {a.dest for a in central_sub._actions}
        module_dests = {a.dest for a in module_parser._actions if a.dest != "help"}
        missing = module_dests - central_dests
        assert not missing, (
            f"'{command}' module parser defines flags the central parser lacks "
            f"(unified CLI will reject them): {sorted(missing)}"
        )


# Commands migrated to single-definition parsers (Phase 5c): the module's
# main(args=None) standalone path builds its parser FROM the central
# SubcommandParser class, so flags exist in exactly one place.
SINGLE_SOURCE_COMMANDS = [
    ("config", "nexus_core.cli.config_command"),
    ("enhance-status", "nexus_core.cli.enhance_status"),
    ("upload", "nexus_core.cli.upload_skill"),
    ("install", "nexus_core.cli.install_skill"),
    ("install-agent", "nexus_core.cli.install_agent"),
    ("estimate", "nexus_core.cli.estimate_pages"),
    ("extract-test-examples", "nexus_core.cli.test_example_extractor"),
    ("resume", "nexus_core.cli.resume_command"),
    ("quality", "nexus_core.cli.quality_metrics"),
    ("workflows", "nexus_core.cli.workflows_command"),
    ("stream", "nexus_core.cli.streaming_ingest"),
    ("update", "nexus_core.cli.incremental_updater"),
    ("multilang", "nexus_core.cli.multilang_support"),
]


class TestCentralParserSingleSource:
    """Phase 5c: each migrated command's flags are defined exactly once.

    The module's standalone path (main(args=None)) must build a parser that
    is INDISTINGUISHABLE from the central SubcommandParser — same option
    dests AND same defaults. If someone re-adds a module-local add_argument
    block (or the central parser changes without the module following,
    which can't happen while the module builds FROM the central class),
    this fails.
    """

    @pytest.fixture(scope="class")
    def central_parser(self):
        from nexus_core.cli.main import create_parser

        return create_parser()

    @staticmethod
    def _dests_and_defaults(parser):
        return {a.dest: a.default for a in parser._actions if a.dest != "help"}

    @pytest.mark.parametrize(
        "command,module_path", SINGLE_SOURCE_COMMANDS, ids=[c for c, _ in SINGLE_SOURCE_COMMANDS]
    )
    def test_module_parser_identical_to_central(self, central_parser, command, module_path):
        import importlib

        module = importlib.import_module(module_path)
        module_parser = _capture_module_parser(module.main)

        subparsers_action = next(
            a for a in central_parser._actions if isinstance(a, argparse._SubParsersAction)
        )
        central_sub = subparsers_action.choices[command]

        central = self._dests_and_defaults(central_sub)
        module_map = self._dests_and_defaults(module_parser)
        assert module_map == central, (
            f"'{command}' module parser drifted from its central SubcommandParser.\n"
            f"  module-only/changed: "
            f"{ {k: v for k, v in module_map.items() if central.get(k, object()) != v} }\n"
            f"  central-only/changed: "
            f"{ {k: v for k, v in central.items() if module_map.get(k, object()) != v} }"
        )

    @pytest.mark.parametrize(
        "command,module_path", SINGLE_SOURCE_COMMANDS, ids=[c for c, _ in SINGLE_SOURCE_COMMANDS]
    )
    def test_option_strings_identical_to_central(self, central_parser, command, module_path):
        """Flags (not just dests) must match — catches alias drift like -m/-u/-t."""
        import importlib

        module = importlib.import_module(module_path)
        module_parser = _capture_module_parser(module.main)

        subparsers_action = next(
            a for a in central_parser._actions if isinstance(a, argparse._SubParsersAction)
        )
        central_sub = subparsers_action.choices[command]

        def option_strings(parser):
            return {tuple(a.option_strings) for a in parser._actions if a.dest != "help"}

        assert option_strings(module_parser) == option_strings(central_sub)
