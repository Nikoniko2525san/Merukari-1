import json
import sys

from .source import SourceListing


def read_listings_from_stdin() -> list[SourceListing]:
    """
    標準入力からJSON形式の商品データを受け取る。
    """

    data = json.load(sys.stdin)

    listings = []

    for item in data:
        listings.append(
            SourceListing(
                id=str(item["id"]),
                title=str(item["title"]),
                purchase_price=int(item["purchase_price"]),
                shipping_size=int(item["shipping_size"]),
                shipping_fee=int(item["shipping_fee"]),
                is_large=bool(item["is_large"]),
                url=str(item.get("url", "")),
            )
        )

    return listings
