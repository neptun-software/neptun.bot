import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy_playwright.page import PageMethod
from scrapy.linkextractors import LinkExtractor
from neptunscraper.items import DockerDocsComposeItem, DockerDocsComposeSectionItem, DockerDocsComposeCodeItem


def set_playwright_true(request, response):
    request.meta["playwright"] = True
    return request


class DockerDocsComposeSpider(CrawlSpider):
    name = 'dockerDocsComposeSpider'
    allowed_domains = ['docs.docker.com']
    start_urls = ['https://docs.docker.com/compose']

    rules = (
        Rule(
            LinkExtractor(restrict_xpaths=(
                    '//li[button/span[contains(text(), "Docker Compose")]]'
                    '//ul[@class="ml-3"]//a'
                )
            ),
            follow=True,
            callback='parse_docker_compose_links'
        ),
    )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, meta={"playwright": True})

    def parse_docker_compose_links(self, response):
        self.logger.info("Started parsing the following compose-page: %s", response.url)

        # Extract title and URL
        title = response.xpath('//title/text()').get(default='No Title').strip()
        self.logger.info(f"Parsing page: {response.url}")

        # Parse content sections
        for section in response.xpath('//main//section'):
            section_title = section.xpath('.//h2/text()').get(default='No Title').strip()
            section_content = section.xpath('.//div[contains(@class, "content")]/descendant-or-self::*').getall()

            # Create section item
            section_item = DockerDocsComposeSectionItem(
                title=section_title,
                content=''.join(section_content),
                url=response.url
            )
            yield section_item

        # Parse code snippets
        for code_block in response.xpath('//pre'):
            code_content = code_block.xpath('text()').get()
            code_language = code_block.xpath('@class').re_first(r'language-(\w+)')

            if code_content is not None:
                code_content = code_content.strip()
            else:
                code_content = ''  # Or handle the case where no code is found

            # Create code item
            code_item = DockerDocsComposeCodeItem(
                language=code_language,
                code=code_content,
                url=response.url
            )
            yield code_item

