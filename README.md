# Async Execution Engine Demo

A minimal event-driven limit order execution engine demonstrating:

• Partial fill tracking across order replacements  
• Price-based order replacement logic  
• Slippage modeling  
• Tick-size rounding  
• Exchange abstraction via protocol interface  
• Deterministic mock exchange for testing  

This project isolates execution logic from exchange connectivity using a clean interface boundary.

## Architecture

ExecutionEngine
    ↳ ExchangeInterface (Protocol)
        ↳ MockExchange (simulation)

The engine accumulates fill deltas across replaced orders and stops when the global target size is achieved (with floating point tolerance protection).

## Run

python run.py

