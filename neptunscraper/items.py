# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DockerImageItem(scrapy.Item):
    name = scrapy.Field()
    uploader = scrapy.Field()
    is_official_image = scrapy.Field()
    is_verified_publisher = scrapy.Field()
    last_update = scrapy.Field()
    description = scrapy.Field()
    chips = scrapy.Field()
    downloads = scrapy.Field()
    pulls_last_week = scrapy.Field()
    stars = scrapy.Field()
    tags = scrapy.Field()


class DockerBlogPostItem(scrapy.Item):
    title = scrapy.Field()
    authors = scrapy.Field()
    post_tags = scrapy.Field()
    content = scrapy.Field()
    categories = scrapy.Field()
    posted_on = scrapy.Field()
    sections = scrapy.Field()


class DockerBlogPostSectionItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    code = scrapy.Field()


class DockerBlogPostCodeItem(scrapy.Item):
    content = scrapy.Field()


class DockerDocsComposeItem(scrapy.Item):
    content = scrapy.Field()


class DockerDocsComposeSectionItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()


class DockerDocsComposeCodeItem(scrapy.Item):
    language = scrapy.Field()
    code = scrapy.Field()
    url = scrapy.Field()
