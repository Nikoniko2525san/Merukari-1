from .mercari_api_source import MercariAPISource


def main() -> None:
    api = MercariAPISource(
        "http://localhost:8001/mercari"
    )

    keywords = [
        "ポケモンカード",
        "ポケカ SAR",
        "遊戯王",
        "遊戯王 レリーフ",
    ]

    for keyword in keywords:
        print("=" * 60)
        print(f"検索: {keyword}")

        try:
            listings = api.fetch(keyword)

            for listing in listings:
                print(f"商品: {listing.title}")
                print(f"価格: ¥{listing.purchase_price:,}")
                print(f"URL: {listing.url}")
                print(f"売却済み: {listing.is_sold}")
                print()

        except Exception as error:
            print(f"取得エラー: {error}")


if __name__ == "__main__":
    main()
