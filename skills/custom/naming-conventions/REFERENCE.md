# Naming Conventions Reference

Use when [SKILL.md](SKILL.md) is too short to choose a name.

## Case Style Details

Case varies by language, framework, team. Surrounding file wins.

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
| Config / data files | Preserve tool schema style exactly; do not rename keys to satisfy code naming prefs. |

Acronyms follow local convention: `httpClient`, `HttpClient`, `HTTPClient`, or `http_client`. Pick one style per codebase area; stay consistent.

## Verb Guide

Use verb that best matches behavior. Do not invent near-synonyms for established concept.

### CRUD / Resource Verbs

| Verb | Use For | Notes |
|---|---|---|
| `get` | Retrieve one expected item/property | Decide repo-wide whether missing values raise, return null/None, or return optional/result type. |
| `list` | Retrieve multiple items | Prefer over `getAll`. |
| `create` | Create new resource | Should not merely assign property. |
| `update` | Modify existing resource | Usually implies persistence/external state. |
| `delete` | Remove resource | Prefer over mixing `remove`, `destroy`, and `delete` without semantic distinction. |
| `set` | Assign value to existing property/object | Cardinality matters: `setTag` vs `setTags`. |
| `deploy` | Perform deployment side effects | Do not use for building deployment config. |
| `build` | Construct and return object | Should be side-effect free. |

### Non-CRUD Verbs

| Verb | Use For | Examples |
|---|---|---|
| `is`, `has`, `can`, `should` | Boolean predicates | `isReady`, `hasAccess`, `canRetry`, `shouldRefresh` |
| `validate` | Check correctness | `validateConfig`, `validatePayload` |
| `parse` | Raw input to structured data | `parseConfig`, `parseModelUri` |
| `format`, `render` | Structured data to text/markup/output | `formatStatus`, `renderTemplate` |
| `serialize`, `deserialize` | Wire/storage conversion | `serializeConfig`, `deserializePayload` |
| `compute`, `calculate` | Derive value | `computeScore`, `calculateTotal` |
| `handle`, `on` | Event handlers/callbacks | `handleClick`, `onMessage` |
| `ensure` | Idempotently make condition true | `ensureWorkspaceExists` |
| `find` | Search that may return nothing | `findUserByEmail` |
| `apply`, `process`, `run`, `execute` | Broad operation | Prefer more specific verb when available. |

## Resource And API Naming

Apply to code identifiers, REST paths, RPC methods, GraphQL fields, CLI commands, and API surfaces.

- Pick one resource noun per concept; reuse everywhere.
- Singular for one resource; plural for collections.
- Prefer general-to-specific order: `model_version_status`, `modelVersionStatus`, `ModelVersionStatus`.
- Mirror code/API names when practical.
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

Use qualifiers by concept and cardinality.

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

Prefer no preposition when argument is obvious: `getModel(modelId)`, not `getModelWithId(modelId)`.

| Preposition | Use For | Examples |
|---|---|---|
| `by` | Lookup, filtering, or sorting by property value | `listOrdersByStatus`, `getModelVersionByTag`, `sortByCreatedAt` |
| `to` | Transformation/conversion | `configToPayload`, `modelToDict`, `celsiusToFahrenheit` |
| `for` | Association, scope, audience, ownership, belonging | `getConfigForEndpoint`, `listPermissionsForUser` |

`by` vs `for`:

- `by` answers "which items match this property value?"
- `for` answers "what belongs to, is scoped to, or is intended for this entity?"
- Use `by` for `listOrdersByStatus("paid")`.
- Use `for` for `listOrdersForCustomer(customerId)`.

## Review Notes

- Guidelines inform review comments; they should not create churn for harmless existing names.
- Favor clarity and local consistency over strict conformance.
- Flag intentional deviations instead of silently renaming public APIs or persisted schema keys.
- Take care with generated code, external schemas, public API compatibility, database columns, config keys; renaming may break users/data.
