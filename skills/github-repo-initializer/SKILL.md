---
name: github-repo-initializer
description: Initialize a new GitHub open-source repository with all essential community health files (README, CONTRIBUTING, CODE_OF_CONDUCT, LICENSE, SECURITY, SUPPORT, issue/PR templates). Use this skill whenever the user mentions creating a new repo, setting up an open-source project, initializing a GitHub repository, or adding standard community files. Also use it when the user asks about "community profile", "health files", or wants to follow GitHub's best practices for open source.
---

# GitHub Repository Initializer (API-First Version)

This skill automates the creation of a standard, high-quality GitHub open-source repository by fetching the **official raw Markdown guidelines** directly from GitHub's documentation API.

## Core Principle: Fetch First, Generate Second

**Do not** rely on memorized templates or outdated examples. The official GitHub documentation evolves. Your job is to:

1. **Fetch** the latest official guidelines via the GitHub Docs API.
2. **Parse** the fetched Markdown to extract the required structure and recommendations.
3. **Generate** the files based strictly on the fetched specifications.

---

## The GitHub Docs API Rule

GitHub provides a hidden API that returns the pure Markdown body of any documentation page.

**Conversion Rule:**
- Normal URL: `https://docs.github.com/en/<path>`
- API URL: `https://docs.github.com/api/article/body?pathname=/en/<path>`

You **MUST** use the API URLs to retrieve content. Do not scrape the HTML pages.

---

## Mandatory API Endpoints to Fetch

When initializing a repository, you **must** perform a `GET` request to the following 5 API endpoints first. Their raw Markdown contains all the rules you need.

1. **Community Health Setup (Overall Index)**
   - API: `https://docs.github.com/api/article/body?pathname=/en/communities/setting-up-your-project-for-healthy-contributions`
   - Use for: Understanding the overall structure of `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, and `SUPPORT.md`.

2. **Default Community Health Files (`.github` repository)**
   - API: `https://docs.github.com/api/article/body?pathname=/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file`
   - Use for: Understanding how to structure shared community files across multiple repositories.

3. **Community Profile Checklist**
   - API: `https://docs.github.com/api/article/body?pathname=/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories`
   - Use for: Getting the definitive list of required files (`README`, `LICENSE`, `CODE_OF_CONDUCT`, `CONTRIBUTING`, etc.).

4. **Licensing Guide**
   - API: `https://docs.github.com/api/article/body?pathname=/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository`
   - Use for: Understanding how to choose and add a `LICENSE` file (including the full text of MIT, Apache-2.0, GPL-3.0).

5. **Issue and Pull Request Templates**
   - API: `https://docs.github.com/api/article/body?pathname=/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates`
   - Use for: Learning the YAML frontmatter and Markdown structure for `ISSUE_TEMPLATE` and `PULL_REQUEST_TEMPLATE.md`.

---

## Step-by-Step Workflow

### Step 1: Clarify the Project Context
Before fetching, ask the user for:
- Project name and brief description.
- Preferred license (default to **MIT** if they are unsure).
- Any specific contribution rules or security contact email.
- Programming language/platform (for the README prerequisites section).

### Step 2: Fetch the Official Data
Execute the 5 GET requests listed above. Store the returned Markdown bodies in memory (or reference them during generation). Read them thoroughly to extract:
- The recommended headings for `CONTRIBUTING.md` (e.g., "How to report bugs", "Submitting changes", "Coding standards").
- The standard text for `CODE_OF_CONDUCT.md` (the Contributor Covenant is usually recommended).
- The instructions for `SECURITY.md` (emphasizing *private* reporting).
- The structure of issue templates (bug reports, feature requests).

### Step 3: Generate the Files
Based on the fetched rules AND the user's answers, produce the following files for the user:

- **`README.md`**: Include project name, description, installation, quick start, and links to other files (`CONTRIBUTING.md`, `LICENSE`, etc.).
- **`CONTRIBUTING.md`**: Follow the structure extracted from the API response. Be welcoming and practical.
- **`CODE_OF_CONDUCT.md`**: Adopt the Contributor Covenant (or another version if explicitly requested) as per the fetched guidelines.
- **`LICENSE`**: Copy the full text of the chosen license from the fetched licensing guide.
- **`SECURITY.md`**: Outline the private reporting process as per the official recommendations.
- **`SUPPORT.md`**: (Optional) Explain where to get help.
- **`.github/ISSUE_TEMPLATE/bug_report.md`**: Use the standard template structure.
- **`.github/ISSUE_TEMPLATE/feature_request.md`**: Use the standard template structure.
- **`.github/PULL_REQUEST_TEMPLATE.md`**: Include a checklist for contributors.

### Step 4: Advise on Default Health Files
If the user owns multiple repositories, suggest creating a public `.github` repository and placing shared files (like `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`) there. Explain that this centralizes maintenance.

### Step 5: Present the Results
Output the generated file contents clearly. Use code blocks with the correct file paths (e.g., `path/to/repo/README.md`). Remind the user to review the files before committing.

---

## Important Constraints

- **No Hardcoded Templates**: The only text you should hardcode are the API URLs. All content structures must be derived from the API responses.
- **Lean Output**: Keep explanations brief. Focus on generating high-quality, compliant files.
- **Flexibility**: If the user provides specific custom text (e.g., "Our company uses a custom CLA"), override the fetched rules with the user's explicit instructions.

---

## Example Interaction

**User**: "Set up a repo for my JavaScript library 'dom-helper'."

**You**:
1. Ask: "Which license? (recommend MIT)" and "Any special contribution rules?"
2. Fetch all 5 API endpoints.
3. Parse the Markdown to extract the recommended structures.
4. Generate all files according to the fetched specs and the user's answers.
5. Present the files.

---