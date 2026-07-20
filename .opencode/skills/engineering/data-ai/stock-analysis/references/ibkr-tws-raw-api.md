# IBKR/TWS raw API notes

Use this when a stock-analysis task explicitly requires IBKR/TWS API access and Python packages such as `ibapi` or `ib_insync` are missing.

## Raw protocol facts verified

- TWS/Gateway socket port may be probed with a normal TCP connect, e.g. `127.0.0.1:4002`.
- v100 handshake:
  - Send `b"API\0" + uint32_be(len(payload)) + payload`
  - Payload example: `b"v100..178\0"`
  - Server replies as length-prefixed NUL fields: server version, connection time.
- Start API:
  - Send length-prefixed NUL fields: `[71, 2, clientId, ""]`.
- Symbol search:
  - `reqMatchingSymbols` request fields: `[81, reqId, pattern]`.
  - Matching-symbol response begins with message id `79`, then `reqId`, result count, and contract blocks.
- Delayed market data:
  - Send market data type request `[59, 1, 3]` before quote subscriptions.
  - Status `10167 Requested market data is not subscribed. Displaying delayed market data...` means delayed data is being returned.
- Stock quote request:
  - `REQ_MKT_DATA` works with message version 11:
    `[1, 11, tickerId, 0, symbol, "STK", "", 0.0, "", "", "SMART", primaryExchange, "USD", "", "", "", "", 0, 0, ""]`
  - Without the `11` version field, TWS may parse the tickerId as `Con Id` and return error `320 Unable to parse field: 'Con Id'`.

## Tick types observed

- `66` delayed bid
- `67` delayed ask
- `68` delayed last
- `74` delayed volume
- `75` delayed close
- `58` market data type acknowledgement
- `81` market data tick attributes

## Reporting discipline

- State clearly whether quote data is live or delayed.
- Keep IBKR conId, primary exchange, and delayed-data status in the evidence block.
- Do not place orders from this workflow unless the user explicitly asks and confirms order parameters.
- If a secondary provider is used for fundamentals/history, label it separately. Do not imply it came from IBKR.
