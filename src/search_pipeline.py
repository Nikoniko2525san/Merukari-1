from .market_source import MarketDataSource
from .search_batch import fetch_all_keywords
from .source import ListingSource, SourceListing


def enrich_with_market_prices(
    listings: list[SourceListing],
    market_source: MarketDataSource,
) -> dict[str, tuple[int, ...]]:
    """各商品の相場価格を取得する。"""

    market_prices: dict[str, tuple[int, ...]] = {}

    for listing in listings:
        prices = tuple(
            market_source.search_prices(
                keyword=listing.title,
                limit=100,
            )
        )

        market_prices[listing.id] = prices

    return market_prices


def search_and_get_market_prices(
    source: ListingSource,
    market_source: MarketDataSource,
) -> tuple[list[SourceListing], dict[str, tuple[int, ...]]]:
    """商品検索と相場取得をまとめて実行する。"""

    listings = fetch_all_keywords(source)

    market_prices = enrich_with_market_prices(
        listings=list(listings),
        market_source=market_source,
    )

    return listings, market_prices
