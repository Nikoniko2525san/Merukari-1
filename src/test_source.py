from typing import Iterable

from .source import ListingSource, SourceListing


class TestListingSource(ListingSource):
    """大量の商品処理をテストするためのデータ取得元。"""

    def __init__(self, listings: Iterable[SourceListing]):
        self.listings = tuple(listings)

    def fetch(self) -> Iterable[SourceListing]:
        """登録された商品をまとめて返す。"""
        return self.listings
