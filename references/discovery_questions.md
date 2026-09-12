# ❓ Project Initiator — Discovery Question Bank

This document outlines the phased question sequences used during the pre-flight discovery protocol. Use native interactive tools (such as Antigravity's `ask_question`) or structured numbered CLI prompts on other platforms.

---

## 💡 Phase 1: Idea Discovery & PRD Formulation

### 1.1 Project Vision & Problem Space
1. **Core Concept:** In 1–2 sentences, what is this application or tool, and what does it do?
2. **The Problem:** What friction, inefficiency, or missing capability does this solve? Why isn't there an existing tool that already does this well?
3. **Target Persona:** Who is the primary user? (e.g. Solo developer, enterprise engineering team, casual consumer, data scientist).
4. **Primary User Journey:** What is the step-by-step path the user takes from opening the app to achieving their goal?

### 1.2 MVP Scope & Boundaries
1. **The Core 3 Features:** What are the three non-negotiable features without which this project is useless?
2. **Explicit Non-Goals:** What are things we are strictly NOT building in v1.0 to avoid scope creep?
3. **Success Metric:** How do we measure that this project succeeded? (e.g. <100ms execution, zero setup config, 100% test coverage).

---

## 🏗️ Phase 2: Technical Architecture & System Design

### 2.1 Tech Stack Preferences
1. **Runtime & Language:**
   - Option A: TypeScript / Node / Bun (Full-stack JS/TS ecosystem)
   - Option B: Python 3.11+ / FastAPI / Asyncio (Data, AI, CLI automation)
   - Option C: Go / Rust (High throughput, single binary, minimal memory)
   - Option D: User's custom stack choice
2. **Frontend & Interface:**
   - Option A: CLI / Terminal tool (Rich, Inquirer, Click/Commander)
   - Option B: Modern Web UI (Next.js, React, Tailwind, Vite)
   - Option C: Desktop App (Tauri, Electron)
   - Option D: Headless API / Library / Microservice
3. **Data Persistence & State:**
   - Option A: Embedded SQLite / DuckDB / Local JSON (Zero external infrastructure)
   - Option B: Relational Database (PostgreSQL / MySQL + Prisma/SQLAlchemy)
   - Option C: Key-Value / In-Memory Cache (Redis, KV)
   - Option D: Stateless / File-based storage

### 2.2 Architectural Boundaries & External Services
1. **Third-Party APIs:** Does this project need LLM APIs, payment gateways, OAuth providers, or external scrapers?
2. **Execution Model:** Synchronous REST vs Asynchronous Event-Driven / Worker Queue?

---

## 🤖 Phase 3: Agent Directives & `/vibe-map` Integration

### 3.1 Agent Boundaries & Rules
1. **Strict File Locking:** Confirm that AI models must operate strictly within predefined directories and ask explicit permission before creating new files or folders.
2. **`/vibe-map` Attachment:** Confirm that `/vibe-map` will be initiated to continuously trace components and analyze change blast radiuses.
3. **Testing Bar:** Unit tests required for all business logic before considering a task complete?

---

## 🛡️ Phase 4: Security & Performance Guardrails

### 4.1 Security Constraints
1. **Authentication Mode:** Anonymous / Local only, API Keys, Session Cookies, or OAuth2 / JWT?
2. **Secrets Handling:** Confirm standard `.env` + `.env.example` isolation with zero committed secrets.
3. **Data Sensitivity:** Does the app handle PII, payments, or proprietary user data requiring end-to-end encryption?

### 4.2 Performance Budgets
1. **Response Latency:** Sub-100ms for standard actions?
2. **Memory Footprint:** Strict memory capping or streaming for large files?
3. **Asset Constraints:** Bundle size limits (<150KB gzip for web apps)?
