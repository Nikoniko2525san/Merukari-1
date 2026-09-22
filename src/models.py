from dataclasses import dataclass


@dataclass(frozen=True)
class Listing:
    id: str
    title: str
    purchase_price: int
    expected_sale_price: int
    url: str = ""

    @property
    def expected_profit(self) -> int:
        return self.expected_sale_price - self.purchase_price

    @property
    def profit_rate(self) -> float:
        if self.purchase_price <= 0:
            return 0.0
        return self.expected_profit / self.purchase_price

    @property
    def meets_profit_target(self) -> bool:
        return self.profit_rate >= 0.30
