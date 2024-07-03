# Neptun Webscraper

[![codecov](https://codecov.io/gh/jonasfroeller/tech-stack-ai-configuration-data-scraper/branch/main/graph/badge.svg?token=tech-stack-ai-configuration-data-scraper_token_here)](https://codecov.io/gh/jonasfroeller/tech-stack-ai-configuration-data-scraper)
[![CI](https://github.com/jonasfroeller/tech-stack-ai-configuration-data-scraper/actions/workflows/main.yml/badge.svg)](https://github.com/jonasfroeller/tech-stack-ai-configuration-data-scraper/actions/workflows/main.yml)

## Install it from PyPI

```bash
pip install neptun_webscraper
```

## Usage

```py
from neptun_webscraper import BaseClass
from neptun_webscraper import base_function

BaseClass().base_method()
base_function()
```

```bash
python -m neptun_webscraper
```

```bash
neptun_webscraper
```

## Docker Hub Scraper

```bash
python -m neptun_webscraper dockerhub --query=python
```

## Quay IO Scraper

```bash
python -m neptun_webscraper quay --query=python
```

## Development

## Create a virtualenv

```bash
make virtualenv
source .venv/bin/activ
```

## Format the code

```bash
make fmt
```

## Lint the code

```bash
make lint
```

## Contributing

More commands are in the [Makefile](Makefile).

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.
