import json
import urllib.parse
import urllib.request

from .source import SourceListing


class MercariAPISource:
    """商品検索APIからメルカリ商品を取得する。"""

    def __init__(self, endpoint: str):
        self.endpoint = endpoint.rstrip("/")

    def fetch(self, keyword: str):
        params = urllib.parse.urlencode({
            "keyword": keyword,
        })

        url = f"{self.endpoint}?{params}"

        request = urllib.request.Request(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": "Merukari-1/1.0",
            },
            method="GET",
        )

        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(
                response.read().decode("utf-8")
            )

        listings = []

        for item in data.get("items", []):
            listings.append(
                SourceListing(
                    id=str(item["id"]),
                    title=str(item["title"]),
                    purchase_price=int(item["price"]),
                    shipping_size=int(item.get("shipping_size", 60)),
                    shipping_fee=int(item.get("shipping_fee", 0)),
                    is_large=bool(item.get("is_large", False)),
                    url=str(item.get("url", "")),
                    is_sold=bool(item.get("is_sold", False)),
                )
            )

        return listings
