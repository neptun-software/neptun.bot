FROM python:3.7-slim
COPY . /app
WORKDIR /app
RUN pip install .
CMD ["tech_stack_ai_configuration_data_scraper"]
