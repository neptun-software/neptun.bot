from itemadapter import ItemAdapter
import os
import json
from collections import defaultdict
from neptunscraper import items
import psycopg

from neptunscraper.items import DockerBlogPostItem, DockerImageItem


class DockerPipeline:

    def open_spider(self, spider):
        self.items = []

    def close_spider(self, spider):
        sorted_items = sorted(self.items, key=lambda x: self.sort_downloads(x['downloads']))

        output_dir = spider.output_dir if hasattr(spider, 'output_dir') else 'output'
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'output.json')

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sorted_items, f, ensure_ascii=False, indent=4)

    def process_item(self, item, spider):
        self.items.append(ItemAdapter(item).asdict())
        return item

    def sort_downloads(self, downloads):
        if downloads.endswith('+'):
            return int(downloads[:-1])
        else:
            return float(downloads[:-1])


class BasePostgresPipeline:
    def __init__(self):
        self.connection = psycopg.connect(
        dbname="neptun_data",
        user="root",
        password="secret",
        host="localhost",
        port="5432"
        )
        self.cursor = self.connection.cursor()


class SaveRegistryToPostgresPipeline(BasePostgresPipeline):
    def __init__(self):
        super().__init__()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS docker_images (
                name TEXT PRIMARY KEY,
                details JSONB
            );
        """)

    def close_spider(self, spider):
        if self.connection:
            self.connection.commit()
            self.cursor.close()
            self.connection.close()

    def process_item(self, item, spider):
        if isinstance(item, DockerImageItem):
            item_data = dict(item)
            name = item_data.pop('name')
            details = json.dumps(item_data)  # Convert dict to JSON string

            try:
                self.cursor.execute("""
                    INSERT INTO docker_images (name, details)
                    VALUES (%s, %s)
                    ON CONFLICT (name) 
                    DO UPDATE SET details = EXCLUDED.details;
                """, (name, details))
            except Exception as e:
                spider.logger.error(f"Error inserting item into PostgreSQL: {e}")
            return item


class SaveBlogPostToPostgresPipeline(BasePostgresPipeline):
    def __init__(self):
        super().__init__()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS docker_blog_posts (
                title TEXT PRIMARY KEY,
                details JSONB
            );
        """)

    def close_spider(self, spider):
        if self.connection:
            self.connection.commit()
            self.cursor.close()
            self.connection.close()

    def process_item(self, item, spider):
        if isinstance(item, DockerBlogPostItem):
            item_data = dict(item)
            title = item_data.pop('title')
            details = json.dumps(item_data)
            try:
                self.cursor.execute("""
                    INSERT INTO docker_blog_posts(title, details)
                    VALUES (%s, %s)
                    ON CONFLICT (id) 
                    DO UPDATE SET details = EXCLUDED.details;
                """, (title, details))
            except Exception as e:
                spider.logger.error(f"Error inserting item into PostgreSQL: {e}")

        return item







