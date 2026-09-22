from .database import Database
from .filter import ProductCandidate
from .processor import process_product
from .settings import get_discord_webhook_url
from .shipping import ShippingInfo


def main() -> None:
    webhook_url = get_discord_webhook_url()
    database = Database()

    # テスト用の商品データ
    # 実際のメルカリ商品データ取得部分は後で接続する。
    product = ProductCandidate(
        id="test-001",
        title="テスト商品",
        purchase_price=10000,
        market_prices=(15000, 16000, 17000),
        shipping=ShippingInfo(
            size=60,
            shipping_fee=750,
            is_large=False,
        ),
        url="https://example.com",
    )

    try:
        process_product(
            product=product,
            database=database,
            discord_webhook_url=webhook_url,
        )
    finally:
        database.close()


if __name__ == "__main__":
    main()
