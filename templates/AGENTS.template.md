# 🤖 AGENTS.md — Operational Rules & Guidelines for AI Agents

> **Project Name:** {{PROJECT_NAME}}  
> **Enforcement Level:** STRICT & MANDATORY  
> **Applies to:** Antigravity, Claude Code, Cursor, Windsurf, Copilot, Cline, and any autonomous AI coding subagents.

---

## 🛑 MANDATORY PRIME DIRECTIVES (NON-NEGOTIABLE)

All AI agents operating within this repository MUST read and strictly adhere to these directives. Failure to comply compromises project architecture and safety.

### 🔒 1. THE FILE STRUCTURE LOCK & PERMISSION MANDATE
1. **Pre-Existing Structure Only:** You are strictly bound to the directories and files defined in `ARCHITECTURE.md` and registered in `.structure_lock.json`.
2. **Zero Unauthorized Creations:** You MUST NEVER unilaterally create a new file or directory without asking the user.
3. **Explicit Permission Required:** If you identify a genuine architectural need for a new file or directory:
   - **PAUSE** execution immediately.
   - **PROPOSE** the exact file path and explain why it is essential.
   - **WAIT** for the user's explicit consent before creating it.
   - Once approved, register the new path in `.structure_lock.json`.

```text
[AGENT PERMISSION PROTOCOL]
Need new file/dir? ➔ STOP ➔ Ask User: "I recommend creating <path> because <reason>. Do you approve?" ➔ If Yes: create & update lock ➔ If No: use existing files
```

---

### 🗺️ 2. MANDATORY INTEGRATION & EXECUTION OF `/vibe-map`
This project mandates continuous architectural visibility and impact blast-radius analysis via the `/vibe-map` skill:

1. **Skill Attachment:** Ensure the `/vibe-map` skill is attached to the project workspace (`.agents/skills/vibe-map/` or globally available).
2. **Pre-Change Impact Check:** Before modifying or refactoring any core module or shared dependency, run:
   ```bash
   /vibe-map impact "<target_file>"
   ```
   to assess what other components will be affected.
3. **Post-Milestone Sync:** After completing any major feature or architectural change, trigger a map update:
   ```bash
   /vibe-map update
   ```
   to keep `vibe-map-out/codebase_map.json` and `vibe-map-out/VIBE_MAP.md` synchronized.

---

### 📋 3. SPEC-FIRST WORKFLOW (READ BEFORE WRITING)
Before writing or altering any production code:
1. Consult **[PRD.md](file:///PRD.md)** to verify business intent and scope.
2. Consult **[ARCHITECTURE.md](file:///ARCHITECTURE.md)** to verify data models, boundaries, and tech stack standards.
3. Consult **[SECURITY_AND_PERFORMANCE.md](file:///SECURITY_AND_PERFORMANCE.md)** to guarantee zero security regressions and stay within performance budgets.

---

## 🛠️ 4. Code Quality & Implementation Standards

- **Complete Implementations Only:** Never write stub implementations, fake mock data, or omit logic with comments like `// TODO: implement later`. Complete all logic end-to-end.
- **Strict Typing:** All code must be strongly typed (e.g. TypeScript with zero `any`, Python with strict PEP 484 type hints).
- **Error Handling:** Every async operation, external API request, or file I/O must include comprehensive error handling with user-friendly logging.
- **Test-Driven Rigor:** Every new feature must be accompanied by unit or integration tests under `tests/`. Do not consider a task complete until tests pass.

---

## 👥 5. Subagent Delegation Guidelines

When dispatching tasks to subagents:
- **Research Agent:** Use for non-destructive reading, dependency audits, documentation checks, and inspecting reference APIs.
- **Core Builder Agent:** Confined exclusively to authorized module directories specified in the task prompt.
- **Reviewer Agent:** Validates completed code against `SECURITY_AND_PERFORMANCE.md` before final integration.
