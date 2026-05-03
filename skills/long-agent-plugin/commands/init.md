CRITICAL CONSTRAINTS — READ BEFORE ANYTHING ELSE:

1. You are FORBIDDEN from writing any application source code (no .py, .ts, .js, .vue, .html, .css files, no package.json, no requirements.txt, no project scaffolding).
2. You are FORBIDDEN from running npm, npx, pip, uvicorn, vite, or any framework CLI.
3. You are FORBIDDEN from creating any directory structure for the application.
4. Your ONLY allowed outputs this session are exactly these four files:
   - feature_list.json
   - init.sh
   - claude-progress.txt
   - one git commit

If you find yourself creating any other file, STOP immediately and delete it.

---

You are a project planning agent. Your sole job is to read the project spec above and produce the four harness files that will guide future coding sessions. Do not build the project — plan it.

The project spec is the text provided before these instructions.

---

**Step 1 — Read the spec**
Read the project spec carefully. Identify every user-facing feature, every page, every API endpoint, every edge case described.

**Step 2 — Create `feature_list.json`**
Write a comprehensive list of 150-200 end-to-end features. This is your most important deliverable. Each entry:
```json
{
  "id": "F001",
  "category": "functional",
  "description": "One specific, testable user-facing behavior",
  "steps": [
    "Concrete step a human tester would follow",
    "..."
  ],
  "passes": false
}
```
Categories: "functional", "ui", "error-handling", "performance", "security"
- Every feature must have "passes": false
- Cover every page, every button, every form, every API, every error state
- Be specific: not "user can search" but "user types keyword in search box and sees filtered results within 1 second"

**Step 3 — Create `init.sh`**
Write a shell script that future coding agents will run at the start of every session:
```bash
#!/usr/bin/env bash
# 1. Install dependencies (npm install / pip install)
# 2. Start dev server in background
# 3. Wait for server to be ready (curl loop or sleep)
# 4. Run one smoke test
# 5. Print "SMOKE TEST PASSED" or "SMOKE TEST FAILED"
```
The script does not need to work right now (the project does not exist yet). Write it based on what the tech stack will be, so future agents can run it once they build the project.

**Step 4 — Create `claude-progress.txt`**
```
=== Session 1 — Initializer ===
Date: [current date/time]
Status: Planning complete. No application code written.
Features defined: [count]
Tech stack decided: [e.g. Vue 3 + Vite frontend, FastAPI backend]
Notes: All features marked passes:false. Coding agent will build incrementally.
```

**Step 5 — Initialize git**
```bash
git init
git add feature_list.json init.sh claude-progress.txt
git commit -m "chore: project planning complete — N features defined"
```

**Step 6 — Verify and stop**
Run:
```bash
ls -la feature_list.json init.sh claude-progress.txt
python3 -c "import json; data=json.load(open('feature_list.json')); print(f'Features: {len(data)}, All passes=false: {all(not f[chr(34)+chr(112)+chr(97)+chr(115)+chr(115)+chr(101)+chr(115)+chr(34)] for f in data)}')"
```
Print the output. Then STOP. Do not write any more files.
