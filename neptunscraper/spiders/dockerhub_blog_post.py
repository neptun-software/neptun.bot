import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy_playwright.page import PageMethod
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from neptunscraper.items import DockerImageItem


class DockerHubBlogSpider(CrawlSpider):
    name = 'dockerhubBlogPostSpider'
    allowed_domains = ['https://hub.docker.com']
    start_urls = ['https://www.docker.com/blog']

    rules = (
        Rule(LinkExtractor(allow="/blog", ), follow=False),
    )

    def parse_item(self, response):
        yield {
            'name': 'test'
        }

