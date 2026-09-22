from dataclasses import dataclass

from .config import EXCLUDE_LARGE_ITEMS, MAX_SHIPPING_SIZE


@dataclass(frozen=True)
class ShippingInfo:
    """商品の発送情報。"""

    size: int
    shipping_fee: int
    is_large: bool = False


def is_acceptable_size(shipping: ShippingInfo) -> bool:
    """大型商品やサイズ上限を超える商品を除外する。"""
    if EXCLUDE_LARGE_ITEMS and shipping.is_large:
        return False

    if shipping.size > MAX_SHIPPING_SIZE:
        return False

    return True


def get_shipping_fee(shipping: ShippingInfo) -> int:
    """送料を取得する。"""
    return shipping.shipping_fee
