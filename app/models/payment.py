from dataclasses import dataclass

@dataclass
class Payment:
    id: str
    merchant_id: str
    amount: int
    currency: str
    payment_method: str
    date: str