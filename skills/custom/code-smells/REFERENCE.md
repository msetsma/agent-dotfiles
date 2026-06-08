# Code Smell Reference

Taxonomy/refactoring names come from common refactoring literature, especially Refactoring.Guru smell categories and Martin Fowler catalog. Apply with local language/framework conventions.

## How To Apply This Catalog

- Treat smell as review hypothesis, not verdict.
- Prefer smallest behavior-preserving refactor that removes risk.
- Do not churn stable code just to satisfy catalog name.
- Framework glue, generated code, DTOs, migrations, schemas, public API compatibility can justify shapes that smell in domain code.
- When language has first-class feature, prefer idiom over generic pattern.

## Bloaters

Code too large or primitive to change safely.

| Smell | Signal | Suggested refactor |
|---|---|---|
| **Long Function / Long Method** | More than one reason to change; hard to name or test directly | Extract Function; split by responsibility |
| **Long Parameter List** | More than 3-4 related parameters, especially repeated together | Introduce Parameter Object; Preserve Whole Object |
| **Large Class / God Object** | Many fields/methods, low cohesion, many unrelated callers | Extract Class; Extract Module/Package |
| **Primitive Obsession** | Raw strings, maps, tuples, numbers, or booleans represent domain concepts | Replace Primitive with Value Object/Enum/Newtype |
| **Data Clumps** | Same group of fields or params appears repeatedly | Group into a named type/object/struct |
| **Flag Argument** | Boolean or enum parameter switches behavior inside a function | Split Function; Replace Conditional with Strategy |

```text
# Smell: long parameter list + data clump
createEndpoint(name, region, cpu, memory, gpu, minScale, maxScale)

# Fix: parameter object with a domain name
createEndpoint(config)
```

## Object And Type Abusers

OO/typed/interface code using inheritance, types, or conditionals poorly.

| Smell | Signal | Suggested refactor |
|---|---|---|
| **Switch Statements / Type Codes** | Branching on `type`, `kind`, class name, or repeated `instanceof` checks | Replace Conditional with Polymorphism, Strategy, Dispatch Map, or Pattern Matching |
| **Refused Bequest** | Subclass ignores, disables, or overrides most inherited behavior | Replace Inheritance with Delegation; prefer composition |
| **Temporary Field** | Field only valid during one phase or code path | Extract Class; pass explicit local state |
| **Alternative Classes With Different Interfaces** | Two types do same job under different names | Unify interface; introduce adapter only at boundary |
| **Leaky Abstraction** | Caller must know internals to use abstraction correctly | Tighten interface; move behavior behind boundary |

```text
# Smell: repeated type switching
if shape.kind == "circle": area = circleArea(shape)
else if shape.kind == "square": area = squareArea(shape)

# Fix options
shape.area()                 # polymorphism
areaByKind[shape.kind](shape) # dispatch table
match shape { ... }           # pattern matching where idiomatic
```

## Change Preventers

One conceptual change forces too many edits or moves unrelated code together.

| Smell | Signal | Suggested refactor |
|---|---|---|
| **Divergent Change** | One unit changes for unrelated reasons | Split responsibilities into separate units |
| **Shotgun Surgery** | One conceptual change touches many files | Consolidate related behavior; introduce stable boundary |
| **Parallel Inheritance / Type Hierarchies** | Adding one type forces mirror type elsewhere | Collapse hierarchy; move behavior to source type |
| **Temporal Coupling** | Calls must happen in hidden order | Make invalid states unrepresentable; introduce lifecycle object |
| **Configuration Sprawl** | Same setting interpreted in many places | Centralize config parsing/validation |

## Dispensables

Things adding no current value.

| Smell | Signal | Suggested refactor |
|---|---|---|
| **Duplicate Code** | Same business rule or algorithm in two or more places | Extract Function/Module; create single source of truth |
| **Dead Code** | Unreachable or unused functions, variables, imports, branches | Remove Dead Code |
| **Speculative Generality** | Hooks, abstractions, interfaces, or generics built for imagined future | Inline/remove unused abstraction |
| **Comments As Compensation** | Comment explains what unclear code should express | Rename, extract, or restructure |
| **Lazy Class / Lazy Module** | Unit exists but does almost nothing | Inline Class/Module |
| **Anemic Domain Object** | Data holder has behavior scattered across services/helpers | Move behavior onto domain object unless deliberate DTO |

DTOs, records, structs, schemas, generated models, API payload objects are not automatically smells. Flag anemic object only when behavior clearly belongs with data and moving it reduces coupling.

```text
# Smell: comment compensating for unclear code
x = d * 0.85  # apply 15% discount

# Fix: names expose intent
discountRate = 0.15
discountedPrice = price * (1 - discountRate)
```

## Couplers

Too much knowledge/dependency between units.

