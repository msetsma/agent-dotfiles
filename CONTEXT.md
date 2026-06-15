# Mes

Mes is the user's named Hermes Agent profile/distribution for day-to-day productivity across local notes, work artifacts, developer systems, and approved external tools.

## Language

**Mes**:
The user's named Hermes Agent profile/distribution for day-to-day work. Mes acts as the user within approved permissions and keeps local-first productivity workflows coherent.
_Avoid_: Generic assistant, bot

**Mes V1**:
The first useful Mes release boundary: a Hermes Profile with repo-backed docs and config templates, approved MCP setup for Obsidian, Azure DevOps, Azure cloud read-only context, GitHub read/proposal workflows, bounded sub-agent delegation, and parent-selected model routes.
_Avoid_: Graph dependency, RAG dependency, recursive agents, direct Azure mutation, code-writing agent

**V1 Done Criteria**:
The concrete proof that Mes V1 is useful: launch Mes as a Hermes Profile, load approved MCPs, query Obsidian plus Azure DevOps, GitHub, and Azure cloud read-only context, produce an Obsidian handoff or output artifact, and delegate one bounded Sub-agent with a selected Model Route and restricted Delegated MCP Set.
_Avoid_: Completing deferred systems such as Graph, RAG, Kanban, recursive agents, or code-writing

**Hermes Profile**:
A named Hermes Agent configuration with its own config, MCP connections, skills, memory, sessions, and operational state. Mes should start as a Hermes Profile that can be backed up in a repository.
_Avoid_: Separate app unless Hermes primitives prove insufficient

**Profile Distribution**:
A repo-backed Hermes Profile package using Hermes's native distribution layout. It owns files such as `distribution.yaml`, `SOUL.md`, `config.yaml`, `mcp.json`, `skills/`, and optional `cron/`, while excluding user-owned memories, sessions, secrets, logs, and runtime state.
_Avoid_: Custom Mes package format

**Profile Repository**:
The repository that backs up Mes's durable profile/distribution assets using Hermes's native Profile Distribution layout. It may also contain Mes planning docs, but it does not contain private runtime state, secrets, memories, sessions, logs, or the Obsidian vault.
_Avoid_: Runtime backup, vault backup

**Vault Backup**:
The separate backup/sync mechanism for the Obsidian vault, such as Dropbox, its own repository, or another cloud sync system.
_Avoid_: Mes profile repository

**Harness**:
The Hermes Agent runtime that powers Mes's agent loop, model use, tool calling, and sub-agent orchestration.
_Avoid_: MCP registry, MCP server manager

**MCP Control Plane**:
The Mes-owned layer that starts, configures, health-checks, and gates approved MCP servers before exposing their tools to agents.
_Avoid_: Harness

**Main Agent**:
The primary Mes agent that receives the user's request, plans the work, chooses model routes, and delegates bounded work to sub-agents when useful.
_Avoid_: Root bot, supervisor unless a concrete supervisor abstraction exists

**Sub-agent**:
A bounded-scope agent spawned by the Main Agent for a specific task. The spawning parent chooses the Sub-agent's model route based on the task and any user instruction. A Sub-agent receives an explicit subset of the parent's approved MCP access and may receive multiple MCPs when the task requires it. In the first version, Sub-agents do not spawn other Sub-agents.
_Avoid_: Worker unless the implementation uses that term

**Model Route**:
A named model choice or model alias selected by an agent's parent for a specific task. User instructions can constrain or override the parent's selection.
_Avoid_: Provider name unless the provider is the intended decision

**Sub-agent Depth**:
The maximum number of delegation levels allowed below the Main Agent. The first version has a Sub-agent Depth of one; later versions may allow recursive delegation to an explicit bounded depth.
_Avoid_: Unlimited recursion, agent swarm unless that becomes a concrete product concept

**Approved MCP**:
An MCP server or toolset that Mes is explicitly allowed to start and query for a given task under its current permissions.
_Avoid_: Available MCP, installed MCP

**Delegated MCP Set**:
The explicit subset of a parent's Approved MCPs made available to a Sub-agent for one task. The set can include multiple MCPs, and Obsidian is generally eligible because it is Mes's local knowledge source.
_Avoid_: Full inherited tool access

**Shared Knowledge Source**:
The default read-mostly knowledge available to the Main Agent and Sub-agents. Obsidian is Mes's Shared Knowledge Source; agents can read it broadly, but writes stay constrained to explicit task contracts.
_Avoid_: Optional notes integration

**Operational State Store**:
Mes's runtime and control data, such as MCP registry state, delegated MCP sets, task contracts, model route decisions, traces, health checks, caches, and audit logs. Operational state should be inspectable through supported commands and not casually edited by hand.
_Avoid_: Obsidian, notes

**Human Knowledge**:
Human-readable knowledge that belongs in Obsidian, such as notes, summaries, decisions, durable todos, and wiki pages.
_Avoid_: Run traces, permission state, transient cache data

**Weekly Briefing**:
A scheduled or manually triggered Mes research output that summarizes source-linked developments the user wants to track. Initial topics include the user's work context, new AI models, software engineering news, and broader industry changes. It should be curated, dated, and written as a human-facing output, not treated as raw operational state.
_Avoid_: News firehose, unsourced trend summary

**Briefing Topic Set**:
The user-controlled list of recurring topics, watch phrases, sources, and exclusions that guide a Weekly Briefing. This should be editable by the user, likely in Obsidian or profile docs depending on stability.
_Avoid_: Hard-coded research prompt

**Briefing Output**:
The generated Weekly Briefing artifact, usually a dated note in `mes/outputs/`, with links or citations back to source material and explicit open questions when sources disagree or are thin.
_Avoid_: Silent wiki update, raw link dump

