import os


def get_discord_webhook_url() -> str:
    """環境変数からDiscord Webhook URLを取得する。"""
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL", "").strip()

    if not webhook_url:
        raise RuntimeError(
            "DISCORD_WEBHOOK_URL が設定されていません。"
        )

    return webhook_url
