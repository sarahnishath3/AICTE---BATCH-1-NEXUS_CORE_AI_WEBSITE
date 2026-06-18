"""Back-compat shim — module moved to ``nexus_core.services.git_repo``.

Deprecated: import from ``nexus_core.services.git_repo`` instead.
This shim re-exports the public API and will be removed in a future major release.
"""

from nexus_core.services.git_repo import GitConfigRepo

__all__ = ["GitConfigRepo"]
