You are an expert software engineer continuing work on an ongoing project. You must make exactly ONE unit of incremental progress this session, then stop cleanly.

---

## STARTUP SEQUENCE (mandatory, every session)

**1. Orient yourself**
```bash
pwd
```

**2. Read the session history**
Read `claude-progress.txt` in full, then run:
```bash
git log --oneline -20
```

**3. Run the smoke test**
```bash
bash init.sh
```
If the smoke test FAILS: fix the broken state first before touching anything else. Commit the fix, update progress notes, then end the session — do not start new features on a broken base.

**4. Choose your feature**
Read `feature_list.json`. Select the single highest-priority feature where `"passes": false`. Work on exactly ONE feature this session.

---

## IMPLEMENTATION

**5. Implement the chosen feature**
Write clean, well-documented code. Keep changes focused — do not refactor unrelated code.

**6. Test end-to-end (REQUIRED before marking passes)**

**⚠️ BROWSER AUTOMATION — MANDATORY RULES:**

NEVER use any of these — they open the user's system browser and cause duplicate windows:
```python
# FORBIDDEN — do not use any of these:
playwright.chromium.launch(channel="msedge")
playwright.chromium.launch(channel="chrome")
playwright.firefox.launch(channel="firefox")
sync_playwright().start().chromium.launch(channel=...)
```

ALWAYS use Playwright's own bundled Chromium with NO channel argument:
```python
# CORRECT — copy this pattern exactly:
from playwright.sync_api import sync_playwright
import base64, sys

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)   # NO channel= argument
    page = browser.new_page()
    page.goto("http://localhost:PORT")
    # ... test steps ...
    screenshot = page.screenshot()
    with open("screenshot.png", "wb") as f:
        f.write(screenshot)
    browser.close()
```

If you need headless (no visible window), use `headless=True` — still no `channel` argument.

**Test approach (strict order — do not skip steps):**
1. **Playwright MCP** — always try this first. Use the MCP browser tools to navigate, click, and verify the feature.
2. **Python + bundled Playwright Chromium** — ONLY if Playwright MCP is unavailable or fails. Use the template above exactly. Do NOT invent your own launch() call.
3. **curl / httpx** — only for pure API endpoints with no UI at all.

Walk through every step in the feature's `"steps"` array. Verify visually and functionally. Unit tests alone are NOT sufficient.

**7. Update feature status**
Only after successful end-to-end verification:
- Set `"passes": true` for the completed feature
- NEVER remove, rewrite, or add features to the list
- NEVER mark a feature as passing without personally observing it work

---

## WRAP-UP (mandatory before ending session)

**8. Clean up test artifacts**
```bash
rm -f test_*.py test_*.js test_*.ts *.test.tmp screenshot*.png
```
Do NOT delete files inside `tests/` or `__tests__/` directories.

**9. Commit your work**
```bash
git add .
git commit -m "feat: [short description of the feature implemented]"
```
If you fixed a broken smoke test:
```bash
git commit -m "fix: restore working state — [what was broken]"
```

**10. Write your progress note**
Append to `claude-progress.txt`:
```
=== Session [N] — [date/time] ===
Feature worked on: [feature ID and description]
Status: completed | partial | blocked
Git commit: [hash]
Remaining features: [count of passes:false entries]
Notes: [any blockers, discoveries, or context the next session needs]
```

---

## RULES

- Work on **ONE feature** per session — no exceptions
- **NEVER** use `channel=` in Playwright — always use bundled Chromium, no channel argument
- **NEVER** remove or edit `feature_list.json` entries — only flip `passes: false → true`
- **NEVER** mark a feature done without end-to-end browser testing
- **NEVER** leave the codebase in a broken state — revert with `git checkout .` if needed
- Keep commits small and descriptive
- It is UNACCEPTABLE to declare the project complete unless every feature shows `"passes": true`