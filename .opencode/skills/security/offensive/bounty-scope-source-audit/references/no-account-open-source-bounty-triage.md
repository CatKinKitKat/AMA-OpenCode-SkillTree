# No-account open-source bounty triage

Session pattern: user provided a HackerOne-style scope CSV and asked for bugs that can be found without preparing an account.

## Workflow

1. Parse the CSV first.
2. List `asset_type == SOURCE_CODE` rows before live domains or mobile apps.
3. If only one source-code row exists, start there even if other rows mention repos under `OTHER`.
4. Use gread or a local zip clone for source mapping. If gread output is partial or API formatting is awkward, download the repo archive to `/tmp/<repo>` and use local `rg`/file reads.
5. Start with high-signal sinks, then broaden to no-account service risks:
   - shell/eval: `exec`, `ProcessBuilder`, `scala.sys.process`, `Runtime.getRuntime`, `eval`
   - web routes: `path`, `pathPrefix`, `endpointPath`, `parameters`, `parseEntity`, `extractRequest`
   - auth absence: `authorization`, `authenticate`, `bearer`, `cookie`, `session`, `csrf`
   - cross-origin defaults: `cors`, `Access-Control`, `Origin`
   - request-body and compression: `runReduce(_ ++ _)`, `withoutSizeLimit`, `decodeRequest`, `max-content-length`
   - write endpoints: `publish`, `POST`, `actorSelection`, `complete`
6. Report candidates as `confirmed`, `high-risk design`, or `needs runtime proof`.

## Netflix Atlas notes from 2026-05-11 session

Scope CSV rows:
- Clean `SOURCE_CODE`: `Open Source - Atlas` -> `https://github.com/Netflix/atlas`
- Repo-like but not `SOURCE_CODE`: `Open Source - Zuul`, `Open Source - Spectator`
- Out of scope examples: `Open Source - Consoleme`, `Open Source - Weep`, `Open Source - Dispatch`

Atlas source-first candidate themes:
- Default broad CORS:
  - `atlas-pekko/src/main/resources/reference.conf`: `cors-host-patterns = ["*"]`, `request-handler.cors = true`
  - `atlas-pekko/src/main/scala/com/netflix/atlas/pekko/RequestHandler.scala`: `standardOptions` wraps routes with `cors(...)` when enabled
  - needs runtime proof of exact allowed-origin/credentials/header behavior
- Unauthenticated publish/write endpoint:
  - `atlas-webapi/src/main/scala/com/netflix/atlas/webapi/PublishApi.scala`: `POST /api/v1/publish` -> `parseEntity` -> `validate` -> `/user/publish`
  - `conf/memory.conf` includes `com.netflix.atlas.webapi.PublishApi`
  - grep did not find auth/session/bearer checks in the webapi publish path
  - needs local or documented deployment proof before claiming impact
- Body aggregation / decompression DoS surface:
  - `atlas-pekko/src/main/scala/com/netflix/atlas/pekko/CustomDirectives.scala`: `entity.dataBytes.runReduce(_ ++ _)`
  - `atlas-pekko/src/main/resources/reference.conf`: `max-content-length = 8m`
  - `RequestHandler.scala` uses `decodeRequest` when compression is enabled
  - needs runtime proof of whether request-size limits apply before or after decompression

## Pitfalls

- Do not overclaim source findings as deploy-impact without proving defaults are used in a reachable service mode.
- If a local SBT test run times out or the repo wrapper differs (`project/sbt` rather than `./sbt`), keep the source triage and runtime verification status separate.
- For public bounty scope, avoid broad live probing when the user only asked for no-account/source-first leads.
