from typing import Iterable


class MarketDataSource:
    """相場データの取得元インターフェース。"""

    def search_prices(
        self,
        keyword: str,
        limit: int = 100,
    ) -> Iterable[int]:
        """
        指定キーワードの相場価格を取得する。

        実際のAPI・許可されたデータ取得元を
        後からここに接続する。
        """
        raise NotImplementedError
