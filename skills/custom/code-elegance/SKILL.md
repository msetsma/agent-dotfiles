---
name: code-elegance
description: Applies language-agnostic code elegance patterns to make code clearer, simpler, and easier to change without changing behavior. Use when writing, refactoring, reviewing, or simplifying code in any language; when the user asks for elegant, clean, readable, maintainable, idiomatic, or less nested code; or when code has complex branching, mutable state, validation/error-flow noise, loop/collection clutter, or unmeasured performance work.
---

# Code Elegance

Use this skill to improve code shape through small, behavior-preserving refactors in any programming language. Elegance means fewer moving parts and clearer intent, not cleverness.

For the pattern catalog, see [REFERENCE.md](REFERENCE.md). For concrete review prompts and selection checklists, see [APPLICATION.md](APPLICATION.md).

## Operating Principles

1. Preserve behavior unless the user explicitly asks for a behavior change.
2. Match the repo's existing style before applying any generic pattern.
3. Translate patterns into the language's idioms instead of forcing Python-shaped code.
4. Prefer clarity over density. A shorter expression is worse if it hides intent.
5. Prefer local, boring refactors before adding abstractions.
6. Remove state and branches before adding patterns.
7. Optimize only when there is a plausible cost and the change does not harm readability.
8. Verify with existing tests, type checks, or focused checks when available.

## Default Workflow

1. Read the surrounding code and identify the friction: nesting, duplication, mutable state, unclear names, validation spread, error plumbing, loop noise, or expensive eager work.
2. Choose the smallest applicable pattern from the priority list below.
3. Apply the refactor in one small step.
4. Re-read the result and reject the change if it is more abstract, more magical, or harder to scan.
5. Run targeted verification.
6. Explain the change in terms of reduced branches, reduced state, clearer names, or safer invariants.

## Language Adaptation

Before applying a pattern, map it to the target language's normal tools. Prefer guidance for the languages actually present in the repo.

- Python: guard clauses, comprehensions, generators, dataclasses, enums, context managers.
- TypeScript/JavaScript: early returns, optional chaining, nullish coalescing, discriminated unions, array methods, maps, async resource cleanup patterns.
- Rust: `Result`/`Option`, pattern matching, iterators, ownership/borrowing, enums that encode valid states.
- Go: explicit guard returns, small interfaces, table-driven tests/data, error wrapping, simple structs.
- Bash: small functions, explicit exits, quoted expansions, arrays for lists, `case` for dispatch, `trap` for cleanup, simple pipelines, ShellCheck-compatible style.

If a language lacks a direct feature, preserve the principle rather than emulating syntax awkwardly.

Bash is different: do not force rich type/model patterns into shell. Prefer clear control flow, safe argument handling, predictable error behavior, and moving complex data logic to a real language when shell stops being the right tool.

## Pattern Priority

Apply in this order unless local context strongly says otherwise:

1. **Clarify intent**: intention-revealing names, extracted variables, named constants, single abstraction level.
2. **Flatten control flow**: guard clauses, early returns, fail-fast checks, happy path last.
3. **Reduce mutable state**: single assignment, pure transformations, immutable-first values, command-query separation.
4. **Centralize variation**: dispatch tables/maps, strategy functions/objects, polymorphism, enums/sealed types, parameter objects.
5. **Strengthen boundaries**: parse-don't-validate, invalid states unrepresentable, explicit result/error handling.
6. **Simplify collections**: collection transforms, existence/universal checks, lazy iterators/streams, first-match helpers, batching.
7. **Defer expensive work**: lazy initialization, caching/memoization, batching, short-circuiting.

## Guardrails

- Do not introduce point-free style, monads, trampolines, object pools, flyweights, or fluent builders unless the surrounding code already uses them or the complexity clearly pays for itself.
- Do not replace simple `if` statements with dispatch/polymorphism unless new cases are expected or the branch is already hard to maintain.
- Do not collapse multi-step business logic into a dense one-liner.
- Do not rely on truthiness/nullish defaults when `0`, `False`, `""`, empty collections, or equivalent values are valid; use explicit absence checks.
- Do not hide side effects inside helpers that look like pure queries.
- Coordinate with the `code-smells` skill for smell detection and the `naming-conventions` skill for naming-heavy refactors.

## Review Output

When reporting opportunities, include:

- **Location**: file, function, or line.
- **Friction**: what makes the code harder to read or change.
- **Pattern**: the specific code elegance pattern.
- **Fix**: a concrete refactor, preferably behavior-preserving.
- **Trade-off**: why this is worth it, or why it should be skipped.
