# Code Elegance Application Guide

Use these prompts while editing or reviewing code in any language. Examples use pseudocode only to communicate the shape of the refactor; translate to the target language's idioms.

## Quick Scan

Ask these questions in order:

1. What is the main path, and is it visually obvious?
2. Which variables change value, and can any become derived values?
3. Which conditions are really validation or boundary checks?
4. Which literals, booleans, or comments hide domain language?
5. Which branch exists only to choose a handler, strategy, or data value?
6. Which loops manually implement filtering, mapping, existence checks, or first-match lookup?
7. Which expensive work happens before it is definitely needed?

## Refactor Recipes

### Flatten Nested Flow

Use when nested conditionals make the happy path hard to see.

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

Do not flatten if each nested level represents meaningful structure that would be less clear as independent guards.

### Replace Flag Variables

Use the language's existence, universal, first-match, or direct-return helper when a loop only tracks whether something happened.

```text
has_expired_item = items contains any item where item is expired
first_admin = first user where user is admin, or none
```

Keep the loop when it has side effects, multiple outputs, or needs careful step-by-step names.

### Name Business Rules

Extract names for domain concepts, not mechanics.

```text
minimum_balance = order.total + transaction_fee
has_sufficient_funds = account.balance >= minimum_balance
```

Avoid names like `is_valid_condition` or `calculated_value`; those add noise without meaning.

### Centralize Mode-Based Behavior

Use a dispatch table/map, pattern match, enum method, or strategy object when branches only select a handler.

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

Keep an `if`/`elif` chain when each case has unique control flow, multiple statements, or important inline context.

### Convert Raw Input At Boundaries

Prefer parsing into a typed or validated value once. Use a value object, newtype, branded type, record, struct, class, or factory according to the language.

```text
type EmailAddress:
    value

    parse(raw):
        if raw does not contain "@":
            raise invalid email error
        return EmailAddress(normalized raw)
```

Do not add a domain type for throwaway internal values with no invariant.

### Separate Commands From Queries

Avoid methods that both answer a question and mutate state unless the convention is explicit.

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

Do not make everything lazy. Eager failure is often better for required dependencies.

## Review Comment Template

```text
Location: path/to/file.ext:42
Friction: nested validation hides the main behavior.
Pattern: Guard clauses / fail fast.
Fix: return early for missing user, inactive account, and empty payload, then leave the main path unindented.
Trade-off: preserves behavior and lowers branch depth without adding a new abstraction.
```

## Skip Conditions

Skip the refactor when:

- The code is generated or intentionally mirrors an external schema.
- The local style is different but consistent.
- The "elegant" version would require readers to know an uncommon abstraction.
- Tests are missing and the behavior is subtle enough that a cleanup could hide a regression.
- The pattern solves a theoretical issue but the current code is simple and stable.

## Coordination With Other Skills

- Use `code-smells` first when the task is review-heavy and you need to identify risks.
- Use `naming-conventions` when most of the improvement depends on choosing better names.
- Use `code-elegance` when the desired output is an implemented refactor or a ranked set of concrete cleanup moves.
