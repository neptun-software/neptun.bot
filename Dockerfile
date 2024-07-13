FROM vimagick/scrapyd:latest

WORKDIR /code

COPY . .

RUN pip install logparser

RUN logparser &

RUN pip install scrapy-playwright && \
    playwright install && \
    playwright install-deps

EXPOSE 6800

CMD ["scrapyd"]
