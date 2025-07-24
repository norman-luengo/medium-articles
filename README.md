

<!-- BANNERS -->
<p align="center">
  <a href="https://github.com/norman-luengo/medium-articles/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/norman-luengo/medium-articles.svg" alt="License">
  </a>
  <a href="https://www.python.org/downloads/release/python-3130/">
    <img src="https://img.shields.io/badge/python-3.13%2B-blue.svg" alt="Python 3.13+">
  </a>
  <a href="https://pypi.org/project/pydantic-ai/">
    <img src="https://img.shields.io/pypi/v/pydantic-ai.svg?label=pydantic-ai" alt="pydantic-ai">
  </a>
  <a href="https://fastapi.tiangolo.com/">
    <img src="https://img.shields.io/badge/FastAPI-async%20web%20framework-green" alt="FastAPI">
  </a>
</p>

# medium-articles

This repository contains code and experiments for Medium articles, including AI agent demos and Python concurrency experiments.

## Project Structure

- `agentic_mlflow_article/` — Example FastAPI app using pydantic-ai for LLM-powered endpoints
- `gil_experimentation_article/` — Notebooks and scripts for Python GIL and concurrency experiments


## Requirements

- Python 3.13+
- `pydantic-ai`
- `fastapi`

## Poetry Setup

This project uses [Poetry](https://python-poetry.org/) for dependency management and virtual environments.

### 1. Install Poetry

If you don't have Poetry installed, run:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Or see the [official docs](https://python-poetry.org/docs/#installation) for more options.

### 2. Install Dependencies

From the root of the repository, run:

```bash
poetry install
```

### 3. Activate the Virtual Environment (optional)

To spawn a shell within the Poetry-managed environment:

```bash
poetry shell
```

Or run commands inside the environment with:

```bash
poetry run <command>
```

## License

See [LICENSE](LICENSE).
