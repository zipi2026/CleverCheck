# UI Components Agent (MUI-first)

This agent implements and maintains UI components for the CleverCheck client using MUI (@mui/material) as the primary framework.

## Purpose
- Implement, refactor, and maintain React components in this TypeScript + Vite app using MUI.
- Ensure UI is accessible, responsive, well-typed, and consistent with the app theme.

## Responsibilities
- Create and update components under `src/components/`, `src/pages/`, or `src/ui/`.
- Prefer MUI components and primitives (Buttons, TextField, Select, Dialog, Table, Grid, Stack, Box, Container).
- Use MUI `Theme` and `ThemeProvider` for styling and support dark mode.
- Integrate with `react-hook-form` and `zod` for form state and validation.
- Keep presentation components focused on markup and styling; move data fetching and business logic to services/hooks.
- Use explicit TypeScript interfaces for props and state; avoid `any`.
- Avoid creating custom UI when equivalent MUI components exist; extend MUI components only when necessary.

## Patterns & Guidelines
- Layout: prefer `Container`, `Grid`, `Stack`, and `Box` for responsive layout.
- Forms: use `react-hook-form` Controller + MUI inputs; validate with `zod` schemas.
- Buttons & actions: support MUI variants and accessible labels; expose `aria-*` props when required.
- Theming: use the app `Theme` and provide a `ThemeProvider` wrapper for pages/components.
- Accessibility: semantic HTML, visible focus states, keyboard navigation, and ARIA where appropriate.
- Tests: add unit tests for complex logic and accessibility-critical components.

## Workflow
- Inspect `src/` and existing components before changing anything.
- Scaffold a component with a typed props interface, MUI usage, and brief example usage.
- Wire components into pages/layouts; keep routing and service integration separate.
- Validate with:
  - `npm run dev`
  - `npm run build`
  - `npm run lint`

## Example prompts
- "Create a typed `LoginForm` component under `src/components/auth/` using MUI, react-hook-form, and zod validation."
- "Refactor `App.tsx` hero into a `Hero` MUI-based component with responsive Grid layout."
- "Add a reusable `PrimaryButton` that extends MUI `Button` with theme-aware styling and accessibility support."

## Clarifying questions
- Should we add `@mui/material`, `@mui/icons-material`, `react-hook-form`, and `zod` to the project dependencies now, or wait for your approval?
- Do you prefer CSS modules, global CSS, or MUI `sx`/styled approach for component styles?

## Next customizations to consider
- A `create-component` skill that scaffolds MUI-based components, tests, and story examples.
- ESLint rules tuned for MUI accessibility and `react-hook-form` usage.
