# Mes Implementation Notes

This file archives lower-level details that were removed from `Mes-Planning.html` so the planning doc can stay mid-to-high level. Treat these notes as starting points only. Re-check official docs, package versions, preview status, and auth behavior before implementing anything.

## Hermes Profile Distribution

Native Hermes profile distribution assets may include:

- `distribution.yaml`
- `SOUL.md`
- `config.yaml`
- `mcp.json`
- `skills/`
- optional `cron/`
- `README.md`
- `.env.EXAMPLE`

Do not commit runtime/user-owned state such as `.env`, `auth.json`, `memories/`, `sessions/`, `state.db*`, `logs/`, `workspace/`, caches, local overrides, MCP OAuth tokens, or Obsidian vault contents.

## MCP Candidates

Azure DevOps:

- Preferred first path when supported: Azure DevOps remote MCP at `https://mcp.dev.azure.com/{organization}`.
- Useful remote headers from the prior investigation: `X-MCP-Toolsets` for toolset restriction and `X-MCP-Readonly: true` for read-only posture.
- Local fallback: `npx -y @azure-devops/mcp {organization}`.
- Prefer delegated/browser auth where practical. If a PAT is required, mount it as a runtime secret and scope it narrowly.

Azure cloud:

- Official Azure MCP Server is the preferred cloud candidate.
- Potential startup paths from the prior investigation:
  - `npx -y @azure/mcp@latest server start --read-only`
  - `uvx --from msmcp-azure azmcp server start --read-only`
  - `docker run -i mcr.microsoft.com/azure-sdk/azure-mcp:latest`
- Keep Azure cloud access read-only. Use namespace/service allowlists for inventory, logs, diagnostics, and service details.
- Prefer structured MCP read tools. Treat Azure CLI commands as runbook suggestions, not Mes-executed mutations.

GitHub:

- Use the official GitHub MCP Server or a similarly maintained adapter.
- Start with repo-scoped read access.
- Writes for issues, PR comments, and reviews should remain proposal-first.
- Mes should not push code or apply file changes.

Obsidian:

- `obsidian-mcp` and Vault Operator are candidates if direct filesystem access is not enough.
- Karpathy-style append/review notes and Markdown wiki patterns remain good references.

## ADO Drafting Details

Useful draft fields:

- Title
- Work item type
- Project
- Area path
- Iteration/sprint
- Description
- Acceptance criteria
- Links to Obsidian/source artifacts
- Rationale for field choices

Current iteration should be checked against live Azure DevOps before proposing sprint placement. Dynamic sprint/team context can live in Obsidian, but live ADO wins when they disagree.

## Coding Handoff Details

Prior detailed handoff shape:

- Canonical location: Obsidian first, with external ADO/GitHub drafts linking back.
- Draft folder candidate: `mes/handoffs/`.
- Filename candidate: `YYYY-MM-DD-short-slug.md`.
- Frontmatter candidates: `status`, `type`, `created_by`, `source_refs`, `ado_refs`, `github_refs`, `owner`, `needs_approval`.
- Body sections: `Problem`, `Context Links`, `Constraints`, `Non-Goals`, `Acceptance Criteria`, `Suggested Investigation`, `Test Expectations`, `Open Questions`, `Approval Notes`.

Mes and its sub-agents should not include patches unless a separate coding tool produced them.

## Obsidian Details

Prior folder candidates:

- `mes/inbox/` for capture
- `mes/handoffs/` for handoff drafts
- `mes/outputs/` for generated outputs
- `mes/wiki/` for future durable Mes-authored wiki content

Prior write posture:

- Direct append-only capture only when explicitly requested.
- Direct creation of new handoff/output artifacts only when explicitly requested.
- Wiki changes remain proposals until backup, diff review, and conflict behavior are mature.
- Avoid broad unattended edits outside Mes-owned folders.

## Weekly Briefing Details

Initial briefing topics:

- Work-adjacent developments
- New AI models
- Software engineering tools and practices
- Broader relevant industry movement

Prior output idea:

- Store dated briefing artifacts under a path such as `mes/outputs/weekly-briefings/YYYY-MM-DD.md` after the user approves the recurring output location.

Important constraints:

- Prefer primary sources, official release notes, vendor docs, research papers, reputable reporting, and direct project repositories.
- Include source links and dates for material claims.
- Do not send private project names, customer names, tenant details, or sensitive work terms to public search unless explicitly approved.
- Start as manual one-shot research. Add Hermes cron only after output quality is proven and the job is explicitly enabled.
