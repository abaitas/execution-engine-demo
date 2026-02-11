import asyncio
import random
from typing import AsyncIterator
from execution_engine import ExchangeInterface, OrderUpdate


class MockExchange(ExchangeInterface):

    def __init__(self):
        self.orders = {}
        self.counter = 0

    async def place_limit_order(self, instrument, side, size, price):
        self.counter += 1
        order_id = f"order_{self.counter}"

        self.orders[order_id] = {
            "size": size,
            "filled": 0,
            "price": price,
            "status": "open"
        }

        return order_id

    async def cancel_order(self, order_id):
        if order_id in self.orders:
            self.orders[order_id]["status"] = "canceled"

    async def watch_order(self, order_id) -> AsyncIterator[OrderUpdate]:

        order = self.orders[order_id]

        while order["status"] == "open":

            await asyncio.sleep(0.5)

            remaining = order["size"] - order["filled"]
            fill = random.uniform(0, remaining * 0.5)

            order["filled"] += fill
            remaining = max(order["size"] - order["filled"], 0)

            if remaining <= 1e-6:
                remaining = 0
                order["status"] = "filled"

            yield OrderUpdate(
                order_id=order_id,
                filled=order["filled"],
                remaining=remaining,
                price=order["price"],
                status=order["status"],
            )

            if order["status"] in ("filled", "canceled"):
                break
