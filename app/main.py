import threading

from EventConsumer import EventConsumer
from transformers.PaymentCreatedTransformer import PaymentCreatedTransformer


paymentCreatedConsumer = EventConsumer("payments.created", "localhost:9092", "payment-consumers", PaymentCreatedTransformer())
paymentCreatedConsumer.listen()

thread1 = threading.Thread(target=paymentCreatedConsumer.listen)

thread1.join()