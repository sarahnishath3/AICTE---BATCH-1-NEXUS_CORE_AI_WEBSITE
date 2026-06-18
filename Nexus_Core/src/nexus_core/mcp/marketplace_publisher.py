"""Back-compat shim — module moved to ``nexus_core.services.marketplace_publisher``.

Deprecated: import from ``nexus_core.services.marketplace_publisher`` instead.
This shim re-exports the public API and will be removed in a future major release.
"""

from nexus_core.services.marketplace_publisher import MarketplacePublisher

__all__ = ["MarketplacePublisher"]
