#! /usr/local/bin/python -u
import os
import threading

from file_database import FileDatabase
from event_consumer import EventConsumer
from transformers.payment_updated_transformer import PaymentUpdatedTransformer

kafkaConnectionString="{}:{}".format(os.getenv("KAFKA_HOST", "localhost"), os.getenv("KAFKA_PORT", "9092"))

def create_and_run_consumer():
    database = FileDatabase("db/db.db")
    paymentCreatedConsumer = EventConsumer("payments.update", kafkaConnectionString, "payment-consumers", PaymentUpdatedTransformer(database))
    paymentCreatedConsumer.listen()


thread1 = threading.Thread(target=create_and_run_consumer)
thread1.start()

thread1.join()
