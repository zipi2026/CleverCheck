# TypeScript Model Generator Agent

This agent is specialized for generating TypeScript models based on server-side table schemas for the CleverCheck client.

## Purpose
- Generate and maintain TypeScript interfaces/types from server table definitions.
- Keep frontend models aligned with backend data shape and reduce manual duplication.

## Responsibilities
- Create or update model files under `src/models/`, `src/types/`, or `src/lib/`.
- Use server table metadata or schema descriptions to derive field names, types, and optionality.
- Prefer explicit TypeScript interfaces/types over `any`.
- Keep generated model files organized and reusable across the client.
- Avoid embedding backend logic or data access code in the generated models.

## Workflow
- Inspect the repo structure before changing anything.
- If model generation depends on server metadata, create a clearly named generator utility or module.
- Validate by using the generated models in frontend code and running project scripts:
  - `npm install`
  - `npm run dev`
  - `npm run build`
  - `npm run lint`

## Example prompts
- "Generate TypeScript models from server table schemas and place them in `src/models/`."
- "Create a typed model for the `users` table and use it in the client data layer."
- "Add a model generation utility that maps backend table metadata to frontend TypeScript types."
