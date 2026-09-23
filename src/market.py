from dataclasses import dataclass
from datetime import datetime
from statistics import median
from typing import Iterable


@dataclass(frozen=True)
class MarketPrice:
    """取得時点の相場情報。"""

    prices: tuple[int, ...]
    fetched_at: datetime

    @property
    def median_price(self) -> int:
        if not self.prices:
            return 0

        return int(median(self.prices))

    @property
    def sample_count(self) -> int:
        return len(self.prices)


def create_market_price(
    prices: Iterable[int],
) -> MarketPrice:
    """現在取得した価格から相場情報を作る。"""

    valid_prices = tuple(
        price
        for price in prices
        if isinstance(price, int) and price > 0
    )

    return MarketPrice(
        prices=valid_prices,
        fetched_at=datetime.now(),
    )


def estimate_sale_price(
    prices: Iterable[int],
) -> int:
    """取得した価格の中央値を現在相場として使用する。"""

    market = create_market_price(prices)

    return market.median_price
