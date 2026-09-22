import json
import urllib.parse
import urllib.request
from typing import Iterable

from .market_source import MarketDataSource


class HttpMarketDataSource(MarketDataSource):
    """HTTP APIから相場データを取得するための実装。"""

    def __init__(self, endpoint: str):
        self.endpoint = endpoint.rstrip("/")

    def search_prices(
        self,
        keyword: str,
        limit: int = 100,
    ) -> Iterable[int]:
        params = urllib.parse.urlencode({
            "keyword": keyword,
            "limit": limit,
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
            data = json.loads(response.read().decode("utf-8"))

        prices = data.get("prices", [])

        return tuple(
            int(price)
            for price in prices
            if isinstance(price, (int, float)) and price > 0
        )[:limit]
