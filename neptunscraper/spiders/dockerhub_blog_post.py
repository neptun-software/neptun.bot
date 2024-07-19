import re

import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy_playwright.page import PageMethod
from scrapy.linkextractors import LinkExtractor
from neptunscraper.items import DockerBlogPostItem, DockerBlogPostSectionItem,DockerBlogPostCodeItem
import html2text


def set_playwright_true(request, response):
    request.meta["playwright"] = True
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

        item = DockerBlogPostItem()

        item['title'] = response.css('h1.entry-title::text').extract_first()
        item["categories"] = response.css('.widget_categories li a::text').getall()
        item["post_tags"] = response.css('a[rel="tag"]::text').getall()
        item["authors"] = response.css('a[rel="author"]::text').getall()
        item["posted_on"] = response.css('div.post-date > p::text').get()

        paragraphs = []
        for paragraph in response.css('div.et_pb_module.et_pb_post_content p'):
            if paragraph.css('h1, h2, h3, h4, h5, h6'):
                break
            text_content = paragraph.css('::text').getall()
            paragraphs.append(' '.join(text_content).strip())

        item["content"] = '\n'.join(paragraphs)

        sections = []
        current_section_title = None
        current_section_content = []
        current_section_code = []

        for element in response.css('div.et_pb_module.et_pb_post_content *'):
            if element.root.tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                if current_section_title is not None:
                    sections.append(DockerBlogPostSectionItem(
                        title=current_section_title,
                        content='\n'.join(current_section_content).strip(),
                        code=current_section_code
                    ))

                current_section_title = element.css('::text').get().strip()
                current_section_content = []
                current_section_code = []
            elif element.root.tag == 'p':
                text_content = element.css('::text').getall()
                current_section_content.append(' '.join(text_content).strip())
            elif element.root.tag == 'div' and 'wp-block-syntaxhighlighter-code' in element.attrib.get('class', ''):
                code_html = element.css('td.code').get()
                current_section_code.append(DockerBlogPostCodeItem(
                    content=code_html,
                ))
            elif element.root.tag == 'pre':
                code_html = element.css('pre').get()
                current_section_code.append(DockerBlogPostCodeItem(
                    content=code_html
                ))

        if current_section_title is not None:
            sections.append(DockerBlogPostSectionItem(
                title=current_section_title,
                content='\n'.join(current_section_content).strip(),
                # the code is provided as html: https://www.atatus.com/tools/html-to-text (convert before further usage)
                # https://www.freeformatter.com/json-escape.html#before-output
                code=current_section_code
            ))

        item['sections'] = sections

        yield item
