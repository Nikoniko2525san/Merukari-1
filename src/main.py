import os
import json

from .card_parser import parse_card_title
from .http_market_source import HttpMarketDataSource
from .notifier import send_discord_notification
from .filter import ProductCandidate
from .shipping import ShippingInfo
from .source import SourceListing


def main() -> None:
    with open("src/test_input.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    listings = [
        SourceListing(
            id=str(item["id"]),
            title=str(item["title"]),
            purchase_price=int(item["purchase_price"]),
            shipping_size=int(item["shipping_size"]),
            shipping_fee=int(item["shipping_fee"]),
            is_large=bool(item["is_large"]),
            url=str(item.get("url", "")),
            is_sold=bool(item.get("is_sold", False)),
        )
        for item in data
    ]

    market_source = HttpMarketDataSource(
        "http://localhost:8000/market"
    )

    webhook_url = os.getenv(
        "DISCORD_WEBHOOK_URL",
        "",
    ).strip()

    for listing in listings:

        if listing.is_sold:
            print(f"除外（売却済み）: {listing.title}")
            continue

        card = parse_card_title(listing.title)

        market_fetched_at = datetime.now()

        prices = tuple(
           market_source.search_prices(
              keyword=listing.title,
              limit=100,
           )
        )
        from datetime import datetime

        print("=" * 60)
        print(f"商品: {listing.title}")
        print(f"ゲーム: {card.game}")
        print(f"レアリティ: {card.rarity or 'なし'}")
        print(f"仕入れ価格: ¥{listing.purchase_price:,}")

        if not prices:
            print("相場データ: なし")
            print("→ 判定不可")
            continue

        product = ProductCandidate(
            id=listing.id,
            title=listing.title,
            purchase_price=listing.purchase_price,
            market_prices=prices,
            shipping=ShippingInfo(
                size=listing.shipping_size,
                shipping_fee=listing.shipping_fee,
                is_large=listing.is_large,
            ),
            url=listing.url,
            market_fetched_at=market_fetched_at,
        )

        print(f"相場価格: ¥{product.expected_sale_price:,}")
        print(f"実利益: ¥{product.profit:,}")
        print(f"利益率: {product.profit_rate * 100:.1f}%")

        if product.profit_rate >= 0.30:
            print("→ ★ 通知対象")

            if webhook_url:
                if send_discord_notification(
                    webhook_url,
                    product,
                ):
                    print("→ Discord通知成功")
                else:
                    print("→ Discord通知失敗")
            else:
                print("→ Webhook未設定")
        else:
            print("→ 対象外")


if __name__ == "__main__":
    main()
