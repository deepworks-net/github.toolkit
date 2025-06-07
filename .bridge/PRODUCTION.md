# FCM Bridge Production Guide

## Overview

The FCM Bridge is now production-ready. All GitHub Actions are generated from Formal Conceptual Models (FCMs).

## Production Workflow

1. **Edit FCMs** - Modify axiom definitions in `axioms/`
2. **Generate Actions** - Run `make -f Makefile.bridge generate`
3. **Validate Actions** - Run `make -f Makefile.bridge validate`
4. **Commit Both** - Commit FCMs and generated actions together
5. **CI/CD** - Automated pipeline ensures synchronization

## Key Commands

```bash
# Generate all actions from FCMs
make -f Makefile.bridge generate

# Validate all generated actions
make -f Makefile.bridge validate

# Check synchronization
make -f Makefile.bridge sync

# Full pipeline
make -f Makefile.bridge all
```

## Architecture

```
axioms/           # FCM definitions (source of truth)
├── git/         # Git operation axioms
├── github/      # GitHub-specific axioms
├── release/     # Release management axioms
└── version/     # Version control axioms

actions/          # Generated GitHub Actions
├── core/        # Core atomic actions
└── composite/   # Composite workflow actions

.bridge/          # Bridge infrastructure
├── production-generator.sh
├── production-validator.sh
└── *.bridge-sync metadata
```

## Self-Updating System

The bridge is self-updating:
- CI/CD monitors FCM changes
- Automatically regenerates actions
- Validates before committing
- Maintains synchronization

## Production Checklist

- [ ] All actions have FCM sources
- [ ] Generated actions pass validation
- [ ] CI/CD pipeline active
- [ ] Team trained on FCM editing
- [ ] Backup of manual actions archived
