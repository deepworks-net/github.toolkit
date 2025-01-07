# Version Updater Workflow Documentation

## Overview

The **Version Updater Workflow** is a reusable GitHub workflow designed to update version numbers in specified configuration files. It integrates seamlessly into external repositories for consistent version management across various file formats.

### Key Features

- Dynamically updates version numbers in YAML, JSON, and text files.
- Supports version standardization by removing the `v` prefix if specified.
- Allows external repositories to reuse the workflow by providing inputs for version control.

---

## Inputs

### 1. `version` (Required)

- **Description**: The version number to set.
- **Type**: String
- **Required**: Yes

### 2. `files` (Required)

- **Description**: List of file paths to update. Accepts a JSON array of file paths.
- **Type**: String
- **Required**: Yes

### 3. `strip_v_prefix` (Optional)

- **Description**: Whether to remove the `v` prefix from the version number.
- **Type**: Boolean
- **Default**: `true`

---

## Outputs

The **Version Updater Workflow** does not produce explicit outputs but relies on logs and the updated files for verification and validation.

---

## Expected Behavior

When the **Version Updater Workflow** is used:

1. **With Provided Inputs**:
    - The workflow fetches the repository's code and iterates through the files specified in the `files` input.
    - It updates the `version` field in each file according to the file type.
   
2. **File Types and Behavior**:
    - **YAML Files**: Updates `version:` fields.
    - **JSON Files**: Updates the `version` key in JSON objects.
    - **Generic Text Files**: Uses regex to locate and replace `version` definitions.

3. **Edge Cases**:
    - If a file does not contain a recognizable `version` field, a warning is logged, and the workflow continues.
    - Missing or invalid files are skipped with a warning in the logs.

---

## Example Usage

### Workflow Call

To use the Version Updater Workflow in an external repository:

```yaml
name: Update Version

on:
  workflow_dispatch:  # Allows manual triggering

jobs:
  update-version:
    uses: your-username/github.actions/.github/workflows/version_updater.yml@v1
    with:
      version: "v2.0.1"
      files: '["config.yml", "package.json", "README.md"]'
      strip_v_prefix: false
```

### Logs for Validation

The workflow provides logs for each file it updates, making it easy to verify changes:

```text
Updated version in config.yml to v2.0.1
Updated version in package.json to v2.0.1
Warning: No version field found in README.md
```

---

## Debugging Tips

1. **Validate Inputs**: Ensure the `version` and `files` inputs are correctly specified.
2. **Check File Accessibility**: Confirm that all file paths provided are valid and accessible.
3. **Review Logs**: The workflow logs detailed information about updates and skips, which can help identify issues.

---

## File Structure

### 1. `version_updater.yml`

Defines the reusable workflow with input specifications and steps to execute the **Version Updater** action.

### 2. `version_updater.py`

The Python script used by the action to update files.

---

## References

### Workflow Metadata

```yaml
on:
  workflow_dispatch:  # Allows manual triggering
  workflow_call:
    inputs:
      version:
        required: true
        type: string
      files:
        required: true
        type: string
      strip_v_prefix:
        required: false
        type: boolean
        default: true

jobs:
  update-version:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          repository: ${% raw %}{{ github.repository }}{% endraw %}
          ref: main
          fetch-depth: 0

      - name: Update The Version
        id: update-version
        uses: deepworks-net/github.toolkit/actions/version_updater@v1
        with:
          version: ${% raw %}{{ inputs.version }}{% endraw %}
          files: ${% raw %}{{ inputs.files }}{% endraw %}
          strip_v_prefix: ${% raw %}{{ inputs.strip_v_prefix }}{% endraw %}
```

### Steps in Workflow

1. **Checkout Code**: Ensures the repository is available for modification.
2. **Run Version Updater**: Invokes the `Version Updater` action with provided inputs.
