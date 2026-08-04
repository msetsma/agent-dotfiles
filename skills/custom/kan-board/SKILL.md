---
name: kan-board
description: "Mitchell's local Kan boards — 'Personal' (his own todos, read/write) plus two read-only Azure DevOps mirrors: 'ADO — Mine' (work items assigned to him) and 'ADO — Triage' (unassigned intake Features awaiting a category lead). Use when asked what's on his plate or his board, to add/move/close a personal todo, for what's in his ADO queue or awaiting triage, or before touching any card on those boards."
---

# Kan boards

Self-hosted Kan at <http://board.localhost>, running from `/Users/msetsma/kan-setup`.
One authored board and two one-way mirrors of Azure DevOps (org `steelcase`, identity
`MSETSMA@steelcase.com`). Nothing here ever writes back to ADO.

## Coordinates

| Thing | Value |
|---|---|
| Helper | `/Users/msetsma/kan-setup/bin/kan` (prefer this here — the `kan` MCP server exposes the same ten operations for Desktop/IDE clients, but costs 10 tool schemas per session) |
| Base URL | `http://board.localhost/api/v1` (token in `~/kan-setup/.env`) |
| Workspace | `lzd69j0gxdfh` |
| Freshness + health | `make -C /Users/msetsma/kan-setup status` |
| Sync log | `/Users/msetsma/kan-setup/logs/ado-sync.log` |

| Board | publicId | Mode |
|---|---|---|
| `Personal` | `hbv0uq3xltt5` | read/write |
| `ADO — Mine` | `pml6a5v5dcwg` | **read-only mirror** (~24 cards) |
| `ADO — Triage` | `9mbscre2ms04` | **read-only mirror** (~64 cards) |

| Board | Lists |
|---|---|
| Personal | Inbox `kfbjapjl8wfm` · Next `mzen64issrqk` · Doing `v4xuqcfyukyn` · Waiting `aygo8w37cwjp` · Done `unx75jc539go` |
| ADO — Mine | New `iihhjftsvtjk` · Active `zj8eutp9rhlo` · Review `wjasy9jjvp10` · Closed `odg1iirk57hw` · Other `31lublarf9ic` · Archived `5mzsehlyqq45` |
| ADO — Triage | New `b7dh9o39jiow` · Active `x3nhg62bnh52` · Review `f6iqmbfpnz71` · Closed `q5mi0ieakvgl` · Other `mafaksc24rk8` · Archived `hogpyf1qbzec` |

Personal labels: work `xs55n4g5ti4b` · home `6ba2ijyn7gkx` · deep `adt5plk3dyl1` · quick `xd2glqgljrfj`

## Reading

One request returns a whole board — lists, cards, and full descriptions. Prefer it over
per-card fetches.

```bash
kan board hbv0uq3xltt5                     # everything on Personal
kan lists 9mbscre2ms04                     # list names + card counts only
kan search lzd69j0gxdfh "drawing checker"   # across boards and cards
```

Mirror card titles are `[<WorkItemType>] #<ado-id> <Title>`, so both the id and the ADO
title's own `(Requester)` suffix are greppable:

```bash
kan board 9mbscre2ms04 | jq -r '.lists[].cards[].title' | grep Villarreal
```

Card descriptions carry a direct
`https://dev.azure.com/steelcase/<Project>/_workitems/edit/<id>` link plus state, iteration,
area, assignee, priority, story points, parent, description and acceptance criteria. **The
description is the authoritative reading of the true ADO state** — the Kan list is a
coarse bucket.

## Writing

Only the `Personal` board accepts writes.

```bash
kan card new --list kfbjapjl8wfm --title "Ping Paola re scoping" --label xs55n4g5ti4b
kan card move <cardId> --list v4xuqcfyukyn
kan card set  <cardId> --title "..." --desc "..."
kan card comment <cardId> "waiting on Perrin"
```

Lane meanings: **Inbox** uncategorised capture · **Next** committed to soon · **Doing** in
flight · **Waiting** blocked on someone else · **Done**.

## Rules

- **Never write to a mirror board.** `bin/kan` refuses, and that refusal is correct — do not
  work around it with `kan raw`. Titles, descriptions and lists are overwritten within 30
  minutes, and any comment added to a mirror card survives forever as orphaned noise.
- **To change real work, change the work item in ADO**, then re-sync. Use the `azure-devops`
  MCP (`wit_work_item_write`, `wit_work_item_comment_write`) and then
  `make -C /Users/msetsma/kan-setup sync`. Do not report a change as done based on the Kan
  card until the sync confirms it.
- **Check freshness before trusting a mirror.** Run `make -C /Users/msetsma/kan-setup status`.
  A stale board looks identical to an accurate one. If `status` is not `ok`, the usual cause
  is an expired `az` token — suggest the user type `! az login`, which needs a TTY.
- **Cards are matched to work items by the `#<id>` in the title, falling back to the ADO link
  in the description.** Two independent sources, so a card renamed in the browser is still
  recognised and repaired rather than duplicated. A card matching neither is swept to
  `Archived` on the next sync, as is any duplicate. The mirror self-heals — but don't rely on
  that as licence to edit it.
- **Mirror lists are coarse.** ADO's `Resolved`/`Review`/`In Review` all land in `Review`,
  and a state from a custom process template lands in `Other`. Read the description for the
  exact state rather than inferring it from the list.
- **`Custom.BlockedBoolean` is reflected as a `blocked` label**, not a list.
- Anything the helper doesn't wrap: `kan spec` lists every operation, then `kan raw`. Board
  creation is `POST /workspaces/{id}/boards`, not `POST /boards`.

## Pulling ADO work onto the Personal board

The mirrors are reference; `Personal` is where work is authored. To work an intake item,
copy it across rather than editing the mirror — the mirror card stays as the reference and
`Personal` becomes the scratchpad:

1. Read the mirror card for the ADO id and link.
2. `kan card new --list mzen64issrqk --title "<Topic> (<Requester>)" --desc "<ADO link + why>"`
3. Track your own progress on the Personal card. ADO stays authoritative for the
   work item's real state — see [[portfolio-intake]].

## Scope of the mirrors

| Mirror | WIQL scope |
|---|---|
| `ADO — Mine` | `[System.AssignedTo] = @Me` + one level of children |
| `ADO — Triage` | area under `Analytics\Data Science` **and** type `Feature` **and** unassigned |

Both additionally require "open, or touched within 30 days" (`--since-days`).

`ADO — Triage` is deliberately **not** filtered to "assigned to me". Intake items are
auto-created from the request email with no owner, so that filter matches ~4 items in the
area and 3 already appear on `ADO — Mine`; `CreatedBy` is a service account. The *absence*
of an owner is what defines the triage queue. Widening it (drop the type/assignee clauses
for ~178 open items across all owners) means editing `MIRRORS["triage"]["where"]` in
`bin/ado-kan-sync.py`.

When an item leaves scope — assigned to someone, moved area, or aged out — its card moves to
`Archived`. Cards are never deleted.

Related: [[portfolio-intake]]
