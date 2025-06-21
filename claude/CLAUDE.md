# Claude Code Configuration

This document provides configuration and context for Claude Code when working with the GitHub Toolkit project.

## Project Overview

GitHub Toolkit is a collection of GitHub Actions that provide various operations for Git workflows, version management, and CI/CD pipelines.

## Key Directories

- `/actions/` - Contains all the GitHub Actions
- `/docs/` - Project documentation
- `/tests/` - Test files and test framework
- `/claude/` - Claude Code specific configuration
  - `/claude/config/` - Configuration files
  - `/claude/models/` - Model definitions
  - `/claude/validation/` - Validation schemas

## Development Guidelines

1. Follow existing code patterns and conventions
2. Ensure all changes pass linting and type checking
3. Write tests for new functionality
4. Update documentation when adding new features

## Testing

Run tests using the appropriate commands based on the test framework in use. Check the README or package.json for specific test commands.

## Code Style

- Follow the existing code style in the repository
- Use proper error handling
- Add appropriate logging for debugging
- Keep functions focused and single-purpose

## Git Workflow

- Current branch: `develop/bridge_upgrade`
- Main branch: `main`
- Create meaningful commit messages
- Ensure all tests pass before committing