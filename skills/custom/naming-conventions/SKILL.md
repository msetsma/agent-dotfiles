---
name: naming-conventions
description: Provides language-agnostic naming guidelines for consistent, predictable names across a codebase. Use when creating, renaming, or reviewing functions, methods, classes, variables, files, API resources, CLI commands, or config keys in any language, especially when choosing verbs, resource nouns, qualifiers, prepositions, or case style.
---

# Naming Conventions

Apply when writing/reviewing names in any language. Defaults guide judgment; not mechanical rules.

## Priority Order

1. Match surrounding codebase.
2. Match language/framework idiom.
3. Use this skill's defaults if no stronger local pattern.
4. Flag meaningful inconsistencies; avoid creating third style.

## Core Principle

Prefer predictability over cleverness. Developer should guess name from siblings and find related ops via autocomplete.

Before adding/changing name, scan nearby code. Do not mix names for same concept, like `fetchUser`, `retrieveUser`, and `getUser`, unless codebase makes real semantic distinction.

## Case Style

Case is language-dependent. Do not impose one language's style on another.

| Language / Ecosystem | Functions / Methods | Variables | Types / Classes |
|---|---|---|---|
| Python, Ruby, Rust | `snake_case` | `snake_case` | `PascalCase` |
| JS/TS, Java, Kotlin, Swift | `camelCase` | `camelCase` | `PascalCase` |
| C# | `PascalCase` methods/properties | `camelCase` locals/params | `PascalCase` |
| Go | `camelCase` unexported, `PascalCase` exported | same | same |

Constants, files, modules, packages, private/internal names vary by ecosystem. Follow existing file first; see [REFERENCE.md](REFERENCE.md) for defaults.

## Verb Selection

Functions/methods that do something need clear conventional verb. Palette, not whitelist.

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

Prefer one verb per concept. If codebase uses `get`, do not introduce `fetch`, `retrieve`, or `grab` for same operation.

## Resource And API Names

- Use one resource noun per concept: `endpoint`, not both `endpoint` and `serving_endpoint`.
- Singular for one thing; plural for collections.
- Order general to specific so names group: `modelVersion`, `modelVersionStatus`, `modelVersionTag`.
- Mirror code/API names when practical: `listModelVersions()` maps cleanly to `GET /models/{id}/versions`.
- Keep paths, method names, command names shallow and predictable.

## Qualifiers

- Use `config`, `status`, `payload`, and `latest` consistently when concepts exist.
- Singular name for one value; plural for collections.
- Use `tag` for one tag and `tags` for collection. Example: `setTag(modelId, tag)` sets one; `setTags(modelId, tags)` replaces many; `addTag(modelId, tag)` adds one.

## Prepositions

Prefer names without prepositions when params make relation obvious.

- Use `by` for lookup/filter/sort by property: `listEndpointsByStatus(status)`.
- Use `to` for conversion: `modelToDict(model)`, `configToPayload(config)`.
- Use `for` for association, scope, audience, ownership: `listPermissionsForUser(userId)`.

Translate casing to language: `list_endpoints_by_status`, `listEndpointsByStatus`, `ListEndpointsByStatus`.

## Quick Checklist

1. Name match nearby code for same concept?
2. Case idiomatic for language/file?
3. Verb describe behavior accurately?
4. Cardinality match name (`get`/`list`, singular/plural, `tag`/`tags`)?
5. Resource noun consistent across code, APIs, commands?
6. Qualifiers standard and ordered general to specific?
7. Can preposition drop? If not, is it `by`, `to`, or `for` with right meaning?
8. Autocomplete group related names?

## Examples

```text
getModel(modelId) / get_model(model_id)
listEndpoints() / list_endpoints()
isValid(config) / is_valid(config)
parseConfig(raw) / parse_config(raw)
renderTemplate(context) / render_template(context)
endpointStatusToLabel(status) / endpoint_status_to_label(status)
```
