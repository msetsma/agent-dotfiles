# Tooling

A concise inventory of the tools and MCP servers I use with my agents, and how to install each.

## MCP Servers

### Azure DevOps

Brings Azure DevOps context (projects, repos, builds, work items, wikis) to agents.

- Remote (recommended) — add to `.vscode/mcp.json`:
  ```json
  {
    "servers": {
      "ado-remote-mcp": { "url": "https://mcp.dev.azure.com/{organization}", "type": "http" }
    }
  }
  ```
- Local (stdio):
  ```sh
  npx -y @azure-devops/mcp {organization}
  ```
- Source: https://github.com/microsoft/azure-devops-mcp

### Azure (Azure Cloud)

Official Microsoft Azure MCP server for interacting with Azure resources.

- Install / run:
  ```sh
  npx -y @azure/mcp@latest server start
  ```
- Requires Node.js 20+.
- Source: https://github.com/microsoft/mcp

### Databricks

Access Databricks workspace context from agents.

- Docs MCP (hosted, for documentation queries):
  ```sh
  npx add-mcp https://developers.databricks.com/api/mcp --name databricks-docs -g
  ```
- Workspace MCP (PyPI):
  ```sh
  pip install databricks-mcp-server
  # then set DATABRICKS_HOST and DATABRICKS_TOKEN
  ```
- Docs: https://developers.databricks.com/docs/tools/ai-tools/docs-mcp-server

## CLIs

_(add tools as adopted)_

| Tool | Install | Notes |
| ---- | ------- | ----- |
| caveman | `curl -fsSL .../install.sh \| bash` | Installer-managed, not Dotter-managed. See below. |

### Caveman

Makes agents answer in terse caveman-speak. Shrinks what the agent *says*, not what it knows — code, commands, paths, and error strings stay byte-exact. ~65% fewer output tokens on prose replies, ~8.5% on full agentic coding runs.

- Install (detects every agent on the machine and installs for each):
  ```sh
  curl -fsSL https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.sh | bash
  ```
- Requires Node.js 18+. Safe to re-run; re-run to update. Per-agent installs, flags, and uninstall live in the repo's `INSTALL.md`.
- Gotcha: on Claude Code the installer only checks whether the plugin is *present*, so it reports "already installed" and skips even when the plugin is **disabled** and contributing nothing. If `/skills` shows no caveman skills, re-running the installer will not help. Check and fix directly:
  ```sh
  claude plugin list                    # look for Status: ✘ disabled
  claude plugin enable caveman@caveman  # writes enabledPlugins in ~/.claude/settings.json
  ```
  Enablement lives in `~/.claude/settings.json` under `enabledPlugins`, separately from `~/.claude/plugins/installed_plugins.json`. The two can drift.
- Usage: `/caveman [lite|full|ultra|wenyan]` to set the level, "normal mode" to stop. Also `/caveman-commit`, `/caveman-review`, `/caveman-stats`, and `/caveman-compress <file>` (rewrites a memory file like `CLAUDE.md` into caveman-speak).
- Source: https://github.com/JuliusBrussee/caveman

Deliberately **not** vendored under `skills/vendor`. The installer already places it in both agent skill trees — a Claude Code plugin (`caveman@caveman`, plus hooks in `~/.claude/settings.json`) and skill copies in `~/.agents/skills/caveman*`. Adding a copy here would make Dotter collide with those installer-owned directories and load caveman twice under Claude.