| Smell | Signal | Suggested refactor |
|---|---|---|
| **Feature Envy** | Function uses another object/module's data more than its own | Move Function/Method to owner of data |
| **Inappropriate Intimacy** | Units reach into each other's internals | Encapsulate; expose intention-revealing methods |
| **Message Chains** | `a.b().c().d().e()` or equivalent nested property walking | Hide Delegate; ask for needed value directly |
| **Middle Man** | Unit only forwards calls without policy or translation | Remove Middle Man |
| **Global State** | Hidden dependencies make tests/order matter | Inject dependency; pass context explicitly |

```text
# Smell: caller knows the whole object graph
city = order.customer.address.city

# Fix: expose the concept the caller needs
city = order.shippingCity()
```

## Error And Boundary Smells

Often real defects. Weight higher than style concerns.

| Smell | Signal | Suggested refactor |
|---|---|---|
| **Swallowed Error** | Empty catch/except/rescue, ignored `Result`, ignored promise rejection | Catch specific errors; log/return/raise intentionally |
| **Broad Catch** | Catches every error type and handles same way | Catch specific exceptions/errors |
| **Mixed Error Strategy** | Same layer sometimes throws, returns null, returns error codes, and logs | Pick one strategy per boundary |
| **Inconsistent Return Shape** | Function returns collection, scalar, null, and error sentinel in normal flow | Normalize return type; use Option/Result/exception idiom |
| **String-Built Boundary** | SQL, shell command, path, URL, HTML, or regex assembled unsafely | Use structured API, escaping, parameterization, or builder |
| **Unvalidated Input Crossing Trust Boundary** | Request, file, CLI, DB, or external API data used as trusted | Validate/parse at boundary |

```text
# Smell: unsafe boundary string
query = "select * from users where id = " + userId

# Fix: use the database driver's parameter API
query("select * from users where id = ?", [userId])
```

## State And Control Flow Smells

| Smell | Signal | Suggested refactor |
|---|---|---|
| **Deep Nesting / Arrow Code** | More than about three indentation levels | Guard clauses; early returns; extract function |
| **Hidden Mutation** | Function name looks like query but changes state | Rename command or split query from mutation |
| **Shared Mutable Default / Static State** | Calls unexpectedly share data | Allocate per call/instance; make state explicit |
| **Boolean Blindness** | Call sites pass `true, false, true` with no meaning | Replace boolean flags with named options or separate methods |
| **Magic Literal** | Unexplained number/string controls behavior | Replace Magic Literal with constant, enum, or named concept |

```text
# Smell: deep nesting
if order exists:
  if order.isPaid:
    if order.hasItems:
      ship(order)

# Fix: guard clauses
if order is missing: return
if not order.isPaid: return
if not order.hasItems: return
ship(order)
```

## Language-Specific Traps

Check relevant language after general pass.

| Language | Common traps | Typical fix |
|---|---|---|
| **Python** | Mutable default args; bare `except`; `== None`; wildcard imports; manual index loops; mixed return types | `None` sentinel; catch specific exceptions; `is None`; explicit imports; `enumerate`; consistent return type |
| **JavaScript/TypeScript** | Unhandled promises; `any` sprawl; truthiness bugs; mutation of shared objects; optional/null confusion | `await`/catch; narrow types; explicit null checks; immutable updates; strict compiler settings |
| **C#** | Null-heavy APIs; overused inheritance; service classes with all behavior; exception-policy drift | Nullable annotations; composition; move behavior; consistent exception policy |
| **Go** | Ignored errors; package-level mutable state; huge interfaces; context not propagated | Always check errors; inject dependencies; define small consumer-side interfaces; pass `context.Context` |
| **Rust** | Excessive cloning; `unwrap`/`expect` outside tests/prototypes; fighting borrow checker with global state | Borrow intentionally; return `Result`; model ownership clearly |
| **Shell** | Unquoted variables; unchecked command failure; string-built paths/commands | Quote variables; `set -euo pipefail` where suitable; arrays/structured command args |

## Refactoring Selection

- **Extract Function** when block has name, separate responsibility, or testable decision.
- **Inline Function** when indirection hides trivial operation.
- **Extract Class/Module** when data + behavior form coherent concept.
- **Move Function/Method** when behavior mostly uses another unit's data.
- **Introduce Parameter Object** when related params travel together.
- **Replace Conditional With Strategy/Polymorphism/Dispatch** when branching repeats by type/mode.
- **Replace Primitive With Value Object/Enum/Newtype** when raw values carry domain rules.
- **Hide Delegate** when callers traverse internal object graphs.
- **Remove Dead Code** when only justification is future possibility.

## Canonical References

- Refactoring.Guru - Code Smells: https://refactoring.guru/refactoring/smells
- Martin Fowler - Catalog of Refactorings: https://refactoring.com/catalog/
- Martin Fowler - Refactoring: Improving the Design of Existing Code, 2nd Edition
