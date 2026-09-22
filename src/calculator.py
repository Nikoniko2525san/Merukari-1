from .models import Listing


TARGET_PROFIT_RATE = 0.30


def calculate_profit(listing: Listing) -> int:
    """想定販売価格から仕入れ価格を引いて利益を計算する。"""
    return listing.expected_sale_price - listing.purchase_price


def calculate_profit_rate(listing: Listing) -> float:
    """仕入れ価格に対する利益率を計算する。"""
    if listing.purchase_price <= 0:
        return 0.0

    return calculate_profit(listing) / listing.purchase_price


def meets_profit_target(listing: Listing) -> bool:
    """利益率30%以上ならTrueを返す。"""
    return calculate_profit_rate(listing) >= TARGET_PROFIT_RATE
