from .database import Database
from .filter import ProductCandidate, is_good_candidate
from .notifier import send_discord_notification


def process_product(
    product: ProductCandidate,
    database: Database,
    discord_webhook_url: str,
) -> bool:
    # すでに通知済みなら何もしない
    if database.is_notified(product.id):
        return False

    # 利益率・サイズなどの条件を満たさなければ何もしない
    # DBにも登録しないので、次回また判定できる
    if not is_good_candidate(product):
        return False

    # 条件を満たした商品を保存
    database.add_listing(
        listing_id=product.id,
        title=product.title,
        purchase_price=product.purchase_price,
        expected_sale_price=product.expected_sale_price,
        url=product.url,
    )

    # Discordへ通知
    notified = send_discord_notification(
        discord_webhook_url,
        product,
    )

    # 通知成功した場合だけ「通知済み」にする
    if notified:
        database.mark_notified(product.id)

    return notified
