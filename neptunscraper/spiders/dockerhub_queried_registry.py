import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy_playwright.page import PageMethod
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from neptunscraper.items import DockerImageItem
import re


class DockerhubQueriedRegistrySpider(CrawlSpider):
    name = "dockerhubQueriedRegistrySpider"
    allowed_domains = ["hub.docker.com"]

    custom_settings = {
        'ITEM_PIPELINES': {
            'neptunscraper.pipelines.SaveRegistryToPostgresPipeline': 300,
        }
    }

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

        # Name of the repository (check both <h1> and <h2>)
        name = response.css('h1.MuiTypography-h2::text, h2.MuiTypography-h2::text').get()
        item['name'] = name.strip() if name else None

        # Determine if the publisher is verified
        verified_publisher_icon = response.css('svg[data-testid="official-icon"]')
        item["is_verified_publisher"] = bool(verified_publisher_icon)

        # Extract downloads
        downloads_elem = response.css('svg[data-testid="DownloadIcon"] + p.MuiTypography-body1::text').get()
        item['downloads'] = self.parse_downloads(downloads_elem) if downloads_elem else response.css(
            'p.MuiTypography-body1:nth-child(3)::text').get()

        description = response.css('p[data-testid="description"]::text').get()

        if not description:
            description = response.css('p.MuiTypography-body1:nth-child(3)::text').get()
            if str(item['downloads']) in str(description):
                description = None
        item['description'] = description

        # Chips (Tags)
        item['chips'] = [chip.strip() for chip in response.css('span.MuiChip-labelSmall::text').getall() if
                         chip.strip().lower() not in ["new", "image"]]

        stars_text = response.css('svg[data-testid="StarOutlineIcon"] + span.MuiTypography-body1 strong::text').get()
        item['stars'] = stars_text.strip() if stars_text else None

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

    def parse_downloads(self, downloads_elem):
        if not downloads_elem:
            return None

        # Remove non-numeric characters
        downloads_elem = re.sub(r'\D', '', downloads_elem)

        # Check if the resulting string has a length > 0
        if len(downloads_elem) == 0:
            return None

        # Convert the remaining string to an integer
        try:
            downloads = int(downloads_elem)
        except ValueError:
            return None

        return downloads

    @staticmethod
    def parse_update_string(update_string):
        return update_string.strip() if update_string else None

    @staticmethod
    def parse_downloads(downloads_text):
        if downloads_text:
            return downloads_text.strip()
        return None


