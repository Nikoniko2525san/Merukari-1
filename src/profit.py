from .models import Listing
from .config import MERCARI_FEE_RATE, MIN_PROFIT_RATE


def calculate_selling_fee(sale_price: int) -> int:
    """販売価格からメルカリ販売手数料を計算する。"""
    return int(sale_price * MERCARI_FEE_RATE)


def calculate_net_profit(
    purchase_price: int,
    sale_price: int,
    shipping_fee: int = 0,
) -> int:
    """手数料と送料を引いた実利益を計算する。"""
    selling_fee = calculate_selling_fee(sale_price)

    return sale_price - purchase_price - selling_fee - shipping_fee


def calculate_net_profit_rate(
    purchase_price: int,
    sale_price: int,
    shipping_fee: int = 0,
) -> float:
    """仕入れ価格に対する実利益率を計算する。"""
    if purchase_price <= 0:
        return 0.0

    profit = calculate_net_profit(
        purchase_price,
        sale_price,
        shipping_fee,
    )

    return profit / purchase_price


def meets_profit_target(
    purchase_price: int,
    sale_price: int,
    shipping_fee: int = 0,
) -> bool:
    """手数料・送料を引いた実利益率が30%以上か判定する。"""
    return (
        calculate_net_profit_rate(
            purchase_price,
            sale_price,
            shipping_fee,
        )
        >= MIN_PROFIT_RATE
    )
