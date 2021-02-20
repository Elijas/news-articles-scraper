from logging_facade import init_logging
from spider import ReqSpider, ReqSpiderDependenciesFactory


def main():
    init_logging()

    dependencies_factory = ReqSpiderDependenciesFactory(
        start_urls=[
            'https://www.delfi.lt/news/daily/world/zymus-britu-istorikas-universitetuose-valdzia-uzgrobe-kairieji.d?id=86510023'
        ],
    )
    with dependencies_factory.build_context() as dependencies:
        ReqSpider.run(dependencies)


if __name__ == '__main__':
    main()
