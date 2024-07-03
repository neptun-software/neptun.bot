import json
import os
import re
from datetime import datetime, timedelta

import scrapy
from dateutil.relativedelta import relativedelta
from scrapy.selector import Selector
from scrapy_playwright.page import PageMethod

SCRAPY_SETTINGS = {
    "DOWNLOAD_HANDLERS": {
        "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    },
    "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7",
    "PLAYWRIGHT_BROWSER_TYPE": "chromium",
    "USER_AGENT": None,  # None => using browsers user agent instead
}


def parse_update_string(update_string):
    print(f"Parsing update string: '{update_string}'")
    match = re.search(
        r"Updated (a|\d+) (day|week|month|year)s? ago", update_string
    )
    if not match:
        print(f"String format not recognized: '{update_string}'")
        raise ValueError("String format not recognized")

    value_str, unit = match.group(1), match.group(2)
    print(f"Extracted value: {value_str}, unit: {unit}")

    # Handle the case where 'a' is used instead of a number
    value = 1 if value_str == "a" else int(value_str)

    current_date = datetime.now()

    if unit == "day":
        past_date = current_date - timedelta(days=value)
    elif unit == "week":
        past_date = current_date - timedelta(weeks=value)
    elif unit == "month":
        past_date = current_date - relativedelta(months=value)
    elif unit == "year":
        past_date = current_date - relativedelta(years=value)

    formatted_date = past_date.strftime("%Y-%m-%d")
    print(f"Calculated past date: {formatted_date}")
    return formatted_date


class DockerhubDockerRegistrySpider(scrapy.Spider):
    name = "dockerhubDockerRegistrySpider"
    custom_settings = SCRAPY_SETTINGS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.output_dir = f"./neptun_webscraper/spiders/logs/{self.timestamp}"
        os.makedirs(self.output_dir, exist_ok=True)
        self.items = {}

    def start_requests(self):
        for index, url in enumerate(self.start_urls, start=1):
            print("---")
            print("Starting request: " + url)
            print("---")
            yield scrapy.Request(
                url,
                meta=dict(
                    page_number=index,
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod("wait_for_selector", "div#searchResults"),
                        # timeouts, if more than one page to crawl
                        # PageMethod(
                        # "click",
                        # selector="button#onetrust-reject-all-handler",
                        # ),
                        PageMethod(
                            "screenshot",
                            path=f"{self.output_dir}/screenshot_page_{index}.png",  # noqa: E501
                            full_page=True,
                        ),
                    ],
                ),
            )

    def parse(self, response):
        page_number = response.meta.get("page_number")
        if page_number is None:
            self.logger.warning(
                "Page number not found in meta: %s", response.url
            )
            return

        responseHTML = response.text
        selector = Selector(text=responseHTML)
        search_result = selector.css("#searchResults")
        print("---")
        print("#search_results", search_result)
        print("---")

        items = []

        if search_result:
            search_result_items = search_result.xpath(
                '//a[@data-testid="imageSearchResult"]'
            )

            for result in search_result_items:
                item = self.parse_result(result)
                items.append(item)
        else:
            print("---")
            print("No search results found...")
            print("---")

        if items:
            self.items[page_number] = items

            yield {"page_number": page_number, "items": items}

    def parse_result(self, result):
        item = {}

        # Extract name
        name_elem = result.css('[data-testid="product-title"]::text').get()
        item["name"] = name_elem if name_elem else None

        # Extract uploader
        uploader_elem = result.css("span::text").re(r"^By (.+)")
        if uploader_elem:
            item["uploader"] = uploader_elem[0].strip()
        else:
            official_icon = result.css('[data-testid="official-icon"]')
            verified_publisher_icon = result.css(
                '[data-testid="verified_publisher-icon"]'
            )

            item["is_official_image"] = bool(official_icon)
            item["is_verified_publisher"] = bool(verified_publisher_icon)

        # Extract last update and description
        update_elem = result.css('span:contains("Updated")::text').get()
        if update_elem:
            item["last_update"] = parse_update_string(update_elem.strip())
            desc_elem = result.xpath(
                './/span[contains(text(), "Updated")]/ancestor::div[1]/following-sibling::p[1]/text()'  # noqa: E501
            ).get()
            item["description"] = desc_elem.strip() if desc_elem else None
        else:
            item["last_update"] = None
            item["description"] = None

        # Extract chips (categories)
        chips = result.css('[data-testid="productChip"] span::text').getall()
        item["chips"] = chips

        # Extract downloads (total pulls)
        download_icon = result.css('[data-testid="FileDownloadIcon"]')
        if download_icon:
            downloads = download_icon.xpath(
                "following-sibling::p/text()"
            ).get()
            item["downloads"] = downloads.strip() if downloads else None

        # Extract pulls last week
        pulls_elem = (
            result.css('p:contains("Pulls:")')
            .xpath("following-sibling::p/text()")
            .get()
        )
        item["pulls_last_week"] = (
            pulls_elem.replace(",", "") if pulls_elem else None
        )

        # Extract stars
        stars_elem = result.xpath(
            '//svg[@data-testid="StarOutlineIcon"]/following-sibling::span/strong/text()'  # noqa: E501
        ).get()
        item["stars"] = stars_elem.strip() if stars_elem else None

        return item

    # https://docs.scrapy.org/en/latest/topics/feed-exports.html?highlight=close#close
    def close(self, reason):
        for page_number, items in self.items.items():
            filename = f"{self.output_dir}/data_page_{page_number}.json"
            with open(filename, "w") as f:
                json.dump(items, f, indent=2)
            self.logger.info(
                f"Items from page {page_number} have been written to {filename}"  # noqa: E501
            )
