import re

import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy_playwright.page import PageMethod
from scrapy.linkextractors import LinkExtractor
from neptunscraper.items import DockerDocsComposeItem, DockerDocsComposeSectionItem, DockerDocsComposeCodeItem
import html2text


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
        self.logger.info("Hi, this is an docker-compose-docs page! %s", response.url)

