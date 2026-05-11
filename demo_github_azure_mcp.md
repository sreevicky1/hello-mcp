# Session 8 — GitHub & Azure MCP Demo Script

This session shows **consumer side** of MCP: using production MCP servers from Claude Desktop. The custom FastMCP servers in this folder (math/tools, prompts, resources) cover the **builder side**; this script complements them.

## Setup (one-time)

### Step 1 — Install Node.js (LTS)

Both servers run on Node. On a fresh Windows machine, install via winget:

```powershell
winget install OpenJS.NodeJS.LTS --accept-source-agreements --accept-package-agreements --silent
```

This installs Node + npm + `npx.cmd` to `C:\Program Files\nodejs\`. Verify:

```powershell
& "C:\Program Files\nodejs\node.exe" --version
& "C:\Program Files\nodejs\npx.cmd" --version
```

Why winget and not the official installer? It is non-interactive and the install path is predictable, which matters because the MCP config below hard-codes that path.

### Step 2 — Create a GitHub Personal Access Token (PAT)

GitHub's OAuth server does **not** support Dynamic Client Registration (RFC 7591), which is the only auth flow the generic `mcp-remote` client implements. The hosted GitHub MCP server therefore needs a PAT instead of OAuth.

1. Go to https://github.com/settings/tokens (Classic) → **Generate new token (classic)**.
2. Note: `claude-mcp-demo`. Expiration: pick a short window for class (7–30 days).
3. Scopes — minimum set for the demo flows:
   - `repo` (full control of private repos) — required for PR create / review / branch ops.
   - `read:org` — required for org-scoped queries.
   - `read:user` — required for `get_me`.
   - `gist` — optional, useful if demoing gist operations.
4. **Generate token**, copy it (it's only shown once).
5. Open `claude_desktop_config.json` and replace `PASTE_YOUR_GITHUB_PAT_HERE` in the `github.env.AUTH_HEADER` value, **keeping the `Bearer ` prefix**:
   ```
   "AUTH_HEADER": "Bearer ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
   ```

> Why the funny `"Authorization:${AUTH_HEADER}"` shape? `mcp-remote` splits header strings at the first `:` to derive name/value. Putting `Bearer ` inside the env var (instead of writing `"Authorization: Bearer ${PAT}"`) sidesteps a leading-space bug in the header parser that bites on Windows.

### Step 3 — Confirm the config

`claude_desktop_config.json` now has two new entries beside the three local FastMCP servers:

- `github` → `mcp-remote https://api.githubcopilot.com/mcp/` with `Authorization: Bearer <PAT>` (GitHub's hosted server, PAT auth)
- `azure` → `@azure/mcp@latest server start` (uses your local `az login`)

Both use the absolute path `C:\Program Files\nodejs\npx.cmd`. **Why?** Claude Desktop on Windows spawns child processes with a stripped PATH, so a bare `"command": "npx"` fails with `spawn npx ENOENT` even after Node is installed. Always point at `npx.cmd` directly.

### Step 4 — Restart Claude Desktop

1. Quit Claude Desktop fully (system tray → Quit, not just close window).
2. Relaunch it.
3. For `azure`, confirm `az account show` returns your subscription. If not, run `az login` first.
4. Open the MCP / tools panel in Claude Desktop; `github` and `azure` should appear with no error badge.
5. Quick sanity check — ask: *"What's my GitHub username?"* It should call `get_me` on the `github` server and answer without prompting for anything else.

> ⚠️ **Don't commit the PAT.** `claude_desktop_config.json` in `session8_mcp/` is meant as a teaching artifact. Before sharing the repo, replace the live token with the placeholder again (or `.gitignore` the file).

Quick sanity prompts:

- *"What's my GitHub username?"* → `github` server resolves via `get_me`.
- *"List my Azure subscriptions."* → `azure` server calls `subscriptions`.

---

## Part A — GitHub MCP

Run these in order against your `module3_agents` repo:

1. **Discover** — *"List my public repos and show the most recently updated one."*
2. **Read code** — *"In my `module3_agents` repo, find every file that imports `fastmcp` and summarize what each server does."*
3. **Branch + commit** — *"Create a branch `demo/add-mcp-readme` off main in that repo, and add a file `session8_mcp/README.md` containing a one-paragraph intro to MCP."*
4. **Open PR** — *"Open a pull request from `demo/add-mcp-readme` into main titled 'Add session 8 MCP intro', with a body describing what changed."*
5. **Review flow** — *"List the open PRs on that repo. For the one I just opened, leave a review comment on the README file asking to add a 'Prerequisites' section."*
6. **Triage** — *"Show me all open issues labeled `bug` across my repos sorted by oldest first."*

Talking points:
- The same tool surface (`create_pull_request`, `create_pull_request_review`, etc.) is what Copilot uses — you're using GitHub's first-party MCP server, not a third-party wrapper.
- PAT scopes (`repo`, `read:org`, `read:user`) are what gate which tools succeed — a "tool not allowed" error usually means a missing scope, not a server bug.

---

## Part B — Azure MCP

Run these against the `coding_ninja` resource group from your earlier deploy:

1. **Inventory** — *"List the resource groups in my Azure subscription and show what's inside `coding_ninja`."*
2. **App status** — *"Show the current revision, replica count, and ingress URL of the `mcp-server` Container App in `coding_ninja`."*
3. **Logs** — *"Tail the last 50 lines from the `mcp-logs` Log Analytics workspace for the `mcp-server` Container App, filtered to errors."*
4. **Registry** — *"List images in the `acrcodingninja` container registry and show the tags for `mcp-server`."*
5. **Cost / scale insight** — *"What is the CPU/memory configured on `mcp-server`, and based on recent logs is it idle most of the time?"*
6. **Chained tools (read-only)** — *"What would the command be to roll the Container App to the latest image tag in ACR?"* — show the call shape without actually deploying.

Talking points:
- Auth reuses the same `DefaultAzureCredential` chain as the Azure SDK — no separate token to manage.
- Azure MCP wraps many Resource Provider APIs, so the same server covers Container Apps, ACR, Log Analytics, Storage, Cosmos, Key Vault, etc.

---

## Part C — Cross-server moment (the punchline)

One prompt that uses **both** servers in a single turn — this is the demo's "wow":

> *"Pull the latest commit SHA of `main` in my `module3_agents` repo (GitHub MCP), then check whether the `mcp-server` Container App in `coding_ninja` is running a Docker tag matching that SHA (Azure MCP). Tell me if prod is behind."*

Why this matters:
- One assistant, two vendors, one workflow.
- Neither GitHub nor Microsoft wrote anything custom to make this work — they just both spoke MCP.
- That is the entire pitch: MCP is the **USB-C of agent tooling**.

---

## If something doesn't connect

- Use the MCP Inspector (already in `deploy mcp in azure.txt`):
  ```
  npx @modelcontextprotocol/inspector
  ```
  Point it at the same command/args from `claude_desktop_config.json` to isolate whether the issue is the server or Claude Desktop.
- Check Claude Desktop logs: `%APPDATA%\Claude\logs\mcp-server-<name>.log`.
- GitHub returning 401? Token expired or scope missing. Regenerate at https://github.com/settings/tokens and update `AUTH_HEADER` in the config.
- GitHub returning the `Incompatible auth server: does not support dynamic client registration` error? You forgot the `--header` arg — `mcp-remote` is falling back to OAuth (which GitHub's auth server doesn't support).
- Azure auth failing? Re-run `az login` and restart Claude Desktop.
