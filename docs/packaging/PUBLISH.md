# Publishing to PyPI

This guide explains how to publish `todo-ai` to the Python Package Index (PyPI).

## Prerequisites

1. **PyPI Account:** You need an account on [PyPI](https://pypi.org/).
2. **API Token:** Create an API token in your PyPI account settings.
3. **Twine:** The tool used to upload packages.

## Automated Build & Check

We have a helper script that builds the package and verifies the metadata:

```bash
./release/publish_pypi.sh
```

This script will:
1. Clean old build artifacts.
2. Build the source distribution (`.tar.gz`) and wheel (`.whl`).
3. Run `twine check` to ensure the `README.md` renders correctly on PyPI.

## Publishing

Once the build verification passes, upload the package using `twine`.

### TestPyPI (Optional but Recommended)

First, upload to TestPyPI to verify everything looks right:

```bash
python3 -m twine upload --repository testpypi dist/*
```

You can then test installation:
```bash
pip install --index-url https://test.pypi.org/simple/ --no-deps ai-todo
```

### Production PyPI

When ready, upload to the real PyPI:

```bash
python3 -m twine upload dist/*
```

You will be prompted for your username (`__token__`) and your API token (starts with `pypi-`).

## Post-Publishing

1. **Verify Installation:**
    ```bash
    pipx install todo-ai --force
    ```

2. **Check Listing:**
    Visit [https://pypi.org/project/todo-ai/](https://pypi.org/project/todo-ai/) to ensure the description and metadata are correct.
