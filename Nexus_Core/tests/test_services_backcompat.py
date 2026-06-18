"""Back-compat shims: old nexus_core.mcp.* paths re-export nexus_core.services.*.

The domain modules moved to nexus_core.services in the Phase 5a MCP
unification; thin shims remain at the old mcp/ paths so external imports keep
working. These tests pin each shim to the real services object (identity, not
just importability) so a drifting shim fails loudly.
"""


def test_marketplace_manager_shim():
    from nexus_core.mcp.marketplace_manager import MarketplaceManager as ShimClass
    from nexus_core.services.marketplace_manager import MarketplaceManager

    assert ShimClass is MarketplaceManager


def test_marketplace_publisher_shim():
    from nexus_core.mcp.marketplace_publisher import MarketplacePublisher as ShimClass
    from nexus_core.services.marketplace_publisher import MarketplacePublisher

    assert ShimClass is MarketplacePublisher


def test_config_publisher_shim():
    from nexus_core.mcp.config_publisher import (
        CATEGORY_KEYWORDS as SHIM_KEYWORDS,
    )
    from nexus_core.mcp.config_publisher import (
        ConfigPublisher as ShimClass,
    )
    from nexus_core.mcp.config_publisher import (
        detect_category as shim_detect_category,
    )
    from nexus_core.services.config_publisher import (
        CATEGORY_KEYWORDS,
        ConfigPublisher,
        detect_category,
    )

    assert ShimClass is ConfigPublisher
    assert shim_detect_category is detect_category
    assert SHIM_KEYWORDS is CATEGORY_KEYWORDS


def test_source_manager_shim():
    from nexus_core.mcp.source_manager import SourceManager as ShimClass
    from nexus_core.services.source_manager import SourceManager

    assert ShimClass is SourceManager


def test_git_repo_shim():
    from nexus_core.mcp.git_repo import GitConfigRepo as ShimClass
    from nexus_core.services.git_repo import GitConfigRepo

    assert ShimClass is GitConfigRepo


def test_services_package_has_no_mcp_dependency():
    """services/ must import cleanly without reaching into nexus_core.mcp."""
    import subprocess
    import sys

    code = (
        "import sys\n"
        "import nexus_core.services.config_publisher\n"
        "import nexus_core.services.marketplace_manager\n"
        "import nexus_core.services.marketplace_publisher\n"
        "import nexus_core.services.source_manager\n"
        "import nexus_core.services.git_repo\n"
        "assert 'nexus_core.mcp' not in sys.modules, 'services imported nexus_core.mcp'\n"
    )
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
