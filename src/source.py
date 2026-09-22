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


class ListingSource:
    """商品データ取得元の基本インターフェース。"""

    def fetch(self) -> Iterable[SourceListing]:
        """
        商品データを取得する。

        実際の取得処理は、このクラスを継承した
        データ取得元側で実装する。
        """
        raise NotImplementedError
