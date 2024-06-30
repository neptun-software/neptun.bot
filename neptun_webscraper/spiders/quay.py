import scrapy


class QuayDockerRegistrySpider(scrapy.Spider):
    name = "quayDockerRegistry"
    
    def parse(self, response):
        # TODO: Extract data from Quay.io search results
        item = {}
