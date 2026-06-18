"""Test suite for Python package structure.

Tests that the package structure is correct and imports work properly.
This ensures modern Python packaging (src/ layout, pyproject.toml) is successful.
"""

import sys
from pathlib import Path

import pytest


class TestCliPackage:
    """Test nexus_core.cli package structure and imports."""

    def test_cli_package_exists(self):
        """Test that nexus_core.cli package can be imported."""
        import nexus_core.cli

        assert nexus_core.cli is not None

    def test_cli_has_version(self):
        """Test that nexus_core.cli package has __version__."""
        import nexus_core.cli

        assert hasattr(nexus_core.cli, "__version__")
        assert nexus_core.cli.__version__ == "3.9.0.dev0"

    def test_cli_has_all(self):
        """Test that nexus_core.cli package has __all__ export list."""
        import nexus_core.cli

        assert hasattr(nexus_core.cli, "__all__")
        assert isinstance(nexus_core.cli.__all__, list)
        assert len(nexus_core.cli.__all__) > 0

    def test_llms_txt_detector_import(self):
        """Test that LlmsTxtDetector can be imported from nexus_core.cli."""
        from nexus_core.cli import LlmsTxtDetector

        assert LlmsTxtDetector is not None

    def test_llms_txt_downloader_import(self):
        """Test that LlmsTxtDownloader can be imported from nexus_core.cli."""
        from nexus_core.cli import LlmsTxtDownloader

        assert LlmsTxtDownloader is not None

    def test_llms_txt_parser_import(self):
        """Test that LlmsTxtParser can be imported from nexus_core.cli."""
        from nexus_core.cli import LlmsTxtParser

        assert LlmsTxtParser is not None

    def test_open_folder_import(self):
        """Test that open_folder can be imported from nexus_core.cli (if utils exists)."""
        try:
            from nexus_core.cli import open_folder

            # If import succeeds, function should not be None
            assert open_folder is not None
        except ImportError:
            # If utils.py doesn't exist, that's okay for now
            pytest.skip("utils.py not found, skipping open_folder test")

    def test_cli_exports_match_all(self):
        """Test that exported items in __all__ can actually be imported."""
        import nexus_core.cli as cli

        for item_name in cli.__all__:
            if item_name == "open_folder" and cli.open_folder is None:
                # open_folder might be None if utils doesn't exist
                continue
            assert hasattr(cli, item_name), f"{item_name} not found in cli package"


class TestMcpPackage:
    """Test nexus_core.mcp package structure and imports."""

    def test_mcp_package_exists(self):
        """Test that nexus_core.mcp package can be imported."""
        import nexus_core.mcp

        assert nexus_core.mcp is not None

    def test_mcp_has_version(self):
        """Test that nexus_core.mcp package has __version__."""
        import nexus_core.mcp

        assert hasattr(nexus_core.mcp, "__version__")
        assert nexus_core.mcp.__version__ == "3.9.0.dev0"

    def test_mcp_has_all(self):
        """Test that nexus_core.mcp package has __all__ export list."""
        import nexus_core.mcp

        assert hasattr(nexus_core.mcp, "__all__")
        assert isinstance(nexus_core.mcp.__all__, list)

    def test_mcp_tools_package_exists(self):
        """Test that nexus_core.mcp.tools subpackage can be imported."""
        import nexus_core.mcp.tools

        assert nexus_core.mcp.tools is not None

    def test_mcp_tools_has_version(self):
        """Test that nexus_core.mcp.tools has __version__."""
        import nexus_core.mcp.tools

        assert hasattr(nexus_core.mcp.tools, "__version__")
        assert nexus_core.mcp.tools.__version__ == "3.9.0.dev0"


