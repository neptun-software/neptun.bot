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
    categories = scrapy.Field()
    posted_on = scrapy.Field()
    blog_content = scrapy.Field()

