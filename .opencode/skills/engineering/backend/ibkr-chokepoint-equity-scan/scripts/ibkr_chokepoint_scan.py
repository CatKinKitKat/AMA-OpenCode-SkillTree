#!/usr/bin/env python3
"""Raw IBKR TWS/Gateway contract + delayed quote scanner.

Usage:
  python3 ibkr_chokepoint_scan.py ASTS RKLB RDW AEHR ACMR

No ibapi/ib_insync dependency. Read-only: discovers contracts and subscribes to
market data; it never sends order messages.
"""
from __future__ import annotations

import argparse
import json
import socket
import struct
import time
from typing import Any

REQ_MKT_DATA = 1
CANCEL_MKT_DATA = 2
START_API = 71
REQ_MARKET_DATA_TYPE = 59
REQ_MATCHING_SYMBOLS = 81

TICK_DELAYED_BID = 66
TICK_DELAYED_ASK = 67
TICK_DELAYED_LAST = 68
TICK_DELAYED_CLOSE = 75


def recv_msg(sock: socket.socket) -> bytes | None:
    header = sock.recv(4)
    if not header:
        return None
    size = struct.unpack(">I", header)[0]
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            break
        data += chunk
    return data


def send_fields(sock: socket.socket, fields: list[Any]) -> None:
    payload = b"\0".join(str(field).encode() for field in fields) + b"\0"
    sock.sendall(struct.pack(">I", len(payload)) + payload)


def connect(host: str, port: int, client_id: int) -> tuple[socket.socket, list[str], list[list[str]]]:
    sock = socket.socket()
    sock.settimeout(1.5)
    sock.connect((host, port))
    payload = b"v100..178\0"
    sock.sendall(b"API\0" + struct.pack(">I", len(payload)) + payload)
    hello = (recv_msg(sock) or b"").split(b"\0")
    send_fields(sock, [START_API, 2, client_id, ""])
    init: list[list[str]] = []
    end = time.time() + 2
    while time.time() < end:
        try:
            msg = recv_msg(sock)
        except TimeoutError:
            break
        if msg:
            init.append([x.decode("utf-8", "ignore") for x in msg.split(b"\0")[:8]])
    return sock, [x.decode("utf-8", "ignore") for x in hello[:2]], init


