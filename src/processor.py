from .database import Database
from .filter import ProductCandidate, is_good_candidate
from .notifier import send_discord_notification


def process_product(
    product: ProductCandidate,
    database: Database,
    discord_webhook_url: str,
) -> bool:
    """
    商品を判定し、条件を満たしていて未通知ならDiscordへ通知する。

    Returns:
        True: 通知した
        False: 通知しなかった
    """

    if database.exists(product.id):
        return False

    if not is_good_candidate(product):
        database.add_listing(
            listing_id=product.id,
            title=product.title,
            purchase_price=product.purchase_price,
            expected_sale_price=product.expected_sale_price,
            url=product.url,
        )
        return False

    database.add_listing(
        listing_id=product.id,
        title=product.title,
        purchase_price=product.purchase_price,
        expected_sale_price=product.expected_sale_price,
        url=product.url,
    )

    notified = send_discord_notification(
        discord_webhook_url,
        product,
    )

    if notified:
        database.mark_notified(product.id)

    return notified
