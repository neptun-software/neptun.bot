# Scrapy settings for neptunscraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from . import helpers
import random

BOT_NAME = "neptunscraper"

SPIDER_MODULES = ["neptunscraper.spiders"]
NEWSPIDER_MODULE = "neptunscraper.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "neptunscraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
PLAYWRIGHT_BROWSER_TYPE = "chromium"
USER_AGENT = None


PLAYWRIGHT_LAUNCH_OPTIONS = {
    'headless': True,
    'args': ['--no-sandbox', '--disable-setuid-sandbox']
}

ITEM_PIPELINES = {
    # 'neptunscraper.pipelines.DockerPipeline': 300,
}

# REDIRECT_ENABLED = True
# RETRY_HTTP_CODES = [429]

ROTATING_PROXY_LIST = helpers.fetch_and_parse_proxies('https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt')


DOWNLOADER_MIDDLEWARES = {
  #  'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
  #  'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
  #  'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
  #  'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
  #  'neptunscraper.middlewares.TooManyRequestsRetryMiddleware': 543,
}

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 0.5
AUTOTHROTTLE_DEBUG = True

DOWNLOAD_DELAY = 5
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 1

LOG_LEVEL = 'DEBUG'

PLAYWRIGHT_ABORT_REQUEST = helpers.should_abort_request

# PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 1 * 1000
'''
PLAYWRIGHT_CONTEXTS = {
    "default": {
        "proxy": {
            "server": random.choice(helpers.fetch_and_parse_proxies('https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt')),
        },
    },
    "alternative": {
        "proxy": {
            "server": random.choice(helpers.fetch_and_parse_proxies('https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt')),
        },
    }
}
'''

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "neptunscraper.middlewares.NeptunscraperSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "neptunscraper.middlewares.NeptunscraperDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "neptunscraper.pipelines.NeptunscraperPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
