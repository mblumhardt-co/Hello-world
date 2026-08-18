# Ethernet Sell Agent

A conversational sales agent for a telecommunications carrier's Ethernet
access wholesale desk. A human buyer chats in plain English; behind the
scenes the agent fills out and tracks an access order (an ASR in ASOG
format) without ever exposing that machinery to the buyer.

This is the **sell** side only. A matching **buy** agent (so two carriers'
agents can negotiate an order automatically) is a future step.

New to running code from a terminal, or working from an iPad? See
[SETUP.md](SETUP.md) for a plain-language, step-by-step walkthrough.

## How it works

- `sell_agent/asr.py` -- the order record (a pragmatic subset of ASR/ASOG
  fields for an Ethernet circuit). Fields split into **essential** (must ask
  the buyer) and **enrichable** (the agent derives/defaults them).
- `sell_agent/storage.py` -- orders are saved as JSON files under `orders/`,
  one per PON (Purchase Order Number), so they persist across conversations.
- `sell_agent/tools.py` -- the tools Claude uses to create, update, look up,
  and submit orders.
- `sell_agent/agent.py` -- the system prompt and the tool-use loop.
- `sell_agent/cli.py` -- a terminal chat interface.

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your-key-here
```

## Run it

```bash
python3 -m sell_agent.cli
```

Then just talk to it, e.g.:

> I'd like to place a new order.
> PON is ACME-0042.
> I need a 100 Meg Ethernet circuit at 123 Main St, Springfield, by end of next month.

Orders are saved to `orders/<PON>.json` and can be looked up again by PON in
a later conversation, even after restarting the CLI.

## Notes / next steps

- The ASR/ASOG field set here is a reasonable starting point, not a
  certified implementation -- validate it against your actual
  trading-partner spec before using this for real orders.
- No buyer authentication yet -- fine for a single-user demo, not for
  production.
- The buy agent, and the buy<->sell negotiation flow, come next.
