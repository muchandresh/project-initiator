# 🛡️ SECURITY_AND_PERFORMANCE.md — Mandatory Guardrails & Standards

> **Project Name:** {{PROJECT_NAME}}  
> **Classification:** Production / Critical  
> **Status:** Enforced  
> **Last Audited:** {{DATE}}  

---

## 🔒 PART 1: SECURITY SPECIFICATIONS & MANDATORY RULES

Every component and line of code added to this project must conform to these security standards. Violations must be blocked immediately.

### 1.1 Secrets & Credential Management
- **Zero Secrets in Code:** Hardcoded API keys, passwords, bearer tokens, or database credentials in source files are strictly forbidden.
- **Environment Isolation:** All environment configurations must be loaded via `.env` files (ignored in `.gitignore`) and accessed via typed config managers.
- **Template Provided:** Provide `.env.example` with dummy keys for development onboarding.

### 1.2 Input Validation & Injection Prevention
- **Strict Parameter Validation:** Every endpoint, CLI flag, or user input MUST pass through strict schema validation (e.g. Zod, Pydantic, Joi) before hitting core logic.
- **SQL / NoSQL Injection:** Parameterized queries and ORM abstractions ONLY. Raw string concatenation in queries is strictly prohibited.
- **Command Injection Prevention:** Never pass unescaped user inputs directly to shell execution commands (`subprocess`, `child_process.exec`). Use safe argument arrays.
- **XSS & Content Sanitization:** Sanitize all rendered HTML/markdown inputs. Strip untrusted scripts, iframes, and malicious attributes.

### 1.3 Authentication & Authorization
- **Session / Token Security:** Use secure, HTTP-only, SameSite cookies or short-lived JWTs with cryptographically secure rotation.
- **Principle of Least Privilege:** Scope permissions strictly to the user or worker role required for that exact operation.
- **Rate Limiting & Abuse Prevention:** Enforce rate-limiting on sensitive operations (auth, search, external API triggers, expensive computations).

### 1.4 Safe Error Reporting
- Never expose stack traces, database schema details, or raw server paths to end users.
- Mask internal exceptions behind generic error messages with an internal correlation ID logged to safe log drains.

---

## ⚡ PART 2: PERFORMANCE SPECIFICATIONS & BUDGETS

Code written must meet or exceed these explicit performance thresholds.

### 2.1 Latency & Response Budgets
| Operation Type | Target P95 Latency | Maximum Tolerable Latency |
| :--- | :--- | :--- |
| **API Endpoints (Read)** | < 100ms | 250ms |
| **API Endpoints (Write/Mutate)** | < 200ms | 500ms |
| **CLI Command Response / Startup** | < 150ms | 400ms |
| **Database Queries** | < 20ms | 50ms |
| **Frontend Initial Content Paint (FCP)** | < 1.0s | 1.8s |

### 2.2 Database & Persistence Optimization
- **Mandatory Indexing:** Every column referenced in `WHERE`, `ORDER BY`, or `JOIN` clauses must be indexed.
- **N+1 Query Elimination:** Eager load related records or utilize batch resolvers (DataLoader).
- **Connection Pooling:** Always configure sane connection pool minimums and maximums; never open ad-hoc unpooled database connections.

### 2.3 Memory & Resource Management
- **Streaming Large Data:** Stream large files, exports, or batch data using buffers/generators rather than loading complete payloads into memory.
- **Garbage Collection & Leaks:** Ensure event listeners, file descriptors, and intervals are cleaned up and unsubscribed properly.
- **Worker Concurrency:** Limit simultaneous worker tasks with backpressure to prevent CPU starvation.

### 2.4 Bundle & Asset Budgets (If Frontend/Web)
- **Max Initial JS Bundle:** < 150KB gzip compressed.
- **Code Splitting & Lazy Loading:** Non-critical views and heavy libraries (charts, rich editors) must be loaded dynamically on demand.

---

## ✅ PART 3: PRE-COMMIT & PRE-MERGE AUDIT CHECKLIST

Before marking any milestone or pull request complete:
- [ ] No plaintext secrets or keys committed (`git diff` inspection).
- [ ] All inputs validated with typed schema validators.
- [ ] Rate limits and authentication middleware verified.
- [ ] Tests covering edge cases, invalid payloads, and security boundaries written and passing.
- [ ] Performance benchmarks validated against latency budgets.
- [ ] `/vibe-map` run to verify clean architecture and minimal blast radius.
