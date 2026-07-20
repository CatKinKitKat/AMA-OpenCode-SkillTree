# Atlas source-audit notes

Session scope:
- Target repo: `Netflix/atlas`
- Source repo inspected via gread, then a shallow zip clone under `/tmp/atlas`

Key findings:
- `atlas-webapi/src/main/scala/com/netflix/atlas/webapi/PublishApi.scala`
  - `POST /api/v1/publish` and `POST /api/v1/publish-fast` accept JSON body, validate, and forward to `/user/publish`.
  - No route-local auth/session/token check was present in the source path.
- `atlas-pekko/src/main/resources/reference.conf`
  - shipped defaults: `cors-host-patterns = ["*"]` and `request-handler.cors = true`.
- `atlas-pekko/src/main/scala/com/netflix/atlas/pekko/CustomDirectives.scala`
  - `parseEntity` does `entity.dataBytes.runReduce(_ ++ _)`, so request bodies are fully buffered before decode.
- `atlas-standalone/src/main/scala/com/netflix/atlas/standalone/Main.scala`
  - standalone launch path is `atlas-standalone/runMain com.netflix.atlas.standalone.Main <config-file>`.
- `conf/memory.conf`
  - enabling `PublishApi` in the standalone profile can be done by adding the publish actor and endpoint.

Operational notes:
- `./sbt` is not present in this repo. Use `sh project/sbt ...`.
- First sbt invocation may spend a long time downloading boot artifacts. Do not confuse boot delay with a hung service.
- For fast proof-of-concept, prefer a minimal config and source inspection over full test suite execution.

PoC bundle pattern:
- `report.md`
- `poc-publish.sh`
- `poc-cors.sh`
- `poc-gzip-body.sh`

Verification reminders:
- Prove the endpoint with a valid JSON POST first.
- Then confirm CORS behavior with an `Origin` header.
- Then probe the compressed-body path separately.
