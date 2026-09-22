from dataclasses import dataclass

from .config import EXCLUDE_LARGE_ITEMS, MAX_SHIPPING_SIZE, MIN_PROFIT_RATE
from .market import estimate_sale_price
from .profit import calculate_net_profit, calculate_net_profit_rate
from .shipping import ShippingInfo, is_acceptable_size


@dataclass(frozen=True)
class ProductCandidate:
    id: str
    title: str
    purchase_price: int
    market_prices: tuple[int, ...]
    shipping: ShippingInfo
    url: str = ""

    @property
    def expected_sale_price(self) -> int:
        return estimate_sale_price(self.market_prices)

    @property
    def profit(self) -> int:
        return calculate_net_profit(
            self.purchase_price,
            self.expected_sale_price,
            self.shipping.shipping_fee,
        )

    @property
    def profit_rate(self) -> float:
        return calculate_net_profit_rate(
            self.purchase_price,
            self.expected_sale_price,
            self.shipping.shipping_fee,
        )


def is_good_candidate(product: ProductCandidate) -> bool:
    """通知対象の商品か判定する。"""

    if product.purchase_price <= 0:
        return False

    if not is_acceptable_size(product.shipping):
        return False

    if product.expected_sale_price <= 0:
        return False

    return product.profit_rate >= MIN_PROFIT_RATE
