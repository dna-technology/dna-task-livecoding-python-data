import json
import uuid

import pytest

from transformers.payment_updated_transformer import PaymentUpdatedTransformer
from file_database import FileDatabase


@pytest.fixture
def database():
    db = FileDatabase("db/db.db")
    yield db
    db.get_connection().close()

@pytest.fixture
def transformer(database: FileDatabase):
    transformer = PaymentUpdatedTransformer(database)
    return transformer

def test_payment_updated_transformer(transformer: PaymentUpdatedTransformer, database: FileDatabase):
    payment_id = str(uuid.uuid4())
    merchant_id_1 = str(uuid.uuid4())
    merchant_id_2 = str(uuid.uuid4())
    store_id_1 = str(uuid.uuid4())
    store_id_2 = str(uuid.uuid4())

    initial_event = json.dumps({
        "id": payment_id,
        "merchantId": merchant_id_1,
        "store_id": store_id_1,
        "amount": 150,
        "currency": "USD",
        "paymentMethod": "CreditCard",
        "date": "2024-06-17"
    })

    updated_event = json.dumps({
        "id": payment_id,
        "merchantId": merchant_id_2,
        "store_id": store_id_2,
        "amount": 200,
        "currency": "EUR",
        "paymentMethod": "CreditCard",
        "date": "2024-06-18"
    })

    transformer.transform(initial_event)

    cursor = database.get_connection().cursor()
    cursor.execute("SELECT * FROM payments WHERE id = ?", (payment_id,))
    result = cursor.fetchone()
    assert result == (
        payment_id, merchant_id_1, 150, "USD", "CreditCard", "2024-06-17"
    )

    transformer.transform(updated_event)

    cursor.execute("SELECT * FROM payments WHERE id = ?", (payment_id,))
    result = cursor.fetchone()
    assert result == (
        payment_id, merchant_id_2, 200, "EUR", "CreditCard", "2024-06-18"
    )
