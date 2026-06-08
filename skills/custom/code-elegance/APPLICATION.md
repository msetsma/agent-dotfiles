# Code Elegance Application Guide

Use prompts while editing/reviewing code in any language. Examples use pseudocode only to show refactor shape; translate to target language idioms.

## Quick Scan

Ask in order:

1. What is main path, and is it visually obvious?
2. Which variables change value, and can any become derived values?
3. Which conditions are validation or boundary checks?
4. Which literals, booleans, or comments hide domain language?
5. Which branch only chooses handler, strategy, or data value?
6. Which loops manually implement filtering, mapping, existence checks, or first-match lookup?
7. Which expensive work happens before definitely needed?

## Refactor Recipes

### Flatten Nested Flow

Use when nested conditionals hide happy path.

```text
function ship(order):
    if order is missing:
        return no shipment
    if order is not paid:
        return no shipment
    if order has no items:
        return no shipment

    return create shipment for order
```

Do not flatten if each nested level represents meaningful structure clearer as nesting than independent guards.

### Replace Flag Variables

Use language's existence, universal, first-match, or direct-return helper when loop only tracks whether something happened.

```text
has_expired_item = items contains any item where item is expired
first_admin = first user where user is admin, or none
```

Keep loop when it has side effects, multiple outputs, or needs careful step-by-step names.

### Name Business Rules

Extract names for domain concepts, not mechanics.

```text
minimum_balance = order.total + transaction_fee
has_sufficient_funds = account.balance >= minimum_balance
```

Avoid names like `is_valid_condition` or `calculated_value`; they add noise without meaning.

### Centralize Mode-Based Behavior

Use dispatch table/map, pattern match, enum method, or strategy object when branches only select handler.

```text
handlers = {
    create: create_user,
    update: update_user,
    delete: delete_user,
}

handler = handlers.get(command)
if handler is missing:
    raise unknown command error
return handler(payload)
```

Keep `if`/`elif` chain when each case has unique control flow, multiple statements, or important inline context.

### Convert Raw Input At Boundaries

Prefer parsing into typed/validated value once. Use value object, newtype, branded type, record, struct, class, or factory by language.

```text
type EmailAddress:
    value

    parse(raw):
        if raw does not contain "@":
            raise invalid email error
        return EmailAddress(normalized raw)
```

Do not add domain type for throwaway internal values with no invariant.

### Separate Commands From Queries

Avoid methods that both answer question and mutate state unless convention is explicit.

```text
if cart.can_apply(discount):
    cart.apply(discount)
```

This is clearer than `cart.apply_if_valid(discount)` when callers need to reason about eligibility separately.

### Defer Expensive Work

Use lazy initialization for optional expensive dependencies.

```text
type Report:
    source
    cached_rows = none

    rows():
        if cached_rows is empty:
            cached_rows = load_rows(source)
        return cached_rows
```

Do not make everything lazy. Eager failure often better for required dependencies.

## Review Comment Template

```text
Location: path/to/file.ext:42
Friction: nested validation hides the main behavior.
Pattern: Guard clauses / fail fast.
Fix: return early for missing user, inactive account, and empty payload, then leave the main path unindented.
Trade-off: preserves behavior and lowers branch depth without adding a new abstraction.
```

## Skip Conditions

Skip refactor when:

- Code is generated or intentionally mirrors external schema.
- Local style differs but is consistent.
- "Elegant" version requires uncommon abstraction knowledge.
- Tests missing and behavior subtle enough that cleanup could hide regression.
- Pattern solves theoretical issue but current code is simple and stable.

## Coordination With Other Skills

- Use `code-smells` first when task is review-heavy and risks need identification.
- Use `naming-conventions` when improvement depends mostly on better names.
- Use `code-elegance` when desired output is implemented refactor or ranked cleanup moves.
