import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy_playwright.page import PageMethod
from neptunscraper.items import DockerBlogPostItem
from scrapy.linkextractors import LinkExtractor


class DockerhubQueriedBlogPostSpider(CrawlSpider):
    name = "dockerhubDockerBlogPostSpider"
    allowed_domains = ["hub.docker.com"]
    start_urls = ["https://www.docker.com/blog/"]

    rules = (
        Rule(
            LinkExtractor(allow='blog'),
            callback='parse_item',
            follow=False
        ),
    )

    def __init__(self, query=None, *args, **kwargs):
        self.start_urls = ['https://www.docker.com/blog/']
        super(DockerhubQueriedBlogPostSpider, self).__init__(*args, **kwargs)


    def parse_item(self, response):
        item = {}

        yield {}
