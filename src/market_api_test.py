from .http_market_source import HttpMarketDataSource


def main() -> None:
    api = HttpMarketDataSource(
        "http://localhost:8000/market"
    )

    test_keywords = [
        "ポケモンカード SAR リザードンex 123/099",
        "遊戯王 青眼の白龍 レリーフ",
    ]

    for keyword in test_keywords:
        print(f"\n検索: {keyword}")

        prices = api.search_prices(
            keyword=keyword,
            limit=100,
        )

        for price in prices:
            print(f"¥{price:,}")


if __name__ == "__main__":
    main()
