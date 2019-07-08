import asyncio
import string
import random


async def publish(queue):
    choices = string.ascii_lowercase + string.digits
    while True:
        host_id = "".join(random.choices(choices, k=4))
        msg = Message
