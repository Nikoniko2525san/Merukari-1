from typing import Iterable

from .source import ListingSource, SourceListing


class MercariListingSource(ListingSource):
    """メルカリの商品検索用のデータ取得クラス。"""

    def __init__(
        self,
        listings: Iterable[SourceListing] = (),
    ):
        self.listings = tuple(listings)

    def fetch(
        self,
        keyword: str | None = None,
    ) -> Iterable[SourceListing]:
        """取得済みの商品からキーワードで絞り込む。"""

        for listing in self.listings:
            if listing.is_sold:
                continue

            if keyword:
                if keyword.lower() not in listing.title.lower():
                    continue

            yield listing
