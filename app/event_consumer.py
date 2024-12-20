import six
import sys

from transformers.abstract_transformer import AbstractTransformer

if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves
from kafka import KafkaConsumer


class EventConsumer:
    def __init__(self, topic_name: str, broker: str, group_id: str, transformer: AbstractTransformer):
        self.topic_name = topic_name
        self.broker = broker
        self.group_id = group_id

        self.transformer = transformer
        self.consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers=[broker],
            group_id="group_id",
            enable_auto_commit=True,
        )

    def listen(self, max_messages=None):
        print(f"Consumer with group id: {self.group_id} listening to topic {self.topic_name} from broker {self.broker}")

        messages_read = 0
        for message in self.consumer:
            key = message.key.decode("utf-8") if message.key else None
            value = message.value.decode("utf-8")

            self.transformer.transform(value)

            messages_read += 1
            if max_messages and messages_read >= max_messages:
                return
