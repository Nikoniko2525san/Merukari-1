from .database import Database
from .search_source import SearchListingSource
from .source import SourceListing
from .test_market_source import TestMarketDataSource


def main() -> None:
    # 大量の商品を想定したテストデータ
    listings = [
        SourceListing(
            id="item001",
            title="iPhone 15 128GB",
            purchase_price=50000,
            shipping_size=60,
            shipping_fee=750,
            is_large=False,
            url="https://example.com/item001",
        ),
        SourceListing(
            id="item002",
            title="iPad 第10世代",
            purchase_price=30000,
            shipping_size=80,
            shipping_fee=850,
            is_large=False,
            url="https://example.com/item002",
        ),
        SourceListing(
            id="item003",
            title="ゲーミングPC",
            purchase_price=80000,
            shipping_size=120,
            shipping_fee=1200,
            is_large=True,
            url="https://example.com/item003",
        ),
    ]

    # 商品取得元
    source = SearchListingSource(listings)

    # 相場データ（テスト）
    market_source = TestMarketDataSource({
        "iPhone 15 128GB": (70000, 75000, 78000),
        "iPad 第10世代": (35000, 38000, 40000),
        "ゲーミングPC": (120000, 130000, 140000),
    })

    database = Database()

    try:
        all_listings = list(source.fetch())

        print(f"取得商品数: {len(all_listings)}件")
        print("=" * 40)

        for listing in all_listings:
            prices = tuple(
                market_source.search_prices(
                    keyword=listing.title,
                    limit=100,
                )
            )

            if not prices:
                print(f"{listing.title}: 相場データなし")
                continue

            sale_price = int(sorted(prices)[len(prices) // 2])

            profit = (
                sale_price
                - listing.purchase_price
                - int(sale_price * 0.10)
                - listing.shipping_fee
            )

            profit_rate = (
                profit / listing.purchase_price
                if listing.purchase_price > 0
                else 0
            )

            print(f"商品: {listing.title}")
            print(f"仕入れ価格: ¥{listing.purchase_price:,}")
            print(f"相場価格: ¥{sale_price:,}")
            print(f"実利益: ¥{profit:,}")
            print(f"利益率: {profit_rate * 100:.1f}%")

            if listing.is_large:
                print("→ 大型商品のため除外")
            elif listing.shipping_size > 100:
                print("→ サイズ超過のため除外")
            elif profit_rate >= 0.30:
                print("→ ★ 通知対象")
            else:
                print("→ 対象外")

            print("-" * 40)

    finally:
        database.close()


if __name__ == "__main__":
    main()
