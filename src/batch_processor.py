from typing import Iterable

from .database import Database
from .filter import ProductCandidate
from .processor import process_product
from .source import SourceListing
from .shipping import ShippingInfo


def convert_source_listing(
    listing: SourceListing,
    market_prices: tuple[int, ...],
) -> ProductCandidate:
    """取得元の商品データをBot内部の商品データへ変換する。"""

    return ProductCandidate(
        id=listing.id,
        title=listing.title,
        purchase_price=listing.purchase_price,
        market_prices=market_prices,
        shipping=ShippingInfo(
            size=listing.shipping_size,
            shipping_fee=listing.shipping_fee,
            is_large=listing.is_large,
        ),
        url=listing.url,
    )


def process_batch(
    listings: Iterable[SourceListing],
    market_prices: dict[str, tuple[int, ...]],
    database: Database,
    discord_webhook_url: str,
) -> int:
    """
    大量の商品をまとめて処理する。

    通知に成功した商品の数を返す。
    """

    notified_count = 0

    for listing in listings:
        prices = market_prices.get(listing.id, ())

        product = convert_source_listing(
            listing=listing,
            market_prices=prices,
        )

        if process_product(
            product=product,
            database=database,
            discord_webhook_url=discord_webhook_url,
        ):
            notified_count += 1

    return notified_count
