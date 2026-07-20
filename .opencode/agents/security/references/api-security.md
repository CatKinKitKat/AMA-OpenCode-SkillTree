# API Security Reference

**Author:** azizaeffendi  
**Last Updated:** 2026-06-05  
**Applies To:** REST APIs, GraphQL APIs, Node.js, Python/FastAPI, Go

---

## Quick Reference

Run these grep commands against your codebase to surface common API security issues immediately.

```bash
# Find endpoints missing authentication middleware
grep -rn "router\.\(get\|post\|put\|delete\|patch\)" --include="*.js" --include="*.ts" | grep -v "auth\|verify\|protect\|require"

# Find hardcoded API keys or tokens
grep -rn "api_key\s*=\s*['\"][A-Za-z0-9_\-]\{20,\}" --include="*.js" --include="*.ts" --include="*.py"

# Find wildcard CORS configuration
grep -rn "origin.*['\"]?\*['\"]?" --include="*.js" --include="*.ts" --include="*.py"

# Find missing ownership checks on resource endpoints
grep -rn "params\.id\|req\.params\.id\|request\.path_params" --include="*.js" --include="*.ts" --include="*.py" | grep -v "userId\|owner\|user_id"

# Find GraphQL introspection enabled
grep -rn "introspection.*true\|disableIntrospection.*false" --include="*.js" --include="*.ts"

# Find rate limiting gaps
grep -rn "app\.\(get\|post\|use\)" --include="*.js" --include="*.ts" | grep -v "rateLimit\|throttle\|limiter"

# Find SQL injection risk (raw query concatenation)
grep -rn "query\s*=\s*['\"]SELECT\|execute(['\"]SELECT" --include="*.js" --include="*.ts" --include="*.py"

# Find missing input validation
grep -rn "req\.body\.\|request\.json()" --include="*.js" --include="*.ts" --include="*.py" | grep -v "validate\|schema\|zod\|joi\|pydantic"
```

---

## REST API Authentication

### Rule: Every Endpoint Must Verify Authentication

No endpoint should be reachable without verifying that the caller holds a valid credential. Authentication should be enforced at the middleware layer: not duplicated per route: so that new routes are protected by default.

**Vulnerable Pattern: No Auth Check:**

```javascript
// INSECURE: Route has no authentication middleware
app.get('/api/users/:id', async (req, res) => {
  const user = await db.users.findById(req.params.id);
  res.json(user);
});

app.post('/api/orders', async (req, res) => {
  const order = await db.orders.create(req.body);
  res.json(order);
});
```

**Vulnerable Pattern: Auth Only on Some Routes:**

```javascript
// INSECURE: Auth applied inconsistently
app.get('/api/profile', authenticate, getProfile);   // protected
app.get('/api/settings', getSettings);               // FORGOT auth
app.post('/api/payment', authenticate, processPayment);
```

**Secure Pattern: Bearer Token with Global Middleware:**

```javascript
// auth.middleware.js
const jwt = require('jsonwebtoken');

function authenticate(req, res, next) {
  const authHeader = req.headers['authorization'];

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({
      error: 'Unauthorized',
      message: 'Authorization header with Bearer token required'
    });
  }

  const token = authHeader.split(' ')[1];

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;  // attach verified user to request
    next();
  } catch (err) {
    if (err.name === 'TokenExpiredError') {
      return res.status(401).json({ error: 'Token expired' });
    }
    return res.status(401).json({ error: 'Invalid token' });
  }
}

module.exports = { authenticate };

// routes.js — apply globally, then exempt public routes
app.use('/api', authenticate);                        // ALL /api routes require auth
app.post('/api/auth/login', loginHandler);            // Explicitly public
app.post('/api/auth/register', registerHandler);      // Explicitly public
app.get('/api/users/:id', getUserHandler);            // Protected by default
app.post('/api/orders', createOrderHandler);          // Protected by default
```

**Python / FastAPI Bearer Token:**

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# All protected routes declare the dependency
@app.get("/api/users/{user_id}")
async def get_user(user_id: str, current_user: dict = Depends(verify_token)):
    ...
