from typing import Iterable

from .source import ListingSource, SourceListing


class MercariListingSource(ListingSource):
    """メルカリの商品取得用インターフェース。"""

    def __init__(self, listings: Iterable[SourceListing] = ()):
        self.listings = tuple(listings)

    def fetch(self) -> Iterable[SourceListing]:
        return self.listings
