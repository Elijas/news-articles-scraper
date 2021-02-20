from logging_facade import init_logging
from spider import ReqSpider, ReqSpiderDependenciesFactory


def main():
    init_logging()

    dependencies_factory = ReqSpiderDependenciesFactory(
        start_urls=[
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ],
    )
    with dependencies_factory.build_context() as dependencies:
        ReqSpider.run(dependencies)


if __name__ == '__main__':
    main()
