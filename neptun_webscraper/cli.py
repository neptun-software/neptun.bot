"""CLI interface for neptun_webscraper project.

Be creative! do whatever you want!

- Install click or typer and create a CLI app
- Use builtin argparse
- Start a web application
- Import things from your .base module
"""

import argparse
from scrapy.crawler import CrawlerProcess
from neptun_webscraper.spiders.dockerhub import DockerhubDockerRegistrySpider
from neptun_webscraper.spiders.quay import QuayDockerRegistrySpider

def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m neptun_webscraper` and `$ neptun_webscraper `.

    This is your program's entry point.

    You can change this function to do whatever you want.
    Examples:
        * Run a test suite
        * Run a server
        * Do some other stuff
        * Run a command line application (Click, Typer, ArgParse)
        * List all available tasks
        * Run an application (Flask, FastAPI, Django, etc.)

    ---

    Choose between different spiders.  
    Examples:
    ```
    python -m neptun_webscraper dockerhub --query=python
    ```

    ```
    python -m neptun_webscraper quay --query=python
    ```
    """

    parser = argparse.ArgumentParser(description="Neptune WebScraper CLI")
    parser.add_argument("spider", choices=["dockerhub", "quay"], help="Choose the spider to run")
    parser.add_argument("--query", default="", help="Search query for the registry")
    args = parser.parse_args()

    process = CrawlerProcess()

    if args.spider == "dockerhub":
        spider = DockerhubDockerRegistrySpider
        start_urls = [f"https://hub.docker.com/search?q={args.query}&page={i}" for i in range(1, 11)]
    elif args.spider == "quay":
        spider = QuayDockerRegistrySpider
        start_urls = [f"https://quay.io/search?q={args.query}"]

    process.crawl(spider, start_urls=start_urls)
    process.start()
