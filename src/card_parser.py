import re
from dataclasses import dataclass


@dataclass(frozen=True)
class CardInfo:
    game: str
    name: str
    card_number: str = ""
    rarity: str = ""
    product_type: str = "single"


def detect_game(title: str) -> str:
    if "ポケモンカード" in title or "ポケカ" in title:
        return "pokemon"

    if "遊戯王" in title:
        return "yugioh"

    return "unknown"


def detect_rarity(title: str) -> str:
    rarities = [
        "SAR",
        "SR",
        "UR",
        "AR",
        "HR",
        "RRR",
        "RR",
        "ACE",
        "レリーフ",
        "プリズマ",
        "シークレット",
        "25th",
    ]

    for rarity in rarities:
        if rarity.lower() in title.lower():
            return rarity

    return ""


def detect_product_type(title: str) -> str:
    if "BOX" in title.upper():
        return "box"

    if "ボックス" in title:
        return "box"

    if "パック" in title:
        return "pack"

    return "single"


def detect_card_number(title: str) -> str:
    patterns = [
        r"\b\d{1,3}/\d{1,3}\b",
        r"\b[A-Z]{1,5}-\d{1,3}\b",
        r"\b[A-Z]{1,5}\d{1,3}\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, title)

        if match:
            return match.group(0)

    return ""


def parse_card_title(title: str) -> CardInfo:
    return CardInfo(
        game=detect_game(title),
        name=title.strip(),
        card_number=detect_card_number(title),
        rarity=detect_rarity(title),
        product_type=detect_product_type(title),
    )
