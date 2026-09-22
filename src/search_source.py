from typing import Iterable

from .source import ListingSource, SourceListing


class SearchListingSource(ListingSource):
    """
    許可されたデータ取得元から商品一覧を受け取るためのクラス。
    """

    def __init__(self, listings: Iterable[SourceListing]):
        self.listings = tuple(listings)

    def fetch(self) -> Iterable[SourceListing]:
        """取得済みの商品一覧をまとめて返す。"""
        return self.listings
