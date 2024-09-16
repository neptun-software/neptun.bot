from itemadapter import ItemAdapter
import os
import json
from collections import defaultdict
from neptunscraper import items


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

