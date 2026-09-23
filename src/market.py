from dataclasses import dataclass
from statistics import median
from typing import Iterable


@dataclass(frozen=True)
class MarketPrice:
    """取得した相場価格。"""

    prices: tuple[int, ...]

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
    """有効な価格だけを相場データとして使用する。"""

    valid_prices = tuple(
        price
        for price in prices
        if isinstance(price, int) and price > 0
    )

    return MarketPrice(valid_prices)


def estimate_sale_price(
    prices: Iterable[int],
) -> int:
    """
    現在取得した価格から想定販売価格を計算する。

    外れ値の影響を受けにくいよう中央値を使用する。
    """

    market = create_market_price(prices)

    return market.median_price
