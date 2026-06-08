---
name: code-smells
description: Detects language-agnostic code smells and suggests concrete refactors. Use when writing new code, reviewing diffs/PRs, or when the user asks to improve, refactor, clean up, simplify, or review code in common languages such as Python, JavaScript/TypeScript, C#, Go, Rust, Kotlin, Shell, or config formats.
---

# Code Smell Detection

Use this skill to find maintainability risks and suggest concrete, behavior-preserving refactors across standard languages. Smell = signal, not proof. Prioritize bug surface, change friction, or clear readability cost.

For full catalog, examples, language-specific traps, see [REFERENCE.md](REFERENCE.md).

## Review Workflow

When reviewing code or diff:

1. Identify language and local idioms before judging.
2. Scan size, duplication, coupling, conditionals, state mutation, error traps, unclear naming, dead/speculative code, deep nesting.
3. Check language-specific pitfalls after general smell pass.
4. Prioritize `high` severity findings first.
5. Group minor `low` severity findings so review stays actionable.
6. For every smell, suggest concrete fix.
7. Use before/after snippets only when fix becomes clearer.

When writing new code:

1. Keep functions small enough to name and test directly.
2. Prefer explicit data shapes over loose bags of primitives.
3. Put behavior near owning data or boundary.
4. Keep error handling specific and visible.
5. Add abstraction only when it removes real duplication or isolates change.

## Response Protocol

For each smell found, output:

1. **Location** — file + line/function/class.
2. **Smell** — named smell.
3. **Why it matters** — concrete risk: bugs, maintainability, readability, performance, or change friction.
4. **Suggested fix** — refactoring technique + concise explanation.
5. **Severity** — `low`, `medium`, or `high`.

## Severity Guide

- **high** — likely bugs, security issues, data loss, or blocked changes; examples: duplicated business rules, unsafe shared mutable state, injection-prone string building, swallowed exceptions.
- **medium** — clear maintainability cost without immediate defect; examples: long functions, large classes, feature envy.
- **low** — readability/polish; examples: unclear names, minor duplication, comments compensating for unclear code.

## Checklist

- **Size** — functions over about 60 lines, low-cohesion classes, modules doing too much.
- **Duplication** — repeated logic that can drift.
- **Coupling** — message chains, feature envy, reaching into another unit's internals.
- **Conditionals** — type switching, flag args, nested branching that should be dispatch, strategy, pattern matching, or polymorphism.
- **State** — hidden mutation, shared mutable defaults, temporal coupling, inconsistent return shapes.
- **Errors** — swallowed exceptions, broad catches, ignored results, mixed error strategies.
- **Boundaries** — string-built SQL/paths/commands, unvalidated input, leaked internals.
- **Naming** — unclear names needing comments to explain intent.
- **Dead/speculative code** — unused code or abstractions for imagined future.
- **Nesting** — arrow code or more than about three indentation levels.

## Guardrails

- Suggest; do not bulldoze. Explain trade-off; subjective calls stay subjective.
- Prefer smallest refactor that resolves issue.
- Do not add abstraction if it adds more complexity than it removes.
- Keep behavior identical unless fixing actual bug; call bug fixes out separately.
- Match repo style/conventions.
- Use naming-conventions skill when main issue is naming.
- Respect generated code, external schemas, public API compatibility, framework conventions.
