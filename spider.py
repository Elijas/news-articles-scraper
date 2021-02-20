import contextlib
from dataclasses import dataclass
from typing import List

import scrapy
from bs4 import BeautifulSoup
from scrapy import Request
from scrapy.crawler import CrawlerProcess
from scrapy.exporters import CsvItemExporter


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
                FAKEUSERAGENT_PROVIDERS=[
                    'scrapy_fake_useragent.providers.FakeUserAgentProvider',  # this is the first provider we'll try
                    'scrapy_fake_useragent.providers.FakerProvider',
                    # if FakeUserAgentProvider fails, we'll use faker to generate a user-agent string for us
                    'scrapy_fake_useragent.providers.FixedUserAgentProvider',  # fall back to USER_AGENT value
                ],
                USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
                FEED_FORMAT='csv',
                FEED_URI='output.csv',
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
        soup = BeautifulSoup(response.body, features='lxml')
        article_title = ' '.join(soup.find_all(class_='article-title')[0].text.replace('\n', '').replace('\t', '').split()[:-1])
        yield {
            'article_title': article_title
        }
        soup

    @classmethod
    def run(cls, dependencies):
        process = CrawlerProcess(dependencies.scrapy_settings)
        crawler = process.create_crawler(cls)
        process.crawl(crawler, dependencies)
        process.start()  # the script will block here until the crawling is finished
        return crawler
