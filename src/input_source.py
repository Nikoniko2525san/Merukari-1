import json
import sys

from .source import SourceListing


def read_listings_from_stdin() -> list[SourceListing]:
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
                is_sold=bool(item.get("is_sold", False)),
            )
        )

    return listings
