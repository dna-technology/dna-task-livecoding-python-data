#! /usr/local/bin/python
import os
import threading

from database import Database
from event_consumer import EventConsumer
from transformers.payment_updated_transformer import PaymentUpdatedTransformer

database = Database("db/db.db")

kafkaConnectionString="{}:{}".format(os.getenv("KAFKA_HOST", "localhost"), os.getenv("KAFKA_PORT", "9092"))
paymentCreatedConsumer = EventConsumer("payments.updated", kafkaConnectionString, "payment-consumers", PaymentUpdatedTransformer(database))

thread1 = threading.Thread(target=paymentCreatedConsumer.listen)
thread1.start()

thread1.join()
