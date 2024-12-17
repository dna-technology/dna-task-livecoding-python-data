from transformers.AbstractTransformer import AbstractTransformer


class PaymentCreatedTransformer(AbstractTransformer):
    def transform(self, key: str | None, value: str):
        print(f"Key: {key}; Value: {value}")