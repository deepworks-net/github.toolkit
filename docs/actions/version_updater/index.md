# Version Updater Action Documentation

## Overview

The **Version Updater** GitHub Action is designed to update version numbers in configuration files within a repository. It supports YAML, JSON, and generic text files, making it flexible for various workflows and file formats.

### Key Features

- Updates version numbers in YAML, JSON, and generic text files.
- Allows removing the `v` prefix from versions for standardization.
- Configurable through simple inputs for seamless integration.

---

## Inputs

### 1. `version` (Required)

- **Description**: The version number to set.
- **Type**: String
- **Required**: Yes

### 2. `files` (Optional)

- **Description**: List of file paths to update. Accepts a JSON array of file paths.
- **Type**: String
- **Default**: `[]`

### 3. `strip_v_prefix` (Optional)

- **Description**: Whether to remove the `v` prefix from the version number.
- **Type**: Boolean
- **Default**: `true`

---

## Outputs

The **Version Updater** action does not have explicit outputs but logs detailed information about the updates performed for debugging and validation.

---

## Expected Behavior

1. **When Files are Provided**:
    - The action will iterate through the list of files provided in the `files` input.
    - It identifies file types based on extensions (`.yml`, `.yaml`, `.json`, or generic text).
    - Updates the `version` field in each file to the specified version.

2. **When No Files are Provided**:
    - The action will log a warning indicating that no files were specified.

3. **File Types and Behavior**:
    - **YAML Files**: Updates `version:` fields directly.
    - **JSON Files**: Updates the `version` key in JSON objects.
    - **Generic Text Files**: Uses a regex to locate and replace `version` definitions.

4. **Edge Cases**:
    - If a file does not contain a recognizable `version` field, a warning is logged but the action continues.
    - Missing or invalid files are skipped with warnings.

---

## Example Usage

### Workflow Integration

To use the Version Updater Action in a workflow:

```yaml
name: Update Version

on:
  workflow_dispatch:  # Allows manual triggering

jobs:
  update-version:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Update Version
        uses: your-username/github.actions/path/to/version_updater@v1
        with:
          version: "v1.2.3"
          files: '["config.yml", "package.json", "README.md"]'
          strip_v_prefix: false
```

### Using Logs to Validate Changes

The action outputs logs for each file it updates, which can be reviewed for validation:

```text
Updated version in config.yml to v1.2.3
Updated version in package.json to v1.2.3
Warning: No version field found in README.md
```

---

## Debugging Tips

1. **Validate File Paths**: Ensure all file paths provided in the `files` input are correct and accessible.
2. **Check Version Format**: If `strip_v_prefix` is `true`, ensure the version format matches the expected pattern.
3. **Review Logs**: Logs provide detailed insights into which files were updated or skipped and why.

---

## File Structure

### 1. `action.yml`

Defines the inputs and runtime environment for the action.

### 2. `Dockerfile`

Specifies the container environment for running the action.

### 3. `version_updater.py`

The core Python script responsible for parsing and updating files.

---

## References

### Action Metadata

```yaml
name: Version Updater
description: Updates version numbers in configuration files
inputs:
  version:
    description: "Version number to set"
    required: true
  files:
    description: "Files to update (array of file paths)"
    required: false
    default: "[]"
  strip_v_prefix:
    description: "Remove 'v' prefix from version when updating files"
    required: false
    default: "true"

runs:
  using: "docker"
  image: "Dockerfile"
  env:
    INPUT_VERSION: ${% raw %}{{ inputs.version }}{% endraw %}
    INPUT_FILES: ${% raw %}{{ inputs.files }}{% endraw %}
    INPUT_STRIP_V_PREFIX: ${% raw %}{{ inputs.strip_v_prefix }}{% endraw %}
```

### Script Highlights

- YAML and JSON-specific update functions for precise editing.
- Generic text file support using regex for flexibility.
- Logs warnings for files without version fields or inaccessible paths.
