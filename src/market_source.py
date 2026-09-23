from typing import Iterable


class MarketDataSource:
    """現在の相場データを取得するためのインターフェース。"""

    def search_prices(
        self,
        keyword: str,
        limit: int = 100,
    ) -> Iterable[int]:
        raise NotImplementedError
