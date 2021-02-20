import contextlib
from dataclasses import dataclass
from typing import List

import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess


@dataclass
class ReqSpiderDependencies:
    start_urls: List[str]
    scrapy_settings: dict


class ReqSpiderDependenciesFactory:
    def __init__(self, start_urls: List[str]):
        self._constructor_kwargs = dict(
            start_urls=start_urls,
            scrapy_settings=dict(
                LOG_ENABLED=False,
            )
        )

    @contextlib.contextmanager
    def build_context(self):
        yield ReqSpiderDependencies(
            **self._constructor_kwargs
        )


class ReqSpider(scrapy.Spider):
    name = "req"

    def __init__(self, dependencies: ReqSpiderDependencies, **kwargs):
        self.dep = dependencies
        super().__init__(**kwargs)

    def start_requests(self):
        for url in self.dep.start_urls:
            yield Request(url=url)

    def parse(self, response, **kwargs):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

    @classmethod
    def run(cls, dependencies):
        process = CrawlerProcess(dependencies.scrapy_settings)
        crawler = process.create_crawler(cls)
        process.crawl(crawler, dependencies)
        process.start()  # the script will block here until the crawling is finished
        return crawler
