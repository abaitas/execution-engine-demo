# Async Execution Engine (Python Library)

A minimal, pip-installable event-driven execution engine demonstrating production-style
limit order management with strict exchange abstraction.

This project isolates execution logic from connectivity using a clean interface boundary.

---

## What It Demonstrates

- Partial fill tracking across order replacements
- Global target accumulation across multiple orders
- Price-distance based order replacement logic
- Slippage modeling
- Tick-size rounding
- Async order lifecycle handling (asyncio)
- Exchange abstraction via protocol interface
- Deterministic mock exchange for reproducible testing
- Floating-point tolerance protection for execution completion

The engine accumulates fill deltas across replaced orders and stops only when
the global target size is achieved.

---

## Architecture

ExecutionEngine
    ↓
ExchangeInterface (Protocol)
    ↓
Concrete Exchange (MockExchange or real adapter)

Execution logic is fully decoupled from connectivity.
Any exchange implementation conforming to ExchangeInterface can be plugged in.

---

## Installation

Install in editable mode:

pip install -e .

---

## Example

Run the included example:

python examples/simple_run.py

Example import:

from execution_engine.engine import ExecutionEngine

