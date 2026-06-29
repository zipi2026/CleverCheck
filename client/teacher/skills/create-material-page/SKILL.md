# Create Material Page Skill

This skill guides an AI agent to scaffold a content/material page in the CleverCheck client.

## Purpose
- Scaffold a reusable, accessible "material" or content page (list and detail) following project patterns.
- Keep UI, routing, and data concerns separated and typed.

## When to use
- When adding course/material pages, resource listings, or content detail views.
- When you need a consistent page structure: hero/header, list/grid, and detail view.

## Steps
1. Inspect existing UI conventions (component layout, CSS approach) in `src/` to match styles.
2. Create page files under `src/pages/materials/` (e.g., `Index.tsx`, `Detail.tsx`) and index exports.
3. Add small presentational components under `src/components/materials/` (e.g., `MaterialCard`, `MaterialList`).
4. Define explicit TypeScript interfaces for material data under `src/models/` or `src/types/` and import them in components.
5. Implement accessible lists and detail markup (semantic elements, aria labels, keyboard focus management).
6. Wire routes into the router (e.g., `/materials`, `/materials/:id`) and add navigation links in appropriate layout components.
7. Keep data fetching in services/hooks (e.g., `src/services/materials.ts` or `src/hooks/useMaterials.ts`).
8. Add client-side pagination or lazy loading for long lists if needed.
9. Add basic unit tests for components with critical behavior and a minimal integration test for routing if available.
10. Validate by running `npm run dev`, `npm run build`, and `npm run lint`.

## Quality criteria
- Components are small, reusable, and well-typed.
- Markup is accessible and responsive.
- Routes and navigation are clear and tested.
- No data-fetching inside presentational components; services/hooks handle it.

## Example prompts
- "Scaffold a `materials` list page and `materials/:id` detail page wired into the router."
- "Create a `MaterialCard` component and `useMaterials` hook that returns typed `Material` objects."
- "Add tests for the `MaterialList` component and a route integration test for `/materials`."
