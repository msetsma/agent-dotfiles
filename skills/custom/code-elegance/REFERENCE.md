# Code Elegance Pattern Reference

Agent-facing catalog distilled from `raw-dump/`. Use as selection guide, not checklist to force onto every change. Source notes are Python-heavy; translate patterns into target language idioms.

## Language Translation Rule

Apply principle, not source-note syntax:

| Principle | Generic shape | Common equivalents |
|---|---|---|
| Guard invalid cases first | Early exit before main work | Guard clauses, early returns, explicit error returns, early throws |
| Encode alternatives explicitly | One named representation per case | Enums, tagged unions, pattern matching, dispatch maps, `case` in shell |
| Represent absence explicitly | Distinguish missing from present-but-empty | `Option`/`Maybe`, nullable types, sentinel values, explicit error return |
| Transform collections directly | Name operation instead of hand-rolling loop | `map`/`filter`, comprehensions, iterators, array methods, shell loops when clearer than pipelines |
| Protect resource lifetimes | Pair setup and teardown structurally | `defer`, `try/finally`, RAII, context managers, Bash `trap` cleanup |
| Make illegal states hard to build | Validate at construction or boundaries | constructors/factories, value objects, schemas, argument parsing and validation |

## Bash Exception

Bash benefits from early exits, named constants, `case` dispatch, focused functions, cleanup traps. It should not imitate app-code abstractions. For shell, prefer:

- quote expansions unless word splitting intentional
- use arrays for lists instead of space-delimited strings
- validate required commands, files, args up front
- use `case` for command dispatch
- keep pipelines simple enough to debug
- move complex parsing, nested data, or business rules out of Bash

## Control Flow

| Pattern | Use when | Avoid when |
|---|---|---|
| **Early Return / Guard Clause** | Preconditions, invalid states, or edge cases obscure main path | Function tiny and branch already clear |
| **Fail Fast** | Bad input should stop work before side effects | Partial success or best-effort behavior intended |
| **Flatten Arrow** | Nested `if` blocks push happy path several levels deep | Nesting models real hierarchy more clearly than guards |
| **Short-Circuiting** | Expensive/unsafe checks should only run when needed | Valid falsey/nullish values need explicit handling |
| **Dispatch Table / Map** | Branch maps keys/types/commands to handlers | Each branch has unrelated setup or bespoke logic |
| **Strategy / Polymorphism** | Same operation varies by type, provider, or mode | Only two simple cases and no growth pressure |

Default move: guard clauses first. Reach for dispatch/polymorphism only after branch table stable enough to name.

## State And Data

| Pattern | Use when | Avoid when |
|---|---|---|
| **Single Assignment** | Variable repeatedly reassigned while derived | Small loop accumulator is clearest |
| **Immutable-First Design** | Shared mutable data creates aliasing/order bugs | Mutation local, isolated, much simpler |
| **Stateless Transformation** | Function mutates inputs, globals, or caches unnecessarily | API intentionally stateful |
| **Temporal Coupling Elimination** | Calls must happen in hidden order to work | Order explicit and framework-enforced |
| **Command-Query Separation** | Method/function both mutates and returns data | Language/framework convention combines them intentionally |
| **Parameter Object** | Same parameter group travels together | Function has few obvious parameters |
| **Preserve Whole Object** | Callers pass many fields from same object | Passing object creates unwanted coupling |

Default move: make data flow visible. Prefer returning new values or named domain objects over mutating inputs across long span.

## Clarity And Simplification

| Pattern | Use when | Avoid when |
|---|---|---|
| **Intention-Revealing Names** | Comments explain what name should say | Local convention uses known short name like `i`, `x`, or `ctx` |
| **Extract Variable** | Complex expression hides meaning or repeats | Extracted name only restates code |
| **Inline Variable** | Temporary adds no meaning and increases scan cost | Name explains business rule or non-obvious calculation |
| **Replace Magic Literal** | Number/string carries domain meaning | Literal is universal convention like `0`, `1`, or `404` in HTTP code |
| **Replace Comment With Function** | Comment describes code block | Comment explains why, not what |
| **Consistent Abstraction Level** | Function mixes business intent with low-level mechanics | Split forces jumps through trivial wrappers |
| **Remove Dead Code** | Code unused, unreachable, commented out, or speculative | Compatibility or migration windows require keeping it |
| **Consolidate Duplicate Fragments** | Branches repeat setup, teardown, or assignment | Extraction blurs meaningful differences |

