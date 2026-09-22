from typing import Iterable

from .search_config import SEARCH_KEYWORDS, MAX_ITEMS_PER_KEYWORD
from .source import ListingSource, SourceListing


def fetch_all_keywords(
    source: ListingSource,
) -> list[SourceListing]:
    """
    設定された全キーワードの商品を取得する。

    同じ商品が複数キーワードに該当した場合は、
    商品IDで重複を除外する。
    """

    results: dict[str, SourceListing] = {}

    for keyword in SEARCH_KEYWORDS:
        listings = fetch_keyword(
            source=source,
            keyword=keyword,
        )

        for listing in listings:
            if listing.id not in results:
                results[listing.id] = listing

    return list(results.values())


def fetch_keyword(
    source: ListingSource,
    keyword: str,
) -> Iterable[SourceListing]:
    """
    1つのキーワードの商品を取得する。

    現在のListingSourceには検索機能がないため、
    TestListingSourceなどでは全商品を取得してから
    キーワードで絞り込む。
    """

    count = 0

    for listing in source.fetch():
        if keyword.lower() not in listing.title.lower():
            continue

        yield listing

        count += 1

        if count >= MAX_ITEMS_PER_KEYWORD:
            break
