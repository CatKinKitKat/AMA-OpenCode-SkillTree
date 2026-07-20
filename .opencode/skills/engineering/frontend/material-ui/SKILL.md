---
name: material-ui
description: Material-UI (MUI) React components, theming, and customization. Use when building or styling UI in the the-frontend-portal (the-frontend-portal)-buttons, forms, TextField, theme, ThemeProvider in the the-project Platform ecosystem.
---

# Material-UI (MUI) - the-frontend-portal

Skill for **Material-UI** in the the-frontend-portal project. Reference documentation: [MUI v5](https://v5.mui.com/).

## Technology Stack (the-frontend-portal)

- **Material-UI:** 5.4.4 (the-frontend-portal the-frontend-portal)
- **React:** 17.0.2
- **Project:** `the-frontend-portal/the-frontend-portal/`

## When to Use This Skill

- Use MUI components (Button, TextField, Dialog, Table, etc.)
- Adjust theme (colors, typography, density)
- Customize components with ThemeProvider and styleOverrides

## Component Usage

- **Button:** `<Button variant="contained">Label</Button>`
- **TextField:** `<TextField label="Outlined" />`, variants `outlined` | `filled` | `standard`
- **ThemeProvider:** wrap the app to apply the global theme

```jsx
<ThemeProvider theme={theme}>
  <TextField label="Outlined" />
  <Button>Submit</Button>
</ThemeProvider>
```

## Theming

- **createTheme:** define palette, typography, components.
- **Component overrides:** `components.MuiButton.styleOverrides.root`, etc.
- **Default props:** e.g. `MuiButton: { defaultProps: { size: 'small' } }` for density.

Theme example with typography and density:

```javascript
const theme = createTheme({
  typography: {
    button: { fontSize: '1rem' },
  },
  components: {
    MuiButton: {
      defaultProps: { size: 'small' },
      styleOverrides: { root: { fontSize: '1rem' } },
    },
    MuiTextField: {
      defaultProps: { margin: 'dense' },
    },
  },
});
```

## the-frontend-portal Context

- Forms with React Hook Form + Yup. MUI for presentation (TextField, Select, etc.).
- Tables with @tanstack/react-table and MUI components (Table, TableHead, TableBody).
- Feedback: react-toastify. Icons and layout with MUI when applicable.

## Best Practices

- Reuse the project theme instead of scattered inline styles.
- Use consistent variants and sizes (contained/outlined, small/medium).

## Reference

- MUI v5: https://v5.mui.com/
- Context7 library ID: `/websites/v5_mui_material-ui`
