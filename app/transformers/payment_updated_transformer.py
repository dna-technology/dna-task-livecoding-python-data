import json

from models.payment import Payment
from transformers.abstract_transformer import AbstractTransformer


class PaymentUpdatedTransformer(AbstractTransformer):
    def transform(self, value: str):
        try:
            data = json.loads(value)
            payment = Payment(
                id=data["id"],
                merchant_id=data.get("merchantId"),
                amount=int(data.get("amount", 0)),
                currency=data.get("currency"),
                payment_method=data.get("paymentMethod"),
                date=data.get("date")
            )

            self.upsert(payment)
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
            print(f"Failed to process event: {e}")

    def upsert(self, payment: Payment):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO payments (id, merchant_id, amount, currency, payment_method, date)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                merchant_id = excluded.merchant_id,
                amount = excluded.amount,
                currency = excluded.currency,
                payment_method = excluded.payment_method,
                date = excluded.date
        """, (
            payment.id,
            payment.merchant_id,
            payment.amount,
            payment.currency,
            payment.payment_method,
            payment.date
        ))
        self.conn.commit()
