import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy_playwright.page import PageMethod
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from neptunscraper.items import DockerImageItem


class DockerhubQueriedRegistrySpider(CrawlSpider):
    name = "dockerhubDockerQueriedRegistrySpider"
    allowed_domains = ["hub.docker.com"]

    rules = (
        Rule(
            LinkExtractor(allow='/_/'),
            callback='parse_registry',
            follow=False
        ),
        Rule(
            LinkExtractor(allow='/tags'),
            callback='parse_registry',
            follow=False
        )
    )

    def __init__(self, query=None, *args, **kwargs):
        super(DockerhubQueriedRegistrySpider, self).__init__(*args, **kwargs)
        self.query = query
        # check whether: username/image or image
        self.start_urls = [f'https://hub.docker.com/r/{query}/tags' if '/' in query and len(
            query.split('/')) == 2 else f'https://hub.docker.com/_/{query}/tags']

    def start_requests(self):
        self.logger.info(f"Starting request: {self.start_urls[0]}")
        yield scrapy.Request(
            self.start_urls[0],
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod("wait_for_selector", 'div[data-testid="repotagsTagList"]'),
                ]
            ),
            callback=self.parse_registry
        )

    def parse_registry(self, response):
        item = DockerImageItem()

        name = response.css('h1.MuiTypography-h2::text').get()
        item['name'] = name.strip() if name else None

        # determine if the publisher is verified
        official_icon = response.css('svg[data-testid="official-icon"]')
        verified_publisher_icon = response.css('svg[data-testid="verified_publisher-icon"]')

        item["is_official_image"] = bool(official_icon)
        item["is_verified_publisher"] = bool(verified_publisher_icon)

        description = response.css('p[data-testid="description"]::text').get()
        item['description'] = description.strip() if description else None

        item['chips'] = response.css('a[data-testid="productChip"] span::text').getall()

        downloads_elem = response.css('p.MuiTypography-body1.css-12r72vy::text').get()
        item['downloads'] = self.parse_downloads(downloads_elem) if downloads_elem else None

        stars = response.css('svg[data-testid="StarOutlineIcon"] + span > strong::text').get()
        item['stars'] = stars.strip() if stars else None
        tags = {}

        tag_items = response.css('div[data-testid="repotagsTagListItem"]')
        for tag_item in tag_items:
            tag_name = tag_item.css('a[data-testid="navToImage"]::text').get()

            if tag_name:
                tag_version = self.extract_type_and_version(tag_name)
                if tag_version:
                    type_name, version = tag_version
                    tags.setdefault(version, []).append(type_name)
                else:
                    tags.setdefault('default', []).append(tag_name)
            else:
                tags.setdefault('default', []).append("")

        formatted_tags = {}
        for key, values in tags.items():
            formatted_tags[key] = values

            item['tags'] = formatted_tags
        yield item

    def extract_type_and_version(self, tag_name):
        if tag_name and '-' in tag_name:
            parts = tag_name.rsplit('-', 1)
            if len(parts) == 2:
                return parts[0], parts[1]

        return None

    @staticmethod
    def parse_update_string(update_string):
        return update_string.strip() if update_string else None

    @staticmethod
    def parse_downloads(downloads_text):
        if downloads_text:
            return downloads_text.strip()
        return None


if __name__ == "__main__":
    query = "python"  # Replace with your query
    output_dir = "output"
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': f'{output_dir}/output.json',
        'LOG_LEVEL': 'INFO',
        'PLAYWRIGHT_INCLUDE_PATH': True,  # Ensure Playwright is included in the path
        'PLAYWRIGHT_BROWSER': 'chromium',  # Specify the browser to use (chromium or firefox)
    })
    process.crawl(DockerhubQueriedRegistrySpider, query=query)
    process.start()
