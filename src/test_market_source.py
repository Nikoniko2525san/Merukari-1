from typing import Iterable

from .market_source import MarketDataSource


class TestMarketDataSource(MarketDataSource):
    """テスト用の相場データ取得元。"""

    def __init__(self, prices: dict[str, tuple[int, ...]]):
        self.prices = prices

    def search_prices(
        self,
        keyword: str,
        limit: int = 100,
    ) -> Iterable[int]:
        """指定キーワードのテスト相場を返す。"""
        return self.prices.get(keyword, ())[:limit]
