import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy_playwright.page import PageMethod
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from neptunscraper.items import DockerBlogPostItem, DockerBlogPostSectionItem


def set_playwright_true(request, response):
    request.meta["playwright"] = True
    request.meta["playwright_page_methods"] = {
        "wait_for_search_results": PageMethod("wait_for_selector", "div#searchResults"),
        "set_extra_http_headers": PageMethod("set_extra_http_headers", {"DNT": "1"}),
    }
    return request


class DockerHubBlogSpider(CrawlSpider):
    name = 'dockerhubBlogPostSpider'
    allowed_domains = ['www.docker.com']
    start_urls = ['https://www.docker.com/blog']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="wp-pagenavi"]//a[@class="nextpostslink"]'),
             follow=True,
             callback='parse_blog_post_pagination_page',
             process_request=set_playwright_true),
        Rule(LinkExtractor(restrict_xpaths='//h2[@class="entry-title"]/a'),
             callback='parse_blog_post',
             follow=False,
             process_request=set_playwright_true),
    )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, meta={"playwright": True})

    def parse_blog_post_pagination_page(self, response):
        self.logger.info("Hi, this is an pagination page! %s", response.url)

    def parse_blog_post(self, response):
        self.logger.info("Hi, this is an blog-post page! %s", response.url)


