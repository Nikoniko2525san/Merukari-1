import json
import urllib.request

from .filter import ProductCandidate


def send_discord_notification(
    webhook_url: str,
    product: ProductCandidate,
) -> bool:
    """条件を満たした商品をDiscordへ通知する。"""

    message = (
        "🔥 利益30%以上の商品を検出\n\n"
        f"商品名: {product.title}\n"
        f"仕入れ価格: ¥{product.purchase_price:,}\n"
        f"想定販売価格: ¥{product.expected_sale_price:,}\n"
        f"想定利益: ¥{product.profit:,}\n"
        f"利益率: {product.profit_rate * 100:.1f}%\n"
        f"発送サイズ: {product.shipping.size}\n"
        f"送料: ¥{product.shipping.shipping_fee:,}\n"
        f"URL: {product.url}"
    )

    payload = json.dumps({
        "content": message
    }).encode("utf-8")

    request = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return 200 <= response.status < 300
    except Exception:
        return False
