from .card_parser import parse_card_title
from .search_batch import fetch_all_keywords
from .search_source import SearchListingSource
from .source import SourceListing


def main() -> None:
    # 大量処理のテスト用商品
    listings = [
        SourceListing(
            id="card001",
            title="ポケモンカード SAR リザードンex 123/099",
            purchase_price=5000,
            shipping_size=30,
            shipping_fee=230,
            is_large=False,
            url="https://example.com/card001",
        ),
        SourceListing(
            id="card002",
            title="遊戯王 青眼の白龍 レリーフ",
            purchase_price=10000,
            shipping_size=30,
            shipping_fee=230,
            is_large=False,
            url="https://example.com/card002",
        ),
        SourceListing(
            id="card003",
            title="ポケモンカード AR ピカチュウ",
            purchase_price=3000,
            shipping_size=30,
            shipping_fee=230,
            is_large=False,
            url="https://example.com/card003",
        ),
        SourceListing(
            id="card004",
            title="遊戯王 シークレット ブラック・マジシャン",
            purchase_price=8000,
            shipping_size=30,
            shipping_fee=230,
            is_large=False,
            url="https://example.com/card004",
        ),
    ]

    source = SearchListingSource(listings)

    results = fetch_all_keywords(source)

    print(f"大量検索結果: {len(results)}件")
    print("=" * 50)

    for listing in results:
        card = parse_card_title(listing.title)

        print(f"商品: {listing.title}")
        print(f"ゲーム: {card.game}")
        print(f"レアリティ: {card.rarity or 'なし'}")
        print(f"種類: {card.product_type}")
        print(f"仕入れ価格: ¥{listing.purchase_price:,}")
        print("-" * 50)


if __name__ == "__main__":
    main()
