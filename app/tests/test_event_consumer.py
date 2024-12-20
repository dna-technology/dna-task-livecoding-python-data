import json
import os
import sqlite3
import sys
from sqlite3 import Connection

import pytest
import six

if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves
from kafka import KafkaProducer

from abstract_database import AbstractDatabase
from event_consumer import EventConsumer
from transformers.abstract_transformer import AbstractTransformer


class DummyTransformer(AbstractTransformer):
    def transform(self, value: str):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO raw_events (event_data)
            VALUES (?)
        """, (value,))
        self.conn.commit()

class DummyDatabase(AbstractDatabase):
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute("""
                CREATE TABLE raw_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_data TEXT
                )
            """)
    def get_connection(self) -> Connection:
        return self.conn


@pytest.fixture
def database():
    database = DummyDatabase()
    yield database
    database.get_connection().close()

@pytest.fixture
def dummy_transformer(database):
    return DummyTransformer(database)

@pytest.fixture
def kafka_connection_string():
    return "{}:{}".format(os.getenv("KAFKA_HOST", "localhost"), os.getenv("KAFKA_PORT", "9092"))

@pytest.fixture
def kafka_producer(kafka_connection_string):
    producer = KafkaProducer(
        bootstrap_servers=[kafka_connection_string],
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    yield producer
    producer.close()

def test_event_consumer(kafka_producer, kafka_connection_string, database, dummy_transformer):
    topic_name = "payments.updated"
    group_id = "payment-consumers"

    consumer = EventConsumer(topic_name, kafka_connection_string, group_id, dummy_transformer)

    event_data = {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "merchantId": "M12345",
        "storeId": "S12345",
        "amount": 150,
        "currency": "USD",
        "paymentMethod": "CreditCard",
        "date": "2024-06-17"
    }

    kafka_producer.send(topic_name, event_data)
    kafka_producer.flush()

    consumer.listen(1)

    cursor = database.get_connection().cursor()
    cursor.execute("SELECT event_data FROM raw_events")
    result = cursor.fetchone()
    assert result[0] == json.dumps(event_data)
