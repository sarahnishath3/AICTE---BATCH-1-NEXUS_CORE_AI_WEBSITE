"""Back-compat shim — module moved to ``nexus_core.services.marketplace_manager``.

Deprecated: import from ``nexus_core.services.marketplace_manager`` instead.
This shim re-exports the public API and will be removed in a future major release.
"""

from nexus_core.services.marketplace_manager import MarketplaceManager

__all__ = ["MarketplaceManager"]