```

---

## GraphQL Security

### Disable Introspection in Production

Introspection exposes your entire schema: all types, fields, queries, and mutations: to any caller. In development this is useful. In production it hands attackers a roadmap to every endpoint.

**Vulnerable Pattern:**

```javascript
const server = new ApolloServer({
  typeDefs,
  resolvers,
  // No introspection config — defaults to enabled
});
```

**Secure Pattern:**

```javascript
const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: process.env.NODE_ENV !== 'production',  // disabled in prod
  plugins: [
    // Also block field suggestions that leak schema shape
    {
      requestDidStart() {
        return {
          didResolveOperation({ request, document }) {
            if (process.env.NODE_ENV === 'production') {
              const hasIntrospection = document.definitions.some(
                def => def.selectionSet?.selections?.some(
                  sel => sel.name?.value?.startsWith('__')
                )
              );
              if (hasIntrospection) {
                throw new Error('Introspection is disabled');
              }
            }
          }
        };
      }
    }
  ]
});
```

### Query Depth Limiting

Without depth limits, attackers can craft deeply nested queries that cause exponential database load.

```javascript
// INSECURE: No depth limit
// Attacker sends: { user { posts { comments { author { posts { comments { ... } } } } } } }

// SECURE: Install graphql-depth-limit
const depthLimit = require('graphql-depth-limit');

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    depthLimit(5),              // max 5 levels of nesting
  ]
});
```

### Query Complexity Limiting

```javascript
const { createComplexityLimitRule } = require('graphql-validation-complexity');

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    depthLimit(5),
    createComplexityLimitRule(1000, {  // max complexity score of 1000
      onCost: (cost) => console.log('Query cost:', cost),
      formatErrorMessage: (cost) =>
        `Query complexity ${cost} exceeds maximum of 1000`
    })
  ]
});
```

### GraphQL Rate Limiting

```javascript
const { RateLimiterMemory } = require('rate-limiter-flexible');

const rateLimiter = new RateLimiterMemory({
  keyPrefix: 'graphql',
  points: 100,    // 100 requests
  duration: 60,   // per 60 seconds per IP
});

app.use('/graphql', async (req, res, next) => {
  try {
    await rateLimiter.consume(req.ip);
    next();
  } catch {
    res.status(429).json({ error: 'Too many requests' });
  }
});
```

---

## CORS Misconfiguration

### Dangerous Wildcard Patterns

CORS misconfiguration is one of the most common API vulnerabilities. A wildcard origin (`*`) tells browsers that any website can make credentialed requests to your API.

**Vulnerable Pattern: Wildcard Origin:**

```javascript
// INSECURE: Any origin allowed
app.use(cors({ origin: '*' }));

// Also insecure: Reflecting origin without validation
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', req.headers.origin);  // reflects ANY origin
  res.header('Access-Control-Allow-Credentials', 'true');
  next();
});

// Insecure: Regex too broad
const allowedOrigin = new RegExp('.*\\.myapp\\.com');  // matches evil-myapp.com
```

**Vulnerable Pattern: Null Origin:**

```javascript
// INSECURE: null origin is used by sandboxed iframes and local files
app.use(cors({
  origin: ['https://myapp.com', 'null'],  // "null" is dangerous
  credentials: true
}));
```

**Secure Pattern: Explicit Allowlist:**

```javascript
const cors = require('cors');

const allowedOrigins = [
  'https://myapp.com',
  'https://www.myapp.com',
  'https://admin.myapp.com',
  // Development only — guard with env check
  ...(process.env.NODE_ENV === 'development' ? ['http://localhost:3000'] : [])
];

app.use(cors({
  origin: (origin, callback) => {
    // Allow requests with no origin (server-to-server, curl)
    if (!origin) return callback(null, true);

    if (allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error(`CORS policy does not allow origin: ${origin}`));
    }
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  maxAge: 86400  // cache preflight for 24 hours
}));
```

---

## IDOR: Insecure Direct Object Reference

### The Problem

IDOR occurs when an API uses a user-supplied identifier (path param, query param, body field) to access a resource without verifying that the authenticated user has permission to access that specific resource.

**Vulnerable Pattern: Path Param Without Ownership Check:**

```javascript
// INSECURE: Any authenticated user can fetch any other user's data
app.get('/api/users/:id', authenticate, async (req, res) => {
  const user = await db.users.findById(req.params.id);  // no ownership check!
  res.json(user);
});

// INSECURE: Any user can view any order
app.get('/api/orders/:orderId', authenticate, async (req, res) => {
  const order = await db.orders.findById(req.params.orderId);  // attacker supplies any orderId
  res.json(order);
});

