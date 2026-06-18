# Legacy Documentation Archive

> **Status:** Archived  
> **Reason:** Outdated patterns, phantom commands, or superseded by new docs

---

## Archived Files

| File | Reason | Replaced By |
|------|--------|-------------|
| `QUICKSTART.md` | Old CLI patterns | `docs/getting-started/02-quick-start.md` |
| `USAGE.md` | `python3 cli/X.py` pattern | `docs/user-guide/` + `docs/reference/CLI_REFERENCE.md` |
| `QUICK_REFERENCE.md` | Phantom commands | `docs/reference/CLI_REFERENCE.md` |

---

## Why These Were Archived

### QUICKSTART.md

**Issues:**
- Referenced `pip3 install requests beautifulsoup4` instead of `pip install nexus-core`
- Missing modern commands like `create`

**Use Instead:** [docs/getting-started/02-quick-start.md](../../getting-started/02-quick-start.md)

---

### USAGE.md

**Issues:**
- Used `python3 cli/doc_scraper.py` pattern (removed in v3.x)
- Referenced `python3 cli/enhance_skill_local.py` (now `nexus-core enhance`)
- Referenced `python3 cli/estimate_pages.py` (now `nexus-core estimate`)

**Use Instead:**
- [docs/reference/CLI_REFERENCE.md](../../reference/CLI_REFERENCE.md) - Complete command reference
- [docs/user-guide/](../../user-guide/) - Common tasks

---

### QUICK_REFERENCE.md

**Issues:**
- Documented phantom commands like `nexus-core merge-sources`
- Documented phantom commands like `nexus-core split-config`
- Documented phantom commands like `nexus-core generate-router`

**Use Instead:** [docs/reference/CLI_REFERENCE.md](../../reference/CLI_REFERENCE.md)

---

## Current Documentation

For up-to-date documentation, see:

- [docs/README.md](../../README.md) - Documentation hub
- [docs/getting-started/](../../getting-started/) - New user guides
- [docs/user-guide/](../../user-guide/) - Common tasks
- [docs/reference/](../../reference/) - Technical reference
- [docs/advanced/](../../advanced/) - Power user topics

---

*Last archived: 2026-02-16*
