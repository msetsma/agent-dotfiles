# Agent Dotfiles

Dotter-managed agent skill dotfiles for the agents I use.

This repo currently targets:

- Codex custom skills: `~/.agents/skills`
- Claude skills: `~/.claude/skills`

It intentionally does not manage `~/.codex/skills`, which contains Codex system-managed skills in this environment.

## Layout

```text
.dotter/
  global.toml      # Dotter package definitions
  local.toml       # Local package selection
skills/
  custom/          # Skills written or maintained here
  vendor/          # External skills I like and choose to keep here
.dotter/
  targets/         # Dotter source aliases; do not edit directly
```

`skills/custom` and `skills/vendor` are the canonical source directories. Claude and Codex deploy from the same skill contents so both agents stay identical.

Dotter does not allow deploying the same source path to multiple targets in one run, so `.dotter/targets` contains symlink aliases used only by Dotter.

## What To Touch

Add or edit skills here:

```text
skills/custom/
skills/vendor/
```

Edit deployment config here only when adding another agent or changing target paths:

```text
.dotter/global.toml
.dotter/local.toml
```

Do not add skills here:

```text
.dotter/targets/
```

That directory exists only so Dotter can deploy the same skill tree to both Claude and Codex.

For example:

```text
skills/custom/my-skill/SKILL.md
```

deploys to:

```text
~/.agents/skills/my-skill/SKILL.md
~/.claude/skills/my-skill/SKILL.md
```

## Usage

Preview changes:

```sh
dotter -d -v deploy
```

Deploy changes:

```sh
dotter deploy
```

Dotter uses `.dotter/local.toml` by default. The checked-in default enables both Codex and Claude packages:

```toml
packages = ["codex", "claude"]
```

## Adding A Skill

Create a folder under `skills/custom` for skills maintained in this repo:

```text
skills/custom/example-skill/SKILL.md
```

Create a folder under `skills/vendor` for external skills you want this repo to carry:

```text
skills/vendor/some-external-skill/SKILL.md
```

Skill folder names must be unique across `skills/custom` and `skills/vendor`, because both directories deploy into the same target directory for each agent.

## Notes

- Do not put secrets in this repo.
- Run `dotter -d -v deploy` before deploying if you have edited skill names or moved folders.
- If a deployed target already contains a non-Dotter file with the same path, Dotter may skip or require force. Prefer resolving the conflict manually instead of using force by default.
- The hidden `.gitkeep` files only keep empty scaffold directories in git. Remove them from a directory after adding the first real skill there.