// INSECURE: Any user can update any record
app.put('/api/documents/:docId', authenticate, async (req, res) => {
  await db.documents.updateById(req.params.docId, req.body);
  res.json({ success: true });
});
```

**Secure Pattern: Always Filter by Authenticated userId:**

```javascript
// SECURE: Resource is fetched by BOTH resource id AND the authenticated user's id
app.get('/api/users/:id', authenticate, async (req, res) => {
  const { id } = req.params;
  const userId = req.user.id;  // from verified JWT, not from request body

  // User can only access their own record; admins can access any
  if (id !== userId && req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Forbidden' });
  }

  const user = await db.users.findById(id);
  if (!user) return res.status(404).json({ error: 'Not found' });
  res.json(user);
});

// SECURE: Order lookup scoped to authenticated user
app.get('/api/orders/:orderId', authenticate, async (req, res) => {
  const order = await db.orders.findOne({
    id: req.params.orderId,
    userId: req.user.id  // attacker cannot access another user's order
  });

  if (!order) return res.status(404).json({ error: 'Not found' });
  res.json(order);
});

// SECURE: Document update scoped to owner
app.put('/api/documents/:docId', authenticate, async (req, res) => {
  const updated = await db.documents.updateOne(
    { id: req.params.docId, ownerId: req.user.id },  // WHERE clause includes owner
    req.body
  );

  if (!updated) return res.status(404).json({ error: 'Not found' });
  res.json({ success: true });
});
```

**Python / FastAPI IDOR Fix:**

```python
@app.get("/api/orders/{order_id}")
async def get_order(
    order_id: str,
    current_user: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    order = await db.execute(
        select(Order).where(
            Order.id == order_id,
            Order.user_id == current_user["sub"]  # always scope to authenticated user
        )
    )
    order = order.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Not found")
    return order
```

---

## Input Validation on All API Endpoints

All user-supplied data must be validated for type, format, length, and allowed values before use.

**Vulnerable Pattern: No Validation:**

```javascript
app.post('/api/transfer', authenticate, async (req, res) => {
  const { toAccount, amount } = req.body;
  // No validation: amount could be negative, string, or missing
  await db.transfers.create({ from: req.user.id, to: toAccount, amount });
  res.json({ success: true });
});
```

**Secure Pattern: Schema Validation with Zod (Node.js):**

```javascript
const { z } = require('zod');

const transferSchema = z.object({
  toAccount: z.string().uuid('Invalid account ID'),
  amount: z.number()
    .positive('Amount must be positive')
    .max(10000, 'Amount exceeds per-transfer limit')
    .multipleOf(0.01, 'Amount must have at most 2 decimal places'),
  note: z.string().max(256).optional()
});

app.post('/api/transfer', authenticate, async (req, res) => {
  const result = transferSchema.safeParse(req.body);

  if (!result.success) {
    return res.status(400).json({
      error: 'Validation failed',
      details: result.error.errors
    });
  }

  const { toAccount, amount, note } = result.data;
  await db.transfers.create({ from: req.user.id, to: toAccount, amount, note });
  res.json({ success: true });
});
```

**Python Pydantic Validation:**

```python
from pydantic import BaseModel, Field, validator
from decimal import Decimal

class TransferRequest(BaseModel):
    to_account: str = Field(..., description="UUID of destination account")
    amount: Decimal = Field(..., gt=0, le=10000, decimal_places=2)
    note: str | None = Field(None, max_length=256)

    @validator('to_account')
    def validate_uuid(cls, v):
        import uuid
        try:
            uuid.UUID(v)
        except ValueError:
            raise ValueError('Invalid account ID format')
        return v

@app.post("/api/transfer")
async def create_transfer(
    body: TransferRequest,
    current_user: dict = Depends(verify_token)
):
    await db.transfers.create(
        from_account=current_user["sub"],
        to_account=body.to_account,
        amount=body.amount
    )
    return {"success": True}
```

---

## Pitfalls

### Pitfall 1: JWT `none` Algorithm Attack

Never trust the algorithm declared in the JWT header. An attacker can change `alg` to `none` and send an unsigned token if your library honors the header.

```javascript
// VULNERABLE: trusts the header's algorithm
const decoded = jwt.verify(token, secret);  // some libs allow alg:none bypass

// SECURE: explicitly specify allowed algorithms
const decoded = jwt.verify(token, secret, { algorithms: ['HS256'] });
```

### Pitfall 2: Mass Assignment

When you pass `req.body` directly to a model update, attackers can set fields like `isAdmin: true` or `balance: 99999` that were never intended to be user-editable.

```javascript
// VULNERABLE
await User.updateById(req.params.id, req.body);

// SECURE: whitelist fields explicitly
const { displayName, bio, avatarUrl } = req.body;
await User.updateById(req.params.id, { displayName, bio, avatarUrl });
```

### Pitfall 3: 401 vs 403 Confusion Leaks Resource Existence

Returning 404 for all resource-not-found or forbidden responses prevents attackers from enumerating resource IDs. Returning 403 only when a resource exists but the user can't access it leaks that the resource ID is valid.

```javascript
// LEAKS: confirms resource exists with different status codes
const doc = await db.documents.findById(req.params.id);
if (!doc) return res.status(404).json({ error: 'Not found' });
if (doc.ownerId !== req.user.id) return res.status(403).json({ error: 'Forbidden' });

// SECURE: uniform 404 for not-found and unauthorized access
const doc = await db.documents.findOne({
  id: req.params.id,
  ownerId: req.user.id
});
if (!doc) return res.status(404).json({ error: 'Not found' });  // attacker learns nothing
```

### Pitfall 4: Rate Limiting Applied Only at the Load Balancer

IP-based rate limiting at the load balancer is bypassed when attackers distribute across thousands of IPs. Apply rate limiting per user account as well.

```javascript
// SECURE: rate limit per userId, not just per IP
const rateLimiter = new RateLimiterMemory({ points: 20, duration: 60 });

async function perUserRateLimit(req, res, next) {
  const key = req.user?.id || req.ip;  // use userId when authenticated
  try {
    await rateLimiter.consume(key);
    next();
  } catch {
    res.status(429).json({ error: 'Rate limit exceeded' });
  }
}
```

### Pitfall 5: GraphQL Batching Amplification

GraphQL allows sending an array of operations in one request. Without limits, this bypasses per-request rate limits.

```javascript
// SECURE: disable or limit query batching
const server = new ApolloServer({
  allowBatchedHttpRequests: false,  // disable entirely in prod
  // OR limit batch size:
  // allowBatchedHttpRequests: true,
  // maxBatchSize: 5
});
```

### Pitfall 6: Verbose Error Messages in Production

Stack traces and database error messages expose schema details, file paths, and query structure to attackers.

```javascript
// VULNERABLE
app.use((err, req, res, next) => {
  res.status(500).json({ error: err.message, stack: err.stack });  // leaks internals
});

// SECURE
app.use((err, req, res, next) => {
  console.error(err);  // log full error server-side
  const isProd = process.env.NODE_ENV === 'production';
  res.status(500).json({
    error: isProd ? 'Internal server error' : err.message
  });
});
```

### Pitfall 7: Missing Content-Type Enforcement

APIs that accept any Content-Type can be tricked into parsing XML (XXE attacks) or other formats when only JSON is expected.

```javascript
// SECURE: enforce Content-Type for mutation endpoints
app.use('/api', (req, res, next) => {
  if (['POST', 'PUT', 'PATCH'].includes(req.method)) {
    if (!req.is('application/json')) {
      return res.status(415).json({ error: 'Content-Type must be application/json' });
    }
  }
  next();
});
```

---

## Verification

Run these commands after applying fixes to confirm security controls are in place.

```bash
# 1. Verify unauthenticated requests are rejected
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/users/123
# Expected: 401

# 2. Verify Bearer token is required
curl -s -H "Authorization: Basic dXNlcjpwYXNz" http://localhost:3000/api/users/123
# Expected: 401

# 3. Test IDOR — attempt to access another user's resource with valid token
TOKEN=$(curl -s -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"attacker@example.com","password":"password123"}' | jq -r .token)

curl -s -H "Authorization: Bearer $TOKEN" http://localhost:3000/api/users/VICTIM_USER_ID
# Expected: 403 or 404

# 4. Verify CORS rejects unauthorized origins
curl -s -H "Origin: https://evil.com" -I http://localhost:3000/api/users
# Expected: No Access-Control-Allow-Origin header, or header does NOT contain evil.com

# 5. Test GraphQL introspection is disabled in production
curl -s -X POST http://localhost:3000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { types { name } } "}' | jq .errors
# Expected: error about introspection being disabled

# 6. Test input validation rejects invalid data
curl -s -X POST http://localhost:3000/api/transfer \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"toAccount":"not-a-uuid","amount":-100}'
# Expected: 400 with validation errors

# 7. Verify rate limiting kicks in
for i in {1..25}; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/users)
  echo "Request $i: $STATUS"
done
# Expected: 429 after threshold is exceeded
```
