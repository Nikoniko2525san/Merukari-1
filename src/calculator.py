from .models import Listing
from .profit import calculate_net_profit, calculate_net_profit_rate
from .config import MIN_PROFIT_RATE


def calculate_profit(
    listing: Listing,
    shipping_fee: int = 0,
) -> int:
    """手数料・送料を引いた実利益を計算する。"""
    return calculate_net_profit(
        purchase_price=listing.purchase_price,
        sale_price=listing.expected_sale_price,
        shipping_fee=shipping_fee,
    )


def calculate_profit_rate(
    listing: Listing,
    shipping_fee: int = 0,
) -> float:
    """仕入れ価格に対する実利益率を計算する。"""
    return calculate_net_profit_rate(
        purchase_price=listing.purchase_price,
        sale_price=listing.expected_sale_price,
        shipping_fee=shipping_fee,
    )


def meets_profit_target(
    listing: Listing,
    shipping_fee: int = 0,
) -> bool:
    """実利益率が30%以上ならTrueを返す。"""
    return calculate_profit_rate(
        listing,
        shipping_fee,
    ) >= MIN_PROFIT_RATE
