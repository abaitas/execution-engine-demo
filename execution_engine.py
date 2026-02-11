import asyncio
from dataclasses import dataclass
from typing import AsyncIterator, Protocol


# ===== Data Models =====

@dataclass
class MarketSnapshot:
    best_bid: float
    best_ask: float


@dataclass
class OrderUpdate:
    order_id: str
    filled: float
    remaining: float
    price: float
    status: str


@dataclass
class ReplaceConfig:
    check_period: float
    max_distance_pct: float


# ===== Exchange Interface =====

class ExchangeInterface(Protocol):
    async def place_limit_order(self, instrument: str, side: str, size: float, price: float) -> str: ...
    async def cancel_order(self, order_id: str) -> None: ...
    async def watch_order(self, order_id: str) -> AsyncIterator[OrderUpdate]: ...


# ===== Execution Engine =====

class ExecutionEngine:

    def __init__(
        self,
        exchange: ExchangeInterface,
        instrument: str,
        price_step: float,
        slippage: float,
        replace_config: ReplaceConfig,
    ):
        self.exchange = exchange
        self.instrument = instrument
        self.price_step = price_step
        self.slippage = slippage
        self.replace_config = replace_config
        self.market: MarketSnapshot | None = None

    def update_market(self, snapshot: MarketSnapshot):
        self.market = snapshot

    def _round_to_step(self, value: float) -> float:
        return round(value / self.price_step) * self.price_step

    def _choose_price(self, side: str) -> float:
        if self.market is None:
            raise RuntimeError("Market not set")

        raw = self.market.best_ask if side == "buy" else self.market.best_bid

        if side == "buy":
            raw *= (1 + self.slippage)
        else:
            raw *= (1 - self.slippage)

        return self._round_to_step(raw)

    async def execute(self, side: str, size: float):
        total_filled = 0.0
        global_target = size  # constant
        EPSILON = 1e-6

        while True:

            remaining_global = global_target - total_filled

            if remaining_global <= EPSILON:
                print("Execution complete.")
                return

            price = self._choose_price(side)

            order_id = await self.exchange.place_limit_order(
                instrument=self.instrument,
                side=side,
                size=remaining_global,
                price=price,
            )

            print(f"Placed order {order_id} at {price}")

            prev_filled = 0.0

            async for update in self.exchange.watch_order(order_id):

                print(update)

                # compute delta fill for THIS order
                delta = update.filled - prev_filled
                prev_filled = update.filled

                # accumulate across ALL replaced orders
                total_filled += delta
                total_filled = min(total_filled, global_target)

                print(f"Total filled so far: {total_filled}")

                # early stop protection
                if global_target - total_filled <= EPSILON:
                    print("Execution complete.")
                    return

                if update.status in ("filled", "canceled"):
                    break

                await asyncio.sleep(self.replace_config.check_period)

                new_price = self._choose_price(side)
                distance = abs(new_price - price) / price

                if distance > self.replace_config.max_distance_pct:
                    print("Price moved. Replacing order.")
                    await self.exchange.cancel_order(order_id)
                    break
