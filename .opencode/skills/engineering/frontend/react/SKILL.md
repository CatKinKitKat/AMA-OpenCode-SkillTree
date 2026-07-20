---
name: react
description: React components, hooks (useState, useEffect, useContext), and best practices for building UIs. Use when working on the the-frontend-portal (the-frontend-portal), creating React components, managing state, or implementing frontend features in the the-project Platform ecosystem.
---

# React - the-frontend-portal

Skill for development with **React** in the the-project Platform the-frontend-portal (Micro-Frontend) project. Reference documentation: [Context7 - React](https://react.dev).

## Technology Stack (the-frontend-portal)

- **React:** 17.0.2 (the-frontend-portal the-frontend-portal)
- **Build:** Webpack 5, npm 8.x
- **Runtime:** Browser (Chrome, Firefox, Safari)
- **Project:** `the-frontend-portal/the-frontend-portal/`

## When to Use This Skill

- Work on the-frontend-portal components or pages
- Implement local or shared state with hooks
- Integrate with shared API (appData, indicators, map)
- Reuse logic with custom hooks

## Core Patterns

### State with useState

```javascript
import { useState } from 'react';

function MyComponent() {
  const [value, setValue] = useState(null);

  function handleClick() {
    setValue(newValue);
  }
  // ...
}
```

- `useState` returns `[state, setState]`. The setter re-renders the component.
- Initialization: `useState(initialValue)` or `useState(() => expensiveInit())`.

### Side Effects with useEffect

- Effects: subscriptions, fetch, timers. Use `useEffect(callback, [deps])`.
- Cleanup when the component unmounts: return a function from the callback.
- Avoid unnecessary dependencies to prevent extra effect runs.

### Hooks Rules

- Use hooks only at top level (not inside loops/conditions).
- Use them only in functional components or custom hooks.
- Keep components and hooks pure when possible.

## frontend-portal-specific Integration

- **shared API:** The the-frontend-portal receives `sharedApi` (appData, indicators, map, units) and should use these APIs for shared data, notifications, and map interactions.
- **Events:** Publish `onthe-backendCreated`, `onthe-backendUpdated`, etc., according to the the-web-portal contract.
- **Embedding:** Main component `<the-backend sharedApi={mockedAPI} />`. Support standalone mode and embedded mode in the-portal-platform.

## Project Structure (the-frontend-portal)

- Components in folders by feature or type (e.g., alerts, distribution-lists, map).
- Reusable hooks in `hooks/`.
- Global state (if needed) via Context or the library chosen by the project.

## Best Practices

- Prefer functional components and hooks.
- Extract repeated logic into custom hooks.
- Use `useMemo`/`useCallback` only when there is a real performance gain.
- Keep components small and focused.

## Reference

- Official documentation: https://react.dev
- Context7 library ID: `/reactjs/react.dev` (check for current examples and APIs)
