---
name: portfolio-intake
description: Answer questions about Mitchell's Operations Portfolio Lead intake work — open requests, who owns what, where a card is stuck, who to pull into a scoping session. Use when the user asks about intake, portfolio requests, "what's open", "what's blocking X", "what do I need to schedule", the portfolio lead meeting, or a named intake project.
---

# Portfolio Intake

Mitchell is **Operations Portfolio Lead** for the Data Science practice: he takes intake
requests from the operations category of the business through meeting → scoring → scoping.

Cards are the truth for state. The vault is the truth for substance. Comments are the truth
for both intent and progress.

## Coordinates

| Thing | Value |
|---|---|
| ADO org / project | `steelcase` / `Analytics` |
| Intake area path | `Analytics\Data Science` |
| Mitchell's delivery area | `Analytics\MLOps` |
| Mitchell's email | `MSETSMA@steelcase.com` |
| Card web link | `https://dev.azure.com/steelcase/Analytics/_workitems/edit/<id>` |
| Local context | `/Users/msetsma/Documents/notes/wiki/Operations Portfolio.md` |

## What an intake card looks like

- Auto-created from the project-request email — no owner, no gatekeeper at creation.
- Work item type **Feature**; title convention **`Topic (Requester)`**
  (e.g. `Drawing Checker Agent (Paola Villarreal)`).
- **Descriptions are typically empty. The substance lives in comments.** Any question about
  intent, assignment, or scheduling requires reading comments — fields will not answer it.

## Roles

| Role | Scope | Owns |
|---|---|---|
| **Portfolio lead** | whole portfolio | assigning intake to a category lead; runs the portfolio lead meeting where projects are scored |
| **Category lead** | a business category | intake from that category, end to end after assignment — **including booking their own meetings** |
| **APL** (Area/Practice Lead) | a discipline | staffing and priority within that discipline |
| **ADL** (Agile Delivery Lead) | a delivery team | backlog, board, and agile rituals |
| **Pipeline lead** | the purchase pipeline — dealers, sales, go-to-market | intake from those areas, same as any category lead |

| Person | Category lead | APL | Other |
|---|---|---|---|
| **Mitchell** (user) | Operations | — | — |
| **Katie R.** | Pipeline | Data Science | leads all portfolio work |
| **Chloe** | Marketing | — | — |
| **Sydney** | IT | Analytics Engineering | — |
| **Kevin T.** | — | MLOps / AI Platform | manager, Data Engineering & MLOps |
| **Hunter** | — | Data Engineering | — |
| **Andrei** + **Christy** | EMEA (Europe + Africa), all categories | — | — |
| **Eduardo "Lalo"** | Regional (Mexico / Monterrey) | Low-code AI automation | manager; new to the team |
| **Katie B.** | — | — | ADL for most projects |

