from .database import Database
from .search_pipeline import search_and_get_market_prices
from .settings import get_discord_webhook_url
from .test_market_source import TestMarketDataSource
from .test_source import TestListingSource
from .source import SourceListing
from .batch_processor import process_batch


def main() -> None:
    webhook_url = get_discord_webhook_url()
    database = Database()

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
    ]

    source = TestListingSource(listings)

    market_source = TestMarketDataSource({
        "iPhone 15 128GB": (70000, 72000, 75000),
        "ゲーミングPC RTX3060": (90000, 95000, 100000),
    })

    try:
        found_listings, market_prices = search_and_get_market_prices(
            source=source,
            market_source=market_source,
        )

        notified_count = process_batch(
            listings=found_listings,
            market_prices=market_prices,
            database=database,
            discord_webhook_url=webhook_url,
        )

        print(f"通知成功: {notified_count}件")

    finally:
        database.close()


if __name__ == "__main__":
    main()
