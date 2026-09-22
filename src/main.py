from .card_parser import parse_card_title
from .database import Database
from .http_market_source import HttpMarketDataSource
from .search_source import SearchListingSource
from .source import SourceListing


def main() -> None:
    # トレカのテスト商品
    listings = [
        SourceListing(
            id="card001",
            title="ポケモンカード SAR リザードンex 123/099",
            purchase_price=5000,
            shipping_size=30,
            shipping_fee=230,
            is_large=False,
            url="https://example.com/card001",
        ),
        SourceListing(
            id="card002",
            title="遊戯王 青眼の白龍 レリーフ",
            purchase_price=10000,
            shipping_size=30,
            shipping_fee=230,
            is_large=False,
            url="https://example.com/card002",
        ),
    ]

    source = SearchListingSource(listings)

    # テスト用相場API
    market_source = HttpMarketDataSource(
        "http://localhost:8000/market"
    )

    database = Database()

    try:
        all_listings = list(source.fetch())

        print(f"取得商品数: {len(all_listings)}件")
        print("=" * 50)

        for listing in all_listings:
            card = parse_card_title(listing.title)

            print(f"商品: {listing.title}")
            print(f"ゲーム: {card.game}")
            print(f"カード番号: {card.card_number or 'なし'}")
            print(f"レアリティ: {card.rarity or 'なし'}")
            print(f"種類: {card.product_type}")

            prices = tuple(
                market_source.search_prices(
                    keyword=listing.title,
                    limit=100,
                )
            )

            if not prices:
                print("相場データなし")
                print("-" * 50)
                continue

            sale_price = sorted(prices)[len(prices) // 2]

            selling_fee = int(sale_price * 0.10)

            profit = (
                sale_price
                - listing.purchase_price
                - selling_fee
                - listing.shipping_fee
            )

            profit_rate = (
                profit / listing.purchase_price
                if listing.purchase_price > 0
                else 0
            )

            print(f"仕入れ価格: ¥{listing.purchase_price:,}")
            print(f"相場価格: ¥{sale_price:,}")
            print(f"販売手数料: ¥{selling_fee:,}")
            print(f"送料: ¥{listing.shipping_fee:,}")
            print(f"実利益: ¥{profit:,}")
            print(f"利益率: {profit_rate * 100:.1f}%")

            if profit_rate >= 0.30:
                print("→ ★ 通知対象")
            else:
                print("→ 対象外")

            print("-" * 50)

    finally:
        database.close()


if __name__ == "__main__":
    main()
