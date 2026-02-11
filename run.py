import asyncio
from execution_engine import ExecutionEngine, ReplaceConfig, MarketSnapshot
from mock_exchange import MockExchange

async def market_simulator(engine):
    import random
    while True:
        bid = 100 + random.uniform(-2, 2)
        ask = bid + 1
        engine.update_market(
            MarketSnapshot(best_bid=bid, best_ask=ask)
        )
        await asyncio.sleep(1)

async def main():

    exchange = MockExchange()

    engine = ExecutionEngine(
        exchange=exchange,
        instrument="BTC-PERP",
        price_step=0.5,
        slippage=0.0,
        replace_config=ReplaceConfig(
            check_period=1,
            max_distance_pct=0.02,
        ),
    )

    asyncio.create_task(market_simulator(engine))

    # wait until first market update arrives
    while engine.market is None:
        await asyncio.sleep(0.1)

    await engine.execute(side="buy", size=5)


if __name__ == "__main__":
    asyncio.run(main())
