# Code Elegance Pattern Reference

This is the agent-facing catalog distilled from `raw-dump/`. Use it as a selection guide, not a checklist to force onto every change. The source notes are Python-heavy, but these patterns should be translated into the target language's idioms.

## Language Translation Rule

Apply the principle, not the source-note syntax:

| Principle | Generic shape | Common equivalents |
|---|---|---|
| Guard invalid cases first | Early exit before main work | Guard clauses, early returns, explicit error returns, early throws |
| Encode alternatives explicitly | One named representation per case | Enums, tagged unions, pattern matching, dispatch maps, `case` in shell |
| Represent absence explicitly | Distinguish missing from present-but-empty | `Option`/`Maybe`, nullable types, sentinel values, explicit error return |
| Transform collections directly | Name the operation instead of hand-rolling the loop | `map`/`filter`, comprehensions, iterators, array methods, shell loops when clearer than pipelines |
| Protect resource lifetimes | Pair setup and teardown structurally | `defer`, `try/finally`, RAII, context managers, Bash `trap` cleanup |
| Make illegal states hard to build | Validate at construction or boundaries | constructors/factories, value objects, schemas, argument parsing and validation |

## Bash Exception

Bash can benefit from early exits, named constants, dispatch with `case`, focused functions, and cleanup traps. It should not imitate application-code abstractions. For shell, prefer:

- quote expansions unless word splitting is intentional
- use arrays for lists instead of space-delimited strings
- validate required commands, files, and arguments up front
- use `case` for command dispatch
- keep pipelines simple enough to debug
- move complex parsing, nested data, or business rules out of Bash

## Control Flow

| Pattern | Use when | Avoid when |
|---|---|---|
| **Early Return / Guard Clause** | Preconditions, invalid states, or edge cases obscure the main path | The function is tiny and the branch is already clear |
| **Fail Fast** | Bad input should stop work before side effects happen | Partial success or best-effort behavior is intended |
| **Flatten Arrow** | Nested `if` blocks push the happy path several levels deep | The nesting models a real hierarchy more clearly than guards |
| **Short-Circuiting** | Expensive or unsafe checks should only run when needed | Valid falsey/nullish values need explicit handling |
| **Dispatch Table / Map** | A branch maps keys/types/commands to handlers | Each branch has unrelated setup or heavy bespoke logic |
| **Strategy / Polymorphism** | The same operation varies by type, provider, or mode | There are only two simple cases and no growth pressure |

Default move: use guard clauses first. Reach for dispatch or polymorphism only after the branch table is stable enough to name.

## State And Data

| Pattern | Use when | Avoid when |
|---|---|---|
| **Single Assignment** | A variable is repeatedly reassigned while being derived | A small loop accumulator is the clearest shape |
| **Immutable-First Design** | Shared mutable data creates aliasing or ordering bugs | Mutation is local, isolated, and much simpler |
| **Stateless Transformation** | A function mutates inputs, globals, or caches unnecessarily | The API is intentionally stateful |
| **Temporal Coupling Elimination** | Calls must happen in a hidden order to work | The order is explicit and enforced by the framework |
| **Command-Query Separation** | A method/function both mutates and returns data | The language/framework convention intentionally combines them |
| **Parameter Object** | The same parameter group travels together | The function has only a few obvious parameters |
| **Preserve Whole Object** | Callers pass many fields from the same object | Passing the object would create unwanted coupling |

Default move: make data flow visible. Prefer returning new values or named domain objects over mutating inputs across a long span.

## Clarity And Simplification

| Pattern | Use when | Avoid when |
|---|---|---|
| **Intention-Revealing Names** | Comments explain what a name should have said | The local convention uses a well-known short name like `i`, `x`, or `ctx` |
| **Extract Variable** | A complex expression hides meaning or repeats | The extracted name just restates the code |
| **Inline Variable** | A temporary adds no meaning and increases scanning cost | The name explains a business rule or non-obvious calculation |
| **Replace Magic Literal** | A number/string carries domain meaning | The literal is a universal convention like `0`, `1`, or `404` in HTTP code |
| **Replace Comment With Function** | A comment describes a block of code | The comment explains why, not what |
| **Consistent Abstraction Level** | A function mixes business intent with low-level mechanics | Splitting would force readers to jump through trivial wrappers |
| **Remove Dead Code** | Code is unused, unreachable, commented out, or speculative | Compatibility or migration windows require keeping it |
| **Consolidate Duplicate Fragments** | Branches repeat setup, teardown, or assignment | Extracting would blur meaningful differences |

