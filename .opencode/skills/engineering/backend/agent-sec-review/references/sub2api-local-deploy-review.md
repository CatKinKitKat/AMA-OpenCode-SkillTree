# Sub2API local deploy review pattern

Session context: user asked to install/deploy `https://github.com/Wei-Shaw/sub2api` on macOS.

Durable lessons
- Treat Sub2API as MEDIUM/HIGH-ish external service deployment: it is an AI API gateway, stores upstream account/API credentials, exposes admin UI, and can proxy requests to external model providers.
- Do not pipe the upstream one-liners directly (`curl ... install.sh | sudo bash` or `curl ... docker-deploy.sh | bash`) before local review. Prefer cloning/reading `README*`, `deploy/README.md`, compose files, env templates, and shell entrypoints.
- Prefer Docker Compose for the app, but bind the gateway to localhost by default on a workstation: `BIND_HOST=127.0.0.1` and choose a free high port rather than assuming `8080`.
- Generate fixed secrets before first boot: `POSTGRES_PASSWORD`, `REDIS_PASSWORD`, `JWT_SECRET`, `TOTP_ENCRYPTION_KEY`, and `ADMIN_PASSWORD`. Store admin login in a mode-600 file outside public logs.
- Enable safer URL defaults for local deployment when possible: `SECURITY_URL_ALLOWLIST_ENABLED=true`, `SECURITY_URL_ALLOWLIST_ALLOW_INSECURE_HTTP=false`, `SECURITY_URL_ALLOWLIST_ALLOW_PRIVATE_HOSTS=false`.
- If Docker Hub auth/pulls fail but GHCR works, use `ghcr.io/wei-shaw/sub2api:latest` for the app image. Avoid recording "Docker Hub broken" as a rule. This is a transient network/setup symptom.
- If postgres/redis container pulls are blocked but app image is available, a workable macOS fallback is: run the app in Docker, run PostgreSQL/Redis on the host, and connect from container via `host.docker.internal`.
- For Postgres fallback when Homebrew bottles fail, building upstream PostgreSQL source from cached tarball with `--without-icu --without-readline --without-zlib` can produce a local private `postgres`/`psql` under the deployment directory. This is a last-resort workstation workaround, not the preferred production path.

Verification checklist
- `docker compose ps` shows `sub2api` Up/healthy.
- `curl http://127.0.0.1:<port>/health` returns `{"status":"ok"}`.
- `curl -I http://127.0.0.1:<port>/` returns HTTP 200.
- Logs contain: `Database connection successful`, `Redis connection successful`, `Admin user created`, `Server started`.
- Check file modes for `.env`, admin credential file, start/stop helpers.

Reusable local layout
- Deployment root: user-chosen directory such as `~/sub2api-deploy`.
- Keep source clone separate from deployment root.
- `start.sh` should start local DB/cache first, then `docker compose up -d sub2api`.
- `stop.sh` should stop the Docker service and then local DB/cache.

Risk notes
- Admin UI and gateway must not be exposed to LAN/public without explicit user intent and reverse-proxy/auth hardening.
- The service downloads model pricing data from GitHub on first start. This is expected runtime network behavior.
- Data deletion commands in upstream docs (`docker compose down -v`, `rm -rf data postgres_data redis_data`) are destructive. Never run them unless explicitly requested.