Default move: name concept. If naming is hard, code may mix responsibilities.

## Validation And Errors

| Pattern | Use when | Avoid when |
|---|---|---|
| **Validation Guard** | Invalid input should return/raise before work starts | Validation depends on later derived data |
| **Parse, Don't Validate** | Raw input can convert once into safe typed value | Input already trusted/internal |
| **Make Invalid States Unrepresentable** | Repeated checks enforce invariant | Type/model overhead exceeds risk |
| **Result / Error Value** | Failure expected and normal control flow | Exceptions are local idiom and failures exceptional |
| **Sentinel Object** | Usual absent value is also valid data | Language's normal null/none/optional/default value unambiguous |
| **Error Aggregation** | Users need all validation errors at once | Fail-fast safer/simpler |
| **Structured Resource Safety** | Setup and teardown must stay paired | No resource lifetime to protect |
| **Supervisor Pattern** | Independent tasks should isolate/report failures | Failure should cancel whole operation immediately |

Default move: validate at boundaries, convert raw values into stronger shapes, keep error paths explicit.

## Loops And Collections

| Pattern | Use when | Avoid when |
|---|---|---|
| **Collection Transform** | Transforming/filtering collection in one readable step | Expression needs side effects, multiple branches, or complex naming |
| **Lazy Iterator / Stream** | Data large, streaming, or partially consumed | Collection small and reused many times |
| **Existence / Universal Check** | Collection check can short-circuit | Need details about which item failed |
| **First Match Lookup** | Need first matching item | Need all matches or meaningful errors |
| **Indexed / Parallel Iteration** | Index or parallel iteration needed | Index arithmetic central to algorithm |
| **Batching / Chunking** | External calls or memory use improve with batches | Batching changes ordering or transactional semantics |

Default move: replace manual index loops and flag variables with direct iteration, existence checks, universal checks, or first-match helpers when it reveals intent.

## Functional And Expression Patterns

| Pattern | Use when | Avoid when |
|---|---|---|
| **Boolean Expression Return** | Code returns `True`/`False` from direct condition | Intermediate names needed for readability |
| **Ternary Expression** | Condition and both outcomes simple | Either branch contains non-trivial logic |
| **Function Composition** | Pipeline of pure transformations already natural | Debugging intermediate values matters more |
| **Partial Application** | Reusing configured function removes repetition | Hides important args from call site |
| **Memoization** | Pure expensive function repeats inputs | Results depend on time, I/O, or mutable args |
| **Lazy Evaluation** | Work may not be needed or data huge | Eager eval simple and cheap |

Default move: use expression style only when it improves scanning. Do not chase clever density.

## Performance-Aware Patterns

| Pattern | Use when | Avoid when |
|---|---|---|
| **Lazy Initialization** | Construction eagerly performs expensive work that may not be used | Init cost small or failure should happen early |
| **Caching / Memoization** | Repeated pure work measurable or plausibly expensive | Cache invalidation, memory growth, or stale data unclear |
| **Copy-on-Write** | Large shared data copied often but rarely mutated | Plain copying cheap and clearer |
| **Batch Processing** | External calls or I/O dominate cost | Batching weakens error isolation or ordering |
| **Prefetching** | Access patterns predictable | May fetch unused data or complicate correctness |
| **Object Pool / Flyweight** | Allocation/memory pressure measured and significant | Ordinary object creation fine; rarely first fix |

Default move: measure when possible. Prefer algorithmic clarity, laziness, batching before specialized memory patterns.

## Advanced Patterns To Treat Skeptically

- **Point-free / tacit style**: often removes useful names.
- **Trampolining**: only for recursion-depth problems that cannot be rewritten clearly.
- **Monadic error handling**: useful in codebases already using Result/Option abstractions; noisy otherwise.
- **Fluent builders**: useful for complex config; overkill for simple constructors.
- **Object pools and flyweights**: optimization tools, not cleanup tools.
