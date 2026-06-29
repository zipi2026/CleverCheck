# Generate Models Skill

This skill guides an AI agent through generating TypeScript models from server table schemas for the CleverCheck client.

## Purpose
- Create a consistent workflow for generating frontend TypeScript types and interfaces from backend table metadata.
- Keep frontend models synchronized with backend data shapes.
- Reduce manual duplication and make data contracts reusable.

## When to use
- When the task is to generate or update client-side models based on server table definitions.
- When the agent needs to create typed models for API data, database tables, or shared schema metadata.
- When a new backend table or data contract is being introduced and the client needs matching types.

## Steps
1. Confirm the relevant server table schema or metadata source.
2. Create or update a model module under `src/models/`, `src/types/`, or `src/lib/`.
3. Derive field names, types, optionality, and nested structures from the schema.
4. Prefer explicit TypeScript `interface` or `type` declarations over `any`.
5. Keep generated models free of backend logic or data-fetching concerns.
6. If a generation utility is needed, add it in a clearly named file such as `src/models/generate.ts`.
7. Use the generated models in frontend code and ensure they are exported for reuse.
8. Validate with `npm run build` and `npm run lint`.

## Quality criteria
- Models accurately reflect the server table schema.
- Types are explicit and avoid `any` where possible.
- Generated model files are organized and reusable.
- No backend or data access logic is embedded in model definitions.
- Frontend code imports and uses the models consistently.

## Example prompts
- "Generate TypeScript models from server table definitions and save them under `src/models/`."
- "Create a typed model for the `users` table and export it for client usage."
- "Add a model generation utility that converts backend schema metadata into TypeScript types."
