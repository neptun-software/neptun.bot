FROM vimagick/scrapyd:latest

WORKDIR /code

COPY . .


RUN pip install scrapy-playwright && \
    playwright install && \
    playwright install-deps

EXPOSE 9080

CMD ["scrapyrt -i 0.0.0.0 -p 9080"]
