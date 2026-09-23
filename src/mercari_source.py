from typing import Iterable

from .source import ListingSource, SourceListing


class MercariListingSource(ListingSource):
    """メルカリの商品取得元。"""

    def __init__(self, fetcher):
        self.fetcher = fetcher

    def fetch(
        self,
        keyword: str | None = None,
    ) -> Iterable[SourceListing]:
        listings = self.fetcher(keyword)

        for listing in listings:
            if listing.is_sold:
                continue

            if keyword:
                if keyword.lower() not in listing.title.lower():
                    continue

            yield listing
