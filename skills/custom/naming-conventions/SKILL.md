---
name: naming-conventions
description: Provides language-agnostic naming guidelines for consistent, predictable names across a codebase. Use when creating, renaming, or reviewing functions, methods, classes, variables, files, API resources, CLI commands, or config keys in any language, especially when choosing verbs, resource nouns, qualifiers, prepositions, or case style.
---

# Naming Conventions

Apply these guidelines to names you write or review in any language. They are defaults to guide judgment, not rules to enforce mechanically.

## Priority Order

1. Match the surrounding codebase.
2. Match the language or framework idiom.
3. Use this skill's defaults when there is no stronger local pattern.
4. Flag meaningful inconsistencies instead of silently creating a third style.

## Core Principle

Prefer predictability over cleverness. A developer should be able to guess a name from sibling names and find related operations through autocomplete.

Before adding or changing a name, scan nearby code for the established pattern. Do not mix two names for the same concept, such as `fetchUser`, `retrieveUser`, and `getUser`, unless the codebase already makes a real semantic distinction.

## Case Style

Case is language-dependent. Do not impose one language's style on another.

| Language / Ecosystem | Functions / Methods | Variables | Types / Classes |
|---|---|---|---|
| Python, Ruby, Rust | `snake_case` | `snake_case` | `PascalCase` |
| JS/TS, Java, Kotlin, Swift | `camelCase` | `camelCase` | `PascalCase` |
| C# | `PascalCase` methods/properties | `camelCase` locals/params | `PascalCase` |
| Go | `camelCase` unexported, `PascalCase` exported | same | same |

Constants, files, modules, packages, and private/internal names vary more by ecosystem. Follow the existing file first; see [REFERENCE.md](REFERENCE.md) for common defaults.

## Verb Selection

Functions and methods that do something should use a clear conventional verb. Treat these as a palette, not a whitelist.

| Verb | Meaning |
|---|---|
| `get` | Retrieve one item or property |
| `list` | Retrieve multiple items |
| `create` | Create a resource |
| `update` | Modify a resource |
| `delete` | Remove a resource |
| `set` | Assign a property/value |
| `deploy` | Perform deployment side effects |
| `build` | Construct an object without I/O side effects |

Common non-CRUD verbs: `is`, `has`, `can`, `should`, `validate`, `parse`, `format`, `render`, `serialize`, `deserialize`, `compute`, `calculate`, `handle`, `ensure`, `find`, `apply`, `process`, `run`, `execute`.

Prefer one verb per concept. If the codebase uses `get`, do not introduce `fetch`, `retrieve`, or `grab` for the same operation.

## Resource And API Names

- Use one resource noun per concept: `endpoint`, not both `endpoint` and `serving_endpoint`.
- Use singular names for one thing and plural names for collections.
- Order from general to specific so related names group together: `modelVersion`, `modelVersionStatus`, `modelVersionTag`.
- Mirror code and API names where practical: `listModelVersions()` maps cleanly to `GET /models/{id}/versions`.
- Keep nesting shallow and predictable in paths, method names, and command names.

## Qualifiers

- Use `config`, `status`, `payload`, and `latest` consistently when those concepts exist.
- Use singular names for one value and plural names for collections.
- Use `tag` for one tag and `tags` for a collection. Example: `setTag(modelId, tag)` sets one; `setTags(modelId, tags)` replaces many; `addTag(modelId, tag)` adds one.

## Prepositions

Prefer names without prepositions when parameters make the relation obvious.

- Use `by` for lookup, filtering, or sorting by a property: `listEndpointsByStatus(status)`.
- Use `to` for conversion: `modelToDict(model)`, `configToPayload(config)`.
- Use `for` for association, scope, audience, or ownership: `listPermissionsForUser(userId)`.

Translate the casing to the language: `list_endpoints_by_status`, `listEndpointsByStatus`, `ListEndpointsByStatus`.

## Quick Checklist

1. Does the name match nearby code for the same concept?
2. Is the case idiomatic for the language and file?
3. Does the verb accurately describe the behavior?
4. Does cardinality match the name (`get`/`list`, singular/plural, `tag`/`tags`)?
5. Is the resource noun consistent across code, APIs, and commands?
6. Are qualifiers standard and ordered from general to specific?
7. Can the preposition be dropped? If not, is it `by`, `to`, or `for` with the right meaning?
8. Would autocomplete group related names together?

## Examples

```text
getModel(modelId) / get_model(model_id)
listEndpoints() / list_endpoints()
isValid(config) / is_valid(config)
parseConfig(raw) / parse_config(raw)
renderTemplate(context) / render_template(context)
endpointStatusToLabel(status) / endpoint_status_to_label(status)
```
