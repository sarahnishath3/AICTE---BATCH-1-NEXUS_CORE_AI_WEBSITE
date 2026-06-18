"""Back-compat shim — module moved to ``nexus_core.services.source_manager``.

Deprecated: import from ``nexus_core.services.source_manager`` instead.
This shim re-exports the public API and will be removed in a future major release.
"""

from nexus_core.services.source_manager import SourceManager

__all__ = ["SourceManager"]
