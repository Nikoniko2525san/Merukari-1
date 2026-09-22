from .batch_processor import process_batch
from .database import Database
from .search_batch import fetch_all_keywords
from .settings import get_discord_webhook_url
from .test_source import TestListingSource
from .source import SourceListing


def main() -> None:
    webhook_url = get_discord_webhook_url()
    database = Database()

    # テスト用の商品データ
    listings = [
        SourceListing(
            id="test-001",
            title="iPhone 15 128GB",
            purchase_price=50000,
            shipping_size=60,
            shipping_fee=750,
            is_large=False,
            url="https://example.com/1",
        ),
        SourceListing(
            id="test-002",
            title="ゲーミングPC RTX3060",
            purchase_price=60000,
            shipping_size=100,
            shipping_fee=1050,
            is_large=False,
            url="https://example.com/2",
        ),
        SourceListing(
            id="test-003",
            title="大型テレビ 55インチ",
            purchase_price=5000,
            shipping_size=120,
            shipping_fee=1200,
            is_large=True,
            url="https://example.com/3",
        ),
    ]

    source = TestListingSource(listings)

    # テスト用のメルカリ相場
    market_prices = {
        "test-001": (70000, 72000, 75000),
        "test-002": (90000, 95000, 100000),
        "test-003": (15000, 18000, 20000),
    }

    try:
        # 複数キーワードをまとめて検索
        filtered_listings = fetch_all_keywords(source)

        # 利益条件をチェックしてDiscord通知
        notified_count = process_batch(
            listings=filtered_listings,
            market_prices=market_prices,
            database=database,
            discord_webhook_url=webhook_url,
        )

        print(f"通知成功: {notified_count}件")

    finally:
        database.close()


if __name__ == "__main__":
    main()
