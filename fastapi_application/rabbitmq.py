import asyncio
import json
import logging
from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitQueue

from core.config import settings
from core.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

broker = RabbitBroker(
    url=settings.rabbitmq.url_amqp,
    virtualhost=settings.rabbitmq.vhost,
)

queue = RabbitQueue(name=settings.rabbitmq.quitue, durable=True)
app_rb = FastStream(broker)


async def process_message(message):
    try:
        data = json.loads(message)
        logger.info(f"Received message: {data}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode message: {e}")
        print(f"Failed to decode message: {e}")
    except Exception as e:
        logger.error(f"Failed to process message: {e}")


@broker.subscriber(queue)
async def get_message(message):
    await process_message(message)


async def start_broker():
    while True:
        try:
            await broker.connect()
            print("Broker connected and started.")
            break
        except Exception as e:
            print(f"Failed to connect to broker: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)
