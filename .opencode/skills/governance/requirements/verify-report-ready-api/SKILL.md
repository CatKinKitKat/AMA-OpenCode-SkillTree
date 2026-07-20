---
name: verify-report-ready-api
description: Parse a ReadyAPI PDF test report, classify failed tests by service and error type, and generate structured report folders with resume.md summary. Use when processing ReadyAPI test results from example platform test runs.
---

# Verify Report ReadyAPI

Parse a ReadyAPI PDF test report, classify all failed tests by **service** and **error type**, and generate a structured report with individual `.md` files and a `resume.md` summary.

## Parameters

`$ARGUMENTS` is the path to the report folder (e.g. `report/09-04-2026`). The folder must contain a file named `ReadyAPI Test Results.pdf`.

## Steps

### 1. Extract PDF text

Use PyMuPDF (`fitz`) to extract all text from `<folder>/ReadyAPI Test Results.pdf` and save to a temp file.

### 2. Parse failed test cases

Find all `TestCase Summary FAIL` sections in the extracted text. For each:

- Extract test case name (clean PDF artifacts: page headers, `===PAGEBREAK===`, `created with ReadyAPI...`)
- Find the parent TestSuite (from `Summary + TestCase Results` headers that precede the test)
- Find failed step name and error messages from `Step N [name] FAIL: took N ms` patterns
- Find HTTP detail blocks (`Status: FAIL` with Messages/Properties/Request sections) and extract: URL, Method, Request headers/body, Response
- Ignore entries whose name matches a known TestSuite name (e.g. `Alert WS`, `the-backend-algorithms`, etc.)

### 3. Determine service from URL

For each test, extract the service name from the URL pattern `/clientapp/<ServiceName>/`. Fallback mapping by suite name:

| Suite | Service |
|-------|---------|
| Alert WS, the-backend Alert Management, the-backend MANAGEMENT SERVICES, the-backend-algorithms, Alert Type, the-backend Position Debug, External Systems WS | AlertManagement |
| the-backend MONITORING WEB SERVICES | Reporting |
| Bounding Box Calculation | SurveillanceManagement |
| Distribution List WS | DistributionListManagement |
| External Users, Authorization Rules, the-project Platform Authorization | UserInfoManagement |

### 4. Classify error type

Classify each test into ONE of these error types (check in this priority order):

| Error Type | Detection Pattern |
|------------|-------------------|
| `db-connection` | Message contains `Listener refused`, `ORA-12516`, `SQLException` |
| `decimal-formatting` | Expected `[-N]` but Actual `[-N.0]` (integer vs decimal) |
| `notification-log` | Failed step contains `Notification Log` or message has `ID_NOTIF_LOG` + `Missing token` |
| `locode-assertion` | Failed step contains `Get Locode` |
| `data-setup-failure` | Failed step contains `Delete Old Data` |
| `alert-not-created` | Expected count `[1]` or `[2]` but Actual `[0]` on `result[*]` path |
| `alert-count-mismatch` | Count comparison failed with non-zero mismatch, or `JsonPath Count`, or step `GetAlerts from DB` |
| `status-error` | Path `$.status` with expected `success`/`error` mismatch |
| `authorization` | Message contains `unauthorized` or step contains `authorization` |
| `connection-error` | `SocketException`, `Broken pipe`, `Connection reset` |
| `xpath-assertion` | `XPath Match` in message |
| `field-mismatch` | `Smart Assertion` or `does not equal` |
| `response-content` | `Missing token` or `Response is not empty` or `Response contains token` |
| `config-error` | Step contains `config` or `assertion config` |
| `debug-pipeline` | Message contains `DBG_EVENT` or step contains `debug` |
| `surveillance-setup` | Step contains `Check if area` or `Find surveillance` |
| `assertion-mismatch` | Generic `Comparison failed` |
| `other` | Anything else |

### 5. Generate folder structure

Create this structure inside `<folder>/`:

```
<folder>/
├── resume.md
├── <ServiceName>/
│   ├── <error-type>/
│   │   ├── test-name-1.md
│   │   └── test-name-2.md
│   └── <error-type>/
│       └── ...
└── <ServiceName>/
    └── ...
```

Clean any existing service folders before generating.

### 6. Generate individual test `.md` files

Each test file must contain:

```markdown
# <Test Name>

**Suite:** <suite>  
**Service:** <service>  
**Error Type:** <error-type>  
**Failed Step:** <failed step name>

## Error Message

\```
<error message, cleaned of PDF artifacts>
\```

## Stacktrace

\```
Failed Step: <step name>
<error messages>

--- HTTP Request ---
<request details if available>
\```

## cURL

\```bash
<curl command built from URL, method, headers - or "N/A" if no HTTP details>
\```
```

### 7. Generate `resume.md`

The resume must have these sections in order:

1. **Header**: Title with date, Total Failed / Total tests (% failure rate), Source
2. **Failures by Service** table: `| Service | Falhas | % |` - sorted by count descending
3. **Comparison** table with previous report dates (if known from prior runs in `report/` folder - check for other `resume.md` files to extract their totals)
4. **Errors by Type** table: `| Error Type | Count | % | Description |` - sorted by count descending
5. **Detail per Service**: For each service, list error type subsections with test tables linking to the `.md` files

### Error Type Descriptions (for the table)

| Error Type | Description |
|------------|-------------|
| `db-connection` | ORA-12516 / Listener refused / JDBC connection failure |
| `decimal-formatting` | API returns -11.0 instead of -11 (integer vs decimal formatting) |
| `alert-not-created` | Expected alert not found (count=0) - alert engine did not produce the alert |
| `alert-count-mismatch` | Alert count differs from expected (wrong number of alerts) |
| `status-error` | API returned status "error" instead of "success" (or vice-versa) |
| `authorization` | Authorization rule not enforced correctly |
| `connection-error` | SocketException / Broken pipe during HTTP call |
| `xpath-assertion` | XPath assertion failed on SOAP/XML response |
| `field-mismatch` | Field value does not match expected (Smart Assertion) |
| `response-content` | Response missing expected content or empty |
| `config-error` | Configuration assertion failed |
| `debug-pipeline` | Debug pipeline did not produce expected DB events |
| `surveillance-setup` | Surveillance area setup/check failed |
| `notification-log` | Notification log entry not found or missing expected content |
| `locode-assertion` | Locode CRUD operation - expected data not found in DB |
| `data-setup-failure` | Test data setup (Delete Old Data) failed during preparation |
| `assertion-mismatch` | Generic assertion comparison failed |

## Notes

- Filenames are sanitized: max 80 chars, no special chars, spaces replaced by `_`
- Duplicate filenames get a `_1`, `_2` suffix
- PDF text artifacts (`created with ReadyAPI...`, `===PAGEBREAK===`, `Project Results for the-project Platform`) must be stripped from all output
- The curl command should include Content-Type and SOAPAction headers when present
- Always clean existing service folders before regenerating to avoid stale files