**Hermes Memory**:
Hermes Agent's small built-in long-term memory for durable user preferences, environment facts, and instructions about how Mes should work. It should point to Obsidian and summarize usage rules, not duplicate vault content.
_Avoid_: Obsidian mirror, project wiki

**Human Todo Surface**:
The human-editable todo and follow-up surface in Obsidian. The user may directly modify these todos, so Mes must treat them as shared human-owned knowledge.
_Avoid_: Agent work queue

**Agent Work Queue**:
The durable agent coordination surface, likely Hermes Kanban, for tasks that need assignment, retries, worker profiles, handoffs, or long-running multi-agent coordination.
_Avoid_: Human todo list

**Kanban Promotion**:
Moving a Human Todo into the Agent Work Queue. A task is promoted when it needs a named worker/profile, must survive interruption or restart, needs retry/block/unblock state, needs comments or handoff, or spans multiple agent runs.
_Avoid_: Promoting simple personal reminders

**ADO Draft**:
A proposed Azure DevOps work item prepared by Mes but not created or updated until the user approves it. The draft includes fields such as title, type, area/iteration, description, acceptance criteria, links, and rationale.
_Avoid_: Direct ticket creation

**GitHub Draft**:
A proposed GitHub issue, PR comment, or review prepared by Mes but not posted until the user approves it. Mes does not prepare or apply code changes itself.
_Avoid_: Direct GitHub write, code patch

**ADO Board Context**:
Human-maintained context about the user's Azure DevOps boards, sprint calendars, iteration naming, area paths, teams, and work item conventions.
_Avoid_: ADO runtime state

**Stable ADO Context**:
ADO conventions that change rarely, such as work item types, required fields, naming rules, approval checklist, and field templates. This belongs in the Mes Profile Repository.
_Avoid_: Current sprint notes

**Dynamic ADO Context**:
ADO context that changes regularly, such as sprint dates, current iteration, team board notes, active exceptions, and temporary conventions. This belongs in Obsidian.
_Avoid_: Profile config

**Current Iteration**:
The active Azure DevOps sprint/iteration for the relevant team or board. Mes should query Azure DevOps live for this before drafting work items, using Dynamic ADO Context as explanatory fallback rather than authority.
_Avoid_: Inferred sprint

**Stale ADO Context**:
Dynamic ADO Context that conflicts with live Azure DevOps data. Live ADO data wins for draft fields; Mes should flag the stale note and propose an Obsidian update rather than silently editing it.
_Avoid_: Silent correction

**Azure Cloud Context**:
Read-only Azure resource information available to Mes, such as inventory, service configuration, logs, diagnostics, and operational details.
_Avoid_: Azure resource mutation

**Azure Runbook Suggestion**:
A suggested Azure CLI command or procedure produced by Mes for the user to review and run outside Mes. Structured read-only Azure MCP tools are preferred; generated CLI is fallback guidance and not an execution path for Azure mutations.
_Avoid_: Executed Azure mutation

**Coding Handoff**:
A document or structured brief that Mes prepares for a human or separate coding agent/tool to implement code changes. Mes and its sub-agents do not edit code directly.
_Avoid_: Mes code implementation

**Handoff Packet**:
The standard content of a Coding Handoff: problem statement, source context links, relevant Obsidian notes, ADO/GitHub references, constraints, non-goals, acceptance criteria, suggested files or areas to inspect, test expectations, and open questions.
_Avoid_: Patch unless produced by a separate coding tool

**Canonical Handoff Packet**:
The Obsidian note that owns a Handoff Packet. ADO or GitHub drafts may link to or summarize it, but Obsidian remains the canonical human-editable source.
_Avoid_: Ticket-only handoff

**Handoff Draft Folder**:
The Mes-owned Obsidian folder where Mes may create new draft Canonical Handoff Packets when the user explicitly asks for a Coding Handoff. Notes in this folder are drafts and may be revised by the user before being linked or summarized elsewhere.
_Avoid_: Arbitrary vault writes

**Mes-owned Obsidian Folders**:
The constrained Obsidian folder tree where Mes may write under explicit folder-specific policies: `mes/inbox/`, `mes/handoffs/`, `mes/outputs/`, and optionally `mes/wiki/`.
_Avoid_: Writes outside `mes/`

**Vault Read Scope**:
The explicit set of Obsidian folders Mes may read directly. The default scope is `mes/` plus named work or project folders; private, journal, and sensitive folders are ignored unless the user provides manual summaries.
_Avoid_: Whole-vault access by default

**Capture Write**:
An append-only Obsidian write to `mes/inbox/` that Mes may perform without preview when the user explicitly asks Mes to capture a note, task, reminder, command, or meeting fragment.
_Avoid_: Silent note editing

**Handoff Draft Write**:
Creation of a new draft Coding Handoff in `mes/handoffs/` that Mes may perform without preview when the user explicitly asks Mes to prepare a handoff. Editing an existing handoff or linking it into ADO/GitHub still requires preview or approval.
_Avoid_: Silent external posting

**Output Write**:
Creation of a new generated summary, report, or other requested artifact in `mes/outputs/` that Mes may perform without preview when the user explicitly asks for an output. Editing or overwriting existing outputs still requires preview or approval.
_Avoid_: Silent output churn

**Wiki Proposal**:
A proposed durable Obsidian wiki page or wiki edit prepared by Mes for review. In V1, `mes/wiki/` is propose-only: Mes may draft wiki content into `mes/outputs/` or return suggested changes, but it does not directly create or update durable wiki pages.
_Avoid_: Direct wiki write
