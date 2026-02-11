# Execution Engine Demo

Async limit order execution engine with:

- Replace-on-price-move logic
- Partial fill tracking across order replacements
- Slippage modeling
- Price step rounding
- Exchange abstraction via protocol interface
- Mock exchange for deterministic testing

## Structure

- execution_engine.py — core execution logic
- mock_exchange.py — simulated exchange
- run.py — demo runner

## Run

python run.py

