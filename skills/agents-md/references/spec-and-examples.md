# AGENTS.md Specification & Examples

## Table of Contents

1. [Official Specification Summary](#official-specification-summary)
2. [Six Core Content Areas](#six-core-content-areas)
3. [Complete Example: TypeScript Monorepo](#example-typescript-monorepo)
4. [Complete Example: Python Project](#example-python-project)
5. [Complete Example: Java Spring Boot](#example-java-spring-boot)
6. [Complete Example: Rust Project](#example-rust-project)
7. [Complete Example: Go Project](#example-go-project)
7. [Complete Example: Android Multi-Project Workspace](#example-android-multi-project-workspace)
8. [Minimal Template](#minimal-template)

---

## Official Specification Summary

- **Format**: Standard Markdown, no required fields, no strict schema
- **Location**: Project root directory, filename must be `AGENTS.md` (uppercase)
- **Nesting**: Supported in monorepos — agent reads the nearest AGENTS.md
- **Conflict resolution**: Closer (more specific) AGENTS.md takes precedence
- **Tool support**: GitHub Copilot, OpenAI Codex, Google Jules, Cursor, Claude Code (via
  `ln -s AGENTS.md CLAUDE.md`), Aider, and more
- **Maintained by**: Agentic AI Foundation under Linux Foundation
- **Official repo**: https://github.com/agentsmd/agents.md
- **Official site**: https://agentsmd.io/

### Key Differences from README.md

| Dimension | README.md | AGENTS.md |
|-----------|-----------|-----------|
| Audience | Human developers | AI coding agents |
| Content | Project intro, features, usage | Build/test commands, code rules, boundaries |
| Style | Can include backstory, design philosophy | Precise, executable, unambiguous |
| Purpose | Help humans understand "what this is" | Help AI know "how to work on this" |

---

## Six Core Content Areas

Based on GitHub's analysis of 2500+ repositories, the best AGENTS.md files cover these areas:

### 1. Commands
Build, test, run commands. Must be exact and wrapped in backticks.

### 2. Testing
Test strategy, coverage requirements, how to run targeted tests.

### 3. Project Structure
Directory layout with one-line descriptions per directory.

### 4. Code Style
Naming conventions with concrete good/bad examples.

### 5. Git Workflow
Branch naming, commit message format, PR requirements.

### 6. Boundaries
Three-tier: ✅ Always / ⚠️ Ask first / 🚫 Never

---

## Example: TypeScript Monorepo

```markdown
# Acme Platform — AGENTS.md

Full-stack TypeScript monorepo (pnpm + Turborepo). Backend: NestJS, Frontend: Next.js, Shared: TypeScript packages.

## Dev Environment Tips

- Install dependencies: `pnpm install`
- Start all dev servers: `pnpm dev`
- Target a specific package: `pnpm --filter @acme/api dev`
- Check package names in each package's `package.json` (not the root one)
- Node.js >= 20 required. Use `nvm use` to switch.

## Build & Test

| Command | Purpose |
|---------|---------|
| `pnpm build` | Build all packages |
| `pnpm build --filter @acme/ui` | Build a specific package |
| `pnpm test` | Run all tests |
| `pnpm test --filter @acme/api` | Run tests for one package |
| `pnpm vitest run -t "test name"` | Run a single test by name |
| `pnpm lint` | Lint all packages |
| `pnpm lint --filter @acme/ui` | Lint a specific package |
| `pnpm typecheck` | TypeScript type checking |

All tests must pass before committing. After moving files or changing imports, run `pnpm lint` to verify.

## Project Structure

- `apps/api/` — NestJS backend (PostgreSQL + Prisma ORM)
- `apps/web/` — Next.js frontend (React + Tailwind CSS)
- `packages/ui/` — Shared React component library
- `packages/shared/` — Shared types, utils, constants
- `packages/config/` — Shared ESLint, TypeScript configs
- `prisma/` — Database schema and migrations

## Code Style & Conventions

- TypeScript strict mode everywhere
- Single quotes, no semicolons (enforced by Prettier)
- Prefer functional patterns; avoid class components in React
- Naming:
  - Functions: camelCase — `getUserById`, `calculateTotal`
  - Components: PascalCase — `UserCard`, `NavigationMenu`
  - Files: kebab-case — `user-service.ts`, `auth-guard.ts`
  - Constants: UPPER_SNAKE — `MAX_RETRIES`, `API_BASE_URL`
- Error handling: always use `Result<T, E>` pattern from `packages/shared`, never throw raw errors
- Imports: use `@acme/*` workspace aliases, never relative paths across packages

## Boundaries

- ✅ Always: Create/modify files in `apps/` and `packages/`
- ✅ Always: Add tests for any new code
- ⚠️ Ask first: Modify `prisma/schema.prisma` (requires migration)
- ⚠️ Ask first: Change shared package APIs (affects all consumers)
- 🚫 Never: Modify `pnpm-lock.yaml` directly (use `pnpm install`)
- 🚫 Never: Commit `.env` files or secrets
- 🚫 Never: Push directly to `main` branch

## PR / Commit Guidelines

- Commit format: Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`)
- PR title: `[package] description` (e.g., `[api] add user pagination`)
- Run `pnpm lint && pnpm test` before every commit

## Monorepo Navigation

| Package | Path | Description |
|---------|------|-------------|
| @acme/api | `apps/api/` | NestJS backend |
| @acme/web | `apps/web/` | Next.js frontend |
| @acme/ui | `packages/ui/` | Shared components |
| @acme/shared | `packages/shared/` | Types & utilities |

Use `pnpm --filter <package-name>` to target any command to a specific package.
```

---

## Example: Python Project

```markdown
# DataPipeline — AGENTS.md

Python 3.12 ETL pipeline using Apache Airflow, with PostgreSQL and Redis.

## Dev Environment Tips

- Create venv: `python -m venv .venv && source .venv/bin/activate`
- Install deps: `pip install -e ".[dev]"`
- Copy `.env.example` to `.env` and fill in values
- Start local services: `docker compose up -d`

## Build & Test

| Command | Purpose |
|---------|---------|
| `pytest` | Run all tests |
| `pytest tests/test_extract.py` | Run a single test file |
| `pytest -k "test_fetch_api"` | Run tests matching name |
| `ruff check .` | Lint |
| `ruff check --fix .` | Lint with auto-fix |
| `mypy src/` | Type checking |
| `pytest --cov=src` | Test with coverage |

Coverage must be ≥ 80%. All tests must pass before merge.

## Project Structure

- `src/pipeline/` — Main source code
  - `extractors/` — Data source connectors
  - `transformers/` — Data transformation logic
  - `loaders/` — Data destination writers
  - `models/` — Pydantic data models
  - `utils/` — Shared utilities
- `tests/` — Mirrors `src/` structure
- `dags/` — Airflow DAG definitions
- `migrations/` — Database migrations (Alembic)

## Code Style & Conventions

- Follow PEP 8 (enforced by Ruff)
- Type hints required on all function signatures (enforced by mypy strict)
- Use Pydantic v2 models for all data validation
- Error handling: raise custom exceptions from `src/pipeline/exceptions.py`
- Naming:
  - Functions: snake_case — `fetch_user_data`, `transform_record`
  - Classes: PascalCase — `UserExtractor`, `DataTransformer`
  - Constants: UPPER_SNAKE — `MAX_BATCH_SIZE`, `DEFAULT_TIMEOUT`
  - Files: snake_case — `user_extractor.py`, `data_utils.py`

## Boundaries

- ✅ Always: Add/modify code in `src/pipeline/` and `tests/`
- ✅ Always: Add tests for new extractors/transformers/loaders
- ⚠️ Ask first: Modify `dags/` (affects production schedules)
- ⚠️ Ask first: Change Pydantic model schemas (affects API contracts)
- 🚫 Never: Commit `.env` or credentials
- 🚫 Never: Modify `migrations/` without a corresponding model change
- 🚫 Never: Use `print()` for logging — use `structlog` instead

## PR / Commit Guidelines

- Commit format: Conventional Commits
- Run `ruff check . && mypy src/ && pytest` before every commit
```

---

## Example: Java Spring Boot

```markdown
# OrderService — AGENTS.md

Spring Boot 3.2 microservice for order management. Java 21, Gradle, PostgreSQL.

## Dev Environment Tips

- Build: `./gradlew build`
- Run locally: `./gradlew bootRun`
- Run with profile: `./gradlew bootRun --args='--spring.profiles.active=dev'`
- Local config: `~/.orderservice_env` (auto-sourced by startup script)
- JDK 21 required. Check: `java -version`

## Build & Test

| Command | Purpose |
|---------|---------|
| `./gradlew build` | Build project |
| `./gradlew test` | Run all tests |
| `./gradlew test --tests "com.acme.order.*"` | Run specific test class |
| `./gradlew test --tests "*.OrderServiceTest.createOrder"` | Run single test |
| `./gradlew spotlessCheck` | Format check |
| `./gradlew spotlessApply` | Auto-format |
| `./gradlew bootRun` | Start dev server |

## Project Structure

- `src/main/java/com/acme/order/`
  - `controller/` — REST controllers (L5)
  - `service/` — Business logic (L4)
  - `repository/` — Data access (L1)
  - `entity/` — JPA entities (L0)
  - `config/` — Spring configuration (L3)
  - `common/` — Shared utilities (L0)
- `src/test/java/` — Tests mirror main structure
- `src/main/resources/` — Application configs, SQL scripts

## Code Style & Conventions

- Exception handling: always use `BusinessException` from `common/`, never raw `RuntimeException`
- Response wrapping: framework auto-wraps responses — never manually construct `ResponseEntity` bodies
- Layered architecture: strict dependency direction L0→L1→L4→L5 (see `docs/architecture.md`)
- Naming:
  - Methods: camelCase — `findOrderById`, `calculateTotal`
  - Classes: PascalCase — `OrderService`, `PaymentController`
  - Constants: UPPER_SNAKE — `MAX_ORDER_ITEMS`
- Dependency injection: use constructor injection, never field injection

## Boundaries

- ✅ Always: Add/modify code following layered architecture
- ✅ Always: Add tests for new service methods
- ⚠️ Ask first: Modify `entity/` classes (affects DB schema)
- ⚠️ Ask first: Change `config/` (affects application behavior)
- 🚫 Never: Commit `application-dev.yml` with real credentials
- 🚫 Never: Skip service layer (controller must not access repository directly)
- 🚫 Never: Use `@Autowired` field injection

## Verification

After starting the service, verify with:
```bash
curl -s http://localhost:8080/actuator/health | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])"
```

## PR / Commit Guidelines

- Commit format: Conventional Commits
- Run `./gradlew spotlessApply test` before every commit
```

---

## Example: Rust Project

```markdown
# Codex CLI — AGENTS.md

Rust CLI application for AI-powered coding assistance. Uses Bazel for builds.

## Dev Environment Tips

- Install Rust: `rustup toolchain install stable`
- Install Bazel: see `.bazelversion` for required version
- Install tools: `cargo install cargo-insta` (snapshot testing)
- Format on save: `just fmt` (in `codex-rs/` directory)

## Build & Test

| Command | Purpose |
|---------|---------|
| `just fmt` | Format Rust code (run after every change) |
| `just fix -p <project>` | Fix linter issues for a specific project |
| `cargo test -p codex-tui` | Run tests for one crate |
| `cargo test --all-features` | Run full test suite |
| `cargo insta pending-snapshots` | Check pending snapshot updates |
| `cargo insta accept -p codex-tui` | Accept all new snapshots |

Run `just fmt` automatically after making Rust changes — no approval needed. Run `just fix`
before finalizing changes. Ask before running the full test suite.

## Code Style & Conventions

- Collapse if statements per clippy::collapsible_if
- Inline format! args per clippy::uninlined_format_args
- Use method references over closures per clippy::redundant_closure_for_method_calls
- Do not use unsigned integers even if the number cannot be negative
- Prefer comparing entire objects in tests over field-by-field comparison
- Use `pretty_assertions::assert_eq!` in test modules

## Boundaries

- ✅ Always: Run `just fmt` after code changes
- ✅ Always: Add/update tests for changed code
- ⚠️ Ask first: Run the complete test suite (`cargo test --all-features`)
- 🚫 Never: Modify code related to `CODEX_SANDBOX_NETWORK_DISABLED_ENV_VAR`
- 🚫 Never: Modify code related to `CODEX_SANDBOX_ENV_VAR`
```

---

## Example: Go Project

```markdown
# API Gateway — AGENTS.md

Go 1.22 API gateway service with gRPC and HTTP endpoints.

## Dev Environment Tips

- Install deps: `go mod download`
- Run locally: `go run ./cmd/gateway`
- Generate protobuf: `make proto`
- Docker: `docker compose up -d`

## Build & Test

| Command | Purpose |
|---------|---------|
| `make build` | Build binary |
| `make test` | Run all tests |
| `go test ./pkg/auth/...` | Test a specific package |
| `go test -run TestValidateToken ./pkg/auth/` | Run a single test |
| `make lint` | Run golangci-lint |
| `make proto` | Regenerate protobuf files |

## Project Structure

- `cmd/gateway/` — Application entrypoint
- `internal/` — Private application code
  - `auth/` — Authentication middleware
  - `handler/` — HTTP/gRPC handlers
  - `service/` — Business logic
  - `store/` — Data access layer
- `pkg/` — Public library packages
- `proto/` — Protobuf definitions (run `make proto` after changes)
- `api/` — OpenAPI specs

## Code Style & Conventions

- Follow Effective Go and Go Code Review Comments
- Error handling: always wrap errors with `fmt.Errorf("functionName: %w", err)`
- Naming:
  - Exported: PascalCase — `ValidateToken`, `UserService`
  - Unexported: camelCase — `parseConfig`, `httpClient`
  - Acronyms: uppercase — `HTTPClient`, `userID` (not `userId`)
- Table-driven tests preferred
- Use `context.Context` as first parameter in all service methods

## Boundaries

- ✅ Always: Add tests for new handlers and services
- ✅ Always: Run `make proto` after modifying `.proto` files
- ⚠️ Ask first: Change `proto/` definitions (affects downstream services)
- ⚠️ Ask first: Modify `cmd/gateway/` entrypoint
- 🚫 Never: Commit generated `*.pb.go` files manually
- 🚫 Never: Use `panic()` in production code
```

---

## Example: Android Multi-Project Workspace

This example demonstrates an AGENTS.md for a workspace with independent sub-projects
(no root build), platform-specific tooling, and a Common Pitfalls section — a pattern
well-suited for course workspaces, example collections, and multi-app repositories.

```markdown
# Android Course Projects — AGENTS.md

Android development course workspace containing independent experiment/homework projects. Java + Android SDK 35 + Gradle (Kotlin DSL). Each sub-project is a standalone Android app with its own build system.

## Dev Environment Tips

| Requirement | Details |
|-------------|---------|
| JDK | JDK 11+ (path: `D:\apps\java\jdk-21\bin`) |
| Android SDK | `D:\apps\Android\Sdk` |
| Emulator | MEmu (逍遥模拟器), ADB port `127.0.0.1:21503` |
| Gradle | 8.10.2 (wrapper included per project) |

Connect emulator before building:
```powershell
D:\apps\Android\Sdk\platform-tools\adb.exe connect 127.0.0.1:21503
```

If emulator not running, start it first:
```powershell
D:\apps\Microvirt\MEmu\MEmuConsole.exe
```

## Build & Test

All commands must be run from the **specific project directory** (e.g., `cd D:\Working\Code\Android\Experiment_5`).

| Command | Purpose |
|---------|---------|
| `.\gradlew.bat assembleDebug` | Build debug APK |
| `.\gradlew.bat test` | Run unit tests |
| `.\gradlew.bat connectedAndroidTest` | Run instrumented tests (requires device/emulator) |
| `.\gradlew.bat lint` | Run Android Lint |

Install and launch on MEmu:
```powershell
D:\apps\Android\Sdk\platform-tools\adb.exe -s 127.0.0.1:21503 install -r app\build\outputs\apk\debug\app-debug.apk
D:\apps\Android\Sdk\platform-tools\adb.exe -s 127.0.0.1:21503 shell am start -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -n "com.example.<project>/.MainActivity"
```

## Project Structure

This workspace contains **independent** Android projects — each has its own `build.gradle.kts`, `settings.gradle.kts`, and `gradle/` directory. There is no root-level Gradle build.

| Directory | Description |
|-----------|-------------|
| `HellowWorldApp/` | Hello World starter app |
| `Experiment_2/` | Experiment 2 — basic UI controls |
| `Experiment_3/` | Experiment 3 — DatePicker dialog |
| `experiment_4/` | Experiment 4 — Activity data passing |
| `Experiment_5/` | Experiment 5 — SQLite CRUD |
| `OrderFoodApp/` | Food ordering app (Fragment, Navigation) |
| `_Template/StableActivity/` | Project template with `{{PACKAGE_NAME}}` placeholders |

## Code Style & Conventions

**Language**: Java only (no Kotlin in this workspace).

**Naming**:
- Activities: PascalCase with Activity suffix — `MainActivity.java`
- Helpers: PascalCase with descriptive suffix — `MySQLiteOpenHelper.java`
- Layouts: snake_case with type prefix — `activity_main.xml`, `item_dish.xml`

**Activity pattern**:
```java
// Good: extend AppCompatActivity, use setContentView + findViewById
public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }
}
```

**SQLite pattern**:
```java
// Good: extend SQLiteOpenHelper, use ContentValues + parameterized queries
// Use "?" placeholders: db.delete(TABLE, "name = ?", new String[]{name})
```

**New Activity registration**: Every new Activity **must** be registered in `AndroidManifest.xml`:
```xml
<activity android:name=".NewActivity" android:exported="false" />
```

## Boundaries

- ✅ Always: Create new Activities, layouts, and Java classes following existing patterns; modify `AndroidManifest.xml` to register new Activities
- ⚠️ Ask first: Change `compileSdk`/`targetSdk`/`minSdk` versions; modify `libs.versions.toml` dependency versions
- 🚫 Never: Delete existing experiment projects; modify `_Template/` template files; commit APK files or build artifacts; hardcode sensitive data

## Common Pitfalls

- **Each project is independent** — there is no root Gradle build. Always `cd` into the specific project directory before running `.\gradlew.bat`
- **MEmu screenshot issue** — standard `adb shell screencap` may produce blank images. Use `Alt+F3` (MEmu built-in) or `memuc screenshot` instead
- **ADB connection** — always connect to `127.0.0.1:21503` before deploying. If connection refused, start MEmu first and wait ~20 seconds
- **New Activity not showing** — forgetting to register in `AndroidManifest.xml` causes runtime crash
- **Template project** — `_Template/StableActivity/` uses `{{PACKAGE_NAME}}` placeholders; do not build it directly
- **Java 11 source compatibility** — all projects use `JavaVersion.VERSION_11`; do not use Java 17+ features
```

---

## Minimal Template

For when you just need to get started quickly:

```markdown
# [Project Name] — AGENTS.md

[Brief description and tech stack]

## Dev Environment Tips

- Install deps: `[command]`
- Dev server: `[command]`

## Build & Test

| Command | Purpose |
|---------|---------|
| `[build cmd]` | Build |
| `[test cmd]` | Run tests |
| `[lint cmd]` | Lint |

## Project Structure

- `src/` — Source code
- `tests/` — Test files

## Code Style & Conventions

- [Language] conventions
- Naming: [convention]

## Boundaries

- ✅ Always: [what agent can do]
- ⚠️ Ask first: [what needs confirmation]
- 🚫 Never: [what agent must never do]
```