Default move: name the concept. If naming is hard, the code may be mixing responsibilities.

## Validation And Errors

| Pattern | Use when | Avoid when |
|---|---|---|
| **Validation Guard** | Invalid input should return or raise before work starts | Validation depends on later derived data |
| **Parse, Don't Validate** | Raw input can be converted once into a safe typed value | The input is already trusted/internal |
| **Make Invalid States Unrepresentable** | Repeated checks enforce an invariant | The type/model overhead exceeds the risk |
| **Result / Error Value** | Failure is expected and part of normal control flow | Exceptions are the local idiom and failures are exceptional |
| **Sentinel Object** | The usual absent value is also valid data | The language's normal null/none/optional/default value is unambiguous |
| **Error Aggregation** | Users need all validation errors at once | Fail-fast is safer or simpler |
| **Structured Resource Safety** | Setup and teardown must stay paired | There is no resource lifetime to protect |
| **Supervisor Pattern** | Independent tasks should isolate and report failures | A failure should cancel the whole operation immediately |

Default move: validate at boundaries, convert raw values into stronger shapes, and keep error paths explicit.

## Loops And Collections

| Pattern | Use when | Avoid when |
|---|---|---|
| **Collection Transform** | Transforming or filtering a collection in one readable step | The expression needs side effects, multiple branches, or complex naming |
| **Lazy Iterator / Stream** | Data is large, streaming, or partially consumed | The collection is small and reused multiple times |
| **Existence / Universal Check** | A collection check can short-circuit | You need details about which item failed |
| **First Match Lookup** | You need the first matching item | You need all matches or meaningful errors |
| **Indexed / Parallel Iteration** | Index or parallel iteration is needed | Index arithmetic is central to the algorithm |
| **Batching / Chunking** | External calls or memory use improve with batches | Batching changes ordering or transactional semantics |

Default move: replace manual index loops and flag variables with direct iteration, existence checks, universal checks, or first-match helpers when that reveals intent.

## Functional And Expression Patterns

| Pattern | Use when | Avoid when |
|---|---|---|
| **Boolean Expression Return** | Code returns `True`/`False` from a direct condition | Intermediate names are needed for readability |
| **Ternary Expression** | The condition and both outcomes are simple | Either branch contains non-trivial logic |
| **Function Composition** | A pipeline of pure transformations is already natural | Debugging intermediate values matters more |
| **Partial Application** | Reusing a configured function removes repetition | It hides important arguments from the call site |
| **Memoization** | A pure expensive function repeats inputs | Results depend on time, I/O, or mutable arguments |
| **Lazy Evaluation** | Work may not be needed or data may be huge | Eager evaluation is simpler and cheap |

Default move: use expression style only when it improves scanning. Do not chase clever density.

## Performance-Aware Patterns

| Pattern | Use when | Avoid when |
|---|---|---|
| **Lazy Initialization** | Construction eagerly performs expensive work that may not be used | Initialization cost is small or failure should happen early |
| **Caching / Memoization** | Repeated pure work is measurable or plausibly expensive | Cache invalidation, memory growth, or stale data is unclear |
| **Copy-on-Write** | Large shared data is copied often but rarely mutated | Plain copying is cheap and clearer |
| **Batch Processing** | External calls or I/O dominate cost | Batching weakens error isolation or ordering |
| **Prefetching** | Access patterns are predictable | It may fetch unused data or complicate correctness |
| **Object Pool / Flyweight** | Allocation/memory pressure is measured and significant | Ordinary object creation is fine; this is rarely the first fix |

Default move: measure when possible. Prefer algorithmic clarity, laziness, and batching before specialized memory patterns.

## Advanced Patterns To Treat Skeptically

- **Point-free / tacit style**: often removes useful names.
- **Trampolining**: only for recursion-depth problems that cannot be rewritten clearly.
- **Monadic error handling**: useful in codebases that already use Result/Option abstractions; noisy otherwise.
- **Fluent builders**: useful for complex configuration; overkill for simple constructors.
- **Object pools and flyweights**: optimization tools, not cleanup tools.
