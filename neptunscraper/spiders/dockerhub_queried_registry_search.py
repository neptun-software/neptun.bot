import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy_playwright.page import PageMethod
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from neptunscraper.items import DockerImageItem


class DockerhubDockerRegistrySpider(CrawlSpider):
    name = "dockerhubDockerQueriedRegistrySearchSpider"
    allowed_domains = ["hub.docker.com"]

    rules = (
        Rule(
            LinkExtractor(allow=r'/tags$'),
            callback='parse_additional_page',
            follow=False
        ),

        Rule(
            LinkExtractor(allow='search'),
            callback='parse_registry',
            follow=True
        ),

    )

    def __init__(self, query=None, *args, **kwargs):
        super(DockerhubDockerRegistrySpider, self).__init__(*args, **kwargs)
        self.query = query
        self.start_urls = [f'https://hub.docker.com/search?q={query}&page={i}' for i in range(1, 12)]

    def start_requests(self):
        for index, url in enumerate(self.start_urls, start=1):
            self.logger.info(f"Starting request: {url}")
            yield scrapy.Request(
                url,
                meta=dict(
                    page_number=index,
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods={
                        "wait_for_search_results": PageMethod("wait_for_selector", "div#searchResults"),
                    }
                ),
                callback=self.parse_registry
            )

    def parse_registry(self, response):
        search_results = response.xpath('//a[@data-testid="imageSearchResult"]')

        for index, result in enumerate(search_results):
            item = DockerImageItem()
            item['name'] = result.css('[data-testid="product-title"]::text').get()

            try:

                yield {
                    'name': f'Processing {item['name']}',
                    'message': f'Started processing the following webscraper: {self.name} with the query: {self.query}'
                               f' and the scrapped search-item {item['name']}.',
                }

            except Exception as e:
                yield {
                    'name': f"An error occurred while processing: {item['name']}",
                    'message': f'{e}',
                }

        yield {
            'name': f'Finished {self.name}',
            'message': f'Successfully processed the following webscraper: {self.name} with the query: {self.query}'
        }

    def close(self, reason):
        self.logger.info(f"Closed or finished...{reason}")



if __name__ == "__main__":
    query = "python"  # Replace with your query
    output_dir = "output"
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'output/output.json',
        'LOG_LEVEL': 'INFO',
        'PLAYWRIGHT_INCLUDE_PATH': True,  # Ensure Playwright is included in the path
        'PLAYWRIGHT_BROWSER': 'chromium',  # Specify the browser to use (chromium or firefox)
    })
    process.crawl(DockerhubDockerRegistrySpider, query=query, output_dir=output_dir)
    process.start()
