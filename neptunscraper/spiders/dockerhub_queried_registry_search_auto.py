import scrapy
from scrapy.utils import spider
from scrapy_playwright.page import PageMethod
from neptunscraper.items import DockerImageItem


class DockerhubDockerRegistrySearchSpider(spider.Spider):
    name = "dockerhubDockerQueriedRegistrySearchSpider"
    allowed_domains = ["hub.docker.com"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'neptunscraper.pipelines.SaveRegistryToPostgresPipeline': 300,
        }
    }

    def __init__(self, query=None, depth=None, *args, **kwargs):
        super(DockerhubDockerRegistrySearchSpider, self).__init__(*args, **kwargs)
        self.query = query
        self.depth = depth
        self.start_urls = [f'https://hub.docker.com/search?q={query}&page=1']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta=dict(
                    playwright=True,
                    playwright_page_methods={
                        "wait_for_search_results": PageMethod("wait_for_selector", "div#searchResults"),
                    },
                    current_page=1,
                ),
                callback=self.parse
            )

    def parse(self, response):
        self.logger.info("Processing page: %s", response.url)

        image_links = response.css('a[data-testid="imageSearchResult"]::attr(href)').getall()

        for link in image_links:
            yield scrapy.Request(
                    url=f"https://hub.docker.com{link}/tags",
                    meta=dict(
                        playwright=True,
                        playwright_page_methods={
                            "wait_for_selector_repo_name": PageMethod("wait_for_selector",
                                                                      'body[aria-describedby="global-progress"]'),
                            "wait_for_selector_tag_list": PageMethod("wait_for_selector", 'div[data-testid="repotagsTagList"]'),

                        },
                    ),
                    callback=self.parse_registry,
                )

        if 'current_page' in response.meta and (self.depth is None or response.meta['current_page'] <= self.depth):
            current_page = response.meta['current_page']
            next_page = current_page + 1

            next_button_exists = response.xpath('//li[@data-testid="pagination-next"]')

            if next_button_exists:
                yield scrapy.Request(
                    url=f"https://hub.docker.com/search?q=python&page={next_page}",
                    meta=dict(
                        playwright=True,
                        playwright_page_methods={
                            "wait_for_search_results": PageMethod("wait_for_selector", "div#searchResults"),
                        },
                        current_page=next_page,
                    ),
                    callback=self.parse,
                )
            else:
                self.logger.info("No more pages to scrape.")

    def parse_registry(self, response):
        item = DockerImageItem()

        name = response.css('h1.MuiTypography-h2::text, h2.MuiTypography-h2::text').get()
        item['name'] = name.strip() if name else None

        verified_publisher_icon = response.css('svg[data-testid="official-icon"]')
        item["is_verified_publisher"] = bool(verified_publisher_icon)

        # Extract downloads
        downloads_elem = response.css('svg[data-testid="DownloadIcon"] + p.MuiTypography-body1::text').get()
        item['downloads'] = downloads_elem if downloads_elem else response.css(
            'p.MuiTypography-body1:nth-child(3)::text').get()

        if len(str(item['downloads'])) > 4:
            item['downloads'] = None if downloads_elem else response.css(
                'p.MuiTypography-body1:nth-child(4)::text').get()

            if item['downloads'] is None:
                item['downloads'] = response.css('p.MuiTypography-body1:nth-child(5)::text').get()

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

    def close(spider, reason):
        spider.logger.info(f"Spider closed: {spider.name}, due to {reason}")

