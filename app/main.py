import threading

from database import Database
from event_consumer import EventConsumer
from transformers.payment_updated_transformer import PaymentUpdatedTransformer

database = Database("db/db.db")

paymentCreatedConsumer = EventConsumer("payments.updated", "localhost:9092", "payment-consumers", PaymentUpdatedTransformer(database))

thread1 = threading.Thread(target=paymentCreatedConsumer.listen)
thread1.start()

thread1.join()