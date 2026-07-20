---
name: typescript
description: TypeScript types, interfaces, tsconfig, and strict mode for type-safe JavaScript. Use when working on the the-frontend-portal (the-frontend-portal), adding types, configuring compiler options, or writing type-safe React/Node code in the the-project Platform ecosystem.
---

# TypeScript - the-frontend-portal

Skill for development with **TypeScript** in the the-frontend-portal project and other the-project TypeScript projects. Reference documentation: [TypeScript Handbook](https://www.typescriptlang.org/docs/).

## Technology Stack (the-frontend-portal)

- **TypeScript:** 4.7.2 (the-frontend-portal the-frontend-portal)
- **Project:** `the-frontend-portal/the-frontend-portal/`

## When to Use This Skill

- Define types and interfaces for props, state, and APIs
- Configure `tsconfig.json` (strict, module, target)
- Resolve type errors in React components or utilities
- Type REST responses and shared API contracts

## Compiler Options (Recommended)

- **strict:** `true` - enables strictNullChecks, noImplicitAny, noImplicitThis, alwaysStrict.
- **strictNullChecks:** `null` and `undefined` are distinct types. Prevents runtime errors.
- **noImplicitAny:** requires explicit typing where the type would otherwise be `any`.

```json
{
  "compilerOptions": {
    "strict": true,
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "node"
  }
}
```

## Type Patterns

### Interfaces for props and API

```typescript
interface sharedAPI {
  appData: { common: { user: User; operation: OperationData } };
  indicators: { openAlert: (alertId: string) => void };
  map: { centerMapByVesselId: (vesselId: string) => void };
}
```

### Union and null/undefined (strict)

```typescript
let x: number;
let y: number | undefined;
x = undefined; // Error with strictNullChecks
y = undefined;  // Ok
```

### Typing events and callbacks

- Use React types when applicable: `React.ChangeEvent<HTMLInputElement>`, `React.MouseEvent`.
- Callbacks: `(id: string) => void`, etc.

## the-frontend-portal Context

- Type `sharedApi` and sub-objects (appData, indicators, map, units) according to the the-web-portal contract.
- Type DTOs from REST APIs (Alert, DistributionList, SurveillanceInstance, etc.).
- Yup validation: align schemas with TypeScript interfaces when possible.

## Best Practices

- Prefer `interface` for object shapes. Use `type` for unions and mappings.
- Avoid `any`. Use `unknown` and type guards when the type is dynamic.
- Keep reusable definitions in type files (e.g., `types/`, `@types/`).

## Reference

- Official documentation: https://www.typescriptlang.org/docs/
- Context7 library ID: `/websites/typescriptlang`
