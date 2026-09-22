import os


def get_discord_webhook_url() -> str:
    """環境変数からDiscord Webhook URLを取得する。"""
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL", "").strip()

    if not webhook_url:
        raise RuntimeError(
            "DISCORD_WEBHOOK_URL が設定されていません。"
        )

    return webhook_url


def get_market_api_url() -> str:
    """環境変数から相場APIのURLを取得する。"""
    api_url = os.getenv("MARKET_API_URL", "").strip()

    if not api_url:
        raise RuntimeError(
            "MARKET_API_URL が設定されていません。"
        )

    return api_url
