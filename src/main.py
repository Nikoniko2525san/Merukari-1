from .batch_processor import process_batch
from .database import Database
from .source import SourceListing
from .test_market_source import TestMarketDataSource


def main() -> None:
    # テスト用の商品データ
    listings = [
        SourceListing(
            id="test001",
            title="テスト商品",
            purchase_price=10000,
            shipping_size=60,
            shipping_fee=750,
            is_large=False,
            url="https://example.com/test001",
        ),
        SourceListing(
            id="test002",
            title="利益が少ない商品",
            purchase_price=10000,
            shipping_size=60,
            shipping_fee=750,
            is_large=False,
            url="https://example.com/test002",
        ),
    ]

    # テスト用のメルカリ相場
    market_source = TestMarketDataSource({
        "テスト商品": (18000, 19000, 20000),
        "利益が少ない商品": (12000, 12500, 13000),
    })

    market_prices = {}

    for listing in listings:
        prices = tuple(
            market_source.search_prices(
                keyword=listing.title,
                limit=100,
            )
        )

        market_prices[listing.id] = prices

    database = Database()

    try:
        # Discordには送らず、判定だけテスト
        for listing in listings:
            prices = market_prices.get(listing.id, ())

            sale_price = (
                int(sorted(prices)[len(prices) // 2])
                if prices
                else 0
            )

            product_profit = (
                sale_price
                - listing.purchase_price
                - int(sale_price * 0.10)
                - listing.shipping_fee
            )

            profit_rate = (
                product_profit / listing.purchase_price
                if listing.purchase_price > 0
                else 0
            )

            print(f"商品: {listing.title}")
            print(f"仕入れ価格: ¥{listing.purchase_price:,}")
            print(f"想定販売価格: ¥{sale_price:,}")
            print(f"想定利益: ¥{product_profit:,}")
            print(f"利益率: {profit_rate * 100:.1f}%")

            if profit_rate >= 0.30:
                print("→ 通知対象！")
            else:
                print("→ 対象外")

            print("-" * 40)

    finally:
        database.close()


if __name__ == "__main__":
    main()
