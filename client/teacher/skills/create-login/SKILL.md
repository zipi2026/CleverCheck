# Create Login Skill

This skill guides an AI agent through implementing a login flow in the CleverCheck client.

## Purpose
- Create a reusable, accessible login experience in this React + TypeScript + Vite app.
- Keep authentication UI, routing, and service logic clearly separated.
- Provide a consistent workflow for building login features.

## When to use
- When the task is to add user login, authentication routing, or auth service wiring.
- When the agent needs to scaffold login pages, auth hooks, or login-related route handling.

## Steps
1. Inspect the existing app structure in `src/` and identify where the login UI should be added.
2. Add a dedicated auth service or API module, for example `src/auth/` or `src/services/auth.ts`.
3. Create a login page/component under `src/pages/` or `src/components/`.
4. Add a login form with email/username and password fields, accessible labels, and client-side validation.
5. Implement typed request/response interfaces for auth-related API calls.
6. Use `import.meta.env` for login endpoint configuration instead of hardcoding URLs.
7. Connect the login flow to app routing if routing exists; otherwise scaffold a minimal router setup.
8. Add state handling for loading, success, and error messages.
9. Keep authentication side effects and storage concerns (cookies, localStorage, token state) inside auth services or hooks.
10. Validate the implementation with `npm run build` and `npm run lint`.

## Quality criteria
- Login logic is separated from rendering logic.
- Auth requests are typed and reusable.
- No hardcoded backend URLs in components.
- Login form elements are accessible and clearly labeled.
- Errors are handled gracefully and displayed to the user.
- Routing and redirect behavior is clean and maintainable.

## Example prompts
- "Create a login page and auth service for this Vite React app."
- "Implement a typed login API module and connect it to a login form."
- "Add login routing and protected route handling for authenticated users."
