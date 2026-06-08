---
name: code-smells
description: Detects language-agnostic code smells and suggests concrete refactors. Use when writing new code, reviewing diffs/PRs, or when the user asks to improve, refactor, clean up, simplify, or review code in common languages such as Python, JavaScript/TypeScript, C#, Go, Rust, Kotlin, Shell, or config formats.
---

# Code Smell Detection

Use this skill to find maintainability risks and suggest concrete, behavior-preserving refactors across standard languages. A smell is a signal, not proof of bad code: prioritize issues that create bug surface, change friction, or clear readability cost.

For the full catalog, examples, and language-specific traps, see [REFERENCE.md](REFERENCE.md).

## Review Workflow

When reviewing code or a diff:

1. Identify the language and local idioms before judging the code.
2. Scan for size, duplication, coupling, conditionals, state mutation, error-handling traps, unclear naming, dead/speculative code, and deep nesting.
3. Check language-specific pitfalls only after the general smell pass.
4. Prioritize `high` severity findings first.
5. Group minor `low` severity findings so the review stays actionable.
6. For every smell you flag, suggest a concrete fix.
7. Use before/after snippets only when they make the fix clearer.

When writing new code:

1. Keep functions small enough to name and test directly.
2. Prefer explicit data shapes over loose bags of primitives.
3. Put behavior near the data or boundary it belongs to.
4. Keep error handling specific and visible.
5. Add abstraction only when it removes real duplication or isolates change.

## Response Protocol

For each smell found, output:

1. **Location** — file + line/function/class.
2. **Smell** — the named smell.
3. **Why it matters** — concrete risk: bugs, maintainability, readability, performance, or change friction.
4. **Suggested fix** — the refactoring technique and a concise explanation.
5. **Severity** — `low`, `medium`, or `high`.

## Severity Guide

- **high** — likely to cause bugs, security issues, data loss, or blocked changes; examples include duplicated business rules, unsafe shared mutable state, injection-prone string building, and swallowed exceptions.
- **medium** — clear maintainability cost without immediate defect; examples include long functions, large classes, and feature envy.
- **low** — readability or polish; examples include unclear names, minor duplication, and comments compensating for unclear code.

## Checklist

- **Size** — functions over about 60 lines, classes with low cohesion, modules doing too much.
- **Duplication** — repeated logic that can drift.
- **Coupling** — message chains, feature envy, or reaching into another unit's internals.
- **Conditionals** — type switching, flag arguments, or nested branching that should be dispatch, strategy, pattern matching, or polymorphism.
- **State** — hidden mutation, shared mutable defaults, temporal coupling, or inconsistent return shapes.
- **Errors** — swallowed exceptions, broad catches, ignored results, or mixed error strategies.
- **Boundaries** — string-built SQL/paths/commands, unvalidated input, or leaked internal representations.
- **Naming** — unclear names that need comments to explain intent.
- **Dead/speculative code** — unused code or abstractions built for imagined future use.
- **Nesting** — arrow code or more than about three indentation levels.

## Guardrails

- Suggest, do not bulldoze: explain the trade-off and let subjective calls stay subjective.
- Prefer the smallest refactor that resolves the issue.
- Do not introduce an abstraction if it adds more complexity than it removes.
- Keep behavior identical unless fixing an actual bug; call bug fixes out separately.
- Match the repo's existing style and conventions.
- Use the naming-conventions skill when the main issue is naming.
- Respect generated code, external schemas, public API compatibility, and framework conventions.
