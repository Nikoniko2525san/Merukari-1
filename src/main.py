import json
import sys

from .batch_processor import process_batch
from .database import Database
from .input_source import read_listings_from_stdin
from .settings import get_discord_webhook_url
from .test_market_source import TestMarketDataSource


def main() -> None:
    webhook_url = get_discord_webhook_url()
    database = Database()

    # 外部から受け取った商品データ
    listings = read_listings_from_stdin()

    # 現在はテスト用の相場データ
    market_source = TestMarketDataSource({})

    market_prices = {}

    for listing in listings:
        prices = tuple(
            market_source.search_prices(
                keyword=listing.title,
                limit=100,
            )
        )

        market_prices[listing.id] = prices

    try:
        notified_count = process_batch(
            listings=listings,
            market_prices=market_prices,
            database=database,
            discord_webhook_url=webhook_url,
        )

        print(f"通知成功: {notified_count}件")

    finally:
        database.close()


if __name__ == "__main__":
    main()
