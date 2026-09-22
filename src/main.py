from .batch_processor import process_batch
from .database import Database
from .http_market_source import HttpMarketDataSource
from .search_pipeline import search_and_get_market_prices
from .settings import get_discord_webhook_url, get_market_api_url
from .source import ListingSource


class ApiListingSource(ListingSource):
    """
    商品取得APIを接続するための入口。

    実際の許可されたAPI仕様に合わせて fetch() を実装する。
    """

    def fetch(self):
        raise NotImplementedError(
            "商品取得APIの仕様に合わせて fetch() を実装してください。"
        )


def main() -> None:
    webhook_url = get_discord_webhook_url()
    market_api_url = get_market_api_url()

    database = Database()

    source = ApiListingSource()
    market_source = HttpMarketDataSource(market_api_url)

    try:
        listings, market_prices = search_and_get_market_prices(
            source=source,
            market_source=market_source,
        )

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
