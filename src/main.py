from .batch_processor import process_batch
from .database import Database
from .settings import get_discord_webhook_url
from .source import SourceListing
from .test_source import TestListingSource


def main() -> None:
    webhook_url = get_discord_webhook_url()
    database = Database()

    # 大量処理テスト用の商品データ
    listings = [
        SourceListing(
            id="test-001",
            title="テスト商品A",
            purchase_price=10000,
            shipping_size=60,
            shipping_fee=750,
            is_large=False,
            url="https://example.com/1",
        ),
        SourceListing(
            id="test-002",
            title="テスト商品B",
            purchase_price=20000,
            shipping_size=80,
            shipping_fee=850,
            is_large=False,
            url="https://example.com/2",
        ),
        SourceListing(
            id="test-003",
            title="大型テスト商品",
            purchase_price=5000,
            shipping_size=120,
            shipping_fee=1200,
            is_large=True,
            url="https://example.com/3",
        ),
    ]

    source = TestListingSource(listings)

    # 商品IDごとの相場データ
    market_prices = {
        "test-001": (15000, 16000, 17000),
        "test-002": (25000, 26000, 27000),
        "test-003": (10000, 12000, 15000),
    }

    try:
        notified_count = process_batch(
            listings=source.fetch(),
            market_prices=market_prices,
            database=database,
            discord_webhook_url=webhook_url,
        )

        print(f"通知成功: {notified_count}件")

    finally:
        database.close()


if __name__ == "__main__":
    main()