def parse_matches(parts: list[str]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    idx = 3
    try:
        count = int(parts[2])
    except Exception:
        count = 0
    for _ in range(count):
        if idx + 5 >= len(parts):
            break
        con_id, symbol, sec_type, primary, currency = parts[idx:idx + 5]
        idx += 5
        try:
            derivative_count = int(parts[idx])
            idx += 1
        except Exception:
            derivative_count = 0
        derivatives = parts[idx:idx + derivative_count]
        idx += derivative_count
        desc = parts[idx] if idx < len(parts) else ""
        idx += 1
        issuer = parts[idx] if idx < len(parts) else ""
        idx += 1
        out.append({
            "conId": con_id,
            "symbol": symbol,
            "secType": sec_type,
            "primaryExchange": primary,
            "currency": currency,
            "derivatives": derivatives,
            "desc": desc,
            "issuer": issuer,
        })
    return out


def choose_contract(matches: list[dict[str, Any]], symbol: str, currency: str) -> dict[str, Any] | None:
    exact = [m for m in matches if m["symbol"].upper() == symbol.upper() and m["secType"] == "STK" and m["currency"] == currency]
    if exact:
        return exact[0]
    stks = [m for m in matches if m["secType"] == "STK" and m["currency"] == currency]
    return stks[0] if stks else (matches[0] if matches else None)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("symbols", nargs="+", help="Ticker symbols to scan")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=4002)
    parser.add_argument("--client-id", type=int, default=940)
    parser.add_argument("--currency", default="USD")
    parser.add_argument("--seconds", type=float, default=18.0)
    args = parser.parse_args()

    sock, hello, init = connect(args.host, args.port, args.client_id)
    send_fields(sock, [REQ_MARKET_DATA_TYPE, 1, 3])  # delayed data fallback

    contracts: dict[str, dict[str, Any] | None] = {}
    raw_matches: dict[str, list[dict[str, Any]]] = {}
    errors: list[list[str]] = []

    for offset, symbol in enumerate(args.symbols, start=1):
        request_id = 3000 + offset
        send_fields(sock, [REQ_MATCHING_SYMBOLS, request_id, symbol])
        deadline = time.time() + 3
        while time.time() < deadline:
            try:
                msg = recv_msg(sock)
            except TimeoutError:
                continue
            if not msg:
                break
            parts = [x.decode("utf-8", "ignore") for x in msg.split(b"\0")]
            if parts and parts[0] == "79" and parts[1] == str(request_id):
                matches = parse_matches(parts)
                raw_matches[symbol] = matches[:5]
                contracts[symbol] = choose_contract(matches, symbol, args.currency)
                break
            if parts and parts[0] == "4":
                errors.append(parts[:6])

    prices: dict[str, dict[str, Any]] = {}
    for offset, (symbol, contract) in enumerate(contracts.items(), start=1):
        if not contract:
            continue
        ticker_id = 5000 + offset
        primary = contract.get("primaryExchange") or ""
        fields = [
            REQ_MKT_DATA, 11, ticker_id, 0, symbol, "STK", "", 0.0, "", "",
            "SMART", primary, args.currency, "", "", "", "", 0, 0, "",
        ]
        send_fields(sock, fields)
        prices[symbol] = {
            "tickerId": ticker_id,
            "conId": contract.get("conId"),
            "primaryExchange": primary,
            "desc": contract.get("desc"),
            "bid": None,
            "ask": None,
            "last": None,
            "close": None,
            "errors": [],
        }

    id_to_symbol = {item["tickerId"]: symbol for symbol, item in prices.items()}
    deadline = time.time() + args.seconds
    while time.time() < deadline:
        try:
            msg = recv_msg(sock)
        except TimeoutError:
            continue
        if not msg:
            break
        parts = [x.decode("utf-8", "ignore") for x in msg.split(b"\0")]
        if parts and parts[0] == "1" and len(parts) > 5:
            ticker_id = int(parts[2])
            tick_type = int(parts[3])
            value = float(parts[4])
            symbol = id_to_symbol.get(ticker_id)
            if not symbol:
                continue
            if tick_type == TICK_DELAYED_BID:
                prices[symbol]["bid"] = value
            elif tick_type == TICK_DELAYED_ASK:
                prices[symbol]["ask"] = value
            elif tick_type == TICK_DELAYED_LAST:
                prices[symbol]["last"] = value
            elif tick_type == TICK_DELAYED_CLOSE:
                prices[symbol]["close"] = value
        elif parts and parts[0] == "4" and len(parts) > 5:
            request_id = parts[2]
            for symbol, item in prices.items():
                if str(item["tickerId"]) == request_id:
                    item["errors"].append(parts[3:5])

    for symbol, item in prices.items():
        bid = item.get("bid")
        ask = item.get("ask")
        last = item.get("last")
        close = item.get("close")
        midpoint = (bid + ask) / 2 if isinstance(bid, float) and isinstance(ask, float) else None
        px = last if isinstance(last, float) and last > 0 else midpoint or close
        item["price"] = px
        if isinstance(px, float):
            item["buy_pullback"] = round(px * 0.92, 2)
            item["buy_add"] = round(px * 0.85, 2)
            item["stop"] = round(px * 0.78, 2)
            item["take_profit_1"] = round(px * 1.25, 2)
            item["take_profit_2"] = round(px * 1.55, 2)

    print(json.dumps({
        "ibkr": {"host": args.host, "port": args.port, "hello": hello, "init": init},
        "contracts": contracts,
        "prices": prices,
        "raw_matches": raw_matches,
        "errors": errors,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
