import os

from .card_parser import parse_card_title
from .http_market_source import HttpMarketDataSource
from .notifier import send_discord_notification
from .search_batch import fetch_all_keywords
from .search_source import SearchListingSource
from .source import SourceListing
from .filter import ProductCandidate
from .shipping import ShippingInfo


def main() -> None:
    listings = [
        SourceListing(
            id="card001",
            title="ポケモンカード SAR リザードンex 123/099",
            purchase_price=5000,
            shipping_size=30,
            shipping_fee=230,
            is_large=False,
            url="https://example.com/card001",
            is_sold=False,
        ),
        SourceListing(
            id="card002",
            title="遊戯王 青眼の白龍 レリーフ",
            purchase_price=10000,
            shipping_size=30,
            shipping_fee=230,
            is_large=False,
            url="https://example.com/card002",
            is_sold=False,
        ),
        SourceListing(
            id="card003",
            title="ポケモンカード AR ピカチュウ",
            purchase_price=3000,
            shipping_size=30,
            shipping_fee=230,
            is_large=False,
            url="https://example.com/card003",
            is_sold=True,
        ),
        SourceListing(
            id="card004",
            title="遊戯王 シークレット ブラック・マジシャン",
            purchase_price=8000,
            shipping_size=30,
            shipping_fee=230,
            is_large=False,
            url="https://example.com/card004",
            is_sold=False,
        ),
    ]

    source = SearchListingSource(listings)

    market_source = HttpMarketDataSource(
        "http://localhost:8000/market"
    )

    webhook_url = os.getenv(
        "DISCORD_WEBHOOK_URL",
        "",
    ).strip()

    results = fetch_all_keywords(source)

    print(f"出品中の商品: {len(results)}件")
    print("=" * 60)

    for listing in results:
        card = parse_card_title(listing.title)

        prices = tuple(
            market_source.search_prices(
                keyword=listing.title,
                limit=100,
            )
        )

        print(f"商品: {listing.title}")
        print(f"URL: {listing.url}")
        print(f"ゲーム: {card.game}")
        print(f"レアリティ: {card.rarity or 'なし'}")
        print(f"仕入れ価格: ¥{listing.purchase_price:,}")

        if not prices:
            print("相場データ: なし")
            print("→ 判定不可")
            print("-" * 60)
            continue

        sale_price = sorted(prices)[len(prices) // 2]

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
        )

        print(f"相場価格: ¥{sale_price:,}")
        print(f"販売手数料: ¥{int(sale_price * 0.10):,}")
        print(f"送料: ¥{listing.shipping_fee:,}")
        print(f"実利益: ¥{product.profit:,}")
        print(f"利益率: {product.profit_rate * 100:.1f}%")

        if product.profit_rate >= 0.30:
            print("→ ★ 通知対象")

            if webhook_url:
                success = send_discord_notification(
                    webhook_url,
                    product,
                )

                if success:
                    print("→ Discord通知成功")
                else:
                    print("→ Discord通知失敗")
            else:
                print("→ Discord Webhook未設定")

        else:
            print("→ 対象外")

        print("-" * 60)


if __name__ == "__main__":
    main()
