#!/usr/bin/env python3
"""Minimal read-only IBKR/TWS raw socket probe.

Usage:
  python scripts/ibkr_tws_raw_probe.py ASTS RKLB RDW --port 4002

No orders. Resolves contracts with reqMatchingSymbols and requests delayed STK quotes.
"""
import argparse
import json
import socket
import struct
import time


def recv_msg(sock):
    hdr = sock.recv(4)
    if not hdr:
        return None
    size = struct.unpack(">I", hdr)[0]
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            break
        data += chunk
    return data


def send_fields(sock, fields):
    payload = b"\0".join(str(field).encode() for field in fields) + b"\0"
    sock.sendall(struct.pack(">I", len(payload)) + payload)


def connect(host, port, client_id):
    sock = socket.socket()
    sock.settimeout(1.5)
    sock.connect((host, port))
    payload = b"v100..178\0"
    sock.sendall(b"API\0" + struct.pack(">I", len(payload)) + payload)
    hello = recv_msg(sock).split(b"\0")
    send_fields(sock, [71, 2, client_id, ""])
    deadline = time.time() + 2
    init = []
    while time.time() < deadline:
        try:
            msg = recv_msg(sock)
        except TimeoutError:
            break
        if msg:
            init.append([x.decode("utf-8", "ignore") for x in msg.split(b"\0")[:8]])
    return sock, [x.decode("utf-8", "ignore") for x in hello[:2]], init


def parse_match(parts):
    out = []
    idx = 3
    try:
        count = int(parts[2])
    except Exception:
        return out
    for _ in range(count):
        if idx + 5 >= len(parts):
            break
        con_id, symbol, sec_type, primary, currency = parts[idx:idx + 5]
        idx += 5
        try:
            deriv_count = int(parts[idx])
            idx += 1
        except Exception:
            deriv_count = 0
        derivatives = parts[idx:idx + deriv_count]
        idx += deriv_count
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


def choose_contract(matches, symbol):
    exact = [m for m in matches if m["symbol"].upper() == symbol and m["secType"] == "STK" and m["currency"] == "USD"]
    if exact:
        return exact[0]
    stks = [m for m in matches if m["secType"] == "STK" and m["currency"] == "USD"]
    return stks[0] if stks else (matches[0] if matches else None)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("symbols", nargs="+")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=4002)
    parser.add_argument("--client-id", type=int, default=940)
    args = parser.parse_args()

    sock, hello, init = connect(args.host, args.port, args.client_id)
    send_fields(sock, [59, 1, 3])  # delayed market data

    contracts = {}
    prices = {}
    for offset, symbol in enumerate(args.symbols, 1):
        symbol = symbol.upper()
        req_id = 3000 + offset
        send_fields(sock, [81, req_id, symbol])
        deadline = time.time() + 3
        while time.time() < deadline:
            try:
                msg = recv_msg(sock)
            except TimeoutError:
                continue
            if not msg:
                break
            parts = [x.decode("utf-8", "ignore") for x in msg.split(b"\0")]
            if parts and parts[0] == "79" and parts[1] == str(req_id):
                contracts[symbol] = choose_contract(parse_match(parts), symbol)
                break

    ticker_map = {}
    for offset, (symbol, contract) in enumerate(contracts.items(), 1):
        if not contract:
            continue
        ticker_id = 5000 + offset
        ticker_map[ticker_id] = symbol
        prices[symbol] = {
            "tickerId": ticker_id,
            "conId": contract.get("conId"),
            "primaryExchange": contract.get("primaryExchange"),
            "desc": contract.get("desc"),
            "bid": None,
            "ask": None,
            "last": None,
            "close": None,
            "errors": [],
        }
        send_fields(sock, [
            1, 11, ticker_id, 0, symbol, "STK", "", 0.0, "", "",
            "SMART", contract.get("primaryExchange") or "", "USD", "", "",
            "", "", 0, 0, "",
        ])

    deadline = time.time() + 12
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
            symbol = ticker_map.get(ticker_id)
            if symbol:
                if tick_type == 66:
                    prices[symbol]["bid"] = value
                elif tick_type == 67:
                    prices[symbol]["ask"] = value
                elif tick_type == 68:
                    prices[symbol]["last"] = value
                elif tick_type == 75:
                    prices[symbol]["close"] = value
        elif parts and parts[0] == "4" and len(parts) > 5:
            for symbol, row in prices.items():
                if parts[2] == str(row["tickerId"]):
                    row["errors"].append(parts[3:5])

    print(json.dumps({"hello": hello, "init": init, "contracts": contracts, "prices": prices}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