class TestPackageStructure:
    """Test overall package structure integrity (src/ layout)."""

    def test_cli_init_file_exists(self):
        """Test that src/nexus_core/cli/__init__.py exists."""
        init_file = Path(__file__).parent.parent / "src" / "nexus_core" / "cli" / "__init__.py"
        assert init_file.exists(), "src/nexus_core/cli/__init__.py not found"

    def test_mcp_init_file_exists(self):
        """Test that src/nexus_core/mcp/__init__.py exists."""
        init_file = Path(__file__).parent.parent / "src" / "nexus_core" / "mcp" / "__init__.py"
        assert init_file.exists(), "src/nexus_core/mcp/__init__.py not found"

    def test_mcp_tools_init_file_exists(self):
        """Test that src/nexus_core/mcp/tools/__init__.py exists."""
        init_file = (
            Path(__file__).parent.parent / "src" / "nexus_core" / "mcp" / "tools" / "__init__.py"
        )
        assert init_file.exists(), "src/nexus_core/mcp/tools/__init__.py not found"

    def test_cli_init_has_docstring(self):
        """Test that nexus_core.cli/__init__.py has a module docstring."""
        import nexus_core.cli

        assert nexus_core.cli.__doc__ is not None
        assert len(nexus_core.cli.__doc__) > 50  # Should have substantial documentation

    def test_mcp_init_has_docstring(self):
        """Test that nexus_core.mcp/__init__.py has a module docstring."""
        import nexus_core.mcp

        assert nexus_core.mcp.__doc__ is not None
        assert len(nexus_core.mcp.__doc__) > 50  # Should have substantial documentation


class TestImportPatterns:
    """Test that various import patterns work correctly."""

    def test_direct_module_import(self):
        """Test importing modules directly."""
        from nexus_core.cli import llms_txt_detector, llms_txt_downloader, llms_txt_parser

        assert llms_txt_detector is not None
        assert llms_txt_downloader is not None
        assert llms_txt_parser is not None

    def test_class_import_from_package(self):
        """Test importing classes from package."""
        from nexus_core.cli import LlmsTxtDetector, LlmsTxtDownloader, LlmsTxtParser

        assert LlmsTxtDetector.__name__ == "LlmsTxtDetector"
        assert LlmsTxtDownloader.__name__ == "LlmsTxtDownloader"
        assert LlmsTxtParser.__name__ == "LlmsTxtParser"

    def test_package_level_import(self):
        """Test importing entire packages."""
        assert "nexus_core" in sys.modules
        assert "nexus_core.cli" in sys.modules
        assert "nexus_core.mcp" in sys.modules
        assert "nexus_core.mcp.tools" in sys.modules


class TestBackwardsCompatibility:
    """Test that existing code patterns still work."""

    def test_direct_file_import_still_works(self):
        """Test that direct file imports still work (backwards compatible)."""
        # This ensures we didn't break existing code
        from nexus_core.cli.llms_txt_detector import LlmsTxtDetector
        from nexus_core.cli.llms_txt_downloader import LlmsTxtDownloader
        from nexus_core.cli.llms_txt_parser import LlmsTxtParser

        assert LlmsTxtDetector is not None
        assert LlmsTxtDownloader is not None
        assert LlmsTxtParser is not None

    def test_module_path_import_still_works(self):
        """Test that full module path imports still work."""
        import nexus_core.cli.llms_txt_detector
        import nexus_core.cli.llms_txt_downloader
        import nexus_core.cli.llms_txt_parser

        assert nexus_core.cli.llms_txt_detector is not None
        assert nexus_core.cli.llms_txt_downloader is not None
        assert nexus_core.cli.llms_txt_parser is not None


class TestRootPackage:
    """Test root nexus_core package."""

    def test_root_package_exists(self):
        """Test that nexus_core root package can be imported."""
        import nexus_core

        assert nexus_core is not None

    def test_root_has_version(self):
        """Test that nexus_core root package has __version__."""
        import nexus_core

        assert hasattr(nexus_core, "__version__")
        assert nexus_core.__version__ == "3.9.0.dev0"

    def test_root_has_metadata(self):
        """Test that nexus_core root package has metadata."""
        import nexus_core

        assert hasattr(nexus_core, "__author__")
        assert hasattr(nexus_core, "__license__")
        assert nexus_core.__license__ == "MIT"


class TestCLIEntryPoints:
    """Test that CLI entry points are properly configured."""

    def test_main_cli_module_exists(self):
        """Test that main.py module exists and can be imported."""
        from nexus_core.cli import main

        assert main is not None
        assert hasattr(main, "main")
        assert callable(main.main)

    def test_main_cli_has_parser(self):
        """Test that main.py has parser creation function."""
        from nexus_core.cli.main import create_parser

        parser = create_parser()
        assert parser is not None
        # Test that main subcommands are configured
        assert parser.prog == "nexus-core"