Seen in comments, not on the roster: **Alaine Kirkendall** (operations brainstorming),
**Chris Eversole** (optimization problems), **Esteph** `ehernan9@steelcase.com` (Lalo's team).

Reading a card: **Katie R.'s comments are direction** — assignments, routing, questions about
pipeline state. Her assignment comment *is* the handoff. After it, the category lead owns
everything.

## Pipeline

```
email → card auto-created in ADO
  → portfolio lead assigns a category lead
  → *** HANDOFF *** everything below is that lead's own work
  → message requester + book meeting
  → meet, ask questions
  → bring to portfolio lead meeting
  → score
  → if accepted: scope
  → enters backlog          ← ADL owns board from here
```

## Where a card is stuck

"Not scheduled" is only the first of four stalls, and they are different questions. Ask which
one before answering.

| Stall | Signal in comments |
|---|---|
| Assigned, no meeting booked | assignment comment exists; no comment naming a scheduled meeting |
| Met, never taken to portfolio lead meeting | meeting notes present; no scoring/prioritization mention |
| Scored + accepted, never scoped | acceptance noted; no scoping session or scoping doc |
| Scoped, not in backlog | scoping doc exists; no delivery work items or backlog reference |

**Comments are the only signal.** Iteration path is not a stall signal — *all* backlog items
sit at the root `Analytics` iteration, so "on the root iteration" says nothing about whether a
meeting was booked. Do not use it as a filter or a heuristic.

**Unverified assumption worth stating in answers:** this assumes a booked meeting reliably
produces a comment on the card. If meetings can live only in Outlook, every "nothing booked"
answer is a possible false negative. Say so rather than reporting a clean result.

## Routing — who to pull in

Pattern: **pull in the APL for the discipline the work actually lands in.** Hunter for DE,
Kevin T. for MLOps, Sydney for analytics engineering, Katie R. for data science.

| Trigger | Include | Confidence |
|---|---|---|
| Scoping session that is primarily Data Engineering | Hunter | stated as a rule 2026-07-27 |
| MLOps work | Kevin T. | from roster |
| Optimization problem | Chris Eversole | seen once |
| Operations brainstorming | Katie R. + Alaine Kirkendall | seen once |
| Needs Lalo's low-code team | Esteph, **only while Lalo is on vacation** (expires ~early Aug 2026; after that, Lalo) | expiring — confirm before using |

## Querying

`azure-devops` MCP. Arg quirks: the WIQL param is `wiql` (not `query`);
`wit_get_work_items_batch_by_ids` **requires** `project` even with fully-qualified IDs.
Do not use `wit_my_work_items` for a named person — it uses the MCP identity. Filter by email.

1. `mcp__azure-devops__wit_query_by_wiql` — open intake Features:

```sql
SELECT [System.Id], [System.Title], [System.State], [System.AssignedTo],
       [System.IterationPath], [System.CreatedDate]
FROM WorkItems
WHERE [System.AreaPath] UNDER 'Analytics\Data Science'
  AND [System.State] NOT IN ('Closed','Removed','Done')
  AND [System.WorkItemType] = 'Feature'
ORDER BY [System.CreatedDate] DESC
```

2. `mcp__azure-devops__wit_get_work_items_batch_by_ids` with an explicit `fields` array —
   WIQL returns only IDs.
3. Narrow to the cards the question is actually about, **then**
   `mcp__azure-devops__wit_list_work_item_comments`. Reading comments on every open item is
   the main source of wasted calls.
4. Report per card: requester, what the latest comment asks for, who to include, age, and
   which stall it's in.

## Local context

`wiki/Operations Portfolio.md` in the Obsidian vault (`/Users/msetsma/Documents/notes`) is a
compiled page covering the live threads — plant yield optimization (AMEX 7300), QST ticket
sizing, Gurobi → OR-Tools, walls/order-fulfillment (declined, referred to BIA) — with business
cases, named SMEs and sponsors, and open questions. Read it for substance ADO never captures:
verbal commitments, why something was scoped out, dollar figures.

Vault layers: write new notes to `inbox/operations - portfolio/`; `wiki/` holds the compiled
page; originals move to `archive/operations - portfolio/`. **A project note missing from
`inbox/` does not mean the project is gone** — check `wiki/` and `archive/` before saying so.

## Do not infer

- **No central scheduler exists.** Each category lead books their own meetings. Chloe's many
  "initial meeting scheduled" comments are her booking *her own* marketing cards. Do not
  re-derive a coordinator from comment volume.
- Therefore, on an operations card, a missing scheduling comment means **Mitchell hasn't
  booked it**, not "waiting on someone else."
- Don't state a card's status from memory or from a previous session's snapshot. Re-query.

## Open questions

Surface these when they affect an answer; they can't be resolved by querying ADO.

1. Does a booked meeting reliably produce a comment on the card? (Gates every stall answer.)
2. What marks a request as **operations** — epic, tag, requester's org, or just Katie R.'s
   wording? Currently inferred from area/epic plus her saying "since it's operations".
3. Which routing rules above are standing policy vs. situational one-offs?
