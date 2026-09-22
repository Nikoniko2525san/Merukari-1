from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class SourceListing:
    """商品データ取得元から受け取る商品情報。"""

    id: str
    title: str
    purchase_price: int
    shipping_size: int
    shipping_fee: int
    is_large: bool
    url: str = ""
    is_sold: bool = False


class ListingSource:
    """商品データ取得元の基本インターフェース。"""

    def fetch(self) -> Iterable[SourceListing]:
        raise NotImplementedError
