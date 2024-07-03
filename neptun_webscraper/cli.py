import argparse

from scrapy.crawler import CrawlerProcess

from neptun_webscraper.spiders.dockerhub import DockerhubDockerRegistrySpider
from neptun_webscraper.spiders.quay import QuayDockerRegistrySpider


def main():  # pragma: no cover
    """
    CLI interface for neptun_webscraper project.
    This is the program's entry point. The main function executes on commands:
    `python -m neptun_webscraper` and `$ neptun_webscraper `.
    """

    parser = argparse.ArgumentParser(description="Neptune WebScraper CLI")
    parser.add_argument(
        "spider",
        choices=["dockerhub", "quay"],
        default="dockerhub",
        help="Choose a spider to run",
    )
    parser.add_argument(
        "--query", default="", help="Search query for the registry"
    )
    args = parser.parse_args()

    process = CrawlerProcess()

    if args.spider == "dockerhub":
        spider = DockerhubDockerRegistrySpider
        start_urls = [
            f"https://hub.docker.com/search?q={args.query}&page={i}"
            for i in range(1, 11)
        ]
    elif args.spider == "quay":
        spider = QuayDockerRegistrySpider
        start_urls = [f"https://quay.io/search?q={args.query}"]

    process.crawl(spider, start_urls=start_urls)
    process.start()
