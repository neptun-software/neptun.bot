import scrapy


class QuayDockerRegistrySpider(scrapy.Spider):
    name = "quayDockerRegistry"
    start_urls = [
        "https://quay.io/search?q=",
    ]

    """ TODO: Implement the parse method to extract the required data from the Quay.io registry. """
