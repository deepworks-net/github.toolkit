# Repository Audit & Cleanup Tracking

**Purpose**: This document serves as a whitelist for what should remain in the final, clean repository structure.

**Status**: Starting - Empty Whitelist

---

## ✅ WHITELIST - APPROVED TO KEEP

### Core Structure
- `README.md` - Main documentation with action naming convention explained
- `CHANGELOG.md` - Version history
- `LICENSE` - Legal requirements
- `mkdocs.yml` - Documentation site configuration
- `requirements.txt` - Python dependencies
- `Makefile.bridge` - FCM bridge operations
- `analyze-actions.py` - Development analysis tool
- `test-bridge.sh` - FCM bridge testing tool
- `docker-compose.yml` - Docker configuration
- `Dockerfile` - Container definition

### FCM System
- `axioms/` - Complete FCM source definitions
- `.bridge/` - FCM generation system (assumed present)

### Actions (Both Generated and Manual)
- `actions/core/` - All core actions (both hyphen and underscore naming)
- `actions/composite/` - All composite actions
- `actions/shared/` - Shared utilities
- `actions/test_framework/` - Testing framework

### Documentation
- `docs/` - Complete MkDocs documentation structure
- `docs/guides/` - Comprehensive guides
- `docs/examples/` - Complete action examples

### Examples
- `examples/complete-action-example/` - Reference implementation

### Workflows
- `workflows/` - High-level workflow definitions
- `.github/workflows/` - CI/CD automation (assumed present)

### Claude Integration
- `claude/` - Complete Claude Code Docker sidecar with FCM compliance
- `docker.claude-code/` - Docker mount point for Claude Code operation

---

**Last Updated**: Comprehensive whitelist populated after cleanup completion  
**Status**: Repository cleanup complete - all major components approved