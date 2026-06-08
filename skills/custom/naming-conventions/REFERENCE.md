# Naming Conventions Reference

Use this reference when [SKILL.md](SKILL.md) is not enough to choose a name.

## Case Style Details

Case conventions vary by language, framework, and team. The surrounding file wins.

| Ecosystem | Common Defaults |
|---|---|
| Python | `snake_case` functions, methods, variables, modules; `UPPER_SNAKE_CASE` constants; `PascalCase` classes; `_leading_underscore` private/internal names. |
| Ruby | `snake_case` methods and variables; `SCREAMING_SNAKE_CASE` constants; `PascalCase` classes/modules. |
| Rust | `snake_case` functions, variables, modules; `SCREAMING_SNAKE_CASE` constants/statics; `PascalCase` types/traits; `snake_case` crate names. |
| JavaScript / TypeScript | `camelCase` functions and variables; `PascalCase` classes/types/components; constants vary between `UPPER_SNAKE_CASE` and `camelCase` `const`; files vary by project. |
| Java | `camelCase` methods, fields, locals; `UPPER_SNAKE_CASE` constants; `PascalCase` classes/interfaces. |
| C# | `PascalCase` public methods, properties, types; `camelCase` locals/params; private fields vary (`_camelCase` is common). |
| Go | `MixedCaps`; exported identifiers start uppercase, unexported identifiers start lowercase; avoid underscores in identifiers. |
| Kotlin / Swift | `camelCase` functions and variables; `PascalCase` types; constants follow project/platform norms. |
| Shell | Commands/functions often `snake_case` or `kebab-case`; variables commonly `UPPER_SNAKE_CASE` for exported/env values and lowercase for locals. |
| Config / data files | Preserve the tool's schema style exactly; do not rename keys to satisfy code naming preferences. |

Acronyms should follow local convention: `httpClient`, `HttpClient`, `HTTPClient`, or `http_client`. Pick one style per codebase area and stay consistent.

## Verb Guide

Use the verb that most accurately describes behavior. Do not invent near-synonyms for an established concept.

### CRUD / Resource Verbs

| Verb | Use For | Notes |
|---|---|---|
| `get` | Retrieve one expected item or property | Decide repo-wide whether missing values raise, return null/None, or return an optional/result type. |
| `list` | Retrieve multiple items | Prefer over `getAll`. |
| `create` | Create a new resource | Should not merely assign a property. |
| `update` | Modify an existing resource | Usually implies persistence or external state. |
| `delete` | Remove a resource | Prefer over mixing `remove`, `destroy`, and `delete` without semantic distinction. |
| `set` | Assign a value to an existing property/object | Use cardinality accurately: `setTag` vs `setTags`. |
| `deploy` | Perform deployment side effects | Do not use for building deployment config. |
| `build` | Construct and return an object | Should be side-effect free. |

### Non-CRUD Verbs

| Verb | Use For | Examples |
|---|---|---|
| `is`, `has`, `can`, `should` | Boolean predicates | `isReady`, `hasAccess`, `canRetry`, `shouldRefresh` |
| `validate` | Check correctness | `validateConfig`, `validatePayload` |
| `parse` | Raw input to structured data | `parseConfig`, `parseModelUri` |
| `format`, `render` | Structured data to text/markup/output | `formatStatus`, `renderTemplate` |
| `serialize`, `deserialize` | Wire/storage conversion | `serializeConfig`, `deserializePayload` |
| `compute`, `calculate` | Derive a value | `computeScore`, `calculateTotal` |
| `handle`, `on` | Event handling/callbacks | `handleClick`, `onMessage` |
| `ensure` | Idempotently make a condition true | `ensureWorkspaceExists` |
| `find` | Search that may return nothing | `findUserByEmail` |
| `apply`, `process`, `run`, `execute` | Perform a broad operation | Prefer a more specific verb when one exists. |

## Resource And API Naming

These conventions apply to code identifiers, REST paths, RPC methods, GraphQL fields, CLI commands, and other API surfaces.

- Pick one resource noun per concept and reuse it everywhere.
- Use singular for one resource and plural for collections.
- Prefer general-to-specific order: `model_version_status`, `modelVersionStatus`, `ModelVersionStatus`.
- Mirror code and API names when practical.
- Keep nesting shallow and predictable.

```text
# Code                              # Equivalent API
getEndpoint(id)                     GET    /endpoints/{id}
listEndpoints()                     GET    /endpoints
createEndpoint(config)              POST   /endpoints
updateEndpoint(id, config)          PUT    /endpoints/{id}
deleteModelVersion(id, version)     DELETE /models/{id}/versions/{version}
listModelVersions(id)               GET    /models/{id}/versions
```

## Qualifier Naming

Use qualifiers based on concept and cardinality.

| Qualifier | Meaning | Cardinality |
|---|---|---|
| `config` | Configuration object | singular |
| `status` | Status value | singular |
| `payload` | API request or response body | singular |
| `latest` | Most recent version | n/a |
| `tag` | One tag | singular |
| `tags` | Tag collection | plural |

```text
getStatus(endpointId)
buildPayload(config)
getLatestModelVersion(id)
setTag(modelId, tag)
setTags(modelId, tags)
addTag(modelId, tag)
```

## Preposition Semantics

Prefer no preposition when the argument is obvious: `getModel(modelId)`, not `getModelWithId(modelId)`.

| Preposition | Use For | Examples |
|---|---|---|
| `by` | Lookup, filtering, or sorting by a property value | `listOrdersByStatus`, `getModelVersionByTag`, `sortByCreatedAt` |
| `to` | Transformation or conversion | `configToPayload`, `modelToDict`, `celsiusToFahrenheit` |
| `for` | Association, scope, audience, ownership, or belonging | `getConfigForEndpoint`, `listPermissionsForUser` |

`by` vs `for`:

- `by` answers "which items match this property value?"
- `for` answers "what belongs to, is scoped to, or is intended for this entity?"
- Use `by` for `listOrdersByStatus("paid")`.
- Use `for` for `listOrdersForCustomer(customerId)`.

## Review Notes

- These guidelines should inform review comments, not create churn for harmless existing names.
- Favor clarity and local consistency over strict conformance.
- Flag intentional deviations instead of silently renaming public APIs or persisted schema keys.
- Be careful with generated code, external schemas, public API compatibility, database columns, and config keys; renaming may be a breaking change.
