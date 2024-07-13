# NEPTUN-SCRAPER

## RUN 

* Install dependencies

```shell
poetry install
```

* Run Neptun-Scraper

```shell
scrapy crawl dockerhubDockerRegistrySpider -a query="python"
```

* Run Neptun-Bot (WebUI, Rest-Interface, Scrapy-Daemon)
```shell
docker compose up --build
```

* Access the WebUI:
```shell
http://localhost:8000
```

* Access the DAEMON-Interface:
```shell
http://localhost:6802
```

* Create a Scrapyd-Job
```shell
curl http://localhost:6802/schedule.json -d project=neptunscraper -d spider=dockerhubDockerRegistrySpider
```