# Repository Cleanup Progress

**Purpose**: Track progress, issues, and decisions during repository cleanup process.

**Status**: 🔄 In Progress - Phase 1 Cleanup

---

## 📋 Executive Summary

### Issues Identified
- [ ] Duplicated action implementations (hyphen vs underscore naming)
- [ ] Inconsistent directory structures
- [ ] Mixed generated vs manual content
- [ ] Outdated references in documentation
- [ ] Incomplete navigation structure

### Cleanup Objectives
1. **Consolidate Duplicates**: Remove redundant implementations
2. **Standardize Structure**: Consistent naming and organization
3. **Clear Generated vs Manual**: Proper separation and documentation
4. **Update Documentation**: Ensure all references are current
5. **Optimize Navigation**: Logical, complete documentation structure

---

## 🎯 Cleanup Action Plan

### Phase 1: Duplicate Removal
- [ ] **Decision**: Choose between hyphen (generated) vs underscore (manual) actions
- [ ] **Remove**: All `-generated` suffixed directories
- [ ] **Remove**: Loose action files in wrong locations
- [ ] **Remove**: Stage2 and development artifacts

### Phase 2: Structure Standardization  
- [ ] **Consolidate**: Core actions into consistent structure
- [ ] **Organize**: Composite actions properly
- [ ] **Clean**: Remove orphaned files

### Phase 3: Documentation Alignment
- [ ] **Update**: All documentation references
- [ ] **Verify**: Navigation completeness
- [ ] **Test**: All documentation links

### Phase 4: Final Validation
- [ ] **Test**: All workflows and actions
- [ ] **Verify**: FCM bridge operations
- [ ] **Validate**: Documentation site generation

---

## 📊 Progress Tracking

### Completed ✅
- [x] Created comprehensive documentation guides
- [x] Added complete action example
- [x] Updated navigation structure
- [x] Fixed Jinja2 template issues

### In Progress 🔄
- [ ] Repository structure audit (whitelist)
- [ ] Duplicate identification and removal plan
- [ ] Standardization strategy

### Pending ⏳
- [ ] Action consolidation decisions
- [ ] Cleanup execution
- [ ] Final validation

---

## 🔍 Key Decisions Needed

### 1. Action Naming Convention
**Question**: Hyphen (generated) vs Underscore (manual) actions?
- **Option A**: Keep both, clearly document difference
- **Option B**: Standardize on underscores, update bridge
- **Option C**: Standardize on hyphens, update manual actions

### 2. Generated vs Manual Actions
**Question**: How to handle actions that exist in both forms?
- Clear separation of concerns
- Documentation of which is which
- Bridge system updates

### 3. Directory Cleanup
**Question**: What to do with unclear directories (claude/, mechanics/, etc.)?
- Investigate purpose
- Move to archive if unused
- Document if keeping

---

## 📝 Notes

- This document tracks the cleanup process and decisions
- Items move from this document to REPOSITORY_AUDIT.md whitelist when approved
- Each phase must be completed before moving to the next

**Last Updated**: Initial Creation  
**Next Review**: After whitelist population