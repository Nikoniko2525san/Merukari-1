from .http_market_source import HttpMarketDataSource


def main() -> None:
    api = HttpMarketDataSource(
        "http://localhost:8000/market"
    )

    prices = api.search_prices(
        keyword="iPhone 15",
        limit=100,
    )

    print("取得した相場価格:")
    for price in prices:
        print(f"¥{price:,}")


if __name__ == "__main__":
    main()
