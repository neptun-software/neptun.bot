# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DockerhubItem(scrapy.Item):
    name: scrapy.Field
    is_official_image: scrapy.Field
    is_verified_publisher: scrapy.Field
    last_update: scrapy.Field
    description: scrapy.Field
    chips: scrapy.Field
    downloads: scrapy.Field
    pulls_last_week: scrapy.Field
    stars: scrapy.Field


class QuayIoItem(scrapy.Item):
    name: scrapy.Field
    is_official_image: scrapy.Field
    is_verified_publisher: scrapy.Field
    last_update: scrapy.Field
    description: scrapy.Field
    chips: scrapy.Field
    downloads: scrapy.Field
    pulls_last_week: scrapy.Field
    stars: scrapy.Field
