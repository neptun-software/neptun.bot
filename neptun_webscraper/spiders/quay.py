import scrapy


class QuayDockerRegistrySpider(scrapy.Spider):
    name = "quayDockerRegistry"

    def parse(self, response):
        item = {}

        print("TODO: Extract data from Quay.io search results")
