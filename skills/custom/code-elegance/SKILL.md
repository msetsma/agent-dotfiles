---
name: code-elegance
description: Applies language-agnostic code elegance patterns to make code clearer, simpler, and easier to change without changing behavior. Use when writing, refactoring, reviewing, or simplifying code in any language; when the user asks for elegant, clean, readable, maintainable, idiomatic, or less nested code; or when code has complex branching, mutable state, validation/error-flow noise, loop/collection clutter, or unmeasured performance work.
---

# Code Elegance

Use this skill for small, behavior-preserving refactors in any programming language. Elegance = fewer moving parts + clearer intent, not cleverness.

For pattern catalog, see [REFERENCE.md](REFERENCE.md). For review prompts and selection checklists, see [APPLICATION.md](APPLICATION.md).

## Operating Principles

1. Preserve behavior unless user asks for behavior change.
2. Match repo style before generic pattern.
3. Translate patterns into language idioms instead of forcing Python-shaped code.
4. Prefer clarity over density. Shorter expression is worse if it hides intent.
5. Prefer local, boring refactors before abstractions.
6. Remove state and branches before adding patterns.
7. Optimize only with plausible cost and no readability harm.
8. Verify with existing tests, type checks, or focused checks when available.

## Default Workflow

1. Read surrounding code; identify friction: nesting, duplication, mutable state, unclear names, validation spread, error plumbing, loop noise, expensive eager work.
2. Choose smallest applicable pattern from priority list.
3. Apply refactor in one small step.
4. Re-read result; reject if more abstract, magical, or harder to scan.
5. Run targeted verification.
6. Explain change by reduced branches/state, clearer names, or safer invariants.

## Language Adaptation

Before applying pattern, map it to target language's normal tools. Prefer guidance for languages present in repo.

- Python: guard clauses, comprehensions, generators, dataclasses, enums, context managers.
- TypeScript/JavaScript: early returns, optional chaining, nullish coalescing, discriminated unions, array methods, maps, async resource cleanup patterns.
- Rust: `Result`/`Option`, pattern matching, iterators, ownership/borrowing, enums that encode valid states.
- Go: explicit guard returns, small interfaces, table-driven tests/data, error wrapping, simple structs.
- Bash: small functions, explicit exits, quoted expansions, arrays for lists, `case` for dispatch, `trap` for cleanup, simple pipelines, ShellCheck-compatible style.

If language lacks direct feature, preserve principle instead of awkward syntax emulation.

Bash is different: do not force rich type/model patterns into shell. Prefer clear control flow, safe argument handling, predictable errors, and moving complex data logic to real language when shell stops fitting.

## Pattern Priority

Apply in this order unless local context says otherwise:

1. **Clarify intent**: intention-revealing names, extracted variables, named constants, single abstraction level.
2. **Flatten control flow**: guard clauses, early returns, fail-fast checks, happy path last.
3. **Reduce mutable state**: single assignment, pure transformations, immutable-first values, command-query separation.
4. **Centralize variation**: dispatch tables/maps, strategy functions/objects, polymorphism, enums/sealed types, parameter objects.
5. **Strengthen boundaries**: parse-don't-validate, invalid states unrepresentable, explicit result/error handling.
6. **Simplify collections**: collection transforms, existence/universal checks, lazy iterators/streams, first-match helpers, batching.
7. **Defer expensive work**: lazy initialization, caching/memoization, batching, short-circuiting.

## Guardrails

- Do not introduce point-free style, monads, trampolines, object pools, flyweights, or fluent builders unless surrounding code already uses them or complexity clearly pays.
- Do not replace simple `if` statements with dispatch/polymorphism unless new cases are expected or branch is already hard to maintain.
- Do not collapse multi-step business logic into dense one-liner.
- Do not rely on truthiness/nullish defaults when `0`, `False`, `""`, empty collections, or equivalent values are valid; use explicit absence checks.
- Do not hide side effects inside helpers that look like pure queries.
- Coordinate with `code-smells` for smell detection and `naming-conventions` for naming-heavy refactors.

## Review Output

When reporting opportunities, include:

- **Location**: file, function, or line.
- **Friction**: what makes code harder to read/change.
- **Pattern**: specific code elegance pattern.
- **Fix**: concrete refactor, preferably behavior-preserving.
- **Trade-off**: why worth it, or why skip.
